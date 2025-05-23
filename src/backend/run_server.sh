#!/bin/bash
# Run the API server for the EQU IHOME SIM ENGINE v2

# Set environment variables
export SIM_ENV=${SIM_ENV:-development}
export SIM_DEBUG=${SIM_DEBUG:-true}
export SIM_RELOAD=${SIM_RELOAD:-true}
export SIM_API_HOST=${SIM_API_HOST:-0.0.0.0}
export SIM_API_PORT=${SIM_API_PORT:-5005}
export SIM_FEATURES=${SIM_FEATURES:-ENABLE_DEBUG_LOGGING}

# Create log directory if it doesn't exist
mkdir -p logs

# Run the server
echo "Starting API server on ${SIM_API_HOST}:${SIM_API_PORT} in ${SIM_ENV} mode"
python3 -m src.api.server
