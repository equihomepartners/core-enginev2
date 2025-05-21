"""
TLS Metrics module for the EQU IHOME SIM ENGINE v2.

This module defines the metrics used in the Traffic Light System.
"""

from typing import Dict, List, Tuple, Any

from src.tls_module.tls_core import Metric, MetricCategory


def get_economic_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get economic metrics."""
    return [
        (
            "employment_rate",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Percentage of working-age population that is employed",
                "unit": "%",
                "min_value": 50.0,
                "max_value": 98.0,
                "is_higher_better": True,
            },
        ),
        (
            "income_growth",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Annual growth rate of median household income",
                "unit": "%",
                "min_value": -5.0,
                "max_value": 15.0,
                "is_higher_better": True,
            },
        ),
        (
            "industry_diversity",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Measure of diversity in employment sectors",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 1.0,
                "is_higher_better": True,
            },
        ),
        (
            "economic_resilience",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Measure of economic resilience to downturns",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "business_growth",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Annual growth rate of businesses in the area",
                "unit": "%",
                "min_value": -10.0,
                "max_value": 20.0,
                "is_higher_better": True,
            },
        ),
        (
            "unemployment_rate",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Percentage of working-age population that is unemployed",
                "unit": "%",
                "min_value": 2.0,
                "max_value": 20.0,
                "is_higher_better": False,
            },
        ),
        (
            "median_household_income",
            {
                "category": MetricCategory.ECONOMIC,
                "description": "Median annual household income",
                "unit": "AUD",
                "min_value": 40000.0,
                "max_value": 200000.0,
                "is_higher_better": True,
            },
        ),
    ]


def get_real_estate_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get real estate metrics."""
    return [
        (
            "appreciation_1yr",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "1-year property price appreciation rate",
                "unit": "%",
                "min_value": -15.0,
                "max_value": 30.0,
                "is_higher_better": True,
            },
        ),
        (
            "appreciation_3yr",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "3-year annualized property price appreciation rate",
                "unit": "%",
                "min_value": -10.0,
                "max_value": 20.0,
                "is_higher_better": True,
            },
        ),
        (
            "appreciation_5yr",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "5-year annualized property price appreciation rate",
                "unit": "%",
                "min_value": -5.0,
                "max_value": 15.0,
                "is_higher_better": True,
            },
        ),
        (
            "appreciation_10yr",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "10-year annualized property price appreciation rate",
                "unit": "%",
                "min_value": -2.0,
                "max_value": 12.0,
                "is_higher_better": True,
            },
        ),
        (
            "price_volatility",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Standard deviation of annual price changes over 5 years",
                "unit": "%",
                "min_value": 1.0,
                "max_value": 20.0,
                "is_higher_better": False,
            },
        ),
        (
            "days_on_market",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Average days on market for properties",
                "unit": "days",
                "min_value": 7.0,
                "max_value": 180.0,
                "is_higher_better": False,
            },
        ),
        (
            "auction_clearance_rate",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Percentage of auctions resulting in sales",
                "unit": "%",
                "min_value": 40.0,
                "max_value": 95.0,
                "is_higher_better": True,
            },
        ),
        (
            "rental_yield_gross",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Gross rental yield",
                "unit": "%",
                "min_value": 1.0,
                "max_value": 8.0,
                "is_higher_better": True,
            },
        ),
        (
            "vacancy_rate",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Rental vacancy rate",
                "unit": "%",
                "min_value": 0.5,
                "max_value": 10.0,
                "is_higher_better": False,
            },
        ),
        (
            "inventory_months",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Months of inventory (supply)",
                "unit": "months",
                "min_value": 0.5,
                "max_value": 12.0,
                "is_higher_better": False,
            },
        ),
        (
            "median_property_value",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Median property value",
                "unit": "AUD",
                "min_value": 300000.0,
                "max_value": 5000000.0,
                "is_higher_better": True,
            },
        ),
        (
            "price_to_income_ratio",
            {
                "category": MetricCategory.REAL_ESTATE,
                "description": "Ratio of median property price to median annual income",
                "unit": "ratio",
                "min_value": 3.0,
                "max_value": 15.0,
                "is_higher_better": False,
            },
        ),
    ]


