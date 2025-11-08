"""
ctypes wrapper for benchmark_lib
"""

import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import os

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), 'libbenchmark.so')
if not os.path.exists(lib_path):
    # Try alternative locations
    lib_path = os.path.join(os.path.dirname(__file__), '..', 'build', 'libbenchmark.so')
    if not os.path.exists(lib_path):
        lib_path = 'libbenchmark.so'

lib = ctypes.CDLL(lib_path)

# ============================================================================
# Define C structs
# ============================================================================

class DataPoint(ctypes.Structure):
    _fields_ = [
        ("id", ctypes.c_int),
        ("value", ctypes.c_double),
        ("name", ctypes.c_char * 32)
    ]

class Node(ctypes.Structure):
    pass

Node._fields_ = [
    ("data", ctypes.c_int),
    ("next", ctypes.POINTER(Node))
]

# ============================================================================
# 1. FUNCTION CALL OVERHEAD TESTS
# ============================================================================

lib.noop.argtypes = [ctypes.c_int]
lib.noop.restype = ctypes.c_int

def ct_noop(x):
    """Minimal function to measure pure call overhead"""
    return lib.noop(x)

lib.add_numbers.argtypes = [ctypes.c_int, ctypes.c_int]
lib.add_numbers.restype = ctypes.c_int

def ct_add_numbers(a, b):
    """Simple arithmetic operation"""
    return lib.add_numbers(a, b)

lib.calculate_simple.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_double]
lib.calculate_simple.restype = ctypes.c_double

def ct_calculate_simple(a, b, c, d):
    """Multiple parameter function"""
    return lib.calculate_simple(a, b, c, d)

# ============================================================================
# 2. COMPUTE-INTENSIVE WORKLOADS
# ============================================================================

lib.fibonacci_recursive.argtypes = [ctypes.c_int]
lib.fibonacci_recursive.restype = ctypes.c_longlong

def ct_fibonacci_recursive(n):
    """Fibonacci (recursive) - measures call stack overhead"""
    return lib.fibonacci_recursive(n)

lib.fibonacci_iterative.argtypes = [ctypes.c_int]
lib.fibonacci_iterative.restype = ctypes.c_longlong

def ct_fibonacci_iterative(n):
    """Fibonacci (iterative) - measures loop performance"""
    return lib.fibonacci_iterative(n)

lib.is_prime.argtypes = [ctypes.c_longlong]
lib.is_prime.restype = ctypes.c_int

def ct_is_prime(n):
    """Prime number checking - compute intensive"""
    return lib.is_prime(n)

lib.count_primes.argtypes = [ctypes.c_int, ctypes.c_int]
lib.count_primes.restype = ctypes.c_int

def ct_count_primes(start, end):
    """Count primes in range"""
    return lib.count_primes(start, end)

lib.matrix_multiply.argtypes = [
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ctypes.c_int
]
lib.matrix_multiply.restype = None

def ct_matrix_multiply(A, B):
    """Matrix multiplication - compute intensive"""
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.float64)
    lib.matrix_multiply(A, B, C, n)
    return C

lib.compute_math_intensive.argtypes = [ctypes.c_double, ctypes.c_int]
lib.compute_math_intensive.restype = ctypes.c_double

def ct_compute_math_intensive(x, iterations):
    """Mathematical operations - transcendental functions"""
    return lib.compute_math_intensive(x, iterations)

# ============================================================================
# 3. MEMORY-INTENSIVE WORKLOADS
# ============================================================================

lib.sum_array.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int]
lib.sum_array.restype = ctypes.c_double

def ct_sum_array(arr):
    """Array sum - memory read intensive"""
    return lib.sum_array(arr, len(arr))

lib.scale_array.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int, ctypes.c_double]
lib.scale_array.restype = None

def ct_scale_array(arr, factor):
    """Array operations - read and write"""
    lib.scale_array(arr, len(arr), factor)

lib.copy_array.argtypes = [
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ctypes.c_int
]
lib.copy_array.restype = None

def ct_copy_array(src):
    """Memory copy operation"""
    dst = np.empty_like(src)
    lib.copy_array(src, dst, len(src))
    return dst

lib.dot_product.argtypes = [
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ctypes.c_int
]
lib.dot_product.restype = ctypes.c_double

def ct_dot_product(a, b):
    """Array dot product"""
    return lib.dot_product(a, b, len(a))

lib.array_reverse.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int]
lib.array_reverse.restype = None

def ct_array_reverse(arr):
    """Array manipulation with complex access pattern"""
    lib.array_reverse(arr, len(arr))

lib.sum_strided.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int, ctypes.c_int]
lib.sum_strided.restype = ctypes.c_double

def ct_sum_strided(arr, stride):
    """Strided access pattern"""
    return lib.sum_strided(arr, len(arr), stride)

# ============================================================================
# 4. DATA MARSHALLING TESTS
# ============================================================================

lib.string_length.argtypes = [ctypes.c_char_p]
lib.string_length.restype = ctypes.c_int

def ct_string_length(s):
    """String length (measures string marshalling)"""
    return lib.string_length(s.encode('utf-8'))

lib.string_concat.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.string_concat.restype = ctypes.POINTER(ctypes.c_char)

