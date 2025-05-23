"""
Simulation context module for the EQU IHOME SIM ENGINE v2.

This module provides a shared context for simulation modules to maintain state
and provide access to common functionality.
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set

import numpy as np
import structlog
from fastapi import Depends, HTTPException

from src.config.config_loader import SimulationConfig

logger = structlog.get_logger(__name__)

# Global simulation context storage
_simulation_contexts: Dict[str, "SimulationContext"] = {}


class SimulationContext:
    """
    Shared context for simulation modules.

    This class provides a central place for modules to share data and state
    during a simulation run. It is passed between modules and updated as the
    simulation progresses.

    Attributes:
        config: Simulation configuration
        run_id: Unique identifier for the simulation run
        rng: Random number generator
        loans: List of generated loans
        price_paths: Dictionary of price paths by zone
        exits: Dictionary of exit information by loan ID
        cashflows: List of cash flows
        metrics: Dictionary of calculated metrics
        start_time: Start time of the simulation
        module_timings: Dictionary of module execution times
    """

    def __init__(self, config: SimulationConfig, run_id: Optional[str] = None):
        """
        Initialize the simulation context.

        Args:
            config: Simulation configuration
            run_id: Unique identifier for the simulation run (generated if not provided)
        """
        # Configuration
        self.config = config
        self.run_id = run_id or str(uuid.uuid4())

        # Random number generation
        self.rng: Optional[np.random.Generator] = None

        # Simulation state
        self.loans: List[Dict[str, Any]] = []
        self.price_paths: Dict[str, np.ndarray] = {}
        self.exits: Dict[str, Dict[str, Any]] = {}
        self.cashflows: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}

        # TLS module state
        self.tls_data: Dict[str, Dict[str, Any]] = {}

        # Capital allocation state
        self.zone_targets: Dict[str, float] = {}
        self.zone_actual: Dict[str, float] = {}

        # Leverage state
        self.leverage_facilities: Dict[str, Dict[str, Any]] = {}
        self.leverage_draws: List[Dict[str, Any]] = []
        self.leverage_repayments: List[Dict[str, Any]] = []

        # Tranche state
        self.tranches: List[Dict[str, Any]] = []
        self.tranche_cashflows: Dict[str, List[Dict[str, Any]]] = {}

        # Performance tracking
        self.start_time = time.time()
        self.module_timings: Dict[str, float] = {}

        # Guardrail violations
        self.guardrail_violations: List[str] = []

        # Feature flags
        self.features: Set[str] = set()

        logger.info(
            "Simulation context initialized",
            run_id=self.run_id,
            config_summary={
                "fund_size": config.fund_size,
                "fund_term": config.fund_term,
                "vintage_year": config.vintage_year,
            },
        )

    def track_module_time(self, module_name: str) -> None:
        """
        Track the execution time of a module.

        Args:
            module_name: Name of the module
        """
        if module_name in self.module_timings:
            logger.warning("Module timing already exists", module_name=module_name)
            return

        self.module_timings[module_name] = time.time()

    def end_module_time(self, module_name: str) -> float:
        """
        End tracking the execution time of a module.

        Args:
            module_name: Name of the module

        Returns:
            Execution time in seconds
        """
        if module_name not in self.module_timings:
            logger.warning("Module timing not found", module_name=module_name)
            return 0.0

        start_time = self.module_timings[module_name]
        execution_time = time.time() - start_time

        # Replace the start time with the execution time
        self.module_timings[module_name] = execution_time

        logger.debug(
            "Module execution completed",
            module_name=module_name,
            execution_time=execution_time,
        )

        return execution_time

    def add_guardrail_violation(self, violation: str) -> None:
        """
        Add a guardrail violation.

        Args:
            violation: Description of the violation
        """
        self.guardrail_violations.append(violation)
        logger.warning("Guardrail violation", violation=violation)

    def has_guardrail_violations(self) -> bool:
        """
        Check if there are any guardrail violations.

        Returns:
            True if there are violations, False otherwise
        """
        return len(self.guardrail_violations) > 0

    def get_total_execution_time(self) -> float:
        """
        Get the total execution time of the simulation.

        Returns:
            Total execution time in seconds
        """
        return time.time() - self.start_time

    def _extract_api_cashflows(self) -> List[Dict[str, Any]]:
        """
        Extract cashflows in the format expected by the API.

        Returns the fund-level cashflows which contain comprehensive cashflow data
        including capital calls, loan investments, fees, distributions, etc.

        Returns:
            List of fund-level cashflow dictionaries
        """
        if not hasattr(self, "cashflows") or not self.cashflows:
            return []

        cashflows_data = self.cashflows

        # The cashflows are stored as a complex structure from the cashflow aggregator
        if isinstance(cashflows_data, dict):
            # Extract fund-level cashflows - these are the main cashflows for API consumption
            if "fund_level_cashflows" in cashflows_data:
                fund_cashflows = cashflows_data["fund_level_cashflows"]
                if isinstance(fund_cashflows, list):
                    return fund_cashflows

            # Fallback to LP cashflows if fund-level not available
            if "lp_cashflows" in cashflows_data:
                lp_cashflows = cashflows_data["lp_cashflows"]
                if isinstance(lp_cashflows, list):
                    return lp_cashflows

        # If cashflows_data is already a list, use it directly
        elif isinstance(cashflows_data, list):
            return cashflows_data

        return []

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the simulation results.

        Returns:
            Dictionary containing simulation summary
        """
        # Get capital allocation results
        capital_allocation = {
            "zone_targets": self.zone_targets,
            "zone_actual": self.zone_actual,
        }

        # Add capital allocation visualization if available
        if hasattr(self, "allocation_visualization"):
            capital_allocation["visualization"] = {
                "allocation_visualization": self.allocation_visualization,
            }

        # Add allocation comparison if available
        if hasattr(self, "allocation_comparison"):
            capital_allocation["visualization"]["allocation_comparison"] = self.allocation_comparison

        # Add allocation statistics if available
        if hasattr(self, "allocation_stats"):
            capital_allocation["allocation_stats"] = self.allocation_stats

        # Add capital by zone if available
        if hasattr(self, "capital_by_zone"):
            capital_allocation["capital_by_zone"] = self.capital_by_zone

        # Get loan portfolio results
        loan_portfolio = {}

        # Add loan portfolio visualization if available
        if hasattr(self, "loan_portfolio_visualization"):
            loan_portfolio["visualization"] = self.loan_portfolio_visualization

        # Add loan portfolio statistics if available
        if hasattr(self, "loan_portfolio_stats"):
            loan_portfolio["stats"] = self.loan_portfolio_stats

        return {
            "run_id": self.run_id,
            "config_summary": {
                "fund_size": self.config.fund_size,
                "fund_term": self.config.fund_term,
                "vintage_year": self.config.vintage_year,
            },
            "metrics": self.metrics,
            "execution_time": self.get_total_execution_time(),
            "module_timings": self.module_timings,
            "guardrail_violations": self.guardrail_violations,
            "num_loans": len(self.loans),
            "zone_allocation": {
                "targets": self.zone_targets,
                "actual": self.zone_actual,
            },
            "leverage": {
                "facilities": list(self.leverage_facilities.keys()),
                "num_draws": len(self.leverage_draws),
                "num_repayments": len(self.leverage_repayments),
            },
            "tranches": {
                "count": len(self.tranches),
                "names": [
                    (t.get("name", f"Tranche {i}") if isinstance(t, dict)
                     else getattr(t, "name", f"Tranche {i}"))
                    for i, t in enumerate(self.tranches)
                ],
            },
            "capital_allocation": capital_allocation,
            "loans": self.loans,
            "loan_portfolio": loan_portfolio,
            "cashflows": self._extract_api_cashflows(),
            "waterfall": getattr(self, "waterfall", None),  # Include waterfall results
        }


