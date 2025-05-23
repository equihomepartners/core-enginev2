"""
Orchestrator module for the EQU IHOME SIM ENGINE v2.

This module coordinates the execution of simulation modules in the correct sequence.
"""

import asyncio
import time
from typing import Dict, Any, Optional, Callable, Union, Awaitable

import structlog

from src.config.config_loader import SimulationConfig
from src.engine.simulation_context import SimulationContext
from src.utils.metrics import increment_counter, observe_histogram, set_gauge

logger = structlog.get_logger(__name__)


class SimulationOrchestrator:
    """
    Orchestrator for simulation modules.

    This class coordinates the execution of simulation modules in the correct sequence.
    It is responsible for creating the simulation context, calling each module in order,
    and collecting the results.
    """

    def __init__(self):
        """Initialize the simulation orchestrator."""
        self._modules = {}
        self._module_sequence = []

    def register_module(
        self,
        name: str,
        module_func: Union[Callable[[SimulationContext], None], Callable[[SimulationContext], Awaitable[None]]],
        position: Optional[int] = None
    ) -> None:
        """
        Register a simulation module.

        Args:
            name: Module name
            module_func: Module function that takes a SimulationContext and returns None or awaitable None
            position: Position in the execution sequence (appended to the end if not specified)
        """
        self._modules[name] = module_func

        if position is not None:
            # Ensure the sequence is long enough
            while len(self._module_sequence) <= position:
                self._module_sequence.append(None)

            # Set the module at the specific position
            self._module_sequence[position] = name
        else:
            self._module_sequence.append(name)

        # Log whether the module is async or not
        is_async = asyncio.iscoroutinefunction(module_func)

        logger.debug(
            "Module registered",
            name=name,
            position=position or len(self._module_sequence) - 1,
            is_async=is_async,
        )

    async def run_simulation(
        self, config: SimulationConfig, run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a simulation with the given configuration.

        Args:
            config: Simulation configuration
            run_id: Unique identifier for the simulation run (generated if not provided)

        Returns:
            Dictionary containing simulation results
        """
        # Import here to avoid circular imports
        from src.api.websocket_manager import get_websocket_manager
        from src.utils.error_handler import handle_exception, log_error, format_error_response

        # Get WebSocket manager
        websocket_manager = get_websocket_manager()

        # Create simulation context
        context = SimulationContext(config, run_id)

        # Track simulation start
        increment_counter("simulation_runs_total", labels={"status": "started"})
        set_gauge("active_simulations", 1)

        # Send initial progress update
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="orchestrator",
            progress=0.0,
            message="Starting simulation",
        )

        try:
            # Filter out None values and execute modules in sequence
            module_sequence = [name for name in self._module_sequence if name is not None]
            logger.info(f"🚨 DEBUG: Full module sequence: {self._module_sequence}")
            logger.info(f"🚨 DEBUG: Filtered module sequence: {module_sequence}")

            # Calculate progress increment per module
            progress_increment = 100.0 / len(module_sequence)
            current_progress = 0.0
            for i, module_name in enumerate(module_sequence):
                logger.info(f"🚨 DEBUG: About to execute module {module_name} (position {i})")

                # Check for cancellation
                if websocket_manager.is_cancelled(context.run_id):
                    logger.info(
                        "Simulation cancelled",
                        run_id=context.run_id,
                        module_name=module_name,
                    )

                    # Send cancellation message
                    await websocket_manager.send_info(
                        simulation_id=context.run_id,
                        message="Simulation cancelled",
                    )

                    # Update metrics
                    increment_counter("simulation_runs_total", labels={"status": "cancelled"})

                    # Return partial results
                    return context.get_summary()

                if module_name not in self._modules:
                    logger.error("Module not found", module_name=module_name)

                    # Send error message
                    await websocket_manager.send_warning(
                        simulation_id=context.run_id,
                        message=f"Module not found: {module_name}",
                    )

                    continue

                module_func = self._modules[module_name]

                # Send progress update
                await websocket_manager.send_progress(
                    simulation_id=context.run_id,
                    module=module_name,
                    progress=current_progress,
                    message=f"Starting module: {module_name}",
                )

                # Track module execution time
                context.track_module_time(module_name)

                try:
                    # Execute module
                    if asyncio.iscoroutinefunction(module_func):
                        await module_func(context)
                    else:
                        module_func(context)

                    # End module timing
                    execution_time = context.end_module_time(module_name)

                    # Record module execution time
                    observe_histogram(
                        "simulation_runtime_seconds",
                        execution_time,
                        labels={"type": module_name},
                    )

                    # Update progress
                    current_progress += progress_increment

                    # Send progress update
                    await websocket_manager.send_progress(
                        simulation_id=context.run_id,
                        module=module_name,
                        progress=current_progress,
                        message=f"Completed module: {module_name}",
                        data={
                            "execution_time": execution_time,
                            "module_index": i,
                            "total_modules": len(module_sequence),
                        },
                    )

                    # Send intermediate results if available
                    if hasattr(context, f"{module_name}_results"):
                        intermediate_results = getattr(context, f"{module_name}_results")

                        await websocket_manager.send_message(
                            simulation_id=context.run_id,
                            message_type="intermediate_result",
                            data={
                                "module": module_name,
                                "results": intermediate_results,
                            },
                        )

                except Exception as e:
                    # Handle exception
                    error = handle_exception(e)

                    # Log error
                    log_error(error)

                    # Send error message
                    await websocket_manager.send_error(
                        simulation_id=context.run_id,
                        error=format_error_response(error),
                    )

                    # Update metrics
                    increment_counter("simulation_runs_total", labels={"status": "failed"})

                    # Re-raise exception
                    raise

            # Record simulation metrics
            if "irr" in context.metrics:
                observe_histogram("irr_distribution", context.metrics["irr"])

            if "equity_multiple" in context.metrics:
                observe_histogram(
                    "equity_multiple_distribution", context.metrics["equity_multiple"]
                )

            if "var_95" in context.metrics:
                observe_histogram("var_95_distribution", context.metrics["var_95"])

            # Record guardrail violations
            for violation in context.guardrail_violations:
                increment_counter(
                    "guardrail_violations_total", labels={"guardrail": violation}
                )

            # Track simulation completion
            increment_counter("simulation_runs_total", labels={"status": "completed"})

            # Send final progress update
            await websocket_manager.send_progress(
                simulation_id=context.run_id,
                module="orchestrator",
                progress=100.0,
                message="Simulation completed",
                data={
                    "execution_time": context.get_total_execution_time(),
                    "module_count": len(module_sequence),
                },
            )

            # Get simulation summary
            summary = context.get_summary()

            # Send final results
            await websocket_manager.send_result(
                simulation_id=context.run_id,
                result=summary,
            )

            # Store simulation context
            try:
                from src.engine.simulation_context import store_simulation_context
                store_simulation_context(context)
                logger.info("Stored simulation context", run_id=context.run_id)
            except Exception as e:
                logger.warning("Failed to store simulation context", run_id=context.run_id, error=str(e))

            # Store results in persistence layer
            try:
                from src.persistence.result_store import get_result_store
                result_store = get_result_store(context.run_id)
                await result_store.store_result(context)
                logger.info("Stored simulation results", run_id=context.run_id)
            except Exception as e:
                logger.warning("Failed to store simulation results", run_id=context.run_id, error=str(e))

            return summary

        except Exception as e:
            # Handle exception
            error = handle_exception(e)

            # Log error
            log_error(error)

            # Send error message
            await websocket_manager.send_error(
                simulation_id=context.run_id,
                error=format_error_response(error),
            )

            # Update metrics
            increment_counter("simulation_runs_total", labels={"status": "failed"})

            # Re-raise exception
            raise

        finally:
            # Reset active simulations gauge
            set_gauge("active_simulations", 0)

            # Record total simulation time
            observe_histogram(
                "simulation_runtime_seconds",
                context.get_total_execution_time(),
                labels={"type": "total"},
            )


# Global orchestrator instance
_global_orchestrator: Optional[SimulationOrchestrator] = None


def get_orchestrator() -> SimulationOrchestrator:
    """
    Get the global orchestrator instance.

    Returns:
        The global orchestrator instance
    """
    global _global_orchestrator

    if _global_orchestrator is None:
        _global_orchestrator = SimulationOrchestrator()

        # Import modules here to avoid circular imports
        from src.tls_module import get_tls_manager
        from src.capital_allocator import allocate_capital
        from src.engine.loan_generator import generate_loans
        from src.price_path.price_path import simulate_price_paths
        from src.price_path.enhanced_price_path import simulate_enhanced_price_paths
        from src.exit_simulator.exit_simulator import simulate_exits
        from src.exit_simulator.enhanced_exit_simulator import simulate_enhanced_exits
        from src.reinvest_engine.reinvest_engine import reinvest_capital
        from src.leverage_engine.leverage_manager import manage_leverage
        from src.fee_engine.fee_engine import calculate_fees

        # Register implemented modules
        _global_orchestrator.register_module("tls_module", get_tls_manager, position=0)
        _global_orchestrator.register_module("capital_allocator", allocate_capital, position=1)
        _global_orchestrator.register_module("loan_generator", generate_loans, position=2)
        _global_orchestrator.register_module("price_path", simulate_price_paths, position=3)
        _global_orchestrator.register_module("enhanced_price_path", simulate_enhanced_price_paths, position=4)
        _global_orchestrator.register_module("exit_simulator", simulate_exits, position=5)
        _global_orchestrator.register_module("enhanced_exit_simulator", simulate_enhanced_exits, position=6)
        _global_orchestrator.register_module("reinvest_engine", reinvest_capital, position=7)
        _global_orchestrator.register_module("leverage_engine", manage_leverage, position=8)
        _global_orchestrator.register_module("fee_engine", calculate_fees, position=9)

        # Import cashflow aggregator
        from src.cashflow_aggregator import aggregate_cashflows

        # Register cashflow aggregator
        _global_orchestrator.register_module("cashflow_aggregator", aggregate_cashflows, position=10)
        logger.info(f"🚨 DEBUG: Module sequence after cashflow_aggregator: {_global_orchestrator._module_sequence}")

        # Import waterfall engine
        from src.waterfall_engine import calculate_waterfall

        # Register waterfall engine
        _global_orchestrator.register_module("waterfall_engine", calculate_waterfall, position=11)
        logger.info(f"🚨 DEBUG: Module sequence after waterfall_engine: {_global_orchestrator._module_sequence}")

        # Import tranche manager
        from src.tranche_manager import manage_tranches

        # Register tranche manager
        _global_orchestrator.register_module("tranche_manager", manage_tranches, position=12)

        # Import risk metrics
        from src.risk.risk_metrics import RiskMetricsCalculator

        # Register risk metrics
        def calculate_risk_metrics(context: SimulationContext) -> None:
            """Calculate risk metrics."""
            risk_calculator = RiskMetricsCalculator(context)
            risk_calculator.calculate_metrics()

        _global_orchestrator.register_module("risk_metrics", calculate_risk_metrics, position=13)

        # Import guardrail monitor
        from src.risk.guardrail_monitor import GuardrailMonitor

        # Register guardrail monitor
        async def evaluate_guardrails(context: SimulationContext) -> None:
            """Evaluate guardrails."""
            guardrail_monitor = GuardrailMonitor(context)
            await guardrail_monitor.evaluate_guardrails()

        _global_orchestrator.register_module("guardrail_monitor", evaluate_guardrails, position=14)

        # Import performance reporter
        from src.performance_reporter import generate_performance_report

        # Register performance reporter
        _global_orchestrator.register_module("performance_reporter", generate_performance_report, position=15)

    return _global_orchestrator


async def run_simulation(config: SimulationConfig, run_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Run a simulation with the given configuration.

    This is a convenience function that uses the global orchestrator instance.

    Args:
        config: Simulation configuration
        run_id: Unique identifier for the simulation run (generated if not provided)

    Returns:
        Dictionary containing simulation results
    """
    orchestrator = get_orchestrator()
    return await orchestrator.run_simulation(config, run_id)
