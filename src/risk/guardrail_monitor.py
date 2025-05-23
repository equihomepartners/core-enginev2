"""
Guardrail Monitor module for the EQU IHOME SIM ENGINE v2.

This module monitors guardrails for the simulation, ensuring that key risk metrics
stay within acceptable bounds. It is non-blocking, meaning that it reports violations
but does not stop the simulation.
"""

import asyncio
from enum import Enum
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field, asdict
import structlog

from src.engine.simulation_context import SimulationContext
from src.api.websocket_manager import get_websocket_manager
from src.utils.metrics import increment_counter, observe_histogram, set_gauge
from src.utils.error_handler import handle_exception, log_error

# Set up logging
logger = structlog.get_logger(__name__)


class Severity(str, Enum):
    """Severity levels for guardrail breaches."""

    INFO = "INFO"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class Breach:
    """
    Represents a guardrail breach.

    Attributes:
        code: Breach code
        severity: Breach severity
        message: Breach message
        value: Actual value that triggered the breach
        threshold: Threshold value that was breached
        unit: Unit of measurement
        layer: Layer where the breach occurred (Unit, Zone, Portfolio, etc.)
    """

    code: str
    severity: Severity
    message: str
    value: Optional[float] = None
    threshold: Optional[float] = None
    unit: Optional[str] = None
    layer: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class GuardrailReport:
    """
    Report of guardrail breaches.

    Attributes:
        breaches: List of breaches
        simulation_id: Simulation ID
    """

    breaches: List[Breach] = field(default_factory=list)
    simulation_id: Optional[str] = None

    @property
    def worst_level(self) -> Severity:
        """Get the worst severity level in the report."""
        if any(b.severity == Severity.FAIL for b in self.breaches):
            return Severity.FAIL
        if any(b.severity == Severity.WARN for b in self.breaches):
            return Severity.WARN
        return Severity.INFO

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "simulation_id": self.simulation_id,
            "worst_level": self.worst_level,
            "breaches": [b.to_dict() for b in self.breaches],
        }


