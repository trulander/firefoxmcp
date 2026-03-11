FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install curl for wait-for-it.sh
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy configuration files and install dependencies
COPY tests/pyproject.toml tests/uv.lock ./
RUN uv sync

# Copy test scripts and helper
COPY tests/test_integration.py tests/
COPY tests/wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# Run tests after waiting for foxmcp server on port 3000
ENTRYPOINT ["./wait-for-it.sh", "foxmcp", "3000", "uv", "run", "pytest", "tests/test_integration.py", "-s"]
