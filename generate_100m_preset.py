#!/usr/bin/env python3
"""
Generate 100M fund preset configuration for testing.
This script creates a complete simulation configuration using the schema.
"""

import json

def generate_100m_fund_preset():
    """Generate a 100M fund preset configuration with ALL schema parameters."""

    config = {
        # Fund Basics
        "fund_size": 100000000.0,
        "fund_term": 10,
        "vintage_year": 2025,
        "gp_commitment_percentage": 0.02,
        "hurdle_rate": 0.08,
        "carried_interest_rate": 0.20,
        "waterfall_structure": "european",
        "management_fee_rate": 0.02,
        "management_fee_basis": "committed_capital",
        "catch_up_rate": 1.0,

        # Tranche Manager
        "tranche_manager": {
            "enabled": False,
            "tranches": [],
            "reserve_account": {
                "enabled": False,
                "target_percentage": 0.05,
                "initial_funding": 0.03,
                "replenishment_rate": 0.01
            },
            "overcollateralization_test": {
                "enabled": False,
                "threshold": 1.2,
                "test_frequency": "quarterly",
                "cure_period_months": 3
            },
            "interest_coverage_test": {
                "enabled": False,
                "threshold": 1.5,
                "test_frequency": "quarterly",
                "cure_period_months": 3
            }
        },

        # Fee Engine
        "fee_engine": {
            "origination_fee_rate": 0.03,
            "annual_fund_expenses": 0.005,
            "fixed_annual_expenses": 100000,
            "management_fee_schedule": [],
            "expense_growth_rate": 0.02,
            "acquisition_fee_rate": 0.0,
            "disposition_fee_rate": 0.0,
            "setup_costs": 250000
        },

        # Cashflow Aggregator
        "cashflow_aggregator": {
            "time_granularity": "yearly",
            "include_loan_level_cashflows": True,
            "include_fund_level_cashflows": True,
            "include_stakeholder_cashflows": True,
            "simple_interest_rate": 0.05,
            "origination_fee_rate": 0.03,
            "appreciation_share_method": "pro_rata_ltv",
            "distribution_frequency": "annual",
            "distribution_lag": 0,
            "enable_parallel_processing": True,
            "num_workers": 4,
            "enable_scenario_analysis": False,
            "scenarios": [],
            "enable_sensitivity_analysis": False,
            "sensitivity_parameters": [],
            "enable_cashflow_metrics": True,
            "discount_rate": 0.08,
            "enable_tax_impact_analysis": False,
            "tax_rates": {
                "ordinary_income": 0.35,
                "capital_gains": 0.20
            },
            "enable_reinvestment_modeling": True,
            "reinvestment_rate": 0.90,
            "enable_liquidity_analysis": True,
            "minimum_cash_reserve": 0.05,
            "enable_export": False,
            "export_formats": ["csv", "excel"]
        },

        # Loan Parameters
        "reinvestment_period": 5,
        "avg_loan_size": 400000.0,
        "loan_size_std_dev": 100000.0,
        "min_loan_size": 50000.0,
        "max_loan_size": 1000000.0,
        "avg_loan_term": 10,
        "avg_loan_interest_rate": 0.05,
        "avg_loan_ltv": 0.40,
        "ltv_std_dev": 0.10,
        "min_ltv": 0.15,
        "max_ltv": 0.65,

        # Zone Allocations
        "zone_allocations": {
            "green": 0.45,
            "orange": 0.35,
            "red": 0.20
        },

        # Appreciation Rates
        "appreciation_rates": {
            "green": 0.06,
            "orange": 0.05,
            "red": 0.04
        },

        # Price Path
        "price_path": {
            "model_type": "gbm",
            "volatility": {
                "green": 0.12,
                "orange": 0.15,
                "red": 0.18
            },
            "correlation_matrix": {
                "green_orange": 0.7,
                "green_red": 0.5,
                "orange_red": 0.8
            },
            "mean_reversion_params": {
                "speed": 0.2,
                "long_term_mean": 0.05
            },
            "regime_switching_params": {
                "bull_market_rate": 0.08,
                "bear_market_rate": -0.03,
                "bull_to_bear_prob": 0.1,
                "bear_to_bull_prob": 0.3
            },
            "time_step": "monthly",
            "suburb_variation": 0.02,
            "property_variation": 0.01,
            "cycle_position": 0.5
        },

        # Default and Recovery Rates
        "default_rates": {
            "green": 0.005,
            "orange": 0.015,
            "red": 0.025
        },

        "recovery_rates": {
            "green": 0.95,
            "orange": 0.85,
            "red": 0.75
        },

        # Monte Carlo Parameters
        "monte_carlo_enabled": False,
        "num_simulations": 1000,
        "monte_carlo_seed": 42,
        "deterministic_mode": True,

        # Variation Factors
        "variation_factors": {
            "price_path": 0.05,
            "default_events": 0.1,
            "prepayment_events": 0.2,
            "appreciation_rates": 0.05
        },

        # Correlation Matrix
        "correlation_matrix": {
            "price_path_default_events": -0.7,
            "price_path_prepayment_events": 0.3,
            "default_events_prepayment_events": -0.2
        },

        # Exit Simulator
        "exit_simulator": {
            "base_exit_rate": 0.4,
            "time_factor": 0.4,
            "price_factor": 0.6,
            "min_hold_period": 1.0,
            "max_hold_period": 8.0,
            "sale_weight": 0.6,
            "refinance_weight": 0.3,
            "default_weight": 0.1,
            "appreciation_sale_multiplier": 2.0,
            "interest_rate_refinance_multiplier": 3.0,
            "economic_factor_default_multiplier": 2.0,
            "appreciation_share": 0.4,
            "min_appreciation_share": 0.15,
            "max_appreciation_share": 0.65,
            "tiered_appreciation_thresholds": [0.2, 0.5, 1.0],
            "tiered_appreciation_shares": [0.15, 0.25, 0.35, 0.45],
            "base_default_rate": 0.01,
            "recovery_rate": 0.85,
            "foreclosure_cost": 0.1,
            "foreclosure_time": 1.0
        },

        # Enhanced Exit Simulator
        "enhanced_exit_simulator": {
            "refinance_interest_rate_sensitivity": 2.0,
            "sale_appreciation_sensitivity": 1.5,
            "life_event_probability": 0.05,
            "behavioral_correlation": 0.3,
            "recession_default_multiplier": 2.5,
            "inflation_refinance_multiplier": 1.8,
            "employment_sensitivity": 1.2,
            "migration_sensitivity": 0.8,
            "regulatory_compliance_cost": 0.01,
            "tax_efficiency_factor": 0.9,
            "vintage_segmentation": True,
            "ltv_segmentation": True,
            "zone_segmentation": True,
            "var_confidence_level": 0.95,
            "stress_test_severity": 0.3,
            "tail_risk_threshold": 0.05,
            "use_ml_models": True,
            "feature_importance_threshold": 0.05,
            "anomaly_detection_threshold": 3.0
        },

        # Reinvestment Engine
        "reinvestment_engine": {
            "reinvestment_strategy": "rebalance",
            "min_reinvestment_amount": 100000,
            "reinvestment_frequency": "quarterly",
            "reinvestment_delay": 1,
            "reinvestment_batch_size": 50,
            "zone_preference_multipliers": {
                "green": 1.0,
                "orange": 1.0,
                "red": 1.0
            },
            "opportunistic_threshold": 0.05,
            "rebalance_threshold": 0.05,
            "reinvestment_ltv_adjustment": 0,
            "reinvestment_size_adjustment": 0,
            "enable_dynamic_allocation": False,
            "performance_lookback_period": 12,
            "performance_weight": 0.5,
            "max_allocation_adjustment": 0.2,
            "reinvestment_tracking_granularity": "monthly",
            "enable_cash_reserve": False,
            "cash_reserve_target": 0.05,
            "cash_reserve_min": 0.02,
            "cash_reserve_max": 0.1
        },

        # Risk Metrics
        "risk_metrics": {
            "var_confidence_level": 0.95,
            "risk_free_rate": 0.03,
            "benchmark_return": 0.07,
            "min_acceptable_return": 0.04,
            "stress_test_scenarios": []
        }
    }

    return config

if __name__ == "__main__":
    # Generate the preset
    preset = generate_100m_fund_preset()

    # Save to file
    with open("100m_fund_preset.json", "w") as f:
        json.dump(preset, f, indent=2)

    print("Generated 100M fund preset configuration:")
    print(f"- Fund Size: ${preset['fund_size']:,.0f}")
    print(f"- Fund Term: {preset['fund_term']} years")
    print(f"- Average Loan Size: ${preset['avg_loan_size']:,.0f}")
    print(f"- Average LTV: {preset['avg_loan_ltv']:.1%}")
    print(f"- Management Fee: {preset['management_fee_rate']:.1%}")
    print(f"- Vintage Year: {preset['vintage_year']}")
    print("\nConfiguration saved to: 100m_fund_preset.json")
