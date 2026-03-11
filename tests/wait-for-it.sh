#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
port="$2"
shift 2

echo "Waiting for $host:$port (MCP server responding with jsonrpc)..."

until curl -s "http://$host:$port/mcp" | grep -q "jsonrpc"; do
  echo "Still waiting for $host:$port..."
  sleep 2
done

echo "$host:$port is alive - executing: $@"
exec "$@"
