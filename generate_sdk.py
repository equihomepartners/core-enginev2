#!/usr/bin/env python3
"""
Generate SDK script for the EQU IHOME SIM ENGINE v2.

This script generates OpenAPI specifications and SDKs for the EQU IHOME SIM ENGINE v2 API.
"""

import os
import argparse
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)

def generate_openapi():
    """Generate OpenAPI specification."""
    from src.sdk.openapi_gen import generate_openapi_spec

    # Create schemas directory if it doesn't exist
    os.makedirs("schemas", exist_ok=True)

    # Generate OpenAPI specification
    openapi_file = "schemas/openapi.json"
    generate_openapi_spec(output_file=openapi_file)

    logger.info("OpenAPI specification generated", output_file=openapi_file)
    return openapi_file

def generate_graphql():
    """Generate GraphQL schema."""
    from src.sdk.graphql_schema import save_graphql_schema

    # Create schemas directory if it doesn't exist
    os.makedirs("schemas", exist_ok=True)

    # Generate GraphQL schema
    graphql_file = "schemas/schema.graphql"
    save_graphql_schema(graphql_file)

    logger.info("GraphQL schema generated", output_file=graphql_file)
    return graphql_file

def generate_typescript_sdk(openapi_file):
    """Generate TypeScript SDK."""
    from src.sdk.openapi_gen import generate_typescript_sdk

    # Create output directory
    output_dir = "sdk-output/typescript"
    os.makedirs(output_dir, exist_ok=True)

    # Generate TypeScript SDK
    generate_typescript_sdk(
        openapi_file=openapi_file,
        output_dir=output_dir,
        package_name="equihome-sim-sdk",
        package_version="0.1.0",
    )

    logger.info("TypeScript SDK generated", output_dir=output_dir)
    return output_dir

def generate_python_sdk(openapi_file):
    """Generate Python SDK."""
    from src.sdk.openapi_gen import generate_python_sdk

    # Create output directory
    output_dir = "sdk-output/python"
    os.makedirs(output_dir, exist_ok=True)

    # Generate Python SDK
    generate_python_sdk(
        openapi_file=openapi_file,
        output_dir=output_dir,
        package_name="equihome_sim_sdk",
        package_version="0.1.0",
    )

    logger.info("Python SDK generated", output_dir=output_dir)
    return output_dir

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate SDK for the EQU IHOME SIM ENGINE v2")
    parser.add_argument("--openapi", action="store_true", help="Generate OpenAPI specification")
    parser.add_argument("--graphql", action="store_true", help="Generate GraphQL schema")
    parser.add_argument("--typescript", action="store_true", help="Generate TypeScript SDK")
    parser.add_argument("--python", action="store_true", help="Generate Python SDK")
    parser.add_argument("--all", action="store_true", help="Generate all SDKs")

    args = parser.parse_args()

    # Generate OpenAPI specification
    openapi_file = None
    if args.openapi or args.typescript or args.python or args.all:
        openapi_file = generate_openapi()

    # Generate GraphQL schema
    if args.graphql or args.all:
        generate_graphql()

    # Generate TypeScript SDK
    if args.typescript or args.all:
        if openapi_file:
            generate_typescript_sdk(openapi_file)
        else:
            logger.error("Cannot generate TypeScript SDK: OpenAPI specification not generated")

    # Generate Python SDK
    if args.python or args.all:
        if openapi_file:
            generate_python_sdk(openapi_file)
        else:
            logger.error("Cannot generate Python SDK: OpenAPI specification not generated")

    # If no arguments provided, show help
    if not (args.openapi or args.graphql or args.typescript or args.python or args.all):
        parser.print_help()

if __name__ == "__main__":
    main()
