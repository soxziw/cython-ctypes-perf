"""
Comprehensive benchmark runner for Cython vs ctypes performance comparison
"""

import time
import numpy as np
import gc
import sys
import os
import json
from collections import defaultdict
import tracemalloc
import psutil

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))  # For ctypes_wrapper
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # For cython_wrapper (built in root)

# Import wrappers
try:
    import cython_wrapper as cy
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    print("Warning: Cython wrapper not available")

try:
    import ctypes_wrapper as ct
    CTYPES_AVAILABLE = True
except ImportError:
    CTYPES_AVAILABLE = False
    print("Warning: ctypes wrapper not available")


class BenchmarkResult:
    """Store benchmark results"""
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.cython_times = []
        self.ctypes_times = []
        self.cython_memory = None
        self.ctypes_memory = None
        self.params = {}
        
    def add_timing(self, framework, elapsed_time):
        if framework == 'cython':
            self.cython_times.append(elapsed_time)
        else:
            self.ctypes_times.append(elapsed_time)
    
    def get_stats(self, framework):
        times = self.cython_times if framework == 'cython' else self.ctypes_times
        if not times:
            return None
        return {
            'mean': np.mean(times),
            'median': np.median(times),
            'std': np.std(times),
            'min': np.min(times),
            'max': np.max(times),
            'throughput': 1.0 / np.mean(times) if np.mean(times) > 0 else 0
        }
    
    def to_dict(self):
        result = {
            'name': self.name,
            'category': self.category,
            'params': self.params,
            'cython': self.get_stats('cython'),
            'ctypes': self.get_stats('ctypes'),
        }
        
        if self.cython_memory:
            result['cython_memory'] = self.cython_memory
        if self.ctypes_memory:
            result['ctypes_memory'] = self.ctypes_memory
            
        # Calculate speedup
        if result['cython'] and result['ctypes']:
            result['speedup'] = result['ctypes']['mean'] / result['cython']['mean']
        
        return result


