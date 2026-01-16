#!/bin/bash
echo "Benchmarking Python/Glob approach..."
time python3 scripts/generate_sessions_table.py > /dev/null

echo -e "\nBenchmarking JSON approach..."
time python3 scripts/generate_sessions_table_json.py > /dev/null
