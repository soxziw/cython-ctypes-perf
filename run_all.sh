#!/bin/bash
# Complete workflow: build, test, benchmark, and analyze

set -e

echo "=================================================="
echo "Complete Cython vs ctypes Performance Analysis"
echo "=================================================="

# Build
echo ""
echo "Building..."
./build.sh

# Test
echo ""
echo "Running correctness tests..."
make test

# Benchmark
echo ""
echo "Running performance benchmarks..."
echo "This may take several minutes..."
make benchmark

# Analyze
echo ""
echo "Analyzing results..."
cd benchmarks
python analyze_results.py
cd ..

echo ""
echo "=================================================="
echo "Analysis complete!"
echo "=================================================="
echo ""
echo "Results saved to:"
echo "  - benchmarks/benchmark_results.json"
echo "  - benchmarks/benchmark_report.md"
echo "  - benchmarks/*.png (visualization plots)"
echo ""

