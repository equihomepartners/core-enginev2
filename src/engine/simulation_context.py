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

from src.config.config_loader import SimulationConfig

logger = structlog.get_logger(__name__)


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
                "names": [t.get("name", f"Tranche {i}") for i, t in enumerate(self.tranches)],
            },
            "capital_allocation": capital_allocation,
            "loans": self.loans,
            "loan_portfolio": loan_portfolio,
        }
