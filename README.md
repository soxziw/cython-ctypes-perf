# Cython vs ctypes Performance Comparison

CS263 Project

## Overview

This project provides a systematic, quantitative comparison of Cython's compile-time Foreign Function Interface (FFI) and Python's runtime ctypes FFI. It investigates how compilation strategy, type binding, and call overhead impact execution efficiency when bridging Python and C across different workload profiles.

By implementing identical algorithms under both frameworks and measuring throughput, latency, and resource utilization, this project aims to identify when static, C-integrated extensions (Cython) outperform dynamic, runtime FFI (ctypes), and to outline practical guidelines for Python developers choosing between the two for performance-critical applications.

## Project Structure

```
cython-ctypes-perf/
├── src/
│   ├── benchmark_lib.c         # C library implementations
│   ├── benchmark_lib.h         # C library headers
│   ├── cython_wrapper.pxd      # Cython declarations
│   ├── cython_wrapper.pyx      # Cython wrapper implementations
│   └── ctypes_wrapper.py       # ctypes wrapper implementations
├── benchmarks/
│   ├── benchmark_runner.py     # Main benchmark suite
│   └── analyze_results.py      # Results analysis and visualization
├── tests/
│   └── test_correctness.py     # Unit tests for correctness
├── setup.py                    # Cython build configuration
├── Makefile                    # Build automation
├── requirements.txt            # Python dependencies
├── build.sh                    # Build script
├── run_all.sh                  # Complete workflow script
└── README.md                   # This file
```

## Test Cases and Workload Profiles

The benchmark suite includes **10 categories** with **40+ test cases** covering diverse workload profiles:

### 1. Function Call Overhead
- **Minimal function calls** (`noop`) - Pure FFI overhead measurement
- **Simple arithmetic** (`add_numbers`) - Basic operations with multiple parameters
- **Mixed parameter types** (`calculate_simple`) - Integer and float marshalling

### 2. Compute-Intensive Workloads
- **Recursive algorithms** (`fibonacci_recursive`) - Call stack overhead
- **Iterative algorithms** (`fibonacci_iterative`) - Loop performance
- **Prime number checking** (`is_prime`, `count_primes`) - CPU-bound computation
- **Matrix multiplication** - Dense linear algebra operations
- **Transcendental math** (`compute_math_intensive`) - sin, cos, sqrt operations

### 3. Memory-Intensive Workloads
- **Array sum** - Sequential memory reads (tested at multiple sizes: 1K, 10K, 100K elements)
- **Array scaling** - In-place modifications
- **Array copy** - Memory copy operations
- **Dot product** - Read-read operations
- **Array reversal** - Complex access patterns
- **Strided access** - Non-contiguous memory access (stride 1, 10, 100)

### 4. Data Marshalling
- **String operations** - Length calculation and concatenation
- **Struct processing** - Single struct operations
- **Struct arrays** - Array of structures (100 elements)
- Tests various data type conversions between Python and C

### 5. Mixed Workloads
- **Monte Carlo simulation** (`monte_carlo_pi`) - Compute + random access
- **Image blur** - 2D array processing with kernel operations
- **Quicksort** - Mixed compute and memory access

### 6. Memory Allocation Tests
- **C-side allocation** - Allocate, process, and free in C
- Tests overhead of memory management across FFI boundary

### 7. Callback Simulation
- **Repeated operations** - Simulates callback-like behavior
- Measures FFI round-trip overhead

### 8. Buffer Processing
- **Byte buffer manipulation** - Raw buffer operations
- **Checksum calculation** - Byte-level processing

### 9. Pointer-Intensive Operations
- **Linked list** - Create, traverse, and free
- Tests pointer-heavy data structures

### 10. Bitwise Operations
- **Popcount** - Bit counting operations
- **Bitwise reduction** - XOR reduction over arrays

## Installation

### Prerequisites

- Python 3.7+
- GCC or compatible C compiler
- Make

### Quick Start

1. **Clone the repository:**
   ```bash
   cd /root/cython-ctypes-perf
   ```

2. **Install dependencies and build:**
   ```bash
   ./build.sh
   ```

   Or manually:
   ```bash
   pip install -r requirements.txt
   make all
   ```

### Manual Build Steps

If you prefer to build components separately:

```bash
# Build C shared library for ctypes
make ctypes

# Build Cython extension
make cython

# Build both
make all
```

## Usage

### Running Tests

Verify correctness of both implementations:

```bash
make test
```

This runs the unit test suite (`tests/test_correctness.py`) which ensures that Cython and ctypes wrappers produce identical results for all test cases.

### Running Benchmarks

Execute the complete benchmark suite:

```bash
make benchmark
```

This runs `benchmarks/benchmark_runner.py`, which:
- Performs 1000 iterations per benchmark (with 50 warmup iterations)
- Measures execution time with high precision (`time.perf_counter`)
- Collects statistics (mean, median, std, min, max, throughput)
- Tracks memory usage for selected tests
- Saves results to `benchmark_results.json`