def get_demographic_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get demographic metrics."""
    return [
        (
            "population_growth",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Annual population growth rate",
                "unit": "%",
                "min_value": -2.0,
                "max_value": 5.0,
                "is_higher_better": True,
            },
        ),
        (
            "median_age",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Median age of residents",
                "unit": "years",
                "min_value": 25.0,
                "max_value": 60.0,
                "is_higher_better": None,  # Neutral
            },
        ),
        (
            "household_formation_rate",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Annual growth rate of households",
                "unit": "%",
                "min_value": -1.0,
                "max_value": 4.0,
                "is_higher_better": True,
            },
        ),
        (
            "owner_occupier_ratio",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Percentage of properties occupied by owners",
                "unit": "%",
                "min_value": 30.0,
                "max_value": 90.0,
                "is_higher_better": True,
            },
        ),
        (
            "education_level",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Percentage of residents with tertiary education",
                "unit": "%",
                "min_value": 10.0,
                "max_value": 70.0,
                "is_higher_better": True,
            },
        ),
        (
            "family_households",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Percentage of households that are families",
                "unit": "%",
                "min_value": 40.0,
                "max_value": 90.0,
                "is_higher_better": None,  # Neutral
            },
        ),
        (
            "population_density",
            {
                "category": MetricCategory.DEMOGRAPHIC,
                "description": "Population per square kilometer",
                "unit": "people/km²",
                "min_value": 500.0,
                "max_value": 10000.0,
                "is_higher_better": None,  # Neutral
            },
        ),
    ]


def get_risk_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get risk metrics."""
    return [
        (
            "default_probability",
            {
                "category": MetricCategory.RISK,
                "description": "Probability of mortgage default",
                "unit": "%",
                "min_value": 0.1,
                "max_value": 5.0,
                "is_higher_better": False,
            },
        ),
        (
            "recovery_rate",
            {
                "category": MetricCategory.RISK,
                "description": "Expected recovery rate in case of default",
                "unit": "%",
                "min_value": 60.0,
                "max_value": 95.0,
                "is_higher_better": True,
            },
        ),
        (
            "price_drop_frequency",
            {
                "category": MetricCategory.RISK,
                "description": "Frequency of price drops in listings",
                "unit": "%",
                "min_value": 5.0,
                "max_value": 50.0,
                "is_higher_better": False,
            },
        ),
        (
            "market_liquidity",
            {
                "category": MetricCategory.RISK,
                "description": "Measure of market liquidity",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "insurance_cost",
            {
                "category": MetricCategory.RISK,
                "description": "Average annual property insurance cost",
                "unit": "AUD",
                "min_value": 1000.0,
                "max_value": 5000.0,
                "is_higher_better": False,
            },
        ),
        (
            "flood_risk",
            {
                "category": MetricCategory.RISK,
                "description": "Flood risk score",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": False,
            },
        ),
        (
            "bushfire_risk",
            {
                "category": MetricCategory.RISK,
                "description": "Bushfire risk score",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": False,
            },
        ),
    ]


def get_location_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get location metrics."""
    return [
        (
            "school_quality",
            {
                "category": MetricCategory.LOCATION,
                "description": "School quality score",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "crime_rate",
            {
                "category": MetricCategory.LOCATION,
                "description": "Crime incidents per 1000 residents",
                "unit": "incidents/1000",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": False,
            },
        ),
        (
            "walkability",
            {
                "category": MetricCategory.LOCATION,
                "description": "Walkability score",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "transit_accessibility",
            {
                "category": MetricCategory.LOCATION,
                "description": "Public transit accessibility score",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "amenity_proximity",
            {
                "category": MetricCategory.LOCATION,
                "description": "Proximity to amenities score",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "infrastructure_investment",
            {
                "category": MetricCategory.LOCATION,
                "description": "Infrastructure investment per capita",
                "unit": "AUD",
                "min_value": 0.0,
                "max_value": 10000.0,
                "is_higher_better": True,
            },
        ),
        (
            "beach_proximity",
            {
                "category": MetricCategory.LOCATION,
                "description": "Distance to nearest beach",
                "unit": "km",
                "min_value": 0.0,
                "max_value": 50.0,
                "is_higher_better": False,
            },
        ),
        (
            "cbd_proximity",
            {
                "category": MetricCategory.LOCATION,
                "description": "Distance to CBD",
                "unit": "km",
                "min_value": 0.0,
                "max_value": 50.0,
                "is_higher_better": False,
            },
        ),
    ]


def get_supply_demand_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get supply and demand metrics."""
    return [
        (
            "development_pipeline",
            {
                "category": MetricCategory.SUPPLY_DEMAND,
                "description": "New dwellings in development pipeline as percentage of existing stock",
                "unit": "%",
                "min_value": 0.0,
                "max_value": 20.0,
                "is_higher_better": False,
            },
        ),
        (
            "land_availability",
            {
                "category": MetricCategory.SUPPLY_DEMAND,
                "description": "Available land for development as percentage of total area",
                "unit": "%",
                "min_value": 0.0,
                "max_value": 30.0,
                "is_higher_better": True,
            },
        ),
        (
            "zoning_restrictions",
            {
                "category": MetricCategory.SUPPLY_DEMAND,
                "description": "Restrictiveness of zoning regulations",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": False,
            },
        ),
        (
            "demand_pressure",
            {
                "category": MetricCategory.SUPPLY_DEMAND,
                "description": "Measure of demand pressure relative to supply",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "buyer_competition",
            {
                "category": MetricCategory.SUPPLY_DEMAND,
                "description": "Average number of bidders per property",
                "unit": "bidders",
                "min_value": 1.0,
                "max_value": 10.0,
                "is_higher_better": True,
            },
        ),
        (
            "rental_demand",
            {
                "category": MetricCategory.SUPPLY_DEMAND,
                "description": "Rental demand pressure index",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
    ]


def get_temporal_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get temporal metrics."""
    return [
        (
            "price_momentum",
            {
                "category": MetricCategory.TEMPORAL,
                "description": "Short-term price momentum indicator",
                "unit": "index",
                "min_value": -100.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
        (
            "seasonal_factor",
            {
                "category": MetricCategory.TEMPORAL,
                "description": "Seasonal adjustment factor for current season",
                "unit": "factor",
                "min_value": 0.8,
                "max_value": 1.2,
                "is_higher_better": None,  # Neutral
            },
        ),
        (
            "cycle_position",
            {
                "category": MetricCategory.TEMPORAL,
                "description": "Position in the property cycle",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": None,  # Neutral
            },
        ),
        (
            "trend_strength",
            {
                "category": MetricCategory.TEMPORAL,
                "description": "Strength of current price trend",
                "unit": "index",
                "min_value": 0.0,
                "max_value": 100.0,
                "is_higher_better": True,
            },
        ),
    ]


def get_all_metrics() -> List[Tuple[str, Dict[str, Any]]]:
    """Get all metrics."""
    return (
        get_economic_metrics()
        + get_real_estate_metrics()
        + get_demographic_metrics()
        + get_risk_metrics()
        + get_location_metrics()
        + get_supply_demand_metrics()
        + get_temporal_metrics()
    )
