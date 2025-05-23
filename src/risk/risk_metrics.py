"""
Risk Metrics module for the EQU IHOME SIM ENGINE v2.

This module calculates risk metrics for the simulation, including:
- Value at Risk (VaR)
- Conditional Value at Risk (CVaR)
- Sharpe Ratio, Sortino Ratio, Calmar Ratio
- Maximum Drawdown
- Beta, Alpha, Information Ratio
- Stress testing and scenario analysis
"""

import logging
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Union
import structlog
import time
from datetime import datetime

from src.engine.simulation_context import SimulationContext
from src.api.websocket_manager import get_websocket_manager
from src.utils.financial import (
    npv, irr, xirr, equity_multiple, roi, payback_period,
    var, sharpe_ratio, max_drawdown
)
from src.utils.error_handler import handle_exception, log_error
from src.utils.metrics import increment_counter, observe_histogram, set_gauge

# Set up logging
logger = structlog.get_logger(__name__)

class RiskMetricsCalculator:
    """
    Calculator for risk metrics.

    This class calculates risk metrics for the simulation, including:
    - Value at Risk (VaR)
    - Conditional Value at Risk (CVaR)
    - Sharpe Ratio, Sortino Ratio, Calmar Ratio
    - Maximum Drawdown
    - Beta, Alpha, Information Ratio
    - Stress testing and scenario analysis
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the risk metrics calculator.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config
        self.websocket_manager = get_websocket_manager()

        # Get risk metrics configuration with safe attribute access
        risk_config_obj = getattr(self.config, "risk_metrics", {})
        if hasattr(risk_config_obj, 'dict'):
            self.risk_config = risk_config_obj.dict()
        elif isinstance(risk_config_obj, dict):
            self.risk_config = risk_config_obj
        else:
            self.risk_config = {}

        self.var_confidence_level = self.risk_config.get("var_confidence_level", 0.95)
        self.risk_free_rate = self.risk_config.get("risk_free_rate", 0.03)
        self.benchmark_return = self.risk_config.get("benchmark_return", 0.07)
        self.min_acceptable_return = self.risk_config.get("min_acceptable_return", 0.04)
        self.tail_risk_threshold = self.risk_config.get("tail_risk_threshold", 0.05)

        # Check if Monte Carlo is enabled with safe attribute access
        monte_carlo_obj = getattr(self.config, "monte_carlo", {})
        if hasattr(monte_carlo_obj, 'dict'):
            monte_carlo_dict = monte_carlo_obj.dict()
        elif isinstance(monte_carlo_obj, dict):
            monte_carlo_dict = monte_carlo_obj
        else:
            monte_carlo_dict = {}

        self.monte_carlo_enabled = monte_carlo_dict.get("enabled", False)
        self.monte_carlo_simulations = self.risk_config.get("monte_carlo_simulations", 1000)

        # Log Monte Carlo status
        if self.monte_carlo_enabled:
            logger.info(f"Monte Carlo is enabled with {self.monte_carlo_simulations} simulations")
        else:
            logger.info("Monte Carlo is disabled, using deterministic calculations")

        # Get TLS data manager if available
        self.tls_manager = None
        if hasattr(self.context, "tls_manager"):
            self.tls_manager = self.context.tls_manager

        # Extract existing metrics
        self.existing_metrics = self._extract_existing_metrics()

        # Initialize results
        self.risk_metrics = {}
        self.market_price_metrics = {}
        self.credit_metrics = {}
        self.liquidity_metrics = {}
        self.leverage_metrics = {}
        self.concentration_metrics = {}
        self.performance_metrics = {}
        self.stress_test_results = {}
        self.scenario_analysis_results = {}
        self.visualization_data = {}

    def _extract_existing_metrics(self) -> Dict[str, Any]:
        """
        Extract existing metrics from the simulation context.

        Returns:
            Dictionary of existing metrics
        """
        metrics = {}

        # Extract cashflow metrics with safe access
        if hasattr(self.context, "cashflows") and self.context.cashflows:
            # Handle both dict and list cases for cashflows
            if isinstance(self.context.cashflows, dict):
                cashflow_metrics = self.context.cashflows.get("metrics", {})
                fund_level_metrics = cashflow_metrics.get("fund_level_metrics", {}) if isinstance(cashflow_metrics, dict) else {}
            else:
                fund_level_metrics = {}

            # Add fund-level metrics
            metrics.update({
                "irr": fund_level_metrics.get("irr"),
                "moic": fund_level_metrics.get("moic"),
                "tvpi": fund_level_metrics.get("tvpi"),
                "dpi": fund_level_metrics.get("dpi"),
                "rvpi": fund_level_metrics.get("rvpi"),
                "payback_period": fund_level_metrics.get("payback_period"),
                "cash_on_cash": fund_level_metrics.get("cash_on_cash"),
                "npv": fund_level_metrics.get("npv"),
            })

        # Extract exit simulator metrics with safe access
        if hasattr(self.context, "exits") and self.context.exits:
            # Handle both dict and list cases for exits
            if isinstance(self.context.exits, dict):
                exit_stats = self.context.exits.get("enhanced_stats", {})
                risk_metrics = exit_stats.get("risk_metrics", {}) if isinstance(exit_stats, dict) else {}
            else:
                risk_metrics = {}

            # Add exit risk metrics
            metrics.update({
                "value_at_risk": risk_metrics.get("value_at_risk"),
                "conditional_var": risk_metrics.get("conditional_var"),
                "tail_probability": risk_metrics.get("tail_probability"),
                "tail_severity": risk_metrics.get("tail_severity"),
                "max_drawdown": risk_metrics.get("max_drawdown"),
                "stress_test_roi": risk_metrics.get("stress_test_roi"),
                "roi_volatility": risk_metrics.get("roi_volatility"),
            })

        # Extract price path metrics
        if hasattr(self.context, "price_paths") and self.context.price_paths:
            price_path_stats = self.context.price_paths.get("stats", {})

            # Add price path metrics (using average across zones)
            zone_stats = price_path_stats.get("zone_stats", {})
            if zone_stats:
                volatility_values = [stats.get("volatility", 0) for stats in zone_stats.values()]
                sharpe_values = [stats.get("sharpe_ratio", 0) for stats in zone_stats.values()]
                max_drawdown_values = [stats.get("max_drawdown", 0) for stats in zone_stats.values()]

                metrics.update({
                    "price_volatility": np.mean(volatility_values) if volatility_values else None,
                    "price_sharpe_ratio": np.mean(sharpe_values) if sharpe_values else None,
                    "price_max_drawdown": np.mean(max_drawdown_values) if max_drawdown_values else None,
                })

        # Extract reinvestment metrics with safe access
        if hasattr(self.context, "reinvestment") and self.context.reinvestment:
            # Handle both dict and list cases for reinvestment
            if isinstance(self.context.reinvestment, dict):
                reinvest_stats = self.context.reinvestment.get("stats", {})
                concentration = reinvest_stats.get("concentration", {}) if isinstance(reinvest_stats, dict) else {}
            else:
                concentration = {}

            # Add concentration metrics
            metrics.update({
                "zone_hhi": concentration.get("zone_hhi"),
                "suburb_hhi": concentration.get("suburb_hhi"),
                "top_5_concentration": concentration.get("top_5_concentration"),
                "top_10_concentration": concentration.get("top_10_concentration"),
            })

        return metrics

    def calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate risk metrics.

        Returns:
            Dictionary of risk metrics
        """
        logger.info("Calculating risk metrics")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="risk_metrics",
            progress=10.0,
            message="Calculating risk metrics",
        )

        # Start with existing metrics
        self.risk_metrics = self.existing_metrics.copy()

        # Calculate market/price metrics
        self._calculate_market_price_metrics()

        # Calculate credit metrics
        self._calculate_credit_metrics()

        # Calculate liquidity metrics
        self._calculate_liquidity_metrics()

        # Calculate leverage metrics
        self._calculate_leverage_metrics()

        # Calculate concentration metrics
        self._calculate_concentration_metrics()

        # Calculate performance/return-risk metrics
        self._calculate_performance_metrics()

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="risk_metrics",
            progress=50.0,
            message="Risk metrics calculated",
        )

        # Run stress tests
        self._run_stress_tests()

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="risk_metrics",
            progress=70.0,
            message="Stress tests completed",
        )

        # Run scenario analysis
        self._run_scenario_analysis()

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="risk_metrics",
            progress=90.0,
            message="Scenario analysis completed",
        )

        # Generate visualization data
        self._generate_visualization_data()

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="risk_metrics",
            progress=100.0,
            message="Risk metrics calculation completed",
        )

        # Store results in context
        self.context.metrics = {
            "market_price_metrics": self.market_price_metrics,
            "credit_metrics": self.credit_metrics,
            "liquidity_metrics": self.liquidity_metrics,
            "leverage_metrics": self.leverage_metrics,
            "concentration_metrics": self.concentration_metrics,
            "performance_metrics": self.performance_metrics,
            "stress_test_results": self.stress_test_results,
            "sensitivity_analysis": self.scenario_analysis_results,
            "visualization": self.visualization_data,

            # Keep backward compatibility with existing format
            "return_metrics": self._format_return_metrics(),
            "risk_metrics": self._format_risk_metrics(),
            "risk_adjusted_return_metrics": self._format_risk_adjusted_return_metrics(),
            "market_metrics": self._format_market_metrics(),
        }

        logger.info("Risk metrics calculation completed")

        return self.context.metrics

    def _calculate_market_price_metrics(self) -> None:
        """
        Calculate market/price metrics.

        Metrics:
        1. σ (volatility) unit / zone / port
        2. α idiosyncratic share
        3. β macro / β zone
        4. VaR-95 / VaR-99
        5. CVaR
        """
        logger.info("Calculating market/price metrics")

        # 1. Calculate volatility at unit, zone, and portfolio levels
        self._calculate_volatility_metrics()

        # 2 & 3. Calculate alpha idiosyncratic share and beta from TLS data
        self._calculate_alpha_beta_metrics()

        # 4 & 5. Calculate VaR and CVaR metrics
        self._calculate_var_cvar_metrics()

        # Store in market_price_metrics
        self.market_price_metrics = {
            "volatility": {
                "portfolio": self.risk_metrics.get("volatility"),
                "zones": self._get_zone_volatilities(),
                "units": self._get_unit_volatilities(),
            },
            "alpha_idiosyncratic_share": self.risk_metrics.get("alpha_idiosyncratic_share"),
            "beta": {
                "macro": self.risk_metrics.get("beta_macro"),
                "zone": self.risk_metrics.get("beta_zone"),
            },
            "var": {
                "var_95": self.risk_metrics.get("var_95"),
                "var_99": self.risk_metrics.get("var_99"),
                "is_approximation": True,
                "approximation_method": "analytic log-normal VaR",
            },
            "cvar": {
                "cvar_95": self.risk_metrics.get("cvar_95"),
                "cvar_99": self.risk_metrics.get("cvar_99"),
                "requires_mc": True,
            },
        }

    def _calculate_credit_metrics(self) -> None:
        """
        Calculate credit metrics.

        Metrics:
        7. Current LTV
        8. Stress-LTV
        9. Default probability unit / zone
        11. Portfolio default rate
        """
        logger.info("Calculating credit metrics")

        # 7. Calculate current LTV
        current_ltv = self._calculate_current_ltv()

        # 8. Calculate stress LTV (apply -20% price shock)
        stress_ltv = self._calculate_stress_ltv()

        # 9. Get default probability by unit/zone
        default_probs = self._get_default_probabilities()

        # 11. Calculate portfolio default rate (exposure-weighted PD)
        portfolio_default_rate = self._calculate_portfolio_default_rate()

        # Store in credit_metrics
        self.credit_metrics = {
            "current_ltv": current_ltv,
            "stress_ltv": stress_ltv,
            "default_probability": default_probs,
            "portfolio_default_rate": portfolio_default_rate,
        }

    def _calculate_liquidity_metrics(self) -> None:
        """
        Calculate liquidity metrics.

        Metrics:
        12. Liquidity score
        13. Expected exit lag
        14. WAL
        15. CFaR (cash-flow-at-risk)
        """
        logger.info("Calculating liquidity metrics")

        # 12. Get liquidity score from TLS data
        liquidity_score = self._get_liquidity_score()

        # 13. Calculate expected exit lag
        expected_exit_lag = self._calculate_expected_exit_lag()

        # 14. Calculate WAL (Weighted Average Life)
        wal = self._calculate_wal()

        # 15. CFaR (requires MC, so note that)
        cfar = {
            "value": None,
            "requires_mc": True,
            "note": "Cash-flow-at-risk requires Monte Carlo simulation"
        }

        # Store in liquidity_metrics
        self.liquidity_metrics = {
            "liquidity_score": liquidity_score,
            "expected_exit_lag": expected_exit_lag,
            "wal": wal,
            "cfar": cfar,
        }

    def _calculate_leverage_metrics(self) -> None:
        """
        Calculate leverage metrics.

        Metrics:
        16. NAV utilisation
        17. Interest-coverage
        18. VaR uplift from leverage
        """
        logger.info("Calculating leverage metrics")

        # 16. Calculate NAV utilisation
        nav_utilisation = self._calculate_nav_utilisation()

        # 17. Calculate interest coverage
        interest_coverage = self._calculate_interest_coverage()

        # 18. VaR uplift from leverage (requires MC)
        var_uplift = {
            "value": None,
            "requires_mc": True,
            "note": "VaR uplift from leverage requires Monte Carlo simulation"
        }

        # Store in leverage_metrics
        self.leverage_metrics = {
            "nav_utilisation": nav_utilisation,
            "interest_coverage": interest_coverage,
            "var_uplift": var_uplift,
        }

    def _calculate_concentration_metrics(self) -> None:
        """
        Calculate concentration metrics.

        Metrics:
        19. Zone exposure %
        20. Suburb exposure cap
        21. Single-loan exposure
        """
        logger.info("Calculating concentration metrics")

        # 19. Calculate zone exposure percentages
        zone_exposure = self._calculate_zone_exposure()

        # 20. Calculate suburb exposure cap
        suburb_exposure = self._calculate_suburb_exposure()

        # 21. Calculate single-loan exposure
        single_loan_exposure = self._calculate_single_loan_exposure()

        # Store in concentration_metrics
        self.concentration_metrics = {
            "zone_exposure": zone_exposure,
            "suburb_exposure": suburb_exposure,
            "single_loan_exposure": single_loan_exposure,
            "herfindahl_index": self.risk_metrics.get("zone_hhi"),
            "zone_concentration": {
                "green": self._get_zone_concentration("green"),
                "orange": self._get_zone_concentration("orange"),
                "red": self._get_zone_concentration("red"),
                "hhi": self.risk_metrics.get("zone_hhi")
            },
            "suburb_concentration": {
                "top_5_pct": self.risk_metrics.get("top_5_concentration"),
                "top_10_pct": self.risk_metrics.get("top_10_concentration"),
                "hhi": self.risk_metrics.get("suburb_hhi")
            }
        }

    def _calculate_performance_metrics(self) -> None:
        """
        Calculate performance/return-risk metrics.

        Metrics:
        22. Net-IRR point value
        23. Sharpe ratio
        24. Sortino
        25. Hurdle-clear probability
        """
        logger.info("Calculating performance metrics")

        # 22. Get Net-IRR point value
        net_irr = self._get_net_irr()

        # 23. Calculate Sharpe ratio
        sharpe = self._calculate_sharpe_ratio()

        # 24. Calculate Sortino ratio
        sortino = self._calculate_sortino_ratio_metric()

        # 25. Hurdle-clear probability
        hurdle_clear_probability = self._calculate_hurdle_clear_probability()

        # Store in performance_metrics
        self.performance_metrics = {
            "net_irr": net_irr,
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "hurdle_clear_probability": hurdle_clear_probability,
            "calmar_ratio": self.risk_metrics.get("calmar_ratio"),
            "information_ratio": self.risk_metrics.get("information_ratio"),
            "treynor_ratio": self.risk_metrics.get("treynor_ratio"),
            "omega_ratio": self.risk_metrics.get("omega_ratio"),
            "kappa_ratio": self.risk_metrics.get("kappa_ratio"),
            "gain_loss_ratio": self.risk_metrics.get("gain_loss_ratio")
        }

    def _calculate_hurdle_clear_probability(self) -> Dict[str, Any]:
        """
        Calculate hurdle-clear probability.

        Returns:
            Dictionary with hurdle-clear probability metrics
        """
        # Get hurdle rate from config with safe attribute access
        hurdle_rate = getattr(self.config, "hurdle_rate", 0.08)

        # Check if Monte Carlo data is available
        if self.monte_carlo_enabled and hasattr(self.context, "monte_carlo_results"):
            mc_results = self.context.monte_carlo_results
            if mc_results and "returns_distribution" in mc_results:
                # Calculate hurdle-clear probability from Monte Carlo results
                returns_distribution = mc_results.get("returns_distribution", [])
                if returns_distribution:
                    # Count returns above hurdle rate
                    above_hurdle = sum(1 for r in returns_distribution if r >= hurdle_rate)
                    probability = above_hurdle / len(returns_distribution)

                    return {
                        "value": probability,
                        "hurdle_rate": hurdle_rate,
                        "mc_simulations": len(returns_distribution)
                    }

        # If Monte Carlo is not available or no distribution data
        return {
            "value": None,
            "requires_mc": True,
            "hurdle_rate": hurdle_rate,
            "note": "Hurdle-clear probability requires Monte Carlo simulation"
        }

    def _calculate_volatility_metrics(self) -> None:
        """
        Calculate volatility-based metrics.
        """
        logger.info("Calculating volatility metrics")

        # Get returns from cashflows if available
        returns = self._extract_returns()

        if not returns:
            logger.warning("No returns available for volatility calculation")
            return

        # Calculate volatility (standard deviation of returns)
        self.risk_metrics["volatility"] = np.std(returns, ddof=1) if len(returns) > 1 else 0

        # Calculate downside deviation
        self.risk_metrics["downside_deviation"] = self._calculate_downside_deviation(returns)

    def _calculate_alpha_beta_metrics(self) -> None:
        """
        Calculate alpha and beta metrics using TLS data.
        """
        logger.info("Calculating alpha and beta metrics")

        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            logger.warning("No portfolio available for alpha/beta calculation")
            self.risk_metrics["alpha_idiosyncratic_share"] = None
            self.risk_metrics["beta_macro"] = None
            self.risk_metrics["beta_zone"] = None
            return

        # Calculate portfolio beta (macro)
        beta_macro = self._calculate_portfolio_beta_macro()
        self.risk_metrics["beta_macro"] = beta_macro

        # Calculate portfolio beta (zone)
        beta_zone = self._calculate_portfolio_beta_zone()
        self.risk_metrics["beta_zone"] = beta_zone

        # Calculate alpha idiosyncratic share
        alpha_idiosyncratic = self._calculate_alpha_idiosyncratic_share()
        self.risk_metrics["alpha_idiosyncratic_share"] = alpha_idiosyncratic

    def _calculate_var_cvar_metrics(self) -> None:
        """
        Calculate Value at Risk (VaR) and Conditional Value at Risk (CVaR) metrics.
        """
        logger.info("Calculating VaR and CVaR metrics")

        # Check if Monte Carlo data is available
        mc_data_available = False
        if self.monte_carlo_enabled and hasattr(self.context, "monte_carlo_results"):
            mc_results = self.context.monte_carlo_results
            if mc_results and "returns_distribution" in mc_results:
                mc_data_available = True
                logger.info("Using Monte Carlo data for VaR/CVaR calculation")

        if mc_data_available:
            # Calculate VaR and CVaR using Monte Carlo simulation results
            self._calculate_var_cvar_from_mc()
        else:
            # Use analytic approximation for deterministic simulation
            logger.info("Using analytic approximation for VaR/CVaR calculation")
            self._calculate_var_cvar_analytic()

    def _calculate_var_cvar_from_mc(self) -> None:
        """
        Calculate VaR and CVaR using Monte Carlo simulation results.
        """
        # Get returns distribution from Monte Carlo results with safe access
        mc_results = self.context.monte_carlo_results
        if isinstance(mc_results, dict):
            returns_distribution = mc_results.get("returns_distribution", [])
        else:
            returns_distribution = []

        if not returns_distribution:
            logger.warning("No returns distribution available for VaR/CVaR calculation")
            # Fall back to analytic approximation
            self._calculate_var_cvar_analytic()
            return

        # Sort returns for percentile calculation
        sorted_returns = sorted(returns_distribution)
        n = len(sorted_returns)

        # Calculate VaR 95% (5th percentile of negative returns)
        var_95_index = int(n * 0.05)
        var_95 = -sorted_returns[var_95_index]
        self.risk_metrics["var_95"] = var_95

        # Calculate VaR 99% (1st percentile of negative returns)
        var_99_index = int(n * 0.01)
        var_99 = -sorted_returns[var_99_index]
        self.risk_metrics["var_99"] = var_99

        # Calculate CVaR 95% (average of returns below 5th percentile)
        cvar_95_values = sorted_returns[:var_95_index+1]
        cvar_95 = -np.mean(cvar_95_values) if cvar_95_values else var_95
        self.risk_metrics["cvar_95"] = cvar_95

        # Calculate CVaR 99% (average of returns below 1st percentile)
        cvar_99_values = sorted_returns[:var_99_index+1]
        cvar_99 = -np.mean(cvar_99_values) if cvar_99_values else var_99
        self.risk_metrics["cvar_99"] = cvar_99

    def _calculate_var_cvar_analytic(self) -> None:
        """
        Calculate VaR and CVaR using analytic approximation.
        """
        # Get returns from cashflows if available
        returns = self._extract_returns()

        if not returns:
            logger.warning("No returns available for VaR/CVaR calculation")
            self.risk_metrics["var_95"] = None
            self.risk_metrics["var_99"] = None
            self.risk_metrics["cvar_95"] = None
            self.risk_metrics["cvar_99"] = None
            return

        # Calculate VaR at different confidence levels
        # For deterministic simulation, use analytic log-normal VaR: VaR = N⁻¹(0.99)*σ*√T – μT
        volatility = self.risk_metrics.get("volatility", 0.0)
        mean_return = np.mean(returns) if returns else 0.0
        time_horizon = 1.0  # 1 year

        from scipy import stats

        # Calculate VaR 95%
        z_score_95 = stats.norm.ppf(0.95)
        var_95 = z_score_95 * volatility * np.sqrt(time_horizon) - mean_return * time_horizon
        self.risk_metrics["var_95"] = var_95

        # Calculate VaR 99%
        z_score_99 = stats.norm.ppf(0.99)
        var_99 = z_score_99 * volatility * np.sqrt(time_horizon) - mean_return * time_horizon
        self.risk_metrics["var_99"] = var_99

        # For CVaR, note that it requires MC simulation
        # For now, use a simple approximation
        self.risk_metrics["cvar_95"] = var_95 * 1.2  # Simple approximation
        self.risk_metrics["cvar_99"] = var_99 * 1.15  # Simple approximation

    def _run_stress_tests(self) -> None:
        """
        Run stress tests on the portfolio.
        """
        logger.info("Running stress tests")

        # Get stress test scenarios from config
        scenarios = self.risk_config.get("stress_test_scenarios", [])

        if not scenarios:
            logger.warning("No stress test scenarios defined")
            return

        # Run each stress test scenario
        for scenario in scenarios:
            scenario_name = scenario.get("name", "unnamed_scenario")
            logger.info(f"Running stress test scenario: {scenario_name}")

            # Apply stress test parameters
            property_value_shock = scenario.get("property_value_shock", -0.2)
            interest_rate_shock = scenario.get("interest_rate_shock", 0.02)
            default_rate_shock = scenario.get("default_rate_shock", 2.0)
            liquidity_shock = scenario.get("liquidity_shock", 0.5)

            # Calculate stressed metrics
            stressed_metrics = self._calculate_stressed_metrics(
                property_value_shock=property_value_shock,
                interest_rate_shock=interest_rate_shock,
                default_rate_shock=default_rate_shock,
                liquidity_shock=liquidity_shock
            )

            # Store stress test results
            self.stress_test_results[scenario_name] = stressed_metrics

    def _run_scenario_analysis(self) -> None:
        """
        Run scenario analysis on the portfolio.
        """
        logger.info("Running scenario analysis")

        # Get sensitivity parameters from config
        enable_sensitivity = self.risk_config.get("enable_sensitivity_analysis", True)
        sensitivity_parameters = self.risk_config.get("sensitivity_parameters", [])

        if not enable_sensitivity or not sensitivity_parameters:
            logger.warning("Sensitivity analysis disabled or no parameters defined")
            return

        # Run sensitivity analysis for each parameter
        for parameter in sensitivity_parameters:
            logger.info(f"Running sensitivity analysis for parameter: {parameter}")

            # Define parameter range
            parameter_range = self._get_parameter_range(parameter)

            # Calculate metrics for each parameter value
            sensitivity_results = []
            for param_value in parameter_range:
                metrics = self._calculate_metrics_with_parameter(parameter, param_value)
                sensitivity_results.append({
                    "parameter_value": param_value,
                    "irr": metrics.get("irr"),
                    "equity_multiple": metrics.get("equity_multiple"),
                    "roi": metrics.get("roi")
                })

            # Store sensitivity analysis results
            self.scenario_analysis_results[parameter] = sensitivity_results

    def _generate_visualization_data(self) -> None:
        """
        Generate visualization data for risk metrics.
        """
        logger.info("Generating visualization data")

        # Generate risk-return scatter plot
        self.visualization_data["risk_return_scatter"] = self._generate_risk_return_scatter()

        # Generate VaR histogram
        self.visualization_data["var_histogram"] = self._generate_var_histogram()

        # Generate drawdown chart
        self.visualization_data["drawdown_chart"] = self._generate_drawdown_chart()

        # Generate stress test comparison chart
        self.visualization_data["stress_test_comparison"] = self._generate_stress_test_comparison()

        # Generate sensitivity charts
        self.visualization_data["sensitivity_charts"] = self._generate_sensitivity_charts()

        # Generate concentration chart
        self.visualization_data["concentration_chart"] = self._generate_concentration_chart()

    def _format_return_metrics(self) -> Dict[str, Any]:
        """
        Format return metrics for output.

        Returns:
            Dictionary of return metrics
        """
        return {
            "irr": self.risk_metrics.get("irr"),
            "equity_multiple": self.risk_metrics.get("equity_multiple"),
            "moic": self.risk_metrics.get("moic"),
            "tvpi": self.risk_metrics.get("tvpi"),
            "dpi": self.risk_metrics.get("dpi"),
            "rvpi": self.risk_metrics.get("rvpi"),
            "roi": self.risk_metrics.get("roi"),
            "payback_period": self.risk_metrics.get("payback_period"),
            "cash_yield": self.risk_metrics.get("cash_yield"),
            "annualized_return": self.risk_metrics.get("annualized_return")
        }

    def _format_risk_metrics(self) -> Dict[str, Any]:
        """
        Format risk metrics for output.

        Returns:
            Dictionary of risk metrics
        """
        return {
            "var_95": self.risk_metrics.get("var_95"),
            "var_99": self.risk_metrics.get("var_99"),
            "cvar_95": self.risk_metrics.get("cvar_95"),
            "cvar_99": self.risk_metrics.get("cvar_99"),
            "max_drawdown": self.risk_metrics.get("max_drawdown"),
            "volatility": self.risk_metrics.get("volatility"),
            "downside_deviation": self.risk_metrics.get("downside_deviation"),
            "tail_risk": self.risk_metrics.get("tail_risk"),
            "tail_probability": self.risk_metrics.get("tail_probability"),
            "tail_severity": self.risk_metrics.get("tail_severity")
        }

    def _format_risk_adjusted_return_metrics(self) -> Dict[str, Any]:
        """
        Format risk-adjusted return metrics for output.

        Returns:
            Dictionary of risk-adjusted return metrics
        """
        return {
            "sharpe_ratio": self.risk_metrics.get("sharpe_ratio"),
            "sortino_ratio": self.risk_metrics.get("sortino_ratio"),
            "calmar_ratio": self.risk_metrics.get("calmar_ratio"),
            "information_ratio": self.risk_metrics.get("information_ratio"),
            "treynor_ratio": self.risk_metrics.get("treynor_ratio"),
            "omega_ratio": self.risk_metrics.get("omega_ratio"),
            "kappa_ratio": self.risk_metrics.get("kappa_ratio"),
            "gain_loss_ratio": self.risk_metrics.get("gain_loss_ratio")
        }

    def _format_market_metrics(self) -> Dict[str, Any]:
        """
        Format market metrics for output.

        Returns:
            Dictionary of market metrics
        """
        return {
            "beta": self.risk_metrics.get("beta"),
            "alpha": self.risk_metrics.get("alpha"),
            "tracking_error": self.risk_metrics.get("tracking_error"),
            "r_squared": self.risk_metrics.get("r_squared"),
            "upside_capture": self.risk_metrics.get("upside_capture"),
            "downside_capture": self.risk_metrics.get("downside_capture"),
            "upside_potential": self.risk_metrics.get("upside_potential"),
            "downside_risk": self.risk_metrics.get("downside_risk")
        }

    def _format_concentration_metrics(self) -> Dict[str, Any]:
        """
        Format concentration metrics for output.

        Returns:
            Dictionary of concentration metrics
        """
        return {
            "herfindahl_index": self.risk_metrics.get("zone_hhi"),
            "zone_concentration": {
                "green": self._get_zone_concentration("green"),
                "orange": self._get_zone_concentration("orange"),
                "red": self._get_zone_concentration("red"),
                "hhi": self.risk_metrics.get("zone_hhi")
            },
            "suburb_concentration": {
                "top_5_pct": self.risk_metrics.get("top_5_concentration"),
                "top_10_pct": self.risk_metrics.get("top_10_concentration"),
                "hhi": self.risk_metrics.get("suburb_hhi")
            }
        }

    def _extract_returns(self) -> List[float]:
        """
        Extract returns from cashflows.

        Returns:
            List of returns
        """
        returns = []

        # Try to get returns from fund-level cashflows
        if hasattr(self.context, "cashflows") and self.context.cashflows:
            fund_level_cashflows = self.context.cashflows.get("fund_level_cashflows", [])

            if fund_level_cashflows:
                # Calculate period returns
                for i in range(1, len(fund_level_cashflows)):
                    prev_cf = fund_level_cashflows[i-1]
                    curr_cf = fund_level_cashflows[i]

                    prev_value = prev_cf.get("cumulative_cashflow", 0)
                    curr_value = curr_cf.get("cumulative_cashflow", 0)

                    if prev_value != 0:
                        period_return = (curr_value - prev_value) / abs(prev_value)
                        returns.append(period_return)

        # If no returns from cashflows, try to get returns from price paths
        if not returns and hasattr(self.context, "price_paths") and self.context.price_paths:
            price_paths = self.context.price_paths.get("paths", {})

            if price_paths:
                # Use the first price path as a proxy
                first_path = next(iter(price_paths.values()), [])

                if first_path:
                    # Calculate period returns
                    for i in range(1, len(first_path)):
                        prev_price = first_path[i-1].get("price", 0)
                        curr_price = first_path[i].get("price", 0)

                        if prev_price != 0:
                            period_return = (curr_price - prev_price) / prev_price
                            returns.append(period_return)

        return returns

    def _extract_cumulative_returns(self) -> List[float]:
        """
        Extract cumulative returns.

        Returns:
            List of cumulative returns
        """
        cumulative_returns = []

        # Try to get cumulative returns from fund-level cashflows
        if hasattr(self.context, "cashflows") and self.context.cashflows:
            fund_level_cashflows = self.context.cashflows.get("fund_level_cashflows", [])

            if fund_level_cashflows:
                # Get initial investment
                initial_investment = abs(fund_level_cashflows[0].get("capital_calls", 0)) if fund_level_cashflows else 0

                if initial_investment > 0:
                    # Calculate cumulative returns
                    for cf in fund_level_cashflows:
                        cumulative_value = cf.get("cumulative_cashflow", 0)
                        cumulative_return = (cumulative_value + initial_investment) / initial_investment
                        cumulative_returns.append(cumulative_return)

        # If no cumulative returns from cashflows, try to get from price paths
        if not cumulative_returns and hasattr(self.context, "price_paths") and self.context.price_paths:
            price_paths = self.context.price_paths.get("paths", {})

            if price_paths:
                # Use the first price path as a proxy
                first_path = next(iter(price_paths.values()), [])

                if first_path:
                    # Get initial price
                    initial_price = first_path[0].get("price", 0) if first_path else 0

                    if initial_price > 0:
                        # Calculate cumulative returns
                        for point in first_path:
                            price = point.get("price", 0)
                            cumulative_return = price / initial_price
                            cumulative_returns.append(cumulative_return)

        return cumulative_returns

    def _get_zone_volatilities(self) -> Dict[str, float]:
        """
        Get volatility for each zone.

        Returns:
            Dictionary of zone volatilities
        """
        zone_volatilities = {}

        # Try to get zone volatilities from price paths with safe access
        if hasattr(self.context, "price_paths") and self.context.price_paths:
            # Handle both dict and list cases for price_paths
            if isinstance(self.context.price_paths, dict):
                price_path_stats = self.context.price_paths.get("stats", {})
                zone_stats = price_path_stats.get("zone_stats", {}) if isinstance(price_path_stats, dict) else {}
            else:
                zone_stats = {}

            for zone, stats in zone_stats.items():
                zone_volatilities[zone] = stats.get("volatility", 0.0)

        # If no zone volatilities from price paths, try to get from TLS data
        if not zone_volatilities and self.tls_manager:
            # Get zone distribution to get available zones
            zone_distribution = self.tls_manager.get_zone_distribution()
            zones = list(zone_distribution.keys())  # ["green", "orange", "red"]

            for zone in zones:
                # Get suburbs in this zone and calculate average volatility
                suburbs_in_zone = self.tls_manager.get_suburbs_by_zone(zone)
                zone_volatility = 0.0

                if suburbs_in_zone:
                    # Calculate average volatility for suburbs in this zone
                    total_volatility = 0.0
                    for suburb in suburbs_in_zone:
                        suburb_data = suburb.to_dict()
                        total_volatility += suburb_data.get("vol_appreciation", 0.15)  # Default volatility
                    zone_volatility = total_volatility / len(suburbs_in_zone)

                zone_volatilities[zone] = zone_volatility

        return zone_volatilities

    def _get_unit_volatilities(self) -> Dict[str, float]:
        """
        Get volatility for each unit (property).

        Returns:
            Dictionary of unit volatilities
        """
        unit_volatilities = {}

        # Try to get unit volatilities from portfolio with safe access
        if hasattr(self.context, "portfolio") and self.context.portfolio:
            portfolio = self.context.portfolio

            # Handle both dict and list cases for portfolio
            if isinstance(portfolio, dict):
                loans = portfolio.get("loans", [])
            elif isinstance(portfolio, list):
                loans = portfolio  # Portfolio is already a list of loans
            else:
                loans = []

            for loan in loans:
                loan_id = loan.get("loan_id")
                suburb = loan.get("suburb")

                # Try to get volatility from TLS data
                if self.tls_manager and suburb:
                    suburb_data = self.tls_manager.get_suburb_data(suburb)
                    unit_volatilities[loan_id] = suburb_data.get("volatility", 0.0)
                else:
                    # Use portfolio volatility as fallback
                    unit_volatilities[loan_id] = self.risk_metrics.get("volatility", 0.0)

        return unit_volatilities

    def _calculate_portfolio_beta_macro(self) -> float:
        """
        Calculate portfolio beta relative to the macro market.

        Returns:
            Portfolio beta (macro)
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return 1.0  # Default to market beta

        # Get loans
        loans = portfolio.get("loans", [])

        if not loans:
            return 1.0

        # Calculate weighted average beta
        total_value = 0.0
        weighted_beta = 0.0

        for loan in loans:
            suburb = loan.get("suburb")
            value = loan.get("loan_amount", 0.0)

            # Get suburb beta from TLS data
            suburb_beta = 1.0  # Default to market beta

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_beta = suburb_data.get("beta", 1.0)

            weighted_beta += value * suburb_beta
            total_value += value

        if total_value == 0:
            return 1.0

        return weighted_beta / total_value

    def _calculate_portfolio_beta_zone(self) -> Dict[str, float]:
        """
        Calculate portfolio beta relative to each zone.

        Returns:
            Dictionary of zone betas
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {"green": 1.0, "orange": 1.0, "red": 1.0}  # Default to zone beta

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {"green": 1.0, "orange": 1.0, "red": 1.0}

        # Calculate weighted average beta for each zone
        zone_values = {"green": 0.0, "orange": 0.0, "red": 0.0}
        zone_weighted_betas = {"green": 0.0, "orange": 0.0, "red": 0.0}

        for loan in loans:
            suburb = loan.get("suburb")
            value = loan.get("loan_amount", 0.0)

            # Get suburb zone and beta from TLS data
            suburb_zone = "green"  # Default to green zone
            suburb_beta = 1.0  # Default to zone beta

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")
                suburb_beta = suburb_data.get("zone_beta", 1.0)

            zone_weighted_betas[suburb_zone] += value * suburb_beta
            zone_values[suburb_zone] += value

        # Calculate zone betas
        zone_betas = {}

        for zone in zone_values:
            if zone_values[zone] > 0:
                zone_betas[zone] = zone_weighted_betas[zone] / zone_values[zone]
            else:
                zone_betas[zone] = 1.0

        return zone_betas

    def _calculate_alpha_idiosyncratic_share(self) -> float:
        """
        Calculate alpha idiosyncratic share.

        Returns:
            Alpha idiosyncratic share
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return 0.0

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return 0.0

        # Calculate weighted average idiosyncratic share
        total_value = 0.0
        weighted_idiosyncratic = 0.0

        for loan in loans:
            suburb = loan.get("suburb")
            value = loan.get("loan_amount", 0.0)

            # Get suburb idiosyncratic share from TLS data
            idiosyncratic_share = 0.3  # Default idiosyncratic share

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                idiosyncratic_share = suburb_data.get("idiosyncratic_share", 0.3)

            weighted_idiosyncratic += value * idiosyncratic_share
            total_value += value

        if total_value == 0:
            return 0.0

        return weighted_idiosyncratic / total_value

    def _calculate_current_ltv(self) -> Dict[str, Any]:
        """
        Calculate current Loan-to-Value (LTV) ratio.

        Returns:
            Dictionary with current LTV metrics
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "portfolio_ltv": None,
                "loan_ltvs": {},
                "zone_ltvs": {},
                "suburb_ltvs": {}
            }

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {
                "portfolio_ltv": None,
                "loan_ltvs": {},
                "zone_ltvs": {},
                "suburb_ltvs": {}
            }

        # Calculate LTV for each loan
        loan_ltvs = {}
        zone_values = {"green": 0.0, "orange": 0.0, "red": 0.0}
        zone_loans = {"green": 0.0, "orange": 0.0, "red": 0.0}
        suburb_values = {}
        suburb_loans = {}
        total_value = 0.0
        total_loan = 0.0

        for loan in loans:
            loan_id = loan.get("loan_id")
            suburb = loan.get("suburb")
            loan_amount = loan.get("loan_amount", 0.0)
            property_value = loan.get("property_value", 0.0)

            # Calculate loan LTV
            if property_value > 0:
                ltv = loan_amount / property_value
            else:
                ltv = 0.0

            loan_ltvs[loan_id] = ltv

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            # Update zone totals
            zone_values[suburb_zone] += property_value
            zone_loans[suburb_zone] += loan_amount

            # Update suburb totals
            if suburb not in suburb_values:
                suburb_values[suburb] = 0.0
                suburb_loans[suburb] = 0.0

            suburb_values[suburb] += property_value
            suburb_loans[suburb] += loan_amount

            # Update portfolio totals
            total_value += property_value
            total_loan += loan_amount

        # Calculate zone LTVs
        zone_ltvs = {}

        for zone in zone_values:
            if zone_values[zone] > 0:
                zone_ltvs[zone] = zone_loans[zone] / zone_values[zone]
            else:
                zone_ltvs[zone] = 0.0

        # Calculate suburb LTVs
        suburb_ltvs = {}

        for suburb in suburb_values:
            if suburb_values[suburb] > 0:
                suburb_ltvs[suburb] = suburb_loans[suburb] / suburb_values[suburb]
            else:
                suburb_ltvs[suburb] = 0.0

        # Calculate portfolio LTV
        portfolio_ltv = total_loan / total_value if total_value > 0 else 0.0

        return {
            "portfolio_ltv": portfolio_ltv,
            "loan_ltvs": loan_ltvs,
            "zone_ltvs": zone_ltvs,
            "suburb_ltvs": suburb_ltvs
        }

    def _calculate_stress_ltv(self) -> Dict[str, Any]:
        """
        Calculate stress Loan-to-Value (LTV) ratio with -20% price shock.

        Returns:
            Dictionary with stress LTV metrics
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "portfolio_stress_ltv": None,
                "loan_stress_ltvs": {},
                "zone_stress_ltvs": {},
                "suburb_stress_ltvs": {}
            }

        # Get loans
        loans = portfolio.get("loans", [])

        if not loans:
            return {
                "portfolio_stress_ltv": None,
                "loan_stress_ltvs": {},
                "zone_stress_ltvs": {},
                "suburb_stress_ltvs": {}
            }

        # Apply -20% price shock
        price_shock = -0.2

        # Calculate stress LTV for each loan
        loan_stress_ltvs = {}
        zone_values = {"green": 0.0, "orange": 0.0, "red": 0.0}
        zone_loans = {"green": 0.0, "orange": 0.0, "red": 0.0}
        suburb_values = {}
        suburb_loans = {}
        total_value = 0.0
        total_loan = 0.0

        for loan in loans:
            loan_id = loan.get("loan_id")
            suburb = loan.get("suburb")
            loan_amount = loan.get("loan_amount", 0.0)
            property_value = loan.get("property_value", 0.0)

            # Apply price shock
            stressed_value = property_value * (1 + price_shock)

            # Calculate loan stress LTV
            if stressed_value > 0:
                stress_ltv = loan_amount / stressed_value
            else:
                stress_ltv = 0.0

            loan_stress_ltvs[loan_id] = stress_ltv

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            # Update zone totals
            zone_values[suburb_zone] += stressed_value
            zone_loans[suburb_zone] += loan_amount

            # Update suburb totals
            if suburb not in suburb_values:
                suburb_values[suburb] = 0.0
                suburb_loans[suburb] = 0.0

            suburb_values[suburb] += stressed_value
            suburb_loans[suburb] += loan_amount

            # Update portfolio totals
            total_value += stressed_value
            total_loan += loan_amount

        # Calculate zone stress LTVs
        zone_stress_ltvs = {}

        for zone in zone_values:
            if zone_values[zone] > 0:
                zone_stress_ltvs[zone] = zone_loans[zone] / zone_values[zone]
            else:
                zone_stress_ltvs[zone] = 0.0

        # Calculate suburb stress LTVs
        suburb_stress_ltvs = {}

        for suburb in suburb_values:
            if suburb_values[suburb] > 0:
                suburb_stress_ltvs[suburb] = suburb_loans[suburb] / suburb_values[suburb]
            else:
                suburb_stress_ltvs[suburb] = 0.0

        # Calculate portfolio stress LTV
        portfolio_stress_ltv = total_loan / total_value if total_value > 0 else 0.0

        return {
            "portfolio_stress_ltv": portfolio_stress_ltv,
            "loan_stress_ltvs": loan_stress_ltvs,
            "zone_stress_ltvs": zone_stress_ltvs,
            "suburb_stress_ltvs": suburb_stress_ltvs
        }

    def _get_default_probabilities(self) -> Dict[str, Any]:
        """
        Get default probabilities by unit and zone.

        Returns:
            Dictionary with default probabilities
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "loan_default_probs": {},
                "zone_default_probs": {},
                "suburb_default_probs": {}
            }

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {
                "loan_default_probs": {},
                "zone_default_probs": {},
                "suburb_default_probs": {}
            }

        # Get default probabilities for each loan
        loan_default_probs = {}
        zone_default_probs = {"green": 0.0, "orange": 0.0, "red": 0.0}
        zone_loan_counts = {"green": 0, "orange": 0, "red": 0}
        suburb_default_probs = {}
        suburb_loan_counts = {}

        for loan in loans:
            loan_id = loan.get("loan_id")
            suburb = loan.get("suburb")

            # Get default probability from loan or TLS data
            default_prob = loan.get("default_probability", 0.0)

            if default_prob == 0.0 and self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                default_prob = suburb_data.get("default_probability", 0.02)

            loan_default_probs[loan_id] = default_prob

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            # Update zone totals
            zone_default_probs[suburb_zone] += default_prob
            zone_loan_counts[suburb_zone] += 1

            # Update suburb totals
            if suburb not in suburb_default_probs:
                suburb_default_probs[suburb] = 0.0
                suburb_loan_counts[suburb] = 0

            suburb_default_probs[suburb] += default_prob
            suburb_loan_counts[suburb] += 1

        # Calculate average default probability by zone
        for zone in zone_default_probs:
            if zone_loan_counts[zone] > 0:
                zone_default_probs[zone] /= zone_loan_counts[zone]

        # Calculate average default probability by suburb
        for suburb in suburb_default_probs:
            if suburb_loan_counts[suburb] > 0:
                suburb_default_probs[suburb] /= suburb_loan_counts[suburb]

        return {
            "loan_default_probs": loan_default_probs,
            "zone_default_probs": zone_default_probs,
            "suburb_default_probs": suburb_default_probs
        }

    def _calculate_portfolio_default_rate(self) -> float:
        """
        Calculate portfolio default rate (exposure-weighted PD).

        Returns:
            Portfolio default rate
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return 0.0

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return 0.0

        # Calculate exposure-weighted default rate
        total_exposure = 0.0
        weighted_default_rate = 0.0

        for loan in loans:
            loan_amount = loan.get("loan_amount", 0.0)
            suburb = loan.get("suburb")

            # Get default probability from loan or TLS data
            default_prob = loan.get("default_probability", 0.0)

            if default_prob == 0.0 and self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                default_prob = suburb_data.get("default_probability", 0.02)

            weighted_default_rate += loan_amount * default_prob
            total_exposure += loan_amount

        if total_exposure == 0:
            return 0.0

        return weighted_default_rate / total_exposure

    def _get_liquidity_score(self) -> Dict[str, Any]:
        """
        Get liquidity score from TLS data.

        Returns:
            Dictionary with liquidity scores
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "portfolio_liquidity_score": None,
                "loan_liquidity_scores": {},
                "zone_liquidity_scores": {},
                "suburb_liquidity_scores": {}
            }

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {
                "portfolio_liquidity_score": None,
                "loan_liquidity_scores": {},
                "zone_liquidity_scores": {},
                "suburb_liquidity_scores": {}
            }

        # Get liquidity score for each loan
        loan_liquidity_scores = {}
        zone_liquidity_scores = {"green": 0.0, "orange": 0.0, "red": 0.0}
        zone_loan_counts = {"green": 0, "orange": 0, "red": 0}
        suburb_liquidity_scores = {}
        suburb_loan_counts = {}
        total_liquidity_score = 0.0
        total_loans = 0

        for loan in loans:
            loan_id = loan.get("loan_id")
            suburb = loan.get("suburb")

            # Get liquidity score from TLS data
            liquidity_score = 0.5  # Default liquidity score

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                liquidity_score = suburb_data.get("liquidity_score", 0.5)

            loan_liquidity_scores[loan_id] = liquidity_score

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            # Update zone totals
            zone_liquidity_scores[suburb_zone] += liquidity_score
            zone_loan_counts[suburb_zone] += 1

            # Update suburb totals
            if suburb not in suburb_liquidity_scores:
                suburb_liquidity_scores[suburb] = 0.0
                suburb_loan_counts[suburb] = 0

            suburb_liquidity_scores[suburb] += liquidity_score
            suburb_loan_counts[suburb] += 1

            # Update portfolio totals
            total_liquidity_score += liquidity_score
            total_loans += 1

        # Calculate average liquidity score by zone
        for zone in zone_liquidity_scores:
            if zone_loan_counts[zone] > 0:
                zone_liquidity_scores[zone] /= zone_loan_counts[zone]

        # Calculate average liquidity score by suburb
        for suburb in suburb_liquidity_scores:
            if suburb_loan_counts[suburb] > 0:
                suburb_liquidity_scores[suburb] /= suburb_loan_counts[suburb]

        # Calculate portfolio liquidity score
        portfolio_liquidity_score = total_liquidity_score / total_loans if total_loans > 0 else 0.0

        return {
            "portfolio_liquidity_score": portfolio_liquidity_score,
            "loan_liquidity_scores": loan_liquidity_scores,
            "zone_liquidity_scores": zone_liquidity_scores,
            "suburb_liquidity_scores": suburb_liquidity_scores
        }

    def _calculate_expected_exit_lag(self) -> Dict[str, Any]:
        """
        Calculate expected exit lag.

        Returns:
            Dictionary with expected exit lag metrics
        """
        # Get exit simulator config with safe attribute access
        exit_config_obj = getattr(self.config, "exit_simulator", {})
        exit_config = exit_config_obj.dict() if hasattr(exit_config_obj, 'dict') else (exit_config_obj if isinstance(exit_config_obj, dict) else {})

        # Get gamma distribution parameters
        alpha = exit_config.get("exit_lag_alpha", 2.0)
        beta = exit_config.get("exit_lag_beta", 3.0)

        # Calculate expected exit lag (mean of gamma distribution)
        expected_lag = alpha * beta

        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "portfolio_expected_lag": expected_lag,
                "zone_expected_lags": {},
                "suburb_expected_lags": {}
            }

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {
                "portfolio_expected_lag": expected_lag,
                "zone_expected_lags": {},
                "suburb_expected_lags": {}
            }

        # Calculate expected exit lag by zone and suburb
        zone_expected_lags = {"green": 0.0, "orange": 0.0, "red": 0.0}
        suburb_expected_lags = {}

        # Get TLS data for zones and suburbs
        if self.tls_manager:
            # Get zone distribution to get available zones
            zone_distribution = self.tls_manager.get_zone_distribution()
            zones = list(zone_distribution.keys())  # ["green", "orange", "red"]

            for zone in zones:
                # Get suburbs in this zone and calculate average liquidity
                suburbs_in_zone = self.tls_manager.get_suburbs_by_zone(zone)
                zone_liquidity = 0.5  # Default liquidity

                if suburbs_in_zone:
                    # Calculate average liquidity for suburbs in this zone
                    total_liquidity = 0.0
                    for suburb in suburbs_in_zone:
                        total_liquidity += suburb.liquidity_score
                    zone_liquidity = total_liquidity / len(suburbs_in_zone)

                # Adjust expected lag based on liquidity (higher liquidity = lower lag)
                zone_expected_lags[zone] = expected_lag * (1.0 - zone_liquidity * 0.5)

            # Get suburb data
            for loan in loans:
                suburb = loan.get("suburb")

                if suburb and suburb not in suburb_expected_lags:
                    suburb_data = self.tls_manager.get_suburb_data(suburb)
                    suburb_liquidity = suburb_data.get("liquidity_score", 0.5)

                    # Adjust expected lag based on liquidity (higher liquidity = lower lag)
                    suburb_expected_lags[suburb] = expected_lag * (1.0 - suburb_liquidity * 0.5)

        return {
            "portfolio_expected_lag": expected_lag,
            "zone_expected_lags": zone_expected_lags,
            "suburb_expected_lags": suburb_expected_lags
        }

    def _calculate_wal(self) -> float:
        """
        Calculate Weighted Average Life (WAL).

        Returns:
            Weighted Average Life
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return 0.0

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return 0.0

        # Calculate WAL
        total_loan_amount = 0.0
        weighted_life = 0.0

        for loan in loans:
            loan_amount = loan.get("loan_amount", 0.0)
            term_months = loan.get("term_months", 120)  # Default to 10 years

            # Convert to years
            term_years = term_months / 12.0

            weighted_life += loan_amount * term_years
            total_loan_amount += loan_amount

        if total_loan_amount == 0:
            return 0.0

        return weighted_life / total_loan_amount

    def _calculate_nav_utilisation(self) -> float:
        """
        Calculate NAV utilisation.

        Returns:
            NAV utilisation
        """
        # Get leverage data
        leverage_data = self.context.leverage_data if hasattr(self.context, "leverage_data") else {}

        # Get NAV utilisation
        nav_utilisation = leverage_data.get("nav_utilisation", 0.0)

        if nav_utilisation == 0.0:
            # Calculate from leverage config with safe attribute access
            leverage_config_obj = getattr(self.config, "leverage", {})
            leverage_config = leverage_config_obj.dict() if hasattr(leverage_config_obj, 'dict') else (leverage_config_obj if isinstance(leverage_config_obj, dict) else {})
            target_ltv = leverage_config.get("target_ltv", 0.0)
            nav_utilisation = target_ltv

        return nav_utilisation

    def _calculate_interest_coverage(self) -> float:
        """
        Calculate interest coverage ratio.

        Returns:
            Interest coverage ratio
        """
        # Get leverage data
        leverage_data = self.context.leverage_data if hasattr(self.context, "leverage_data") else {}

        # Get interest coverage
        interest_coverage = leverage_data.get("interest_coverage", 0.0)

        if interest_coverage == 0.0:
            # Calculate from cashflows
            if hasattr(self.context, "cashflows") and self.context.cashflows:
                fund_level_cashflows = self.context.cashflows.get("fund_level_cashflows", [])

                if fund_level_cashflows:
                    total_interest = 0.0
                    total_income = 0.0

                    for cf in fund_level_cashflows:
                        interest = cf.get("interest_expense", 0.0)
                        income = cf.get("income", 0.0)

                        total_interest += interest
                        total_income += income

                    if total_interest > 0:
                        interest_coverage = total_income / total_interest

        return interest_coverage

    def _calculate_downside_deviation(self, returns: List[float]) -> float:
        """
        Calculate downside deviation.

        Args:
            returns: List of returns

        Returns:
            Downside deviation
        """
        if not returns:
            return 0.0

        # Calculate downside deviation (standard deviation of returns below minimum acceptable return)
        threshold = self.min_acceptable_return
        downside_returns = [min(0, r - threshold) for r in returns]

        if all(r == 0 for r in downside_returns) or len(downside_returns) < 2:
            return 0.0

        return np.sqrt(np.mean(np.square(downside_returns)))

    def _calculate_sortino_ratio(self, returns: List[float]) -> Optional[float]:
        """
        Calculate Sortino ratio.

        Args:
            returns: List of returns

        Returns:
            Sortino ratio, or None if downside deviation is zero
        """
        if not returns:
            return None

        # Calculate average return
        avg_return = np.mean(returns)

        # Calculate downside deviation
        downside_dev = self._calculate_downside_deviation(returns)

        if downside_dev == 0:
            return None

        return (avg_return - self.risk_free_rate) / downside_dev

    def _calculate_market_metrics(self, returns: List[float]) -> None:
        """
        Calculate market-related metrics.

        Args:
            returns: List of returns
        """
        if not returns:
            return

        # Generate benchmark returns (simple approach for now)
        benchmark_returns = [self.benchmark_return / 12] * len(returns)  # Monthly benchmark returns

        # Calculate beta
        self.risk_metrics["beta"] = self._calculate_beta(returns, benchmark_returns)

        # Calculate alpha
        self.risk_metrics["alpha"] = self._calculate_alpha(returns, benchmark_returns)

        # Calculate tracking error
        self.risk_metrics["tracking_error"] = self._calculate_tracking_error(returns, benchmark_returns)

        # Calculate R-squared
        self.risk_metrics["r_squared"] = self._calculate_r_squared(returns, benchmark_returns)

        # Calculate information ratio
        self.risk_metrics["information_ratio"] = self._calculate_information_ratio(returns, benchmark_returns)

        # Calculate upside/downside capture
        self.risk_metrics["upside_capture"] = self._calculate_upside_capture(returns, benchmark_returns)
        self.risk_metrics["downside_capture"] = self._calculate_downside_capture(returns, benchmark_returns)

        # Calculate upside potential and downside risk
        self.risk_metrics["upside_potential"] = self._calculate_upside_potential(returns)
        self.risk_metrics["downside_risk"] = self._calculate_downside_risk(returns)

    def _calculate_beta(self, returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Calculate beta.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            Beta
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return 0.0

        # Calculate covariance and variance
        covariance = np.cov(returns, benchmark_returns)[0, 1]
        variance = np.var(benchmark_returns, ddof=1)

        if variance == 0:
            return 0.0

        return covariance / variance

    def _calculate_alpha(self, returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Calculate alpha.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            Alpha
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return 0.0

        # Calculate beta
        beta = self._calculate_beta(returns, benchmark_returns)

        # Calculate average returns
        avg_return = np.mean(returns)
        avg_benchmark_return = np.mean(benchmark_returns)

        # Calculate alpha
        return avg_return - self.risk_free_rate - beta * (avg_benchmark_return - self.risk_free_rate)

    def _calculate_tracking_error(self, returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Calculate tracking error.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            Tracking error
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return 0.0

        # Calculate tracking difference
        tracking_diff = [r - b for r, b in zip(returns, benchmark_returns)]

        if len(tracking_diff) < 2:
            return 0.0

        # Calculate tracking error (standard deviation of tracking difference)
        return np.std(tracking_diff, ddof=1)

    def _calculate_r_squared(self, returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Calculate R-squared.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            R-squared
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return 0.0

        # Calculate correlation
        correlation = np.corrcoef(returns, benchmark_returns)[0, 1]

        # Calculate R-squared
        return correlation ** 2

    def _calculate_information_ratio(self, returns: List[float], benchmark_returns: List[float]) -> Optional[float]:
        """
        Calculate information ratio.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            Information ratio, or None if tracking error is zero
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return None

        # Calculate average returns
        avg_return = np.mean(returns)
        avg_benchmark_return = np.mean(benchmark_returns)

        # Calculate tracking error
        tracking_error = self._calculate_tracking_error(returns, benchmark_returns)

        if tracking_error == 0:
            return None

        # Calculate information ratio
        return (avg_return - avg_benchmark_return) / tracking_error

    def _calculate_upside_capture(self, returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Calculate upside capture ratio.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            Upside capture ratio
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return 0.0

        # Filter for positive benchmark returns
        up_returns = [r for r, b in zip(returns, benchmark_returns) if b > 0]
        up_benchmark_returns = [b for b in benchmark_returns if b > 0]

        if not up_returns or not up_benchmark_returns:
            return 0.0

        # Calculate average returns
        avg_up_return = np.mean(up_returns)
        avg_up_benchmark_return = np.mean(up_benchmark_returns)

        if avg_up_benchmark_return == 0:
            return 0.0

        # Calculate upside capture ratio
        return avg_up_return / avg_up_benchmark_return

    def _calculate_downside_capture(self, returns: List[float], benchmark_returns: List[float]) -> float:
        """
        Calculate downside capture ratio.

        Args:
            returns: List of returns
            benchmark_returns: List of benchmark returns

        Returns:
            Downside capture ratio
        """
        if not returns or not benchmark_returns or len(returns) != len(benchmark_returns):
            return 0.0

        # Filter for negative benchmark returns
        down_returns = [r for r, b in zip(returns, benchmark_returns) if b < 0]
        down_benchmark_returns = [b for b in benchmark_returns if b < 0]

        if not down_returns or not down_benchmark_returns:
            return 0.0

        # Calculate average returns
        avg_down_return = np.mean(down_returns)
        avg_down_benchmark_return = np.mean(down_benchmark_returns)

        if avg_down_benchmark_return == 0:
            return 0.0

        # Calculate downside capture ratio
        return avg_down_return / avg_down_benchmark_return

    def _calculate_upside_potential(self, returns: List[float]) -> float:
        """
        Calculate upside potential.

        Args:
            returns: List of returns

        Returns:
            Upside potential
        """
        if not returns:
            return 0.0

        # Calculate upside potential (average of returns above minimum acceptable return)
        threshold = self.min_acceptable_return
        upside_returns = [max(0, r - threshold) for r in returns]

        if all(r == 0 for r in upside_returns):
            return 0.0

        return np.mean(upside_returns)

    def _calculate_downside_risk(self, returns: List[float]) -> float:
        """
        Calculate downside risk.

        Args:
            returns: List of returns

        Returns:
            Downside risk
        """
        if not returns:
            return 0.0

        # Calculate downside risk (average of returns below minimum acceptable return)
        threshold = self.min_acceptable_return
        downside_returns = [min(0, r - threshold) for r in returns]

        if all(r == 0 for r in downside_returns):
            return 0.0

        return -np.mean(downside_returns)

    def _calculate_zone_exposure(self) -> Dict[str, float]:
        """
        Calculate zone exposure percentages.

        Returns:
            Dictionary of zone exposure percentages
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {"green": 0.0, "orange": 0.0, "red": 0.0}

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {"green": 0.0, "orange": 0.0, "red": 0.0}

        # Calculate zone exposure
        zone_exposure = {"green": 0.0, "orange": 0.0, "red": 0.0}
        total_exposure = 0.0

        for loan in loans:
            suburb = loan.get("suburb")
            loan_amount = loan.get("loan_amount", 0.0)

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if self.tls_manager and suburb:
                suburb_data = self.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            zone_exposure[suburb_zone] += loan_amount
            total_exposure += loan_amount

        # Calculate percentages
        if total_exposure > 0:
            for zone in zone_exposure:
                zone_exposure[zone] /= total_exposure

        return zone_exposure

    def _calculate_suburb_exposure(self) -> Dict[str, Any]:
        """
        Calculate suburb exposure metrics.

        Returns:
            Dictionary of suburb exposure metrics
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "top_suburbs": [],
                "max_suburb_exposure": 0.0,
                "suburb_exposure_cap": 0.0
            }

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {
                "top_suburbs": [],
                "max_suburb_exposure": 0.0,
                "suburb_exposure_cap": 0.0
            }

        # Calculate suburb exposure
        suburb_exposure = {}
        total_exposure = 0.0

        for loan in loans:
            suburb = loan.get("suburb")
            loan_amount = loan.get("loan_amount", 0.0)

            if suburb not in suburb_exposure:
                suburb_exposure[suburb] = 0.0

            suburb_exposure[suburb] += loan_amount
            total_exposure += loan_amount

        # Calculate percentages
        suburb_exposure_pct = {}

        if total_exposure > 0:
            for suburb in suburb_exposure:
                suburb_exposure_pct[suburb] = suburb_exposure[suburb] / total_exposure

        # Get top suburbs
        top_suburbs = sorted(
            [
                {"suburb": suburb, "exposure": exposure}
                for suburb, exposure in suburb_exposure_pct.items()
            ],
            key=lambda x: x["exposure"],
            reverse=True
        )

        # Get maximum suburb exposure
        max_suburb_exposure = top_suburbs[0]["exposure"] if top_suburbs else 0.0

        # Get suburb exposure cap from config with safe attribute access
        suburb_exposure_cap = getattr(self.config, "suburb_exposure_cap", 0.2)

        return {
            "top_suburbs": top_suburbs[:10],  # Top 10 suburbs
            "max_suburb_exposure": max_suburb_exposure,
            "suburb_exposure_cap": suburb_exposure_cap
        }

    def _calculate_single_loan_exposure(self) -> Dict[str, Any]:
        """
        Calculate single loan exposure metrics.

        Returns:
            Dictionary of single loan exposure metrics
        """
        # Get portfolio
        portfolio = self.context.portfolio if hasattr(self.context, "portfolio") else None

        if not portfolio:
            return {
                "top_loans": [],
                "max_loan_exposure": 0.0,
                "loan_exposure_cap": 0.0
            }

        # Get loans with safe access
        if isinstance(portfolio, dict):
            loans = portfolio.get("loans", [])
        elif isinstance(portfolio, list):
            loans = portfolio  # Portfolio is already a list of loans
        else:
            loans = []

        if not loans:
            return {
                "top_loans": [],
                "max_loan_exposure": 0.0,
                "loan_exposure_cap": 0.0
            }

        # Calculate loan exposure
        loan_exposure = {}
        total_exposure = 0.0

        for loan in loans:
            loan_id = loan.get("loan_id")
            loan_amount = loan.get("loan_amount", 0.0)

            loan_exposure[loan_id] = loan_amount
            total_exposure += loan_amount

        # Calculate percentages
        loan_exposure_pct = {}

        if total_exposure > 0:
            for loan_id in loan_exposure:
                loan_exposure_pct[loan_id] = loan_exposure[loan_id] / total_exposure

        # Get top loans
        top_loans = sorted(
            [
                {"loan_id": loan_id, "exposure": exposure}
                for loan_id, exposure in loan_exposure_pct.items()
            ],
            key=lambda x: x["exposure"],
            reverse=True
        )

        # Get maximum loan exposure
        max_loan_exposure = top_loans[0]["exposure"] if top_loans else 0.0

        # Get loan exposure cap from config with safe attribute access
        loan_exposure_cap = getattr(self.config, "loan_exposure_cap", 0.05)

        return {
            "top_loans": top_loans[:10],  # Top 10 loans
            "max_loan_exposure": max_loan_exposure,
            "loan_exposure_cap": loan_exposure_cap
        }

    def _get_zone_concentration(self, zone: str) -> float:
        """
        Get concentration for a specific zone.

        Args:
            zone: Zone name

        Returns:
            Zone concentration
        """
        # Try to get from capital allocation with safe access
        if hasattr(self.context, "capital_allocation") and self.context.capital_allocation:
            # Handle both dict and list cases for capital_allocation
            if isinstance(self.context.capital_allocation, dict):
                zone_actual = self.context.capital_allocation.get("zone_actual", {})
                concentration = zone_actual.get(zone, 0.0) if isinstance(zone_actual, dict) else 0.0
                if concentration > 0:
                    return concentration

        # Calculate from zone exposure
        zone_exposure = self._calculate_zone_exposure()
        return zone_exposure.get(zone, 0.0)

    def _get_net_irr(self) -> float:
        """
        Get Net-IRR point value.

        Returns:
            Net-IRR
        """
        # Get IRR from existing metrics
        irr = self.risk_metrics.get("irr")

        if irr is None and hasattr(self.context, "cashflows") and self.context.cashflows:
            fund_level_metrics = self.context.cashflows.get("metrics", {}).get("fund_level_metrics", {})
            irr = fund_level_metrics.get("irr")

        return irr

    def _calculate_sharpe_ratio(self) -> float:
        """
        Calculate Sharpe ratio.

        Returns:
            Sharpe ratio
        """
        # Get returns
        returns = self._extract_returns()

        if not returns:
            return 0.0

        # Calculate Sharpe ratio
        mean_return = np.mean(returns)
        std_return = np.std(returns, ddof=1) if len(returns) > 1 else 0.0

        if std_return == 0:
            return 0.0

        return (mean_return - self.risk_free_rate) / std_return

    def _calculate_sortino_ratio_metric(self) -> float:
        """
        Calculate Sortino ratio.

        Returns:
            Sortino ratio
        """
        # Get returns
        returns = self._extract_returns()

        if not returns:
            return 0.0

        # Calculate Sortino ratio
        mean_return = np.mean(returns)
        downside_deviation = self._calculate_downside_deviation(returns)

        if downside_deviation == 0:
            return 0.0

        return (mean_return - self.min_acceptable_return) / downside_deviation

    def _calculate_stressed_metrics(self, property_value_shock: float, interest_rate_shock: float,
                                   default_rate_shock: float, liquidity_shock: float) -> Dict[str, Any]:
        """
        Calculate metrics under stress test scenario.

        Args:
            property_value_shock: Property value shock as percentage (-1 to 1)
            interest_rate_shock: Interest rate shock in percentage points (-0.1 to 0.1)
            default_rate_shock: Default rate shock as multiplier (0-10)
            liquidity_shock: Liquidity shock as percentage of expected liquidity (0-1)

        Returns:
            Dictionary of stressed metrics
        """
        # For now, use a simplified approach to estimate stressed metrics
        # In a real implementation, this would re-run parts of the simulation with stressed parameters

        # Get base metrics
        base_irr = self.risk_metrics.get("irr", 0.0)
        base_equity_multiple = self.risk_metrics.get("equity_multiple", 1.0)
        base_roi = self.risk_metrics.get("roi", 0.0)
        base_max_drawdown = self.risk_metrics.get("max_drawdown", 0.0)
        base_var_95 = self.risk_metrics.get("var_95", 0.0)

        # Estimate impact of property value shock on IRR
        # Simplified assumption: 1% property value shock reduces IRR by 0.5%
        irr_impact = property_value_shock * 0.5

        # Estimate impact of interest rate shock on IRR
        # Simplified assumption: 1% interest rate shock reduces IRR by 0.3%
        irr_impact += interest_rate_shock * 30

        # Estimate impact of default rate shock on IRR
        # Simplified assumption: 2x default rate reduces IRR by 1%
        irr_impact += (default_rate_shock - 1) * 0.5

        # Estimate impact of liquidity shock on IRR
        # Simplified assumption: 50% liquidity shock reduces IRR by 0.5%
        irr_impact += liquidity_shock * 1.0

        # Calculate stressed metrics
        stressed_irr = max(0.0, base_irr + irr_impact)
        stressed_equity_multiple = max(1.0, base_equity_multiple * (1 + property_value_shock * 0.7))
        stressed_roi = max(0.0, base_roi + irr_impact)
        stressed_max_drawdown = min(1.0, base_max_drawdown + abs(property_value_shock) * 0.5)
        stressed_var_95 = base_var_95 * (1 + abs(property_value_shock) * 0.8)

        # Calculate percentage impact on IRR
        irr_impact_pct = (stressed_irr - base_irr) / base_irr if base_irr != 0 else 0.0

        return {
            "irr": stressed_irr,
            "equity_multiple": stressed_equity_multiple,
            "roi": stressed_roi,
            "max_drawdown": stressed_max_drawdown,
            "var_95": stressed_var_95,
            "impact_pct": irr_impact_pct
        }

    def _get_parameter_range(self, parameter: str) -> List[float]:
        """
        Get range of values for sensitivity analysis.

        Args:
            parameter: Parameter name

        Returns:
            List of parameter values
        """
        # Define parameter ranges for sensitivity analysis
        ranges = {
            "interest_rate": np.linspace(0.01, 0.1, 10),  # 1% to 10%
            "property_value_growth": np.linspace(-0.05, 0.15, 10),  # -5% to 15%
            "default_rate": np.linspace(0.01, 0.2, 10),  # 1% to 20%
            "prepayment_rate": np.linspace(0.0, 0.3, 10),  # 0% to 30%
            "ltv_ratio": np.linspace(0.5, 0.9, 10),  # 50% to 90%
            "leverage_ratio": np.linspace(0.0, 0.7, 10),  # 0% to 70%
            "management_fee_rate": np.linspace(0.01, 0.03, 10),  # 1% to 3%
            "carried_interest_rate": np.linspace(0.1, 0.3, 10),  # 10% to 30%
            "hurdle_rate": np.linspace(0.05, 0.15, 10),  # 5% to 15%
        }

        return ranges.get(parameter, np.linspace(0.0, 1.0, 10))

    def _calculate_metrics_with_parameter(self, parameter: str, param_value: float) -> Dict[str, Any]:
        """
        Calculate metrics with a specific parameter value.

        Args:
            parameter: Parameter name
            param_value: Parameter value

        Returns:
            Dictionary of metrics
        """
        # For now, use a simplified approach to estimate metrics with different parameter values
        # In a real implementation, this would re-run parts of the simulation with different parameters

        # Get base metrics
        base_irr = self.risk_metrics.get("irr", 0.0)
        base_equity_multiple = self.risk_metrics.get("equity_multiple", 1.0)
        base_roi = self.risk_metrics.get("roi", 0.0)

        # Define sensitivity factors for each parameter
        sensitivity_factors = {
            "interest_rate": -5.0,  # 1% increase in interest rate reduces IRR by 5%
            "property_value_growth": 2.0,  # 1% increase in property value growth increases IRR by 2%
            "default_rate": -10.0,  # 1% increase in default rate reduces IRR by 10%
            "prepayment_rate": -1.0,  # 1% increase in prepayment rate reduces IRR by 1%
            "ltv_ratio": 1.0,  # 1% increase in LTV ratio increases IRR by 1%
            "leverage_ratio": 1.5,  # 1% increase in leverage ratio increases IRR by 1.5%
            "management_fee_rate": -20.0,  # 1% increase in management fee rate reduces IRR by 20%
            "carried_interest_rate": -5.0,  # 1% increase in carried interest rate reduces IRR by 5%
            "hurdle_rate": -2.0,  # 1% increase in hurdle rate reduces IRR by 2%
        }

        # Get base parameter value
        base_param_value = self._get_base_parameter_value(parameter)

        # Calculate parameter change
        param_change = param_value - base_param_value

        # Get sensitivity factor
        sensitivity_factor = sensitivity_factors.get(parameter, 0.0)

        # Calculate impact on IRR
        irr_impact = param_change * sensitivity_factor

        # Calculate metrics with parameter
        irr = max(0.0, base_irr * (1 + irr_impact))
        equity_multiple = max(1.0, base_equity_multiple * (1 + irr_impact * 0.5))
        roi = max(0.0, base_roi * (1 + irr_impact * 0.8))

        return {
            "irr": irr,
            "equity_multiple": equity_multiple,
            "roi": roi
        }

    def _get_base_parameter_value(self, parameter: str) -> float:
        """
        Get base value for a parameter.

        Args:
            parameter: Parameter name

        Returns:
            Base parameter value
        """
        # Get base parameter values from config with safe attribute access
        if parameter == "interest_rate":
            return self.risk_config.get("risk_free_rate", 0.03)
        elif parameter == "property_value_growth":
            price_path_obj = getattr(self.config, "price_path", {})
            price_path_dict = price_path_obj.dict() if hasattr(price_path_obj, 'dict') else (price_path_obj if isinstance(price_path_obj, dict) else {})
            return price_path_dict.get("annual_appreciation_rate", 0.03)
        elif parameter == "default_rate":
            exit_sim_obj = getattr(self.config, "exit_simulator", {})
            exit_sim_dict = exit_sim_obj.dict() if hasattr(exit_sim_obj, 'dict') else (exit_sim_obj if isinstance(exit_sim_obj, dict) else {})
            return exit_sim_dict.get("default_probability", 0.05)
        elif parameter == "prepayment_rate":
            exit_sim_obj = getattr(self.config, "exit_simulator", {})
            exit_sim_dict = exit_sim_obj.dict() if hasattr(exit_sim_obj, 'dict') else (exit_sim_obj if isinstance(exit_sim_obj, dict) else {})
            return exit_sim_dict.get("prepayment_probability", 0.1)
        elif parameter == "ltv_ratio":
            loan_gen_obj = getattr(self.config, "loan_generator", {})
            loan_gen_dict = loan_gen_obj.dict() if hasattr(loan_gen_obj, 'dict') else (loan_gen_obj if isinstance(loan_gen_obj, dict) else {})
            return loan_gen_dict.get("ltv_mean", 0.7)
        elif parameter == "leverage_ratio":
            leverage_obj = getattr(self.config, "leverage_engine", {})
            leverage_dict = leverage_obj.dict() if hasattr(leverage_obj, 'dict') else (leverage_obj if isinstance(leverage_obj, dict) else {})
            return leverage_dict.get("target_leverage", 0.5)
        elif parameter == "management_fee_rate":
            return getattr(self.config, "management_fee_rate", 0.02)
        elif parameter == "carried_interest_rate":
            return getattr(self.config, "carried_interest_rate", 0.2)
        elif parameter == "hurdle_rate":
            return getattr(self.config, "hurdle_rate", 0.08)
        else:
            return 0.0

    def _generate_risk_return_scatter(self) -> List[Dict[str, Any]]:
        """
        Generate risk-return scatter plot data.

        Returns:
            List of data points for risk-return scatter plot
        """
        # Generate data points for base case and stress test scenarios
        data_points = []

        # Add base case
        data_points.append({
            "scenario": "Base Case",
            "risk": self.risk_metrics.get("volatility", 0.0),
            "return": self.risk_metrics.get("irr", 0.0)
        })

        # Add stress test scenarios
        for scenario_name, scenario_results in self.stress_test_results.items():
            # Estimate risk (volatility) for the scenario
            # Simplified assumption: risk increases proportionally to the decrease in return
            base_return = self.risk_metrics.get("irr", 0.0)
            scenario_return = scenario_results.get("irr", 0.0)
            base_risk = self.risk_metrics.get("volatility", 0.0)

            if base_return > 0:
                risk_factor = max(1.0, base_return / max(0.001, scenario_return))
                scenario_risk = base_risk * risk_factor
            else:
                scenario_risk = base_risk * 1.5

            data_points.append({
                "scenario": scenario_name,
                "risk": scenario_risk,
                "return": scenario_return
            })

        return data_points

    def _generate_var_histogram(self) -> Dict[str, Any]:
        """
        Generate VaR histogram data.

        Returns:
            Dictionary with VaR histogram data
        """
        # Get returns
        returns = self._extract_returns()

        if not returns:
            return {
                "bins": [],
                "frequencies": [],
                "var_95": 0.0,
                "var_99": 0.0
            }

        # Calculate histogram
        hist, bin_edges = np.histogram(returns, bins=20)

        # Convert to lists for JSON serialization
        bins = bin_edges.tolist()
        frequencies = hist.tolist()

        # Get VaR values
        var_95 = self.risk_metrics.get("var_95", 0.0)
        var_99 = self.risk_metrics.get("var_99", 0.0)

        return {
            "bins": bins,
            "frequencies": frequencies,
            "var_95": var_95,
            "var_99": var_99
        }

    def _generate_drawdown_chart(self) -> List[Dict[str, Any]]:
        """
        Generate drawdown chart data.

        Returns:
            List of data points for drawdown chart
        """
        # Get cumulative returns
        cumulative_returns = self._extract_cumulative_returns()

        if not cumulative_returns:
            return []

        # Calculate drawdowns
        drawdowns = []
        peak = cumulative_returns[0]

        for i, value in enumerate(cumulative_returns):
            if value > peak:
                peak = value
                drawdown = 0.0
            else:
                drawdown = (peak - value) / peak if peak > 0 else 0.0

            # Get year and month
            if hasattr(self.context, "cashflows") and self.context.cashflows:
                fund_level_cashflows = self.context.cashflows.get("fund_level_cashflows", [])

                if i < len(fund_level_cashflows):
                    year = fund_level_cashflows[i].get("year", 0)
                    month = fund_level_cashflows[i].get("month", 0)
                else:
                    year = i // 12
                    month = i % 12 + 1
            else:
                year = i // 12
                month = i % 12 + 1

            drawdowns.append({
                "year": year,
                "month": month,
                "drawdown": drawdown
            })

        return drawdowns

    def _generate_stress_test_comparison(self) -> List[Dict[str, Any]]:
        """
        Generate stress test comparison chart data.

        Returns:
            List of data points for stress test comparison chart
        """
        comparison_data = []

        # Get base case metrics
        base_irr = self.risk_metrics.get("irr", 0.0)
        base_equity_multiple = self.risk_metrics.get("equity_multiple", 1.0)
        base_roi = self.risk_metrics.get("roi", 0.0)
        base_max_drawdown = self.risk_metrics.get("max_drawdown", 0.0)
        base_var_95 = self.risk_metrics.get("var_95", 0.0)

        # Add base case data points
        comparison_data.append({
            "scenario": "Base Case",
            "metric": "IRR",
            "value": base_irr,
            "base_value": base_irr,
            "pct_change": 0.0
        })

        comparison_data.append({
            "scenario": "Base Case",
            "metric": "Equity Multiple",
            "value": base_equity_multiple,
            "base_value": base_equity_multiple,
            "pct_change": 0.0
        })

        comparison_data.append({
            "scenario": "Base Case",
            "metric": "ROI",
            "value": base_roi,
            "base_value": base_roi,
            "pct_change": 0.0
        })

        comparison_data.append({
            "scenario": "Base Case",
            "metric": "Max Drawdown",
            "value": base_max_drawdown,
            "base_value": base_max_drawdown,
            "pct_change": 0.0
        })

        comparison_data.append({
            "scenario": "Base Case",
            "metric": "VaR (95%)",
            "value": base_var_95,
            "base_value": base_var_95,
            "pct_change": 0.0
        })

        # Add stress test scenario data points
        for scenario_name, scenario_results in self.stress_test_results.items():
            # Add IRR data point
            scenario_irr = scenario_results.get("irr", 0.0)
            irr_pct_change = (scenario_irr - base_irr) / base_irr if base_irr != 0 else 0.0

            comparison_data.append({
                "scenario": scenario_name,
                "metric": "IRR",
                "value": scenario_irr,
                "base_value": base_irr,
                "pct_change": irr_pct_change
            })

            # Add Equity Multiple data point
            scenario_equity_multiple = scenario_results.get("equity_multiple", 1.0)
            equity_multiple_pct_change = (scenario_equity_multiple - base_equity_multiple) / base_equity_multiple if base_equity_multiple != 0 else 0.0

            comparison_data.append({
                "scenario": scenario_name,
                "metric": "Equity Multiple",
                "value": scenario_equity_multiple,
                "base_value": base_equity_multiple,
                "pct_change": equity_multiple_pct_change
            })

            # Add ROI data point
            scenario_roi = scenario_results.get("roi", 0.0)
            roi_pct_change = (scenario_roi - base_roi) / base_roi if base_roi != 0 else 0.0

            comparison_data.append({
                "scenario": scenario_name,
                "metric": "ROI",
                "value": scenario_roi,
                "base_value": base_roi,
                "pct_change": roi_pct_change
            })

            # Add Max Drawdown data point
            scenario_max_drawdown = scenario_results.get("max_drawdown", 0.0)
            max_drawdown_pct_change = (scenario_max_drawdown - base_max_drawdown) / base_max_drawdown if base_max_drawdown != 0 else 0.0

            comparison_data.append({
                "scenario": scenario_name,
                "metric": "Max Drawdown",
                "value": scenario_max_drawdown,
                "base_value": base_max_drawdown,
                "pct_change": max_drawdown_pct_change
            })

            # Add VaR (95%) data point
            scenario_var_95 = scenario_results.get("var_95", 0.0)
            var_95_pct_change = (scenario_var_95 - base_var_95) / base_var_95 if base_var_95 != 0 else 0.0

            comparison_data.append({
                "scenario": scenario_name,
                "metric": "VaR (95%)",
                "value": scenario_var_95,
                "base_value": base_var_95,
                "pct_change": var_95_pct_change
            })

        return comparison_data

    def _generate_sensitivity_charts(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate sensitivity charts data.

        Returns:
            Dictionary with sensitivity charts data
        """
        sensitivity_charts = {}

        # Generate sensitivity chart for IRR
        irr_chart = []

        for parameter, sensitivity_results in self.scenario_analysis_results.items():
            parameter_values = [result.get("parameter_value", 0.0) for result in sensitivity_results]
            irr_values = [result.get("irr", 0.0) for result in sensitivity_results]

            irr_chart.append({
                "parameter": parameter,
                "values": parameter_values,
                "metric_values": irr_values
            })

        sensitivity_charts["irr"] = irr_chart

        # Generate sensitivity chart for Equity Multiple
        equity_multiple_chart = []

        for parameter, sensitivity_results in self.scenario_analysis_results.items():
            parameter_values = [result.get("parameter_value", 0.0) for result in sensitivity_results]
            equity_multiple_values = [result.get("equity_multiple", 1.0) for result in sensitivity_results]

            equity_multiple_chart.append({
                "parameter": parameter,
                "values": parameter_values,
                "metric_values": equity_multiple_values
            })

        sensitivity_charts["equity_multiple"] = equity_multiple_chart

        # Generate sensitivity chart for ROI
        roi_chart = []

        for parameter, sensitivity_results in self.scenario_analysis_results.items():
            parameter_values = [result.get("parameter_value", 0.0) for result in sensitivity_results]
            roi_values = [result.get("roi", 0.0) for result in sensitivity_results]

            roi_chart.append({
                "parameter": parameter,
                "values": parameter_values,
                "metric_values": roi_values
            })

        sensitivity_charts["roi"] = roi_chart

        return sensitivity_charts

    def _generate_concentration_chart(self) -> List[Dict[str, Any]]:
        """
        Generate concentration chart data.

        Returns:
            List of data points for concentration chart
        """
        concentration_data = []

        # Add zone concentration data points
        green_concentration = self._get_zone_concentration("green")
        orange_concentration = self._get_zone_concentration("orange")
        red_concentration = self._get_zone_concentration("red")

        total_zone_concentration = green_concentration + orange_concentration + red_concentration

        if total_zone_concentration > 0:
            concentration_data.append({
                "category": "zone",
                "name": "green",
                "value": green_concentration,
                "percentage": green_concentration / total_zone_concentration if total_zone_concentration > 0 else 0.0
            })

            concentration_data.append({
                "category": "zone",
                "name": "orange",
                "value": orange_concentration,
                "percentage": orange_concentration / total_zone_concentration if total_zone_concentration > 0 else 0.0
            })

            concentration_data.append({
                "category": "zone",
                "name": "red",
                "value": red_concentration,
                "percentage": red_concentration / total_zone_concentration if total_zone_concentration > 0 else 0.0
            })

        # Add suburb concentration data points if available
        if hasattr(self.context, "reinvestment") and self.context.reinvestment:
            suburb_concentration = self.context.reinvestment.get("suburb_concentration", {})

            for suburb, value in suburb_concentration.items():
                concentration_data.append({
                    "category": "suburb",
                    "name": suburb,
                    "value": value,
                    "percentage": value
                })

        return concentration_data
