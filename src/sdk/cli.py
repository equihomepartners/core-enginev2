"""
CLI utilities for the SDK generation.

This module provides command-line utilities for generating OpenAPI specifications and SDKs.
"""

import argparse
import os
from pathlib import Path

import structlog

from src.sdk.openapi_gen import (
    generate_openapi_spec,
    generate_typescript_sdk,
    generate_python_sdk,
    generate_all_sdks,
)
from src.sdk.graphql_schema import save_graphql_schema

logger = structlog.get_logger(__name__)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate OpenAPI specifications and SDKs")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # OpenAPI command
    openapi_parser = subparsers.add_parser("openapi", help="Generate OpenAPI specification")
    openapi_parser.add_argument(
        "--output-file",
        default="schemas/openapi.json",
        help="Output file for OpenAPI specification",
    )
    openapi_parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format for OpenAPI specification",
    )

    # GraphQL command
    graphql_parser = subparsers.add_parser("graphql", help="Generate GraphQL schema")
    graphql_parser.add_argument(
        "--output-file",
        default="schemas/schema.graphql",
        help="Output file for GraphQL schema",
    )

    # TypeScript SDK command
    typescript_parser = subparsers.add_parser("typescript", help="Generate TypeScript SDK")
    typescript_parser.add_argument(
        "--openapi-file",
        default="schemas/openapi.json",
        help="Path to the OpenAPI specification file",
    )
    typescript_parser.add_argument(
        "--output-dir",
        default="sdk-output/typescript",
        help="Output directory for TypeScript SDK",
    )
    typescript_parser.add_argument(
        "--package-name",
        default="equihome-sim-sdk",
        help="Package name for TypeScript SDK",
    )
    typescript_parser.add_argument(
        "--package-version",
        default="0.1.0",
        help="Package version for TypeScript SDK",
    )

    # Python SDK command
    python_parser = subparsers.add_parser("python", help="Generate Python SDK")
    python_parser.add_argument(
        "--openapi-file",
        default="schemas/openapi.json",
        help="Path to the OpenAPI specification file",
    )
    python_parser.add_argument(
        "--output-dir",
        default="sdk-output/python",
        help="Output directory for Python SDK",
    )
    python_parser.add_argument(
        "--package-name",
        default="equihome_sim_sdk",
        help="Package name for Python SDK",
    )
    python_parser.add_argument(
        "--package-version",
        default="0.1.0",
        help="Package version for Python SDK",
    )

    # All SDKs command
    all_parser = subparsers.add_parser("all", help="Generate all SDKs")
    all_parser.add_argument(
        "--output-dir",
        default="sdk-output",
        help="Output directory for SDKs",
    )
    all_parser.add_argument(
        "--openapi-file",
        help="Path to the OpenAPI specification file (generated if not provided)",
    )

    args = parser.parse_args()

    if args.command == "openapi":
        # Generate OpenAPI specification
        generate_openapi_spec(
            output_file=args.output_file,
            format=args.format,
        )
    elif args.command == "graphql":
        # Generate GraphQL schema
        save_graphql_schema(args.output_file)
    elif args.command == "typescript":
        # Generate TypeScript SDK
        generate_typescript_sdk(
            openapi_file=args.openapi_file,
            output_dir=args.output_dir,
            package_name=args.package_name,
            package_version=args.package_version,
        )
    elif args.command == "python":
        # Generate Python SDK
        generate_python_sdk(
            openapi_file=args.openapi_file,
            output_dir=args.output_dir,
            package_name=args.package_name,
            package_version=args.package_version,
        )
    elif args.command == "all":
        # Generate all SDKs
        generate_all_sdks(
            output_dir=args.output_dir,
            openapi_file=args.openapi_file,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
