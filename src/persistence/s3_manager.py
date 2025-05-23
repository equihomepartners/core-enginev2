"""
S3 manager module for the EQU IHOME SIM ENGINE v2.

This module provides functionality for S3 storage operations.
It supports both AWS S3 and MinIO, with environment-based configuration.
"""

import json
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import aioboto3
import structlog

logger = structlog.get_logger(__name__)

# Check if S3 is enabled
USE_S3 = os.getenv("USE_S3", "false").lower() == "true"

# S3 endpoint (AWS S3 or MinIO)
S3_ENDPOINT = os.getenv("S3_ENDPOINT", None)

# S3 credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")

# S3 bucket
S3_BUCKET = os.getenv("S3_BUCKET", "simulation-results")

# S3 region
S3_REGION = os.getenv("S3_REGION", "us-east-1")

# S3 prefix
S3_PREFIX = os.getenv("S3_PREFIX", "results")


class S3Manager:
    """
    Manager for S3 storage operations.

    This class provides methods for S3 storage operations.
    It supports both AWS S3 and MinIO, with environment-based configuration.
    """

    def __init__(self):
        """Initialize the S3 manager."""
        self.session = aioboto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=S3_REGION,
        )
        self.endpoint_url = S3_ENDPOINT
        self.bucket = S3_BUCKET
        self.prefix = S3_PREFIX
        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the S3 connection and create bucket if it doesn't exist."""
        if self.initialized:
            return

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # Check if bucket exists
                try:
                    await s3_client.head_bucket(Bucket=self.bucket)
                    logger.info("S3 bucket exists", bucket=self.bucket)
                except Exception:
                    # Create bucket
                    await s3_client.create_bucket(Bucket=self.bucket)
                    logger.info("Created S3 bucket", bucket=self.bucket)

            self.initialized = True
            logger.info("S3 initialized", endpoint_url=self.endpoint_url, bucket=self.bucket)
        except Exception as e:
            logger.error("Failed to initialize S3", error=str(e))
            raise

    async def upload_result(self, simulation_id: str, result: Dict[str, Any]) -> None:
        """
        Upload a simulation result to S3.

        Args:
            simulation_id: Simulation ID
            result: Simulation result
        """
        await self.initialize()

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # Create key
                key = f"{self.prefix}/{simulation_id}.json"

                # Convert result to JSON
                result_json = json.dumps(result)

                # Upload to S3
                await s3_client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=result_json,
                    ContentType="application/json",
                )

                logger.info("Uploaded result to S3", simulation_id=simulation_id, key=key)
        except Exception as e:
            logger.error("Failed to upload result to S3", simulation_id=simulation_id, error=str(e))
            raise

    async def download_result(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        """
        Download a simulation result from S3.

        Args:
            simulation_id: Simulation ID

        Returns:
            Simulation result or None if not found
        """
        await self.initialize()

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return None

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # Create key
                key = f"{self.prefix}/{simulation_id}.json"

                try:
                    # Download from S3
                    response = await s3_client.get_object(Bucket=self.bucket, Key=key)
                    result_json = await response["Body"].read()

                    # Parse JSON
                    result = json.loads(result_json)

                    logger.info("Downloaded result from S3", simulation_id=simulation_id, key=key)
                    return result
                except Exception as e:
                    logger.warning("Result not found in S3", simulation_id=simulation_id, key=key, error=str(e))
                    return None
        except Exception as e:
            logger.error("Failed to download result from S3", simulation_id=simulation_id, error=str(e))
            raise

    async def list_results(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List simulation results from S3.

        Args:
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of simulation results
        """
        await self.initialize()

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return []

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # List objects in bucket with prefix
                response = await s3_client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=self.prefix,
                )

                # Check if any objects were found
                if "Contents" not in response:
                    logger.warning("No results found in S3", bucket=self.bucket, prefix=self.prefix)
                    return []

                # Sort objects by last modified (newest first)
                objects = sorted(
                    response["Contents"],
                    key=lambda obj: obj["LastModified"],
                    reverse=True,
                )

                # Apply pagination
                objects = objects[offset:offset + limit]

                # Download results
                results = []
                for obj in objects:
                    key = obj["Key"]
                    simulation_id = Path(key).stem

                    # Download result
                    result = await self.download_result(simulation_id)
                    if result:
                        results.append(result)

                logger.info("Listed results from S3", count=len(results))
                return results
        except Exception as e:
            logger.error("Failed to list results from S3", error=str(e))
            raise

    async def delete_result(self, simulation_id: str) -> bool:
        """
        Delete a simulation result from S3.

        Args:
            simulation_id: Simulation ID

        Returns:
            True if deleted, False otherwise
        """
        await self.initialize()

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return False

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # Create key
                key = f"{self.prefix}/{simulation_id}.json"

                try:
                    # Check if object exists
                    await s3_client.head_object(Bucket=self.bucket, Key=key)
                except Exception:
                    logger.warning("Result not found in S3", simulation_id=simulation_id, key=key)
                    return False

                # Delete from S3
                await s3_client.delete_object(Bucket=self.bucket, Key=key)

                logger.info("Deleted result from S3", simulation_id=simulation_id, key=key)
                return True
        except Exception as e:
            logger.error("Failed to delete result from S3", simulation_id=simulation_id, error=str(e))
            raise

    async def upload_file(self, file_path: Union[str, Path], key: Optional[str] = None) -> str:
        """
        Upload a file to S3.

        Args:
            file_path: Path to the file
            key: S3 key (optional, defaults to file name)

        Returns:
            S3 key
        """
        await self.initialize()

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return ""

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # Convert file path to Path object
                file_path = Path(file_path)

                # Create key if not provided
                if key is None:
                    key = f"{self.prefix}/files/{file_path.name}"

                # Upload to S3
                await s3_client.upload_file(
                    Filename=str(file_path),
                    Bucket=self.bucket,
                    Key=key,
                )

                logger.info("Uploaded file to S3", file_path=str(file_path), key=key)
                return key
        except Exception as e:
            logger.error("Failed to upload file to S3", file_path=str(file_path), error=str(e))
            raise

    async def download_file(self, key: str, file_path: Union[str, Path]) -> None:
        """
        Download a file from S3.

        Args:
            key: S3 key
            file_path: Path to save the file
        """
        await self.initialize()

        if not USE_S3:
            logger.warning("S3 storage is disabled")
            return

        try:
            # Create S3 client
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                # Convert file path to Path object
                file_path = Path(file_path)

                # Create directory if it doesn't exist
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Download from S3
                await s3_client.download_file(
                    Bucket=self.bucket,
                    Key=key,
                    Filename=str(file_path),
                )

                logger.info("Downloaded file from S3", key=key, file_path=str(file_path))
        except Exception as e:
            logger.error("Failed to download file from S3", key=key, error=str(e))
            raise


# Global S3 manager instance
_global_s3_manager: Optional[S3Manager] = None


def get_s3_manager() -> S3Manager:
    """
    Get the global S3 manager instance.

    Returns:
        The global S3 manager instance
    """
    global _global_s3_manager

    if _global_s3_manager is None:
        _global_s3_manager = S3Manager()

    return _global_s3_manager
