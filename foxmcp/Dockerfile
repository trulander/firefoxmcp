FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Download the server part from the latest release
RUN curl -L "https://github.com/ThinkerYzu/foxmcp/releases/download/v1.1.0/foxmcp-server.zip" -o /tmp/foxmcp-server.zip \
    && unzip /tmp/foxmcp-server.zip -d /tmp/server-tmp \
    && mv /tmp/server-tmp/server-package/* . \
    && rm -rf /tmp/foxmcp-server.zip /tmp/server-tmp

# Patch server.py to allow 0.0.0.0 in Docker
RUN sed -i "s/args.host = 'localhost'/pass/g" server.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000 8765

# Start the server on 0.0.0.0
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8765", "--mcp-port", "3000"]
