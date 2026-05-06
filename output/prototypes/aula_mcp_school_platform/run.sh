#!/usr/bin/env bash
# Aula MCP Demo — runs with mock data, no credentials needed
set -e

cd "$(dirname "$0")"

echo "Running Aula MCP demo server (mock data)..."
echo

node demo_server.js
