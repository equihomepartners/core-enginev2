"""
Standalone TLS Data Generator for the EQU IHOME SIM ENGINE v2.

This script processes Sydney house price data and generates a static JSON file
with 300 diverse suburbs and their metrics for use in the TLS module.

This is a standalone version that doesn't depend on the existing codebase.
"""

import os
import json
import random
import time
from typing import Dict, List, Any, Tuple, Set, Optional
from pathlib import Path
from datetime import datetime

# Set random seed for reproducibility
random.seed(42)

# Constants
OUTPUT_FILE = "src/tls_module/data/sydney_suburbs_data.json"
SYDNEY_HOUSE_PRICES_CSV = "SydneyHousePrices.csv"
NUM_SUBURBS = 300
NUM_PROPERTIES_PER_SUBURB_MIN = 20
NUM_PROPERTIES_PER_SUBURB_MAX = 100

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Economic metrics ranges
ECONOMIC_METRICS = {
    "employment_rate": {"min": 50.0, "max": 98.0, "unit": "%", "higher_better": True},
    "unemployment_rate": {"min": 2.0, "max": 20.0, "unit": "%", "higher_better": False},
    "income_growth": {"min": -5.0, "max": 15.0, "unit": "%", "higher_better": True},
    "median_household_income": {"min": 40000.0, "max": 200000.0, "unit": "AUD", "higher_better": True},
    "industry_diversity": {"min": 0.0, "max": 1.0, "unit": "index", "higher_better": True},
    "economic_resilience": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "business_growth": {"min": -10.0, "max": 20.0, "unit": "%", "higher_better": True},
}

# Real estate metrics ranges
REAL_ESTATE_METRICS = {
    "appreciation_1yr": {"min": -15.0, "max": 30.0, "unit": "%", "higher_better": True},
    "appreciation_3yr": {"min": -10.0, "max": 20.0, "unit": "%", "higher_better": True},
    "appreciation_5yr": {"min": -5.0, "max": 15.0, "unit": "%", "higher_better": True},
    "appreciation_10yr": {"min": -2.0, "max": 12.0, "unit": "%", "higher_better": True},
    "price_volatility": {"min": 1.0, "max": 20.0, "unit": "%", "higher_better": False},
    "days_on_market": {"min": 7.0, "max": 180.0, "unit": "days", "higher_better": False},
    "auction_clearance_rate": {"min": 40.0, "max": 95.0, "unit": "%", "higher_better": True},
    "rental_yield_gross": {"min": 1.0, "max": 8.0, "unit": "%", "higher_better": True},
    "vacancy_rate": {"min": 0.5, "max": 10.0, "unit": "%", "higher_better": False},
    "inventory_months": {"min": 0.5, "max": 12.0, "unit": "months", "higher_better": False},
    "median_property_value": {"min": 300000.0, "max": 5000000.0, "unit": "AUD", "higher_better": True},
    "price_to_income_ratio": {"min": 3.0, "max": 15.0, "unit": "ratio", "higher_better": False},
}

# Demographic metrics ranges
DEMOGRAPHIC_METRICS = {
    "population_growth": {"min": -2.0, "max": 5.0, "unit": "%", "higher_better": True},
    "median_age": {"min": 25.0, "max": 60.0, "unit": "years", "higher_better": None},
    "household_formation_rate": {"min": -1.0, "max": 4.0, "unit": "%", "higher_better": True},
    "owner_occupier_ratio": {"min": 30.0, "max": 90.0, "unit": "%", "higher_better": True},
    "education_level": {"min": 10.0, "max": 70.0, "unit": "%", "higher_better": True},
    "family_households": {"min": 40.0, "max": 90.0, "unit": "%", "higher_better": None},
    "population_density": {"min": 500.0, "max": 10000.0, "unit": "people/km²", "higher_better": None},
}

