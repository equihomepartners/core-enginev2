"""
OpenAPI specification generator for the EQU IHOME SIM ENGINE v2.

This module generates an OpenAPI specification from the FastAPI app.
It also provides utilities for generating client SDKs from the OpenAPI specification.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

import structlog
import yaml
from fastapi.openapi.utils import get_openapi

try:
    from openapi_spec_validator import validate_spec
    VALIDATE_SPEC = True
except ImportError:
    VALIDATE_SPEC = False
    print("WARNING: openapi_spec_validator not installed. Spec validation will be skipped.")

from src.api.server import app

logger = structlog.get_logger(__name__)


def generate_openapi_spec(
    output_file: Optional[str] = None,
    format: str = "json",
    title: Optional[str] = None,
    version: Optional[str] = None,
    description: Optional[str] = None,
    validate: bool = True,
) -> Dict[str, Any]:
    """
    Generate an OpenAPI specification from the FastAPI app.

    Args:
        output_file: Path to the output file (optional)
        format: Output format (json or yaml)
        title: API title (optional, defaults to app title)
        version: API version (optional, defaults to app version)
        description: API description (optional, defaults to app description)
        validate: Whether to validate the OpenAPI specification (default: True)

    Returns:
        OpenAPI specification as a dictionary

    Raises:
        ValueError: If the OpenAPI specification is invalid
        FileNotFoundError: If the output directory does not exist and cannot be created
        PermissionError: If the output file cannot be written
    """

    # Get OpenAPI specification
    openapi_schema = get_openapi(
        title=title or app.title,
        version=version or app.version,
        description=description or app.description,
        routes=app.routes,
    )

    # Add custom info
    openapi_schema["info"]["contact"] = {
        "name": "EQU IHOME",
        "url": "https://equihome.com",
        "email": "info@equihome.com",
    }

    openapi_schema["info"]["license"] = {
        "name": "Proprietary",
        "url": "https://equihome.com/license",
    }

    # Add server URLs
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Local development server"},
        {"url": "https://api.equihome.com", "description": "Production server"},
    ]

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
        },
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    }

    # Apply security to all operations
    if "security" not in openapi_schema:
        openapi_schema["security"] = [{"apiKey": []}]

    # Validate OpenAPI specification if requested
    if validate and VALIDATE_SPEC:
        try:
            validate_spec(openapi_schema)
            logger.info("OpenAPI specification validated successfully")
        except Exception as e:
            logger.error("OpenAPI specification validation failed", error=str(e))
            raise ValueError(f"OpenAPI specification validation failed: {str(e)}")

    # Write to file if specified
    if output_file:
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if format.lower() == "yaml":
                with open(output_path, "w") as f:
                    yaml.dump(openapi_schema, f, sort_keys=False)
            else:
                with open(output_path, "w") as f:
                    json.dump(openapi_schema, f, indent=2)

            logger.info("Generated OpenAPI specification", output_file=str(output_path))
        except FileNotFoundError as e:
            logger.error("Failed to create output directory", error=str(e))
            raise FileNotFoundError(f"Failed to create output directory: {str(e)}")
        except PermissionError as e:
            logger.error("Failed to write output file", error=str(e))
            raise PermissionError(f"Failed to write output file: {str(e)}")
        except Exception as e:
            logger.error("Failed to write output file", error=str(e))
            raise RuntimeError(f"Failed to write output file: {str(e)}")

    return openapi_schema


def generate_typescript_sdk(
    openapi_file: str,
    output_dir: str,
    package_name: str = "equihome-sim-sdk",
    package_version: str = "0.1.0",
) -> None:
    """
    Generate a TypeScript SDK from an OpenAPI specification.

    Args:
        openapi_file: Path to the OpenAPI specification file
        output_dir: Path to the output directory
        package_name: Package name
        package_version: Package version

    Raises:
        FileNotFoundError: If the OpenAPI specification file does not exist
        RuntimeError: If the OpenAPI generator fails
        PermissionError: If the output directory cannot be created
    """
    # Check if OpenAPI file exists
    if not Path(openapi_file).exists():
        error_msg = f"OpenAPI specification file not found: {openapi_file}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Check if openapi-generator-cli is installed
        try:
            result = subprocess.run(
                ["openapi-generator-cli", "--version"],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise FileNotFoundError("openapi-generator-cli not found")
            logger.info("Using OpenAPI Generator CLI", version=result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("openapi-generator-cli not found, installing via npm")
            npm_result = subprocess.run(
                ["npm", "install", "@openapitools/openapi-generator-cli", "-g"],
                check=False,
                capture_output=True,
                text=True,
            )
            if npm_result.returncode != 0:
                error_msg = f"Failed to install OpenAPI Generator CLI: {npm_result.stderr}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

        # Generate TypeScript SDK
        logger.info("Generating TypeScript SDK",
                   openapi_file=openapi_file,
                   output_dir=output_dir,
                   package_name=package_name,
                   package_version=package_version)

        gen_result = subprocess.run(
            [
                "openapi-generator-cli",
                "generate",
                "-i",
                openapi_file,
                "-g",
                "typescript-fetch",
                "-o",
                output_dir,
                "--additional-properties",
                f"npmName={package_name},npmVersion={package_version},supportsES6=true,withInterfaces=true",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        if gen_result.returncode != 0:
            error_msg = f"Failed to generate TypeScript SDK: {gen_result.stderr}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Validate generated SDK
        if not (Path(output_dir) / "api.ts").exists():
            error_msg = "TypeScript SDK generation failed: api.ts not found"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        logger.info(
            "Generated TypeScript SDK successfully",
            output_dir=output_dir,
            package_name=package_name,
        )
    except FileNotFoundError as e:
        logger.error("File not found", error=str(e))
        raise
    except PermissionError as e:
        logger.error("Permission error", error=str(e))
        raise
    except Exception as e:
        logger.error("Failed to generate TypeScript SDK", error=str(e))
        raise RuntimeError(f"Failed to generate TypeScript SDK: {str(e)}")


def generate_python_sdk(
    openapi_file: str,
    output_dir: str,
    package_name: str = "equihome_sim_sdk",
    package_version: str = "0.1.0",
) -> None:
    """
    Generate a Python SDK from an OpenAPI specification.

    Args:
        openapi_file: Path to the OpenAPI specification file
        output_dir: Path to the output directory
        package_name: Package name
        package_version: Package version

    Raises:
        FileNotFoundError: If the OpenAPI specification file does not exist
        RuntimeError: If the OpenAPI generator fails
        PermissionError: If the output directory cannot be created
    """
    # Check if OpenAPI file exists
    if not Path(openapi_file).exists():
        error_msg = f"OpenAPI specification file not found: {openapi_file}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Check if openapi-generator-cli is installed
        try:
            result = subprocess.run(
                ["openapi-generator-cli", "--version"],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                raise FileNotFoundError("openapi-generator-cli not found")
            logger.info("Using OpenAPI Generator CLI", version=result.stdout.strip())
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("openapi-generator-cli not found, installing via npm")
            npm_result = subprocess.run(
                ["npm", "install", "@openapitools/openapi-generator-cli", "-g"],
                check=False,
                capture_output=True,
                text=True,
            )
            if npm_result.returncode != 0:
                error_msg = f"Failed to install OpenAPI Generator CLI: {npm_result.stderr}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

        # Generate Python SDK
        logger.info("Generating Python SDK",
                   openapi_file=openapi_file,
                   output_dir=output_dir,
                   package_name=package_name,
                   package_version=package_version)

        gen_result = subprocess.run(
            [
                "openapi-generator-cli",
                "generate",
                "-i",
                openapi_file,
                "-g",
                "python",
                "-o",
                output_dir,
                "--additional-properties",
                f"packageName={package_name},packageVersion={package_version}",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        if gen_result.returncode != 0:
            error_msg = f"Failed to generate Python SDK: {gen_result.stderr}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Validate generated SDK
        if not (Path(output_dir) / "setup.py").exists():
            error_msg = "Python SDK generation failed: setup.py not found"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        logger.info(
            "Generated Python SDK successfully",
            output_dir=output_dir,
            package_name=package_name,
        )
    except FileNotFoundError as e:
        logger.error("File not found", error=str(e))
        raise
    except PermissionError as e:
        logger.error("Permission error", error=str(e))
        raise
    except Exception as e:
        logger.error("Failed to generate Python SDK", error=str(e))
        raise RuntimeError(f"Failed to generate Python SDK: {str(e)}")


def generate_all_sdks(
    output_dir: str = "sdk-output",
    openapi_file: Optional[str] = None,
    validate: bool = True,
) -> None:
    """
    Generate all SDKs.

    Args:
        output_dir: Path to the output directory
        openapi_file: Path to the OpenAPI specification file (generated if not provided)
        validate: Whether to validate the OpenAPI specification (default: True)

    Raises:
        ValueError: If the OpenAPI specification is invalid
        FileNotFoundError: If the output directory does not exist and cannot be created
        RuntimeError: If the SDK generation fails
    """
    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate OpenAPI specification if not provided
        if not openapi_file:
            logger.info("Generating OpenAPI specification")
            openapi_file = str(output_path / "openapi.json")
            generate_openapi_spec(output_file=openapi_file, validate=validate)
        elif not Path(openapi_file).exists():
            error_msg = f"OpenAPI specification file not found: {openapi_file}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        # Generate TypeScript SDK
        logger.info("Generating TypeScript SDK")
        typescript_dir = str(output_path / "typescript")
        generate_typescript_sdk(
            openapi_file=openapi_file,
            output_dir=typescript_dir,
        )

        # Generate Python SDK
        logger.info("Generating Python SDK")
        python_dir = str(output_path / "python")
        generate_python_sdk(
            openapi_file=openapi_file,
            output_dir=python_dir,
        )

        # Generate GraphQL schema if available
        try:
            from src.sdk.graphql_schema import save_graphql_schema
            logger.info("Generating GraphQL schema")
            graphql_file = str(output_path / "schema.graphql")
            save_graphql_schema(graphql_file)
        except ImportError:
            logger.warning("GraphQL schema generation skipped: strawberry-graphql not installed")

        logger.info("Generated all SDKs successfully",
                   output_dir=output_dir,
                   openapi_file=openapi_file,
                   typescript_dir=typescript_dir,
                   python_dir=python_dir)
    except Exception as e:
        logger.error("Failed to generate all SDKs", error=str(e))
        raise


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Generate OpenAPI specification and SDKs")
    parser.add_argument(
        "--output-dir",
        default="sdk-output",
        help="Output directory for SDKs",
    )
    parser.add_argument(
        "--openapi-file",
        help="Path to the OpenAPI specification file (generated if not provided)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format for OpenAPI specification",
    )
    parser.add_argument(
        "--typescript",
        action="store_true",
        help="Generate TypeScript SDK",
    )
    parser.add_argument(
        "--python",
        action="store_true",
        help="Generate Python SDK",
    )
    parser.add_argument(
        "--graphql",
        action="store_true",
        help="Generate GraphQL schema",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all SDKs",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        default=True,
        help="Validate OpenAPI specification",
    )
    parser.add_argument(
        "--no-validate",
        action="store_false",
        dest="validate",
        help="Skip OpenAPI specification validation",
    )

    args = parser.parse_args()

    try:
        # Create output directory
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate OpenAPI specification if not provided
        if not args.openapi_file:
            logger.info("Generating OpenAPI specification")
            args.openapi_file = str(output_path / f"openapi.{args.format}")
            generate_openapi_spec(
                output_file=args.openapi_file,
                format=args.format,
                validate=args.validate
            )

        # Generate SDKs
        if args.all:
            logger.info("Generating all SDKs")
            generate_all_sdks(
                output_dir=args.output_dir,
                openapi_file=args.openapi_file,
                validate=args.validate
            )
        else:
            if args.typescript:
                logger.info("Generating TypeScript SDK")
                generate_typescript_sdk(
                    openapi_file=args.openapi_file,
                    output_dir=str(output_path / "typescript"),
                )
            if args.python:
                logger.info("Generating Python SDK")
                generate_python_sdk(
                    openapi_file=args.openapi_file,
                    output_dir=str(output_path / "python"),
                )
            if args.graphql:
                try:
                    from src.sdk.graphql_schema import save_graphql_schema
                    logger.info("Generating GraphQL schema")
                    graphql_file = str(output_path / "schema.graphql")
                    save_graphql_schema(graphql_file)
                except ImportError:
                    logger.error("GraphQL schema generation failed: strawberry-graphql not installed")
                    sys.exit(1)

            # If no specific SDK was requested, generate all
            if not (args.typescript or args.python or args.graphql):
                logger.info("No specific SDK requested, generating all")
                generate_all_sdks(
                    output_dir=args.output_dir,
                    openapi_file=args.openapi_file,
                    validate=args.validate
                )

        logger.info("SDK generation completed successfully")
    except Exception as e:
        logger.error("SDK generation failed", error=str(e))
        sys.exit(1)