lib.free_string.argtypes = [ctypes.POINTER(ctypes.c_char)]
lib.free_string.restype = None

def ct_string_concat(s1, s2):
    """String concatenation"""
    result_ptr = lib.string_concat(s1.encode('utf-8'), s2.encode('utf-8'))
    result = ctypes.cast(result_ptr, ctypes.c_char_p).value.decode('utf-8')
    lib.free_string(result_ptr)
    return result

lib.process_datapoint.argtypes = [ctypes.POINTER(DataPoint)]
lib.process_datapoint.restype = ctypes.c_double

def ct_process_datapoint(id, value, name):
    """Process struct"""
    dp = DataPoint()
    dp.id = id
    dp.value = value
    dp.name = name.encode('utf-8')
    return lib.process_datapoint(ctypes.byref(dp))

lib.sum_datapoints.argtypes = [ctypes.POINTER(DataPoint), ctypes.c_int]
lib.sum_datapoints.restype = ctypes.c_double

def ct_sum_datapoints(points):
    """Array of structs"""
    count = len(points)
    dp_array = (DataPoint * count)()
    for i, (id, value, name) in enumerate(points):
        dp_array[i].id = id
        dp_array[i].value = value
        dp_array[i].name = name.encode('utf-8')
    return lib.sum_datapoints(dp_array, count)

# ============================================================================
# 5. MIXED WORKLOADS
# ============================================================================

lib.monte_carlo_pi.argtypes = [ctypes.c_int]
lib.monte_carlo_pi.restype = ctypes.c_double

def ct_monte_carlo_pi(iterations):
    """Monte Carlo calculation"""
    return lib.monte_carlo_pi(iterations)

lib.blur_array.argtypes = [
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
    ctypes.c_int,
    ctypes.c_int
]
lib.blur_array.restype = None

def ct_blur_array(input_arr):
    """Image processing simulation - blur operation"""
    height, width = input_arr.shape
    output_arr = np.zeros((height, width), dtype=np.float64)
    lib.blur_array(input_arr, output_arr, width, height)
    return output_arr

lib.sort_array.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int]
lib.sort_array.restype = None

def ct_sort_array(arr):
    """Sorting - quicksort implementation"""
    lib.sort_array(arr, len(arr))

# ============================================================================
# 6. MEMORY ALLOCATION TESTS
# ============================================================================

lib.allocate_array.argtypes = [ctypes.c_int]
lib.allocate_array.restype = ctypes.POINTER(ctypes.c_double)

lib.free_array.argtypes = [ctypes.POINTER(ctypes.c_double)]
lib.free_array.restype = None

def ct_allocate_and_sum(size):
    """Allocate array and compute sum"""
    arr_ptr = lib.allocate_array(size)
    # Create numpy array from pointer (read-only view)
    arr = np.ctypeslib.as_array(arr_ptr, shape=(size,))
    total = lib.sum_array(arr, size)
    lib.free_array(arr_ptr)
    return total

# ============================================================================
# 7. CALLBACK SIMULATION
# ============================================================================

lib.apply_operation.argtypes = [ctypes.c_double, ctypes.c_int]
lib.apply_operation.restype = ctypes.c_double

def ct_apply_operation(initial, iterations):
    """Apply operation repeatedly"""
    return lib.apply_operation(initial, iterations)

# ============================================================================
# 8. BUFFER PROCESSING
# ============================================================================

lib.process_buffer.argtypes = [ndpointer(ctypes.c_ubyte, flags="C_CONTIGUOUS"), ctypes.c_int]
lib.process_buffer.restype = None

def ct_process_buffer(buffer):
    """Process byte buffer"""
    lib.process_buffer(buffer, len(buffer))

lib.checksum.argtypes = [ndpointer(ctypes.c_ubyte, flags="C_CONTIGUOUS"), ctypes.c_int]
lib.checksum.restype = ctypes.c_uint

def ct_checksum(buffer):
    """Calculate checksum"""
    return lib.checksum(buffer, len(buffer))

# ============================================================================
# 9. POINTER-INTENSIVE OPERATIONS
# ============================================================================

lib.create_list.argtypes = [ctypes.c_int]
lib.create_list.restype = ctypes.POINTER(Node)

lib.sum_list.argtypes = [ctypes.POINTER(Node)]
lib.sum_list.restype = ctypes.c_int

lib.free_list.argtypes = [ctypes.POINTER(Node)]
lib.free_list.restype = None

def ct_list_operations(size):
    """Create, sum, and free linked list"""
    head = lib.create_list(size)
    total = lib.sum_list(head)
    lib.free_list(head)
    return total

# ============================================================================
# 10. BITWISE OPERATIONS
# ============================================================================

lib.popcount.argtypes = [ctypes.c_uint]
lib.popcount.restype = ctypes.c_int

def ct_popcount(n):
    """Count set bits"""
    return lib.popcount(n)

lib.bitwise_reduce.argtypes = [ndpointer(ctypes.c_uint, flags="C_CONTIGUOUS"), ctypes.c_int]
lib.bitwise_reduce.restype = ctypes.c_uint

def ct_bitwise_reduce(arr):
    """Bitwise operations on array"""
    return lib.bitwise_reduce(arr, len(arr))