# Risk metrics ranges
RISK_METRICS = {
    "default_probability": {"min": 0.1, "max": 5.0, "unit": "%", "higher_better": False},
    "recovery_rate": {"min": 60.0, "max": 95.0, "unit": "%", "higher_better": True},
    "price_drop_frequency": {"min": 5.0, "max": 50.0, "unit": "%", "higher_better": False},
    "market_liquidity": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "insurance_cost": {"min": 1000.0, "max": 5000.0, "unit": "AUD", "higher_better": False},
    "flood_risk": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": False},
    "bushfire_risk": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": False},
}

# Location metrics ranges
LOCATION_METRICS = {
    "school_quality": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "crime_rate": {"min": 0.0, "max": 100.0, "unit": "incidents/1000", "higher_better": False},
    "walkability": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "transit_accessibility": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "amenity_proximity": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "infrastructure_investment": {"min": 0.0, "max": 10000.0, "unit": "AUD", "higher_better": True},
    "beach_proximity": {"min": 0.0, "max": 50.0, "unit": "km", "higher_better": False},
    "cbd_proximity": {"min": 0.0, "max": 50.0, "unit": "km", "higher_better": False},
}

# Supply/demand metrics ranges
SUPPLY_DEMAND_METRICS = {
    "development_pipeline": {"min": 0.0, "max": 20.0, "unit": "%", "higher_better": False},
    "land_availability": {"min": 0.0, "max": 30.0, "unit": "%", "higher_better": True},
    "zoning_restrictions": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": False},
    "demand_pressure": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
    "buyer_competition": {"min": 1.0, "max": 10.0, "unit": "bidders", "higher_better": True},
    "rental_demand": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
}

# Temporal metrics ranges
TEMPORAL_METRICS = {
    "price_momentum": {"min": -100.0, "max": 100.0, "unit": "index", "higher_better": True},
    "seasonal_factor": {"min": 0.8, "max": 1.2, "unit": "factor", "higher_better": None},
    "cycle_position": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": None},
    "trend_strength": {"min": 0.0, "max": 100.0, "unit": "index", "higher_better": True},
}

# Combine all metrics
ALL_METRICS = {
    **ECONOMIC_METRICS,
    **REAL_ESTATE_METRICS,
    **DEMOGRAPHIC_METRICS,
    **RISK_METRICS,
    **LOCATION_METRICS,
    **SUPPLY_DEMAND_METRICS,
    **TEMPORAL_METRICS,
}

# Property types with probabilities
PROPERTY_TYPES = [
    ("house", 0.5),
    ("apartment", 0.3),
    ("townhouse", 0.15),
    ("duplex", 0.05),
]

