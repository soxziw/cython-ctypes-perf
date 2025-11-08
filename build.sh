#!/bin/bash
# Build script for Cython-ctypes performance comparison

set -e

echo "=================================================="
echo "Building Cython vs ctypes Performance Benchmarks"
echo "=================================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Error: Python not found"
    exit 1
fi

echo ""
echo "Step 1: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Building C shared library for ctypes..."
make ctypes

echo ""
echo "Step 3: Building Cython extension..."
make cython

echo ""
echo "=================================================="
echo "Build completed successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  - Run tests:      make test"
echo "  - Run benchmarks: make benchmark"
echo "  - Analyze results: make analyze"
echo ""