# Store simulation context
def store_simulation_context(context: SimulationContext) -> None:
    """
    Store a simulation context in the global storage.

    Args:
        context: Simulation context to store
    """
    _simulation_contexts[context.run_id] = context
    logger.info("Stored simulation context", run_id=context.run_id)


# Get simulation context by ID
def get_simulation_context_by_id(simulation_id: str) -> Optional[SimulationContext]:
    """
    Get a simulation context by ID.

    Args:
        simulation_id: Simulation ID

    Returns:
        Simulation context or None if not found
    """
    return _simulation_contexts.get(simulation_id)


# FastAPI dependency for getting simulation context
async def get_simulation_context(simulation_id: Optional[str] = None) -> SimulationContext:
    """
    Get the simulation context for the current request.

    This function is used as a FastAPI dependency to inject the simulation context
    into API endpoints.

    Args:
        simulation_id: Simulation ID (optional, can be provided in the request body)

    Returns:
        Simulation context

    Raises:
        HTTPException: If the simulation context is not found
    """
    # If no simulation ID is provided, return the most recent context
    if not simulation_id and _simulation_contexts:
        return list(_simulation_contexts.values())[-1]

    # If simulation ID is provided, get the context
    if simulation_id and simulation_id in _simulation_contexts:
        return _simulation_contexts[simulation_id]

    # If no context is found, raise an exception
    raise HTTPException(status_code=404, detail="Simulation context not found")