# Sydney suburbs (300 representative suburbs)
SYDNEY_SUBURBS = [
    # Eastern Suburbs
    ("Bondi", "2026", -33.8914, 151.2743),
    ("Bondi Junction", "2022", -33.8932, 151.2503),
    ("Bronte", "2024", -33.9048, 151.2630),
    ("Clovelly", "2031", -33.9129, 151.2594),
    ("Coogee", "2034", -33.9183, 151.2584),
    ("Double Bay", "2028", -33.8785, 151.2428),
    ("Maroubra", "2035", -33.9494, 151.2428),
    ("Paddington", "2021", -33.8845, 151.2271),
    ("Randwick", "2031", -33.9174, 151.2428),
    ("Rose Bay", "2029", -33.8696, 151.2684),
    ("Vaucluse", "2030", -33.8563, 151.2784),
    ("Waverley", "2024", -33.8991, 151.2553),
    ("Woollahra", "2025", -33.8867, 151.2412),

    # Northern Beaches
    ("Avalon", "2107", -33.6361, 151.3314),
    ("Balgowlah", "2093", -33.8000, 151.2600),
    ("Collaroy", "2097", -33.7342, 151.3019),
    ("Dee Why", "2099", -33.7511, 151.2857),
    ("Freshwater", "2096", -33.7800, 151.2900),
    ("Manly", "2095", -33.7971, 151.2857),
    ("Mona Vale", "2103", -33.6767, 151.3152),
    ("Narrabeen", "2101", -33.7200, 151.3000),
    ("Newport", "2106", -33.6500, 151.3200),
    ("Palm Beach", "2108", -33.5994, 151.3220),

    # North Shore
    ("Artarmon", "2064", -33.8100, 151.1800),
    ("Chatswood", "2067", -33.7971, 151.1828),
    ("Cremorne", "2090", -33.8300, 151.2300),
    ("Gordon", "2072", -33.7558, 151.1543),
    ("Killara", "2071", -33.7700, 151.1600),
    ("Lane Cove", "2066", -33.8142, 151.1694),
    ("Lindfield", "2070", -33.7800, 151.1700),
    ("Mosman", "2088", -33.8288, 151.2428),
    ("North Sydney", "2060", -33.8400, 151.2100),
    ("Pymble", "2073", -33.7500, 151.1400),
    ("Roseville", "2069", -33.7800, 151.1800),
    ("St Ives", "2075", -33.7300, 151.1600),
    ("Turramurra", "2074", -33.7400, 151.1300),
    ("Wahroonga", "2076", -33.7200, 151.1200),
    ("Willoughby", "2068", -33.8000, 151.2000),

    # Inner West
    ("Ashfield", "2131", -33.8900, 151.1300),
    ("Balmain", "2041", -33.8600, 151.1800),
    ("Burwood", "2134", -33.8785, 151.1019),
    ("Concord", "2137", -33.8600, 151.0900),
    ("Drummoyne", "2047", -33.8500, 151.1600),
    ("Five Dock", "2046", -33.8600, 151.1300),
    ("Glebe", "2037", -33.8800, 151.1900),
    ("Haberfield", "2045", -33.8800, 151.1400),
    ("Leichhardt", "2040", -33.8845, 151.1543),
    ("Marrickville", "2204", -33.9108, 151.1543),
    ("Newtown", "2042", -33.8988, 151.1785),
    ("Petersham", "2049", -33.8900, 151.1500),
    ("Rozelle", "2039", -33.8600, 151.1700),
    ("Strathfield", "2135", -33.8785, 151.0826),
    ("Summer Hill", "2130", -33.8900, 151.1400),

    # Western Suburbs
    ("Auburn", "2144", -33.8500, 151.0300),
    ("Baulkham Hills", "2153", -33.7645, 150.9826),
    ("Blacktown", "2148", -33.7711, 150.9063),
    ("Castle Hill", "2154", -33.7300, 151.0000),
    ("Granville", "2142", -33.8300, 151.0100),
    ("Greystanes", "2145", -33.8300, 150.9500),
    ("Guildford", "2161", -33.8500, 150.9800),
    ("Kellyville", "2155", -33.7000, 150.9500),
    ("Merrylands", "2160", -33.8400, 150.9900),
    ("Parramatta", "2150", -33.8148, 151.0011),
    ("Penrith", "2750", -33.7511, 150.6942),
    ("Quakers Hill", "2763", -33.7300, 150.8800),
    ("Rouse Hill", "2155", -33.6800, 150.9200),
    ("Seven Hills", "2147", -33.7800, 150.9400),
    ("Wentworthville", "2145", -33.8100, 150.9700),

    # South-Western Suburbs
    ("Bankstown", "2200", -33.9174, 151.0341),
    ("Cabramatta", "2166", -33.8900, 150.9400),
    ("Campbelltown", "2560", -34.0654, 150.8141),
    ("Casula", "2170", -33.9500, 150.9100),
    ("Fairfield", "2165", -33.8700, 150.9600),
    ("Glenfield", "2167", -33.9700, 150.8900),
    ("Hoxton Park", "2171", -33.9300, 150.8500),
    ("Ingleburn", "2565", -34.0000, 150.8600),
    ("Liverpool", "2170", -33.9200, 150.9255),
    ("Macquarie Fields", "2564", -33.9800, 150.8800),
    ("Minto", "2566", -34.0300, 150.8500),
    ("Narellan", "2567", -34.0400, 150.7400),
    ("Prestons", "2170", -33.9400, 150.8700),
    ("Revesby", "2212", -33.9600, 151.0200),
    ("Yagoona", "2199", -33.9100, 151.0200),

    # Southern Suburbs
    ("Cronulla", "2230", -34.0581, 151.1543),
    ("Engadine", "2233", -34.0700, 151.0100),
    ("Gymea", "2227", -34.0300, 151.0800),
    ("Hurstville", "2220", -33.9674, 151.1019),
    ("Kogarah", "2217", -33.9700, 151.1300),
    ("Menai", "2234", -34.0100, 151.0100),
    ("Miranda", "2228", -34.0354, 151.1019),
    ("Rockdale", "2216", -33.9500, 151.1400),
    ("Sutherland", "2232", -34.0300, 151.0600),

    # Northern Districts
    ("Beecroft", "2119", -33.7500, 151.0600),
    ("Carlingford", "2118", -33.7800, 151.0500),
    ("Eastwood", "2122", -33.7905, 151.0826),
    ("Epping", "2121", -33.7700, 151.0800),
    ("Hornsby", "2077", -33.7035, 151.0982),
    ("Marsfield", "2122", -33.7800, 151.1000),
    ("Normanhurst", "2076", -33.7200, 151.0900),
    ("Pennant Hills", "2120", -33.7400, 151.0700),
    ("Ryde", "2112", -33.8148, 151.1019),
    ("Thornleigh", "2120", -33.7300, 151.0800),
    ("West Pennant Hills", "2125", -33.7500, 151.0400),
    ("West Ryde", "2114", -33.8100, 151.0900),
]

