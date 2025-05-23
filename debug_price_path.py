#!/usr/bin/env python3
"""
Debug script to audit the price path configuration issue.
"""

import sys
import os
sys.path.append('/Volumes/OWC Express 1M2/core-simv2')

from src.config.config_loader import load_config_from_dict
from src.engine.simulation_context import SimulationContext

def debug_config_types():
    """Debug the configuration types and structure."""

    # Create a test configuration
    config_dict = {
        "fund_size": 75000000,
        "fund_term": 7,
        "vintage_year": 2025
    }

    print("=== CONFIGURATION DEBUG ===")

    # Load configuration
    config = load_config_from_dict(config_dict)
    print(f"Config type: {type(config)}")
    print(f"Config class: {config.__class__}")

    # Check appreciation_rates
    print(f"\n--- appreciation_rates ---")
    appreciation_rates = getattr(config, "appreciation_rates", None)
    print(f"appreciation_rates type: {type(appreciation_rates)}")
    print(f"appreciation_rates value: {appreciation_rates}")

    if hasattr(appreciation_rates, 'dict'):
        print(f"Has .dict() method: True")
        try:
            dict_result = appreciation_rates.dict()
            print(f"appreciation_rates.dict(): {dict_result}")
            print(f"dict() result type: {type(dict_result)}")
        except Exception as e:
            print(f"Error calling .dict(): {e}")
    else:
        print(f"Has .dict() method: False")

    if hasattr(appreciation_rates, '__dict__'):
        print(f"Has .__dict__: True")
        print(f"appreciation_rates.__dict__: {appreciation_rates.__dict__}")
    else:
        print(f"Has .__dict__: False")

    # Check price_path configuration
    print(f"\n--- price_path ---")
    price_path_config = getattr(config, "price_path", None)
    print(f"price_path_config type: {type(price_path_config)}")
    print(f"price_path_config value: {price_path_config}")

    # Test with fallback to empty dict
    if price_path_config is None:
        price_path_config = {}
        print(f"Using fallback empty dict: {price_path_config}")

    volatility_obj = getattr(price_path_config, "volatility", None)
    print(f"volatility_obj type: {type(volatility_obj)}")
    print(f"volatility_obj value: {volatility_obj}")

    # Test the volatility conversion logic
    print(f"\n--- VOLATILITY CONVERSION TEST ---")
    if volatility_obj is not None:
        if hasattr(volatility_obj, 'dict'):
            volatility = volatility_obj.dict()
        elif hasattr(volatility_obj, '__dict__'):
            volatility = volatility_obj.__dict__
        else:
            volatility = volatility_obj
    else:
        volatility = {
            "green": 0.03,
            "orange": 0.05,
            "red": 0.08
        }

    print(f"Final volatility: {volatility}")
    print(f"Final volatility type: {type(volatility)}")

    # Test .get() method on volatility
    try:
        green_vol = volatility.get("green", 0.05)
        print(f"Green volatility via .get(): {green_vol}")
    except Exception as e:
        print(f"ERROR calling .get() on volatility: {e}")
        print(f"This is the source of the volatility bug!")

    # Test the actual conversion logic
    print(f"\n--- CONVERSION TEST ---")

    # Test appreciation_rates conversion
    if appreciation_rates is not None:
        if hasattr(appreciation_rates, 'dict'):
            converted = appreciation_rates.dict()
        elif hasattr(appreciation_rates, '__dict__'):
            converted = appreciation_rates.__dict__
        else:
            converted = appreciation_rates

        print(f"Converted appreciation_rates: {converted}")
        print(f"Converted type: {type(converted)}")

        # Test .get() method
        try:
            green_rate = converted.get("green", 0.03)
            print(f"Green rate via .get(): {green_rate}")
        except Exception as e:
            print(f"ERROR calling .get() on converted: {e}")
            print(f"This is the source of the bug!")

def debug_simulation_context():
    """Debug how the configuration is stored in simulation context."""

    print("\n=== SIMULATION CONTEXT DEBUG ===")

    config_dict = {
        "fund_size": 75000000,
        "fund_term": 7,
        "vintage_year": 2025
    }

    config = load_config_from_dict(config_dict)
    context = SimulationContext(config=config, run_id="debug-test")

    print(f"Context config type: {type(context.config)}")
    print(f"Context config: {context.config}")

    # Test accessing through context
    appreciation_rates_obj = getattr(context.config, "appreciation_rates", None)
    print(f"From context - appreciation_rates type: {type(appreciation_rates_obj)}")

if __name__ == "__main__":
    debug_config_types()
    debug_simulation_context()
