#!/bin/bash

# Script to copy the TypeScript SDK from the sdk-output directory to the frontend

# Set paths
SDK_SOURCE="../sdk-output/typescript/src"
SDK_DEST="./src/api/sdk"

# Create destination directory if it doesn't exist
mkdir -p "$SDK_DEST"

# Copy SDK files
echo "Copying SDK files from $SDK_SOURCE to $SDK_DEST..."
cp -r "$SDK_SOURCE"/* "$SDK_DEST"/

echo "SDK copied successfully!"
