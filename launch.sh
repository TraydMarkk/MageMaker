#!/bin/bash
# MageMaker Launch Script
# Author: TraydMarkk

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH"
    exit 1
fi

# Launch MageMaker
python3 -m magemaker.gui "$@"