class GuardrailMonitor:
    """
    Monitor for simulation guardrails.

    This class monitors guardrails for the simulation, ensuring that key risk metrics
    stay within acceptable bounds. It is non-blocking, meaning that it reports violations
    but does not stop the simulation.
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the guardrail monitor.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config
        self.websocket_manager = get_websocket_manager()

        # Get guardrail configuration with safe attribute access
        guardrail_obj = getattr(self.config, "guardrails", {})
        self.guardrail_config = guardrail_obj.dict() if hasattr(guardrail_obj, 'dict') else (guardrail_obj if isinstance(guardrail_obj, dict) else {})

        # Initialize report
        self.report = GuardrailReport(simulation_id=context.run_id)

        # Track checked guardrails
        self.checked_guardrails: Set[str] = set()

    async def evaluate_guardrails(self) -> GuardrailReport:
        """
        Evaluate all guardrails.

        Returns:
            Guardrail report
        """
        logger.info("Evaluating guardrails", run_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="guardrail_monitor",
                progress=0.0,
                message="Evaluating guardrails",
            )

        # Get metrics
        metrics = self.context.metrics

        # Check for cancellation
        if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Guardrail evaluation cancelled", run_id=self.context.run_id)
            return self.report

        # Evaluate property/loan level guardrails
        await self._evaluate_loan_guardrails(metrics)

        # Check for cancellation
        if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Guardrail evaluation cancelled", run_id=self.context.run_id)
            return self.report

        # Evaluate zone level guardrails
        await self._evaluate_zone_guardrails(metrics)

        # Check for cancellation
        if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Guardrail evaluation cancelled", run_id=self.context.run_id)
            return self.report

        # Evaluate portfolio level guardrails
        await self._evaluate_portfolio_guardrails(metrics)

        # Check for cancellation
        if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Guardrail evaluation cancelled", run_id=self.context.run_id)
            return self.report

        # Evaluate model/process guardrails
        await self._evaluate_model_guardrails(metrics)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="guardrail_monitor",
                progress=100.0,
                message="Guardrail evaluation completed",
                data=self.report.to_dict(),
            )

        # Store report in context
        self.context.guardrail_report = self.report

        # Log breaches
        for breach in self.report.breaches:
            logger.warning(
                "Guardrail breach",
                run_id=self.context.run_id,
                code=breach.code,
                severity=breach.severity,
                message=breach.message,
                value=breach.value,
                threshold=breach.threshold,
            )

            # Increment Prometheus counter
            increment_counter(
                "guardrail_violations_total",
                labels={"guardrail": breach.code},
            )

        return self.report

    async def _evaluate_loan_guardrails(self, metrics: Dict[str, Any]) -> None:
        """
        Evaluate property/loan level guardrails.

        Args:
            metrics: Simulation metrics
        """
        logger.info("Evaluating loan guardrails", run_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="guardrail_monitor",
                progress=25.0,
                message="Evaluating loan guardrails",
            )

        # 1. Stress LTV (−20% price dip) ≤ 90%
        self._check_stress_ltv_guardrail(metrics)

        # 2. Principal ≤ loan_ticket_limit_zone
        self._check_loan_size_guardrail(metrics)

        # 3. Exit month ≤ max_term_months (120)
        self._check_exit_month_guardrail(metrics)

    async def _evaluate_zone_guardrails(self, metrics: Dict[str, Any]) -> None:
        """
        Evaluate zone level guardrails.

        Args:
            metrics: Simulation metrics
        """
        logger.info("Evaluating zone guardrails", run_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="guardrail_monitor",
                progress=50.0,
                message="Evaluating zone guardrails",
            )

        # 4. Zone NAV weight ≤ capital_limit_zone (e.g. Red ≤ 5%)
        self._check_zone_nav_weight_guardrail(metrics)

        # 5. Default rate zone ≤ 2× city_avg_default
        self._check_zone_default_rate_guardrail(metrics)

        # 6. Sigma price zone ≤ 3× city σ
        self._check_zone_price_volatility_guardrail(metrics)

    async def _evaluate_portfolio_guardrails(self, metrics: Dict[str, Any]) -> None:
        """
        Evaluate portfolio level guardrails.

        Args:
            metrics: Simulation metrics
        """
        logger.info("Evaluating portfolio guardrails", run_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="guardrail_monitor",
                progress=75.0,
                message="Evaluating portfolio guardrails",
            )

        # 7. Single suburb weight ≤ 10% NAV
        self._check_suburb_concentration_guardrail(metrics)

        # 8. Largest single loan weight ≤ 2% NAV
        self._check_loan_concentration_guardrail(metrics)

        # 9. NAV facility utilisation ≤ max_nav_util (cfg)
        self._check_nav_utilization_guardrail(metrics)

        # 10. Interest-coverage ratio (ICR) ≥ 1.25×
        self._check_interest_coverage_guardrail(metrics)

        # 11. Liquidity buffer (cash + undrawn) ≥ 4% NAV
        self._check_liquidity_buffer_guardrail(metrics)

        # 12. Weighted-Avg Life (WAL) ≤ 8 yrs unless wal_override=true
        self._check_wal_guardrail(metrics)

        # 13. VaR-99 ≤ 15% NAV (MC mode only)
        self._check_var_guardrail(metrics)

        # 14. CVaR-99 ≤ 20% NAV (MC mode only)
        self._check_cvar_guardrail(metrics)

        # 15. Net-IRR P5 ≥ hurdle (8%) – 250 bp
        self._check_irr_p5_guardrail(metrics)

        # 16. Hurdle-clear probability ≥ 70% (MC mode only)
        self._check_hurdle_clear_probability_guardrail(metrics)

    async def _evaluate_model_guardrails(self, metrics: Dict[str, Any]) -> None:
        """
        Evaluate model/process guardrails.

        Args:
            metrics: Simulation metrics
        """
        logger.info("Evaluating model guardrails", run_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="guardrail_monitor",
                progress=90.0,
                message="Evaluating model guardrails",
            )

        # 17. Config JSON schema version == engine schema version
        self._check_schema_version_guardrail()

        # 18. Monte-Carlo inner paths ≥ min_paths (500)
        self._check_mc_paths_guardrail(metrics)

        # 19. Seed reproducibility check (rerun hash)
        self._check_seed_reproducibility_guardrail(metrics)

    def _check_stress_ltv_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check stress LTV guardrail.

        Guardrail: Stress-LTV (−20% price dip) ≤ 90%
        Severity: FAIL
        Layer: Unit

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "LTV_STRESS_HIGH" in self.checked_guardrails:
            return

        self.checked_guardrails.add("LTV_STRESS_HIGH")

        # Get stress LTV metrics
        credit_metrics = metrics.get("credit_metrics", {})
        stress_ltv = credit_metrics.get("stress_ltv", {})
        loan_stress_ltvs = stress_ltv.get("loan_stress_ltvs", {})

        # Check each loan
        for loan_id, ltv in loan_stress_ltvs.items():
            # Ensure ltv is a numeric value, not a list
            if isinstance(ltv, (list, tuple)):
                ltv = ltv[0] if ltv else 0.0
            elif not isinstance(ltv, (int, float)):
                continue

            if ltv > 0.9:  # 90%
                self.report.breaches.append(
                    Breach(
                        code="LTV_STRESS_HIGH",
                        severity=Severity.FAIL,
                        message=f"Loan {loan_id} has stress LTV of {ltv:.2%}, exceeding 90%",
                        value=ltv,
                        threshold=0.9,
                        unit="%",
                        layer="Unit",
                    )
                )

    def _check_loan_size_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check loan size guardrail.

        Guardrail: Principal ≤ loan_ticket_limit_zone
        Severity: FAIL
        Layer: Unit

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "LOAN_SIZE_LIMIT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("LOAN_SIZE_LIMIT")

        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return

        # Get loans
        loans = portfolio.get("loans", [])

        if not loans:
            return

        # Get zone ticket limits from config
        zone_ticket_limits = self.guardrail_config.get("zone_ticket_limits", {
            "green": 500000,  # $500k
            "orange": 400000,  # $400k
            "red": 300000,  # $300k
        })

        # Check each loan
        for loan in loans:
            loan_id = loan.get("loan_id")
            loan_amount = loan.get("loan_amount", 0.0)
            suburb = loan.get("suburb")

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if hasattr(self.context, "tls_manager") and self.context.tls_manager and suburb:
                suburb_data = self.context.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            # Get ticket limit for zone
            ticket_limit = zone_ticket_limits.get(suburb_zone, 500000)

            # Ensure loan_amount is a numeric value, not a list
            if isinstance(loan_amount, (list, tuple)):
                loan_amount = loan_amount[0] if loan_amount else 0.0
            elif not isinstance(loan_amount, (int, float)):
                continue

            if loan_amount > ticket_limit:
                self.report.breaches.append(
                    Breach(
                        code="LOAN_SIZE_LIMIT",
                        severity=Severity.FAIL,
                        message=f"Loan {loan_id} amount ${loan_amount:,.0f} exceeds {suburb_zone} zone limit of ${ticket_limit:,.0f}",
                        value=loan_amount,
                        threshold=ticket_limit,
                        unit="$",
                        layer="Unit",
                    )
                )

    def _check_exit_month_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check exit month guardrail.

        Guardrail: Exit month ≤ max_term_months (120)
        Severity: FAIL
        Layer: Unit

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "EXIT_MONTH_LIMIT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("EXIT_MONTH_LIMIT")

        # Get exits
        exits = self.context.exits if hasattr(self.context, "exits") else {}

        if not exits:
            return

        # Ensure exits is a dictionary, not a list
        if isinstance(exits, list):
            # Convert list of exit objects to dictionary
            exits_dict = {}
            for i, exit_obj in enumerate(exits):
                if hasattr(exit_obj, 'loan_id'):
                    exits_dict[exit_obj.loan_id] = exit_obj
                else:
                    exits_dict[f"exit_{i}"] = exit_obj
            exits = exits_dict

        # Get max term months from config
        max_term_months = self.guardrail_config.get("max_term_months", 120)  # 10 years

        # Check each exit
        for loan_id, exit_data in exits.items():
            exit_month = exit_data.get("exit_month", 0)

            # Ensure exit_month is a numeric value, not a list
            if isinstance(exit_month, (list, tuple)):
                exit_month = exit_month[0] if exit_month else 0
            elif not isinstance(exit_month, (int, float)):
                continue

            if exit_month > max_term_months:
                self.report.breaches.append(
                    Breach(
                        code="EXIT_MONTH_LIMIT",
                        severity=Severity.FAIL,
                        message=f"Loan {loan_id} exit month {exit_month} exceeds maximum term of {max_term_months} months",
                        value=exit_month,
                        threshold=max_term_months,
                        unit="months",
                        layer="Unit",
                    )
                )

    def _check_zone_nav_weight_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check zone NAV weight guardrail.

        Guardrail: Zone NAV weight ≤ capital_limit_zone (e.g. Red ≤ 5%)
        Severity: FAIL
        Layer: Zone

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "ZONE_RED_WEIGHT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("ZONE_RED_WEIGHT")

        # Get concentration metrics
        concentration_metrics = metrics.get("concentration_metrics", {})
        zone_exposure = concentration_metrics.get("zone_exposure", {})

        # Get zone limits from config
        zone_limits = self.guardrail_config.get("zone_limits", {
            "red": 0.05,  # 5%
            "orange": 0.3,  # 30%
            "green": 1.0,  # 100%
        })

        # Check each zone
        for zone, exposure in zone_exposure.items():
            limit = zone_limits.get(zone, 1.0)

            # Ensure exposure is a numeric value, not a list
            if isinstance(exposure, (list, tuple)):
                exposure = exposure[0] if exposure else 0.0
            elif not isinstance(exposure, (int, float)):
                continue

            if exposure > limit:
                self.report.breaches.append(
                    Breach(
                        code=f"ZONE_{zone.upper()}_WEIGHT",
                        severity=Severity.FAIL,
                        message=f"{zone.capitalize()} zone exposure of {exposure:.2%} exceeds limit of {limit:.2%}",
                        value=exposure,
                        threshold=limit,
                        unit="%",
                        layer="Zone",
                    )
                )

    def _check_zone_default_rate_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check zone default rate guardrail.

        Guardrail: Default rate zone ≤ 2× city_avg_default
        Severity: WARN
        Layer: Zone

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "PD_ZONE_ALERT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("PD_ZONE_ALERT")

        # Get credit metrics
        credit_metrics = metrics.get("credit_metrics", {})
        default_probability = credit_metrics.get("default_probability", {})
        zone_default_probs = default_probability.get("zone_default_probs", {})

        # Get city average default rate
        city_avg_default = self.guardrail_config.get("city_avg_default", 0.01)  # 1%

        # Check each zone
        for zone, default_rate in zone_default_probs.items():
            threshold = 2 * city_avg_default

            # Ensure default_rate is a numeric value, not a list
            if isinstance(default_rate, (list, tuple)):
                default_rate = default_rate[0] if default_rate else 0.0
            elif not isinstance(default_rate, (int, float)):
                continue

            if default_rate > threshold:
                self.report.breaches.append(
                    Breach(
                        code="PD_ZONE_ALERT",
                        severity=Severity.WARN,
                        message=f"{zone.capitalize()} zone default rate of {default_rate:.2%} exceeds 2× city average of {threshold:.2%}",
                        value=default_rate,
                        threshold=threshold,
                        unit="%",
                        layer="Zone",
                    )
                )

    def _check_zone_price_volatility_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check zone price volatility guardrail.

        Guardrail: Sigma price zone ≤ 3× city σ
        Severity: WARN
        Layer: Zone

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "ZONE_VOLATILITY_HIGH" in self.checked_guardrails:
            return

        self.checked_guardrails.add("ZONE_VOLATILITY_HIGH")

        # Get market price metrics
        market_price_metrics = metrics.get("market_price_metrics", {})
        volatility = market_price_metrics.get("volatility", {})
        zone_volatilities = volatility.get("zones", {})

        # Get city average volatility
        city_avg_volatility = self.guardrail_config.get("city_avg_volatility", 0.05)  # 5%

        # Check each zone
        for zone, vol in zone_volatilities.items():
            threshold = 3 * city_avg_volatility

            # Ensure vol is a numeric value, not a list
            if isinstance(vol, (list, tuple)):
                vol = vol[0] if vol else 0.0
            elif not isinstance(vol, (int, float)):
                continue

            if vol > threshold:
                self.report.breaches.append(
                    Breach(
                        code="ZONE_VOLATILITY_HIGH",
                        severity=Severity.WARN,
                        message=f"{zone.capitalize()} zone price volatility of {vol:.2%} exceeds 3× city average of {threshold:.2%}",
                        value=vol,
                        threshold=threshold,
                        unit="%",
                        layer="Zone",
                    )
                )

    def _check_suburb_concentration_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check suburb concentration guardrail.

        Guardrail: Single suburb weight ≤ 10% NAV
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "SUBURB_CONCENTRATION" in self.checked_guardrails:
            return

        self.checked_guardrails.add("SUBURB_CONCENTRATION")

        # Get concentration metrics
        concentration_metrics = metrics.get("concentration_metrics", {})
        suburb_exposure = concentration_metrics.get("suburb_exposure", {})

        # Get suburb concentration limit from config
        suburb_concentration_limit = self.guardrail_config.get("suburb_concentration_limit", 0.1)  # 10%

        # Check each suburb
        for suburb, exposure in suburb_exposure.items():
            # Ensure exposure is a numeric value, not a list
            if isinstance(exposure, (list, tuple)):
                exposure = exposure[0] if exposure else 0.0
            elif not isinstance(exposure, (int, float)):
                continue

            if exposure > suburb_concentration_limit:
                self.report.breaches.append(
                    Breach(
                        code="SUBURB_CONCENTRATION",
                        severity=Severity.FAIL,
                        message=f"Suburb {suburb} exposure of {exposure:.2%} exceeds limit of {suburb_concentration_limit:.2%}",
                        value=exposure,
                        threshold=suburb_concentration_limit,
                        unit="%",
                        layer="Portfolio",
                    )
                )

    def _check_loan_concentration_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check loan concentration guardrail.

        Guardrail: Largest single loan weight ≤ 2% NAV
        Severity: WARN
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "LOAN_CONCENTRATION" in self.checked_guardrails:
            return

        self.checked_guardrails.add("LOAN_CONCENTRATION")

        # Get concentration metrics
        concentration_metrics = metrics.get("concentration_metrics", {})
        loan_exposure = concentration_metrics.get("loan_exposure", {})

        # Get loan concentration limit from config
        loan_concentration_limit = self.guardrail_config.get("loan_concentration_limit", 0.02)  # 2%

        # Check each loan
        for loan_id, exposure in loan_exposure.items():
            # Ensure exposure is a numeric value, not a list
            if isinstance(exposure, (list, tuple)):
                exposure = exposure[0] if exposure else 0.0
            elif not isinstance(exposure, (int, float)):
                continue

            if exposure > loan_concentration_limit:
                self.report.breaches.append(
                    Breach(
                        code="LOAN_CONCENTRATION",
                        severity=Severity.WARN,
                        message=f"Loan {loan_id} exposure of {exposure:.2%} exceeds limit of {loan_concentration_limit:.2%}",
                        value=exposure,
                        threshold=loan_concentration_limit,
                        unit="%",
                        layer="Portfolio",
                    )
                )

    def _check_nav_utilization_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check NAV utilization guardrail.

        Guardrail: NAV facility utilisation ≤ max_nav_util (cfg)
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "LEVERAGE_UTIL" in self.checked_guardrails:
            return

        self.checked_guardrails.add("LEVERAGE_UTIL")

        # Get leverage metrics
        leverage_metrics = metrics.get("leverage_metrics", {})
        nav_utilisation = leverage_metrics.get("nav_utilisation", 0.0)

        # Get max NAV utilization from config
        max_nav_util = self.guardrail_config.get("max_nav_util", 0.6)  # 60%

        # Ensure nav_utilisation is a numeric value, not a list
        if isinstance(nav_utilisation, (list, tuple)):
            nav_utilisation = nav_utilisation[0] if nav_utilisation else 0.0
        elif not isinstance(nav_utilisation, (int, float)):
            return

        if nav_utilisation > max_nav_util:
            self.report.breaches.append(
                Breach(
                    code="LEVERAGE_UTIL",
                    severity=Severity.FAIL,
                    message=f"NAV utilization of {nav_utilisation:.2%} exceeds limit of {max_nav_util:.2%}",
                    value=nav_utilisation,
                    threshold=max_nav_util,
                    unit="%",
                    layer="Portfolio",
                )
            )

    def _check_interest_coverage_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check interest coverage guardrail.

        Guardrail: Interest-coverage ratio (ICR) ≥ 1.25×
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "INTEREST_COVERAGE" in self.checked_guardrails:
            return

        self.checked_guardrails.add("INTEREST_COVERAGE")

        # Get leverage metrics
        leverage_metrics = metrics.get("leverage_metrics", {})
        interest_coverage = leverage_metrics.get("interest_coverage", 0.0)

        # Get min interest coverage from config
        min_interest_coverage = self.guardrail_config.get("min_interest_coverage", 1.25)  # 1.25×

        # Ensure interest_coverage is a numeric value, not a list
        if isinstance(interest_coverage, (list, tuple)):
            interest_coverage = interest_coverage[0] if interest_coverage else 0.0
        elif not isinstance(interest_coverage, (int, float)):
            return

        if interest_coverage < min_interest_coverage:
            self.report.breaches.append(
                Breach(
                    code="INTEREST_COVERAGE",
                    severity=Severity.FAIL,
                    message=f"Interest coverage ratio of {interest_coverage:.2f}× is below minimum of {min_interest_coverage:.2f}×",
                    value=interest_coverage,
                    threshold=min_interest_coverage,
                    unit="×",
                    layer="Portfolio",
                )
            )

    def _check_liquidity_buffer_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check liquidity buffer guardrail.

        Guardrail: Liquidity buffer (cash + undrawn) ≥ 4% NAV
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "LIQUIDITY_BUFFER_LOW" in self.checked_guardrails:
            return

        self.checked_guardrails.add("LIQUIDITY_BUFFER_LOW")

        # Get liquidity metrics
        liquidity_metrics = metrics.get("liquidity_metrics", {})
        liquidity_buffer = liquidity_metrics.get("liquidity_buffer", 0.0)

        # Get min liquidity buffer from config
        min_liquidity_buffer = self.guardrail_config.get("min_liquidity_buffer", 0.04)  # 4%

        # Ensure liquidity_buffer is a numeric value, not a list
        if isinstance(liquidity_buffer, (list, tuple)):
            liquidity_buffer = liquidity_buffer[0] if liquidity_buffer else 0.0
        elif not isinstance(liquidity_buffer, (int, float)):
            return

        if liquidity_buffer < min_liquidity_buffer:
            self.report.breaches.append(
                Breach(
                    code="LIQUIDITY_BUFFER_LOW",
                    severity=Severity.FAIL,
                    message=f"Liquidity buffer of {liquidity_buffer:.2%} is below minimum of {min_liquidity_buffer:.2%}",
                    value=liquidity_buffer,
                    threshold=min_liquidity_buffer,
                    unit="%",
                    layer="Portfolio",
                )
            )

    def _check_wal_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check WAL guardrail.

        Guardrail: Weighted-Avg Life (WAL) ≤ 8 yrs unless wal_override=true
        Severity: WARN
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "WAL_SOFT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("WAL_SOFT")

        # Check if WAL override is enabled
        wal_override = self.guardrail_config.get("wal_override", False)

        if wal_override:
            return

        # Get liquidity metrics
        liquidity_metrics = metrics.get("liquidity_metrics", {})
        wal = liquidity_metrics.get("wal", 0.0)

        # Get max WAL from config
        max_wal = self.guardrail_config.get("max_wal", 8.0)  # 8 years

        # Ensure wal is a numeric value, not a list
        if isinstance(wal, (list, tuple)):
            wal = wal[0] if wal else 0.0
        elif not isinstance(wal, (int, float)):
            return

        if wal > max_wal:
            self.report.breaches.append(
                Breach(
                    code="WAL_SOFT",
                    severity=Severity.WARN,
                    message=f"Weighted Average Life (WAL) of {wal:.2f} years exceeds limit of {max_wal:.2f} years",
                    value=wal,
                    threshold=max_wal,
                    unit="years",
                    layer="Portfolio",
                )
            )

    def _check_var_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check VaR guardrail.

        Guardrail: VaR-99 ≤ 15% NAV (MC mode only)
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "VaR_99_LIMIT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("VaR_99_LIMIT")

        # Check if Monte Carlo is enabled with safe attribute access
        monte_carlo_obj = getattr(self.config, "monte_carlo", {})
        monte_carlo_dict = monte_carlo_obj.dict() if hasattr(monte_carlo_obj, 'dict') else (monte_carlo_obj if isinstance(monte_carlo_obj, dict) else {})
        monte_carlo_enabled = monte_carlo_dict.get("enabled", False)

        if not monte_carlo_enabled:
            return

        # Get market price metrics
        market_price_metrics = metrics.get("market_price_metrics", {})
        var = market_price_metrics.get("var", {})
        var_99 = var.get("var_99", 0.0)

        # Get max VaR-99 from config
        max_var_99 = self.guardrail_config.get("max_var_99", 0.15)  # 15%

        # Ensure var_99 is a numeric value, not a list
        if isinstance(var_99, (list, tuple)):
            var_99 = var_99[0] if var_99 else 0.0
        elif not isinstance(var_99, (int, float)):
            return

        if var_99 > max_var_99:
            self.report.breaches.append(
                Breach(
                    code="VaR_99_LIMIT",
                    severity=Severity.FAIL,
                    message=f"VaR-99 of {var_99:.2%} exceeds limit of {max_var_99:.2%}",
                    value=var_99,
                    threshold=max_var_99,
                    unit="%",
                    layer="Portfolio",
                )
            )

    def _check_cvar_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check CVaR guardrail.

        Guardrail: CVaR-99 ≤ 20% NAV (MC mode only)
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "CVaR_99_LIMIT" in self.checked_guardrails:
            return

        self.checked_guardrails.add("CVaR_99_LIMIT")

        # Check if Monte Carlo is enabled with safe attribute access
        monte_carlo_obj = getattr(self.config, "monte_carlo", {})
        monte_carlo_dict = monte_carlo_obj.dict() if hasattr(monte_carlo_obj, 'dict') else (monte_carlo_obj if isinstance(monte_carlo_obj, dict) else {})
        monte_carlo_enabled = monte_carlo_dict.get("enabled", False)

        if not monte_carlo_enabled:
            return

        # Get market price metrics
        market_price_metrics = metrics.get("market_price_metrics", {})
        cvar = market_price_metrics.get("cvar", {})
        cvar_99 = cvar.get("cvar_99", 0.0)

        # Get max CVaR-99 from config
        max_cvar_99 = self.guardrail_config.get("max_cvar_99", 0.2)  # 20%

        # Ensure cvar_99 is a numeric value, not a list
        if isinstance(cvar_99, (list, tuple)):
            cvar_99 = cvar_99[0] if cvar_99 else 0.0
        elif not isinstance(cvar_99, (int, float)):
            return

        if cvar_99 > max_cvar_99:
            self.report.breaches.append(
                Breach(
                    code="CVaR_99_LIMIT",
                    severity=Severity.FAIL,
                    message=f"CVaR-99 of {cvar_99:.2%} exceeds limit of {max_cvar_99:.2%}",
                    value=cvar_99,
                    threshold=max_cvar_99,
                    unit="%",
                    layer="Portfolio",
                )
            )

    def _check_irr_p5_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check IRR P5 guardrail.

        Guardrail: Net-IRR P5 ≥ hurdle (8%) – 250 bp
        Severity: WARN
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "IRR_P5_LOW" in self.checked_guardrails:
            return

        self.checked_guardrails.add("IRR_P5_LOW")

        # Check if Monte Carlo is enabled with safe attribute access
        monte_carlo_obj = getattr(self.config, "monte_carlo", {})
        monte_carlo_dict = monte_carlo_obj.dict() if hasattr(monte_carlo_obj, 'dict') else (monte_carlo_obj if isinstance(monte_carlo_obj, dict) else {})
        monte_carlo_enabled = monte_carlo_dict.get("enabled", False)

        if not monte_carlo_enabled:
            return

        # Get performance metrics
        performance_metrics = metrics.get("performance_metrics", {})
        irr_distribution = performance_metrics.get("irr_distribution", {})
        irr_p5 = irr_distribution.get("p5", 0.0)

        # Get hurdle rate from config with safe attribute access
        hurdle_rate = getattr(self.config, "hurdle_rate", 0.08)  # 8%

        # Calculate minimum acceptable IRR P5
        min_irr_p5 = hurdle_rate - 0.025  # hurdle - 250 bp

        # Ensure irr_p5 is a numeric value, not a list
        if isinstance(irr_p5, (list, tuple)):
            irr_p5 = irr_p5[0] if irr_p5 else 0.0
        elif not isinstance(irr_p5, (int, float)):
            return

        if irr_p5 < min_irr_p5:
            self.report.breaches.append(
                Breach(
                    code="IRR_P5_LOW",
                    severity=Severity.WARN,
                    message=f"IRR P5 of {irr_p5:.2%} is below minimum of {min_irr_p5:.2%} (hurdle {hurdle_rate:.2%} - 250 bp)",
                    value=irr_p5,
                    threshold=min_irr_p5,
                    unit="%",
                    layer="Portfolio",
                )
            )

    def _check_hurdle_clear_probability_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check hurdle clear probability guardrail.

        Guardrail: Hurdle-clear probability ≥ 70% (MC mode only)
        Severity: FAIL
        Layer: Portfolio

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "HURDLE_CLEAR_PROB" in self.checked_guardrails:
            return

        self.checked_guardrails.add("HURDLE_CLEAR_PROB")

        # Check if Monte Carlo is enabled with safe attribute access
        monte_carlo_obj = getattr(self.config, "monte_carlo", {})
        monte_carlo_dict = monte_carlo_obj.dict() if hasattr(monte_carlo_obj, 'dict') else (monte_carlo_obj if isinstance(monte_carlo_obj, dict) else {})
        monte_carlo_enabled = monte_carlo_dict.get("enabled", False)

        if not monte_carlo_enabled:
            return

        # Get performance metrics
        performance_metrics = metrics.get("performance_metrics", {})
        hurdle_clear_probability = performance_metrics.get("hurdle_clear_probability", {})
        probability = hurdle_clear_probability.get("value")

        if probability is None:
            return

        # Get min hurdle clear probability from config
        min_hurdle_clear_prob = self.guardrail_config.get("min_hurdle_clear_prob", 0.7)  # 70%

        # Ensure probability is a numeric value, not a list
        if isinstance(probability, (list, tuple)):
            probability = probability[0] if probability else 0.0
        elif not isinstance(probability, (int, float)):
            return

        if probability < min_hurdle_clear_prob:
            self.report.breaches.append(
                Breach(
                    code="HURDLE_CLEAR_PROB",
                    severity=Severity.FAIL,
                    message=f"Hurdle-clear probability of {probability:.2%} is below minimum of {min_hurdle_clear_prob:.2%}",
                    value=probability,
                    threshold=min_hurdle_clear_prob,
                    unit="%",
                    layer="Portfolio",
                )
            )

    def _check_schema_version_guardrail(self) -> None:
        """
        Check schema version guardrail.

        Guardrail: Config JSON schema version == engine schema version
        Severity: INFO
        Layer: Run

        Args:
            None
        """
        # Skip if already checked
        if "INFO_SCHEMA_MISMATCH" in self.checked_guardrails:
            return

        self.checked_guardrails.add("INFO_SCHEMA_MISMATCH")

        # Get schema versions with safe attribute access
        config_schema_version = getattr(self.config, "schema_version", "1.0.0")
        engine_schema_version = "1.0.0"  # This should be a constant defined elsewhere

        if config_schema_version != engine_schema_version:
            self.report.breaches.append(
                Breach(
                    code="INFO_SCHEMA_MISMATCH",
                    severity=Severity.INFO,
                    message=f"Config schema version {config_schema_version} does not match engine schema version {engine_schema_version}",
                    value=None,
                    threshold=None,
                    unit=None,
                    layer="Run",
                )
            )

    def _check_mc_paths_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check Monte Carlo paths guardrail.

        Guardrail: Monte-Carlo inner paths ≥ min_paths (500)
        Severity: WARN
        Layer: Run

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "MC_LOW_PATHS" in self.checked_guardrails:
            return

        self.checked_guardrails.add("MC_LOW_PATHS")

        # Check if Monte Carlo is enabled with safe attribute access
        monte_carlo_obj = getattr(self.config, "monte_carlo", {})
        monte_carlo_dict = monte_carlo_obj.dict() if hasattr(monte_carlo_obj, 'dict') else (monte_carlo_obj if isinstance(monte_carlo_obj, dict) else {})
        monte_carlo_enabled = monte_carlo_dict.get("enabled", False)

        if not monte_carlo_enabled:
            return

        # Get Monte Carlo metrics
        monte_carlo_metrics = metrics.get("monte_carlo_metrics", {})
        inner_paths = monte_carlo_metrics.get("inner_paths", 0)

        # Get min paths from config
        min_paths = self.guardrail_config.get("min_paths", 500)

        # Ensure inner_paths is a numeric value, not a list
        if isinstance(inner_paths, (list, tuple)):
            inner_paths = inner_paths[0] if inner_paths else 0
        elif not isinstance(inner_paths, (int, float)):
            return

        if inner_paths < min_paths:
            self.report.breaches.append(
                Breach(
                    code="MC_LOW_PATHS",
                    severity=Severity.WARN,
                    message=f"Monte Carlo inner paths {inner_paths} is below minimum of {min_paths}",
                    value=inner_paths,
                    threshold=min_paths,
                    unit="paths",
                    layer="Run",
                )
            )

    def _check_seed_reproducibility_guardrail(self, metrics: Dict[str, Any]) -> None:
        """
        Check seed reproducibility guardrail.

        Guardrail: Seed reproducibility check (rerun hash)
        Severity: INFO
        Layer: Run

        Args:
            metrics: Simulation metrics
        """
        # Skip if already checked
        if "SEED_REPRODUCIBILITY" in self.checked_guardrails:
            return

        self.checked_guardrails.add("SEED_REPRODUCIBILITY")

        # This is a placeholder for a more complex check that would compare
        # the results of multiple runs with the same seed to ensure reproducibility
        # For now, we just check if a seed was specified

        seed = getattr(self.config, "seed", None)

        if seed is None:
            self.report.breaches.append(
                Breach(
                    code="SEED_REPRODUCIBILITY",
                    severity=Severity.INFO,
                    message="No seed specified, results may not be reproducible",
                    value=None,
                    threshold=None,
                    unit=None,
                    layer="Run",
                )
            )