class BenchmarkRunner:
    """Run benchmarks and collect results"""
    
    def __init__(self, iterations=100, warmup=10):
        self.iterations = iterations
        self.warmup = warmup
        self.results = []
        
    def run_benchmark(self, name, category, cython_func, ctypes_func, *args, **kwargs):
        """Run a single benchmark"""
        print(f"Running {name}...", end=' ', flush=True)
        
        result = BenchmarkResult(name, category)
        result.params = kwargs.get('params', {})
        
        # Force garbage collection
        gc.collect()
        
        # Warmup phase
        if CYTHON_AVAILABLE:
            for _ in range(self.warmup):
                try:
                    cython_func(*args)
                except Exception as e:
                    print(f"Cython warmup error: {e}")
        
        if CTYPES_AVAILABLE:
            for _ in range(self.warmup):
                try:
                    ctypes_func(*args)
                except Exception as e:
                    print(f"ctypes warmup error: {e}")
        
        # Benchmark Cython
        if CYTHON_AVAILABLE:
            gc.collect()
            for _ in range(self.iterations):
                start = time.perf_counter()
                try:
                    cython_func(*args)
                except Exception as e:
                    print(f"Cython error: {e}")
                    break
                elapsed = time.perf_counter() - start
                result.add_timing('cython', elapsed)
        
        # Benchmark ctypes
        if CTYPES_AVAILABLE:
            gc.collect()
            for _ in range(self.iterations):
                start = time.perf_counter()
                try:
                    ctypes_func(*args)
                except Exception as e:
                    print(f"ctypes error: {e}")
                    break
                elapsed = time.perf_counter() - start
                result.add_timing('ctypes', elapsed)
        
        self.results.append(result)
        
        # Print quick summary
        cy_stats = result.get_stats('cython')
        ct_stats = result.get_stats('ctypes')
        if cy_stats and ct_stats:
            speedup = ct_stats['mean'] / cy_stats['mean']
            print(f"Speedup: {speedup:.2f}x")
        else:
            print("Done")
        
        return result
    
    def run_memory_benchmark(self, name, category, cython_func, ctypes_func, *args):
        """Run benchmark with memory tracking"""
        print(f"Running {name} (with memory tracking)...", end=' ', flush=True)
        
        result = BenchmarkResult(name, category)
        
        # Benchmark Cython with memory tracking
        if CYTHON_AVAILABLE:
            gc.collect()
            tracemalloc.start()
            process = psutil.Process()
            mem_before = process.memory_info().rss
            
            try:
                cython_func(*args)
            except Exception as e:
                print(f"Cython error: {e}")
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss
            
            result.cython_memory = {
                'current': current,
                'peak': peak,
                'rss_delta': mem_after - mem_before
            }
        
        # Benchmark ctypes with memory tracking
        if CTYPES_AVAILABLE:
            gc.collect()
            tracemalloc.start()
            process = psutil.Process()
            mem_before = process.memory_info().rss
            
            try:
                ctypes_func(*args)
            except Exception as e:
                print(f"ctypes error: {e}")
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss
            
            result.ctypes_memory = {
                'current': current,
                'peak': peak,
                'rss_delta': mem_after - mem_before
            }
        
        self.results.append(result)
        print("Done")
        return result
    
    def save_results(self, filename):
        """Save results to JSON file"""
        output = {
            'metadata': {
                'iterations': self.iterations,
                'warmup': self.warmup,
                'cython_available': CYTHON_AVAILABLE,
                'ctypes_available': CTYPES_AVAILABLE,
                'python_version': sys.version,
                'numpy_version': np.__version__
            },
            'results': [r.to_dict() for r in self.results]
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to {filename}")
    
    def print_summary(self):
        """Print summary of results"""
        print("\n" + "="*80)
        print("BENCHMARK SUMMARY")
        print("="*80)
        
        # Group by category
        by_category = defaultdict(list)
        for result in self.results:
            by_category[result.category].append(result)
        
        for category, results in sorted(by_category.items()):
            print(f"\n{category}:")
            print("-" * 80)
            print(f"{'Benchmark':<40} {'Cython (ms)':<15} {'ctypes (ms)':<15} {'Speedup':<10}")
            print("-" * 80)
            
            for result in results:
                cy_stats = result.get_stats('cython')
                ct_stats = result.get_stats('ctypes')
                
                if cy_stats and ct_stats:
                    cy_mean = cy_stats['mean'] * 1000
                    ct_mean = ct_stats['mean'] * 1000
                    speedup = ct_stats['mean'] / cy_stats['mean']
                    print(f"{result.name:<40} {cy_mean:<15.4f} {ct_mean:<15.4f} {speedup:<10.2f}x")
                elif cy_stats:
                    cy_mean = cy_stats['mean'] * 1000
                    print(f"{result.name:<40} {cy_mean:<15.4f} {'N/A':<15} {'N/A':<10}")
                elif ct_stats:
                    ct_mean = ct_stats['mean'] * 1000
                    print(f"{result.name:<40} {'N/A':<15} {ct_mean:<15.4f} {'N/A':<10}")
        
        print("\n" + "="*80)


def run_all_benchmarks():
    """Run all benchmarks"""
    runner = BenchmarkRunner(iterations=1000, warmup=50)
    
    print("Starting comprehensive Cython vs ctypes benchmark suite")
    print(f"Iterations: {runner.iterations}, Warmup: {runner.warmup}\n")
    
    # ========================================================================
    # 1. FUNCTION CALL OVERHEAD
    # ========================================================================
    print("\n" + "="*80)
    print("1. FUNCTION CALL OVERHEAD")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "noop(42)",
            "Function Call Overhead",
            cy.cy_noop, ct.ct_noop, 42
        )
        
        runner.run_benchmark(
            "add_numbers(100, 200)",
            "Function Call Overhead",
            cy.cy_add_numbers, ct.ct_add_numbers, 100, 200
        )
        
        runner.run_benchmark(
            "calculate_simple(1, 2.5, 3, 4.5)",
            "Function Call Overhead",
            cy.cy_calculate_simple, ct.ct_calculate_simple, 1, 2.5, 3, 4.5
        )
    
    # ========================================================================
    # 2. COMPUTE-INTENSIVE WORKLOADS
    # ========================================================================
    print("\n" + "="*80)
    print("2. COMPUTE-INTENSIVE WORKLOADS")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "fibonacci_recursive(20)",
            "Compute-Intensive",
            cy.cy_fibonacci_recursive, ct.ct_fibonacci_recursive, 20,
            params={'n': 20}
        )
        
        runner.run_benchmark(
            "fibonacci_iterative(1000)",
            "Compute-Intensive",
            cy.cy_fibonacci_iterative, ct.ct_fibonacci_iterative, 1000,
            params={'n': 1000}
        )
        
        runner.run_benchmark(
            "is_prime(1000003)",
            "Compute-Intensive",
            cy.cy_is_prime, ct.ct_is_prime, 1000003,
            params={'n': 1000003}
        )
        
        runner.run_benchmark(
            "count_primes(1, 10000)",
            "Compute-Intensive",
            cy.cy_count_primes, ct.ct_count_primes, 1, 10000,
            params={'range': [1, 10000]}
        )
        
        # Matrix multiplication
        size = 50
        A = np.random.rand(size, size)
        B = np.random.rand(size, size)
        runner.run_benchmark(
            f"matrix_multiply({size}x{size})",
            "Compute-Intensive",
            cy.cy_matrix_multiply, ct.ct_matrix_multiply, A.copy(), B.copy(),
            params={'size': size}
        )
        
        runner.run_benchmark(
            "compute_math_intensive(1.5, 10000)",
            "Compute-Intensive",
            cy.cy_compute_math_intensive, ct.ct_compute_math_intensive, 1.5, 10000,
            params={'iterations': 10000}
        )
    
    # ========================================================================
    # 3. MEMORY-INTENSIVE WORKLOADS
    # ========================================================================
    print("\n" + "="*80)
    print("3. MEMORY-INTENSIVE WORKLOADS")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        # Test different array sizes
        for size in [1000, 10000, 100000]:
            arr = np.random.rand(size)
            runner.run_benchmark(
                f"sum_array(size={size})",
                "Memory-Intensive",
                cy.cy_sum_array, ct.ct_sum_array, arr.copy(),
                params={'size': size}
            )
        
        arr = np.random.rand(100000)
        runner.run_benchmark(
            "scale_array(size=100000)",
            "Memory-Intensive",
            cy.cy_scale_array, ct.ct_scale_array, arr.copy(), 2.5
        )
        
        runner.run_benchmark(
            "copy_array(size=100000)",
            "Memory-Intensive",
            cy.cy_copy_array, ct.ct_copy_array, arr.copy()
        )
        
        a = np.random.rand(100000)
        b = np.random.rand(100000)
        runner.run_benchmark(
            "dot_product(size=100000)",
            "Memory-Intensive",
            cy.cy_dot_product, ct.ct_dot_product, a.copy(), b.copy()
        )
        
        runner.run_benchmark(
            "array_reverse(size=100000)",
            "Memory-Intensive",
            cy.cy_array_reverse, ct.ct_array_reverse, arr.copy()
        )
        
        for stride in [1, 10, 100]:
            runner.run_benchmark(
                f"sum_strided(stride={stride})",
                "Memory-Intensive",
                cy.cy_sum_strided, ct.ct_sum_strided, arr.copy(), stride,
                params={'stride': stride}
            )
    
    # ========================================================================
    # 4. DATA MARSHALLING
    # ========================================================================
    print("\n" + "="*80)
    print("4. DATA MARSHALLING")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        # String operations
        test_string = "Hello, World! " * 10
        runner.run_benchmark(
            "string_length(150 chars)",
            "Data Marshalling",
            cy.cy_string_length, ct.ct_string_length, test_string,
            params={'length': len(test_string)}
        )
        
        s1 = "Hello" * 20
        s2 = "World" * 20
        runner.run_benchmark(
            "string_concat(100+100 chars)",
            "Data Marshalling",
            cy.cy_string_concat, ct.ct_string_concat, s1, s2,
            params={'length': len(s1) + len(s2)}
        )
        
        # Struct operations
        runner.run_benchmark(
            "process_datapoint",
            "Data Marshalling",
            cy.cy_process_datapoint, ct.ct_process_datapoint, 42, 3.14, "test"
        )
        
        points = [(i, float(i), f"point_{i}") for i in range(100)]
        runner.run_benchmark(
            "sum_datapoints(100 structs)",
            "Data Marshalling",
            cy.cy_sum_datapoints, ct.ct_sum_datapoints, points,
            params={'count': 100}
        )
    
    # ========================================================================
    # 5. MIXED WORKLOADS
    # ========================================================================
    print("\n" + "="*80)
    print("5. MIXED WORKLOADS")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "monte_carlo_pi(100000)",
            "Mixed Workload",
            cy.cy_monte_carlo_pi, ct.ct_monte_carlo_pi, 100000,
            params={'iterations': 100000}
        )
        
        img = np.random.rand(100, 100)
        runner.run_benchmark(
            "blur_array(100x100)",
            "Mixed Workload",
            cy.cy_blur_array, ct.ct_blur_array, img.copy(),
            params={'size': [100, 100]}
        )
        
        arr = np.random.rand(10000)
        runner.run_benchmark(
            "sort_array(10000)",
            "Mixed Workload",
            cy.cy_sort_array, ct.ct_sort_array, arr.copy(),
            params={'size': 10000}
        )
    
    # ========================================================================
    # 6. MEMORY ALLOCATION
    # ========================================================================
    print("\n" + "="*80)
    print("6. MEMORY ALLOCATION")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "allocate_and_sum(100000)",
            "Memory Allocation",
            cy.cy_allocate_and_sum, ct.ct_allocate_and_sum, 100000,
            params={'size': 100000}
        )
    
    # ========================================================================
    # 7. CALLBACK SIMULATION
    # ========================================================================
    print("\n" + "="*80)
    print("7. CALLBACK SIMULATION")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "apply_operation(1.0, 10000)",
            "Callback Simulation",
            cy.cy_apply_operation, ct.ct_apply_operation, 1.0, 10000,
            params={'iterations': 10000}
        )
    
    # ========================================================================
    # 8. BUFFER PROCESSING
    # ========================================================================
    print("\n" + "="*80)
    print("8. BUFFER PROCESSING")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        buffer = np.random.randint(0, 256, 100000, dtype=np.uint8)
        runner.run_benchmark(
            "process_buffer(100000)",
            "Buffer Processing",
            cy.cy_process_buffer, ct.ct_process_buffer, buffer.copy(),
            params={'size': 100000}
        )
        
        runner.run_benchmark(
            "checksum(100000)",
            "Buffer Processing",
            cy.cy_checksum, ct.ct_checksum, buffer.copy()
        )
    
    # ========================================================================
    # 9. POINTER-INTENSIVE OPERATIONS
    # ========================================================================
    print("\n" + "="*80)
    print("9. POINTER-INTENSIVE OPERATIONS")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "list_operations(1000)",
            "Pointer-Intensive",
            cy.cy_list_operations, ct.ct_list_operations, 1000,
            params={'size': 1000}
        )
    
    # ========================================================================
    # 10. BITWISE OPERATIONS
    # ========================================================================
    print("\n" + "="*80)
    print("10. BITWISE OPERATIONS")
    print("="*80)
    
    if CYTHON_AVAILABLE and CTYPES_AVAILABLE:
        runner.run_benchmark(
            "popcount(0xFFFFFFFF)",
            "Bitwise Operations",
            cy.cy_popcount, ct.ct_popcount, 0xFFFFFFFF
        )
        
        arr = np.random.randint(0, 2**32, 10000, dtype=np.uint32)
        runner.run_benchmark(
            "bitwise_reduce(10000)",
            "Bitwise Operations",
            cy.cy_bitwise_reduce, ct.ct_bitwise_reduce, arr.copy(),
            params={'size': 10000}
        )
    
    # Print and save results
    runner.print_summary()
    runner.save_results('benchmark_results.json')
    
    return runner


if __name__ == '__main__':
    run_all_benchmarks()

