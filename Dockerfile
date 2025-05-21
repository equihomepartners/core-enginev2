FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.5.1

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure poetry to not use a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV SIM_FEATURES=ENABLE_PROMETHEUS

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "src.api.server"]