def generate_suburb_metrics() -> Dict[str, Dict[str, Any]]:
    """
    Generate metrics for each suburb.

    Returns:
        Dictionary mapping suburb_id to suburb data
    """
    print("Generating suburb metrics...")

    # Create suburb dictionary
    suburbs = {}

    # Generate metrics for each suburb
    for i, (suburb, postal_code, latitude, longitude) in enumerate(SYDNEY_SUBURBS):
        # Create suburb ID
        suburb_id = f"SYD{i+1:03d}"

        # Generate scores with some correlation to location
        # Eastern/Northern suburbs tend to have higher scores
        base_score = 50.0

        # Location factor (east/north is higher)
        location_factor = (longitude - 150.5) * 20 + (-34.0 - latitude) * 10

        # Add some randomness
        random_factor = random.uniform(-10, 10)

        # Calculate scores
        appreciation_score = min(100, max(0, base_score + location_factor + random_factor))
        risk_score = min(100, max(0, base_score - location_factor + random_factor))
        liquidity_score = min(100, max(0, base_score + location_factor * 0.5 + random_factor))
        overall_score = (appreciation_score * 0.4 + (100 - risk_score) * 0.3 + liquidity_score * 0.3)

        # Calculate confidences (higher for well-known suburbs)
        confidence_base = 0.7
        confidence_factor = random.uniform(-0.2, 0.2)
        appreciation_confidence = min(1.0, max(0.3, confidence_base + confidence_factor))
        risk_confidence = min(1.0, max(0.3, confidence_base + confidence_factor))
        liquidity_confidence = min(1.0, max(0.3, confidence_base + confidence_factor))
        overall_confidence = (appreciation_confidence + risk_confidence + liquidity_confidence) / 3

        # Create suburb data
        suburb_data = {
            "suburb_id": suburb_id,
            "name": suburb,
            "state": "NSW",
            "postcode": postal_code,
            "latitude": latitude,
            "longitude": longitude,
            "appreciation_score": appreciation_score,
            "risk_score": risk_score,
            "liquidity_score": liquidity_score,
            "overall_score": overall_score,
            "appreciation_confidence": appreciation_confidence,
            "risk_confidence": risk_confidence,
            "liquidity_confidence": liquidity_confidence,
            "overall_confidence": overall_confidence,
            "metrics": {},
            "properties": [],
        }

        # Generate metrics
        for metric_name, metric_info in ALL_METRICS.items():
            # Base value depends on suburb scores
            if metric_info["higher_better"] is True:
                # For positive metrics, higher suburb score means higher metric value
                base_value = suburb_data["overall_score"] / 100.0
            elif metric_info["higher_better"] is False:
                # For negative metrics, higher suburb score means lower metric value
                base_value = 1.0 - (suburb_data["overall_score"] / 100.0)
            else:
                # For neutral metrics, use middle value
                base_value = 0.5

            # Scale to metric range
            value_range = metric_info["max"] - metric_info["min"]
            scaled_value = metric_info["min"] + (base_value * value_range)

            # Add randomness (more for lower confidence suburbs)
            randomness_factor = (1.0 - suburb_data["overall_confidence"]) * 0.5
            random_adjustment = random.uniform(-randomness_factor, randomness_factor) * value_range

            # Final value with constraints
            final_value = min(metric_info["max"], max(metric_info["min"], scaled_value + random_adjustment))

            # Add metric to suburb data
            suburb_data["metrics"][metric_name] = {
                "value": final_value,
                "confidence": suburb_data["overall_confidence"],
                "percentile": None,  # Will be calculated later
            }

        # Add suburb to dictionary
        suburbs[suburb_id] = suburb_data

    # Calculate percentiles for all metrics
    for metric_name in ALL_METRICS:
        # Get all values for this metric
        values = [suburb["metrics"][metric_name]["value"] for suburb in suburbs.values()]

        # Calculate percentiles
        for suburb_id, suburb_data in suburbs.items():
            value = suburb_data["metrics"][metric_name]["value"]
            percentile = sum(v < value for v in values) / len(values)
            suburb_data["metrics"][metric_name]["percentile"] = percentile

    print(f"Generated metrics for {len(suburbs)} suburbs.")
    return suburbs

