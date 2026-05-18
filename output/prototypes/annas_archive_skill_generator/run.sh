#!/usr/bin/env bash
# Anna's Archive Skill Generator - Demo Pipeline
# Runs the full search → download → extract → generate → audit flow with mock data.
# No API keys or network access required.

set -e
cd "$(dirname "$0")"
node demo.js
