# Makefile for building C library and Cython extensions

CC = gcc
CFLAGS = -O3 -march=native -fPIC -Wall
LDFLAGS = -shared -lm

# Directories
SRC_DIR = src
BUILD_DIR = build
LIB_DIR = $(BUILD_DIR)

# Files
C_SOURCES = $(SRC_DIR)/benchmark_lib.c
C_OBJECTS = $(BUILD_DIR)/benchmark_lib.o
SHARED_LIB = $(LIB_DIR)/libbenchmark.so

.PHONY: all clean cython ctypes test benchmark help

all: ctypes cython

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Build C library for ctypes
ctypes: $(SHARED_LIB) $(SRC_DIR)/libbenchmark.so

$(BUILD_DIR)/benchmark_lib.o: $(C_SOURCES) | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(SHARED_LIB): $(C_OBJECTS)
	$(CC) $(LDFLAGS) $^ -o $@

$(SRC_DIR)/libbenchmark.so: $(SHARED_LIB)
	cp $(SHARED_LIB) $(SRC_DIR)/libbenchmark.so

# Build Cython extension
cython:
	python setup.py build_ext --inplace

# Run correctness tests
test: all
	python -m pytest tests/ -v

# Run benchmarks
benchmark: all
	cd benchmarks && python benchmark_runner.py

# Run analysis
analyze:
	cd benchmarks && python analyze_results.py

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)
	rm -f $(SRC_DIR)/*.so
	rm -f $(SRC_DIR)/*.c.o
	rm -f cython_wrapper*.so
	rm -f cython_wrapper.c
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf benchmarks/__pycache__
	rm -rf .pytest_cache
	rm -f benchmark_results.json
	rm -f *.png
	rm -f benchmark_report.md

# Help
help:
	@echo "Available targets:"
	@echo "  all        - Build both ctypes and Cython libraries (default)"
	@echo "  ctypes     - Build C shared library for ctypes"
	@echo "  cython     - Build Cython extension"
	@echo "  test       - Run correctness tests"
	@echo "  benchmark  - Run performance benchmarks"
	@echo "  analyze    - Analyze benchmark results"
	@echo "  clean      - Remove all build artifacts"
	@echo "  help       - Show this help message"