**Note:** The benchmark suite may take 5-15 minutes to complete depending on your hardware.

### Analyzing Results

Generate visualizations and analysis report:

```bash
make analyze
```

This runs `benchmarks/analyze_results.py`, which:
- Loads benchmark results from JSON
- Generates comparison plots:
  - `speedup_by_category.png` - Speedup comparison across all benchmarks
  - `absolute_performance.png` - Absolute execution times
  - `category_summary.png` - Average speedup by category
- Creates `benchmark_report.md` with detailed analysis

### Complete Workflow

Run everything (build, test, benchmark, analyze):

```bash
./run_all.sh
```

## Benchmark Metrics

The benchmark suite measures:

1. **Execution Time**
   - Mean, median, standard deviation
   - Minimum and maximum times
   - Computed over 1000 iterations after warmup

2. **Throughput**
   - Operations per second
   - Calculated as `1 / mean_time`

3. **Speedup**
   - Ratio: `ctypes_time / cython_time`
   - Values > 1.0 indicate Cython is faster
   - Values < 1.0 indicate ctypes is faster

4. **Memory Usage** (selected tests)
   - Peak memory allocation
   - RSS (Resident Set Size) delta
   - Python-level memory tracking

## Expected Results

Based on typical FFI characteristics, you can expect:

### Areas Where Cython Excels (>1.5x speedup)
- **Function call overhead** - Cython has minimal call overhead
- **Compute-intensive loops** - Optimized C integration
- **Small, frequent operations** - Reduced marshalling overhead

### Areas With Similar Performance (0.8x - 1.2x)
- **Large array operations** - Memory bandwidth limited
- **I/O bound operations** - Dominated by external factors
- **Single large computations** - One-time FFI cost amortized

### Key Insights
- **Call frequency matters**: More calls = bigger Cython advantage
- **Data transfer matters**: Large data transfers reduce FFI impact
- **Complexity matters**: Simple wrappers show bigger differences

## Development

### Adding New Benchmarks

1. **Add C function** to `src/benchmark_lib.c` and `src/benchmark_lib.h`
2. **Add Cython wrapper** to `src/cython_wrapper.pyx` and declarations to `src/cython_wrapper.pxd`
3. **Add ctypes wrapper** to `src/ctypes_wrapper.py`
4. **Add test case** to `tests/test_correctness.py`
5. **Add benchmark** to `benchmarks/benchmark_runner.py`
6. **Rebuild**: `make clean && make all`

### Project Guidelines

- **Identical implementations**: C code must be identical for both FFI approaches
- **Fair comparison**: Same optimization levels, same data
- **Statistical rigor**: Multiple iterations, warmup phase, outlier handling
- **Reproducibility**: Documented setup, fixed random seeds where applicable

## Technical Details

### Compilation Flags

**C Library:**
- `-O3`: Maximum optimization
- `-march=native`: CPU-specific optimizations
- `-fPIC`: Position-independent code for shared library

**Cython:**
- `boundscheck=False`: Disable array bounds checking (match C behavior)
- `wraparound=False`: Disable negative indexing
- `cdivision=True`: Use C division semantics
- `language_level=3`: Python 3 syntax

### Memory Layout

- **NumPy arrays**: C-contiguous memory layout (`mode="c"`)
- **Struct alignment**: Natural alignment, matching C ABI
- **String encoding**: UTF-8 for all string operations

## Troubleshooting

### Build Issues

**Problem:** "gcc: command not found"
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install
```

**Problem:** "Python.h: No such file or directory"
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev

# macOS (usually included with Python)
```

**Problem:** Cython import error
```bash
pip install --upgrade Cython
make clean && make cython
```

### Runtime Issues

**Problem:** "libbenchmark.so: cannot open shared object file"
```bash
# Ensure the library is built
make ctypes

# Check if library exists
ls -l src/libbenchmark.so
ls -l build/libbenchmark.so
```

**Problem:** Results seem unrealistic
- Ensure no other heavy processes are running
- Disable CPU frequency scaling for consistent results
- Run benchmarks multiple times and compare

## Results Output

After running benchmarks and analysis, you'll find:

- **`benchmark_results.json`**: Raw benchmark data in JSON format
- **`benchmark_report.md`**: Detailed markdown report with tables and statistics
- **`speedup_by_category.png`**: Visual comparison of all benchmarks
- **`absolute_performance.png`**: Side-by-side execution time comparison
- **`category_summary.png`**: Category-level summary statistics

## Clean Up

Remove all build artifacts and results:

```bash
make clean
```

## References

- [Cython Documentation](https://cython.readthedocs.io/)
- [Python ctypes Documentation](https://docs.python.org/3/library/ctypes.html)
- [NumPy C API](https://numpy.org/doc/stable/reference/c-api/)

## License

This project is created for educational purposes as part of CS263.

## Authors

CS263 Project Team

## Acknowledgments

- Inspired by real-world FFI performance challenges in scientific computing
- Benchmark methodology based on industry best practices for microbenchmarking