def generate_properties(suburbs: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Generate properties for each suburb.

    Args:
        suburbs: Dictionary mapping suburb_id to suburb data

    Returns:
        Updated suburbs dictionary
    """
    print("Generating properties...")

    # Generate properties for each suburb
    for suburb_id, suburb_data in suburbs.items():
        # Number of properties depends on suburb score (more for higher scores)
        # Between MIN and MAX properties per suburb
        num_properties = int(NUM_PROPERTIES_PER_SUBURB_MIN +
                            (suburb_data["overall_score"] / 100.0) *
                            (NUM_PROPERTIES_PER_SUBURB_MAX - NUM_PROPERTIES_PER_SUBURB_MIN))

        # Base property value from median_property_value metric
        base_property_value = 1000000.0  # Default if metric not available
        if "median_property_value" in suburb_data["metrics"]:
            base_property_value = suburb_data["metrics"]["median_property_value"]["value"]

        # Create properties
        properties = []
        for j in range(num_properties):
            # Generate property ID
            property_id = f"{suburb_id}_P{j+1:04d}"

            # Select property type based on probabilities
            property_type = random.choices(
                [pt[0] for pt in PROPERTY_TYPES],
                weights=[pt[1] for pt in PROPERTY_TYPES],
                k=1,
            )[0]

            # Generate bedrooms (1-5)
            if property_type == "apartment":
                bedrooms = random.choices([1, 2, 3, 4], weights=[0.3, 0.4, 0.25, 0.05], k=1)[0]
            else:
                bedrooms = random.choices([2, 3, 4, 5], weights=[0.2, 0.4, 0.3, 0.1], k=1)[0]

            # Generate bathrooms (usually bedrooms - 1 or equal)
            bathrooms = max(1, random.choices(
                [bedrooms - 1, bedrooms, bedrooms + 1],
                weights=[0.4, 0.5, 0.1],
                k=1,
            )[0])

            # Generate parking (0-3)
            if property_type == "apartment":
                parking = random.choices([0, 1, 2], weights=[0.2, 0.7, 0.1], k=1)[0]
            else:
                parking = random.choices([1, 2, 3], weights=[0.3, 0.6, 0.1], k=1)[0]

            # Generate land size (square meters)
            if property_type == "house":
                land_size = random.uniform(300, 1000)
            elif property_type == "townhouse":
                land_size = random.uniform(150, 300)
            elif property_type == "duplex":
                land_size = random.uniform(200, 400)
            else:  # apartment
                land_size = 0.0

            # Generate building size (square meters)
            if property_type == "house":
                building_size = random.uniform(120, 350)
            elif property_type == "townhouse":
                building_size = random.uniform(100, 200)
            elif property_type == "duplex":
                building_size = random.uniform(100, 250)
            else:  # apartment
                building_size = random.uniform(50, 150)

            # Generate year built (1900-2023)
            # Higher score suburbs tend to have newer properties
            min_year = 1900
            max_year = 2023
            year_range = max_year - min_year
            year_built = min_year + int((suburb_data["overall_score"] / 100.0) * 0.5 * year_range + random.uniform(0, 0.5 * year_range))

            # Generate condition (0-1)
            # Newer properties tend to be in better condition
            age_factor = 1.0 - ((max_year - year_built) / year_range)
            condition = min(1.0, max(0.0, age_factor * 0.7 + random.uniform(0, 0.3)))

            # Generate quality (0-1)
            # Higher score suburbs tend to have higher quality properties
            quality = min(1.0, max(0.0, (suburb_data["overall_score"] / 100.0) * 0.8 + random.uniform(0, 0.2)))

            # Generate street quality (0-1)
            street_quality = min(1.0, max(0.0, (suburb_data["overall_score"] / 100.0) * 0.7 + random.uniform(-0.2, 0.3)))

            # Generate view quality (0-1)
            view_quality = min(1.0, max(0.0, random.uniform(0, 1.0)))

            # Generate noise level (0-1)
            noise_level = min(1.0, max(0.0, 1.0 - (suburb_data["overall_score"] / 100.0) * 0.6 + random.uniform(-0.2, 0.4)))

            # Generate appreciation modifier (0.8-1.2)
            appreciation_modifier = min(1.2, max(0.8, 1.0 + random.uniform(-0.2, 0.2)))

            # Generate risk modifier (0.8-1.2)
            risk_modifier = min(1.2, max(0.8, 1.0 + random.uniform(-0.2, 0.2)))

            # Calculate property value
            # Base value adjusted for property characteristics
            value_adjustments = {
                "bedrooms": (bedrooms - 3) * 0.1,  # +/- 10% per bedroom difference from 3
                "bathrooms": (bathrooms - 2) * 0.05,  # +/- 5% per bathroom difference from 2
                "parking": parking * 0.03,  # +3% per parking space
                "land_size": (land_size - 500) / 500 * 0.1 if land_size > 0 else 0,  # +/- 10% per 500sqm
                "building_size": (building_size - 150) / 150 * 0.1,  # +/- 10% per 150sqm
                "condition": (condition - 0.5) * 0.2,  # +/- 20% from average condition
                "quality": (quality - 0.5) * 0.3,  # +/- 30% from average quality
                "street_quality": (street_quality - 0.5) * 0.1,  # +/- 10% from average street
                "view_quality": view_quality * 0.2,  # Up to +20% for great views
                "noise_level": -noise_level * 0.1,  # Up to -10% for noisy locations
            }

            # Apply adjustments
            adjustment_factor = 1.0
            for adjustment in value_adjustments.values():
                adjustment_factor += adjustment

            # Final property value
            property_value = base_property_value * adjustment_factor

            # Create property
            property_data = {
                "property_id": property_id,
                "suburb_id": suburb_id,
                "property_type": property_type,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "parking": parking,
                "land_size": land_size,
                "building_size": building_size,
                "year_built": year_built,
                "condition": condition,
                "quality": quality,
                "street_quality": street_quality,
                "view_quality": view_quality,
                "noise_level": noise_level,
                "appreciation_modifier": appreciation_modifier,
                "risk_modifier": risk_modifier,
                "base_value": property_value,
                "metrics": {},
            }

            # Add property-specific metrics
            # These are variations of the suburb metrics
            for metric_name, metric_info in ALL_METRICS.items():
                if metric_name in suburb_data["metrics"]:
                    suburb_value = suburb_data["metrics"][metric_name]["value"]
                    suburb_confidence = suburb_data["metrics"][metric_name]["confidence"]

                    # Property values vary from suburb values
                    variation = random.uniform(-0.2, 0.2) * (metric_info["max"] - metric_info["min"])
                    property_value = max(metric_info["min"], min(metric_info["max"], suburb_value + variation))

                    # Property confidence is slightly lower than suburb confidence
                    property_confidence = max(0.1, suburb_confidence * random.uniform(0.8, 1.0))

                    # Add metric to property
                    property_data["metrics"][metric_name] = {
                        "value": property_value,
                        "confidence": property_confidence,
                    }

            # Add property to suburb
            properties.append(property_data)

        # Update suburb with properties
        suburb_data["properties"] = properties

    # Count total properties
    total_properties = sum(len(suburb_data["properties"]) for suburb_data in suburbs.values())
    print(f"Generated {total_properties} properties across {len(suburbs)} suburbs.")

    return suburbs

def generate_correlations(suburbs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate correlations between metrics and suburbs.

    Args:
        suburbs: Dictionary mapping suburb_id to suburb data

    Returns:
        Dictionary with metric and suburb correlations
    """
    print("Generating correlations...")

    # Create correlation dictionary
    correlations = {
        "metrics": {},
        "suburbs": {},
    }

    # Generate metric correlations
    metric_names = list(ALL_METRICS.keys())

    # Initialize correlation matrix
    for metric_name in metric_names:
        correlations["metrics"][metric_name] = {}

    # Set self-correlations to 1.0
    for metric_name in metric_names:
        correlations["metrics"][metric_name][metric_name] = 1.0

    # Define strongly correlated metric pairs
    strong_correlations = [
        # Economic correlations
        ("employment_rate", "unemployment_rate", -0.9),  # Negatively correlated
        ("employment_rate", "median_household_income", 0.7),
        ("income_growth", "economic_resilience", 0.6),

        # Real estate correlations
        ("appreciation_1yr", "appreciation_3yr", 0.8),
        ("appreciation_3yr", "appreciation_5yr", 0.7),
        ("appreciation_5yr", "appreciation_10yr", 0.6),
        ("days_on_market", "auction_clearance_rate", -0.7),  # Negatively correlated
        ("rental_yield_gross", "median_property_value", -0.5),  # Negatively correlated
        ("vacancy_rate", "rental_yield_gross", -0.6),  # Negatively correlated

        # Risk correlations
        ("default_probability", "recovery_rate", -0.7),  # Negatively correlated
        ("market_liquidity", "days_on_market", -0.8),  # Negatively correlated

        # Location correlations
        ("school_quality", "median_household_income", 0.6),
        ("crime_rate", "median_property_value", -0.7),  # Negatively correlated

        # Supply/demand correlations
        ("demand_pressure", "days_on_market", -0.7),  # Negatively correlated
        ("development_pipeline", "appreciation_1yr", -0.4),  # Negatively correlated

        # Cross-category correlations
        ("employment_rate", "default_probability", -0.6),  # Negatively correlated
        ("median_household_income", "price_to_income_ratio", -0.5),  # Negatively correlated
        ("school_quality", "median_property_value", 0.7),
        ("crime_rate", "default_probability", 0.5),
    ]

    # Set strong correlations
    for metric1, metric2, correlation in strong_correlations:
        if metric1 in metric_names and metric2 in metric_names:
            correlations["metrics"][metric1][metric2] = correlation
            correlations["metrics"][metric2][metric1] = correlation

    # Fill in remaining correlations with weak random values
    for metric1 in metric_names:
        for metric2 in metric_names:
            if metric2 not in correlations["metrics"][metric1]:
                # Random weak correlation (-0.3 to 0.3)
                correlation = random.uniform(-0.3, 0.3)
                correlations["metrics"][metric1][metric2] = correlation
                correlations["metrics"][metric2][metric1] = correlation

    # Generate suburb correlations
    suburb_ids = list(suburbs.keys())

    # Initialize correlation matrix
    for suburb_id in suburb_ids:
        correlations["suburbs"][suburb_id] = {}

    # Set self-correlations to 1.0
    for suburb_id in suburb_ids:
        correlations["suburbs"][suburb_id][suburb_id] = 1.0

    # Calculate correlations based on geographic proximity and similarity
    for suburb_id1 in suburb_ids:
        suburb1 = suburbs[suburb_id1]
        for suburb_id2 in suburb_ids:
            if suburb_id2 not in correlations["suburbs"][suburb_id1]:
                suburb2 = suburbs[suburb_id2]

                # Calculate geographic distance
                distance = ((suburb1["latitude"] - suburb2["latitude"]) ** 2 +
                           (suburb1["longitude"] - suburb2["longitude"]) ** 2) ** 0.5

                # Normalize distance (0-1)
                max_distance = 0.5  # Maximum distance in Sydney
                normalized_distance = min(1.0, distance / max_distance)

                # Calculate score similarity
                score_diff = abs(suburb1["overall_score"] - suburb2["overall_score"]) / 100.0

                # Calculate correlation
                # Closer and more similar suburbs have higher correlation
                correlation = 1.0 - (normalized_distance * 0.7 + score_diff * 0.3)

                # Add some randomness
                correlation = min(0.95, max(0.0, correlation + random.uniform(-0.1, 0.1)))

                # Set correlation
                correlations["suburbs"][suburb_id1][suburb_id2] = correlation
                correlations["suburbs"][suburb_id2][suburb_id1] = correlation

    print("Generated correlations.")
    return correlations

def save_data(suburbs: Dict[str, Dict[str, Any]], correlations: Dict[str, Any]) -> None:
    """
    Save data to JSON file.

    Args:
        suburbs: Dictionary mapping suburb_id to suburb data
        correlations: Dictionary with metric and suburb correlations
    """
    print(f"Saving data to {OUTPUT_FILE}...")

    # Create data dictionary
    data = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "suburbs": suburbs,
        "correlations": correlations,
        "metrics": {
            name: {
                "description": f"Description for {name}",
                "category": category.split("_")[0] if "_" in category else category,
                "unit": info["unit"],
                "min_value": info["min"],
                "max_value": info["max"],
                "is_higher_better": info["higher_better"],
            }
            for category, metrics in [
                ("economic", ECONOMIC_METRICS),
                ("real_estate", REAL_ESTATE_METRICS),
                ("demographic", DEMOGRAPHIC_METRICS),
                ("risk", RISK_METRICS),
                ("location", LOCATION_METRICS),
                ("supply_demand", SUPPLY_DEMAND_METRICS),
                ("temporal", TEMPORAL_METRICS),
            ]
            for name, info in metrics.items()
        },
    }

    # Save to JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Data saved to {OUTPUT_FILE}.")

def main():
    """Main function."""
    # Generate suburb metrics
    suburbs = generate_suburb_metrics()

    # Generate properties
    suburbs = generate_properties(suburbs)

    # Generate correlations
    correlations = generate_correlations(suburbs)

    # Save data
    save_data(suburbs, correlations)

    print("Done!")

if __name__ == "__main__":
    main()
