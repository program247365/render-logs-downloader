#!/bin/bash

# Run ripgrep and capture output
output=$(rg -c "/post/2025/May/21/8-bit-spelling-game-built-with-claude/" 202505*.txt)

# Print the output (optional, can be commented out)
echo "$output"

# Sum the numbers after the colon
total=$(echo "$output" | awk -F: '{sum += $2} END {print sum}')

echo "Total: $total"
