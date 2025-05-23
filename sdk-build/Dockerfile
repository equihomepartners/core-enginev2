# Lightweight builder
FROM python:3.11-slim

# Install only what the generator needs
RUN apt-get update && apt-get install -y git nodejs npm && rm -rf /var/lib/apt/lists/*

# Install OpenAPI Generator CLI
RUN npm install -g @openapitools/openapi-generator-cli@latest

# Poetry for dependency management
RUN pip install --no-cache-dir poetry==1.8.2

# Copy only pyproject & generator code for layer caching
WORKDIR /workspace
COPY pyproject.toml poetry.lock* ./

# Add SDK extras to pyproject.toml if it doesn't exist
RUN if ! grep -q "\[tool.poetry.extras\]" pyproject.toml; then \
    echo -e "\n[tool.poetry.extras]\nsdk = [\n  \"pyyaml\",\n  \"strawberry-graphql\",\n  \"openapi-spec-validator\"\n]" >> pyproject.toml; \
    fi

# Install dependencies with SDK extras
RUN poetry config virtualenvs.create false \
    && poetry install --only main,sdk --no-interaction --no-root

# Copy rest of the source after deps cached
COPY . .

# Set environment variables
ENV PYTHONPATH=/workspace
ENV OPENAPI_PATH=schemas/openapi.json
ENV OUT_DIR=sdk-output

# Create output directory
RUN mkdir -p ${OUT_DIR}

# Entrypoint: run generator script
ENTRYPOINT ["python", "-m", "src.sdk.openapi_gen"]
