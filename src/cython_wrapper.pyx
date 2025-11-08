# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy

# Import C declarations
from cython_wrapper cimport *

# ============================================================================
# 1. FUNCTION CALL OVERHEAD TESTS
# ============================================================================

def cy_noop(int x):
    """Minimal function to measure pure call overhead"""
    return noop(x)

def cy_add_numbers(int a, int b):
    """Simple arithmetic operation"""
    return add_numbers(a, b)

def cy_calculate_simple(int a, double b, int c, double d):
    """Multiple parameter function"""
    return calculate_simple(a, b, c, d)

# ============================================================================
# 2. COMPUTE-INTENSIVE WORKLOADS
# ============================================================================

def cy_fibonacci_recursive(int n):
    """Fibonacci (recursive) - measures call stack overhead"""
    return fibonacci_recursive(n)

def cy_fibonacci_iterative(int n):
    """Fibonacci (iterative) - measures loop performance"""
    return fibonacci_iterative(n)

def cy_is_prime(long long n):
    """Prime number checking - compute intensive"""
    return is_prime(n)

def cy_count_primes(int start, int end):
    """Count primes in range"""
    return count_primes(start, end)

def cy_matrix_multiply(np.ndarray[double, ndim=2, mode="c"] A,
                        np.ndarray[double, ndim=2, mode="c"] B):
    """Matrix multiplication - compute intensive"""
    cdef int n = A.shape[0]
    cdef np.ndarray[double, ndim=2, mode="c"] C = np.zeros((n, n), dtype=np.float64)
    
    matrix_multiply(&A[0, 0], &B[0, 0], &C[0, 0], n)
    return C

def cy_compute_math_intensive(double x, int iterations):
    """Mathematical operations - transcendental functions"""
    return compute_math_intensive(x, iterations)

# ============================================================================
# 3. MEMORY-INTENSIVE WORKLOADS
# ============================================================================

def cy_sum_array(np.ndarray[double, ndim=1, mode="c"] arr):
    """Array sum - memory read intensive"""
    return sum_array(&arr[0], arr.shape[0])

def cy_scale_array(np.ndarray[double, ndim=1, mode="c"] arr, double factor):
    """Array operations - read and write"""
    scale_array(&arr[0], arr.shape[0], factor)

def cy_copy_array(np.ndarray[double, ndim=1, mode="c"] src):
    """Memory copy operation"""
    cdef np.ndarray[double, ndim=1, mode="c"] dst = np.empty_like(src)
    copy_array(&src[0], &dst[0], src.shape[0])
    return dst

def cy_dot_product(np.ndarray[double, ndim=1, mode="c"] a,
                    np.ndarray[double, ndim=1, mode="c"] b):
    """Array dot product"""
    return dot_product(&a[0], &b[0], a.shape[0])

def cy_array_reverse(np.ndarray[double, ndim=1, mode="c"] arr):
    """Array manipulation with complex access pattern"""
    array_reverse(&arr[0], arr.shape[0])

def cy_sum_strided(np.ndarray[double, ndim=1, mode="c"] arr, int stride):
    """Strided access pattern"""
    return sum_strided(&arr[0], arr.shape[0], stride)

# ============================================================================
# 4. DATA MARSHALLING TESTS
# ============================================================================

def cy_string_length(str s):
    """String length (measures string marshalling)"""
    cdef bytes py_bytes = s.encode('utf-8')
    return string_length(py_bytes)

def cy_string_concat(str s1, str s2):
    """String concatenation"""
    cdef bytes b1 = s1.encode('utf-8')
    cdef bytes b2 = s2.encode('utf-8')
    cdef char* result = string_concat(b1, b2)
    cdef str py_result = result.decode('utf-8')
    free_string(result)
    return py_result

def cy_process_datapoint(int id, double value, str name):
    """Process struct"""
    cdef DataPoint dp
    dp.id = id
    dp.value = value
    
    # Convert Python string to bytes and copy to C char array
    cdef bytes name_bytes = name.encode('utf-8')
    cdef char* name_ptr = name_bytes
    strcpy(dp.name, name_ptr)
    
    return process_datapoint(&dp)

def cy_sum_datapoints(list points):
    """Array of structs"""
    cdef int count = len(points)
    cdef DataPoint* dp_array = <DataPoint*>malloc(count * sizeof(DataPoint))
    
    cdef int i
    cdef bytes name_bytes
    for i in range(count):
        dp_array[i].id = points[i][0]
        dp_array[i].value = points[i][1]
        name_bytes = points[i][2].encode('utf-8')
        strcpy(dp_array[i].name, name_bytes)
    
    cdef double result = sum_datapoints(dp_array, count)
    free(dp_array)
    return result

# ============================================================================
# 5. MIXED WORKLOADS
# ============================================================================

def cy_monte_carlo_pi(int iterations):
    """Monte Carlo calculation"""
    return monte_carlo_pi(iterations)

def cy_blur_array(np.ndarray[double, ndim=2, mode="c"] input_arr):
    """Image processing simulation - blur operation"""
    cdef int height = input_arr.shape[0]
    cdef int width = input_arr.shape[1]
    cdef np.ndarray[double, ndim=2, mode="c"] output_arr = np.zeros((height, width), dtype=np.float64)
    
    blur_array(&input_arr[0, 0], &output_arr[0, 0], width, height)
    return output_arr

def cy_sort_array(np.ndarray[double, ndim=1, mode="c"] arr):
    """Sorting - quicksort implementation"""
    sort_array(&arr[0], arr.shape[0])

# ============================================================================
# 6. MEMORY ALLOCATION TESTS
# ============================================================================

def cy_allocate_and_sum(int size):
    """Allocate array and compute sum"""
    cdef double* arr = allocate_array(size)
    cdef double total = sum_array(arr, size)
    free_array(arr)
    return total

# ============================================================================
# 7. CALLBACK SIMULATION
# ============================================================================

def cy_apply_operation(double initial, int iterations):
    """Apply operation repeatedly"""
    return apply_operation(initial, iterations)

# ============================================================================
# 8. BUFFER PROCESSING
# ============================================================================

def cy_process_buffer(np.ndarray[unsigned char, ndim=1, mode="c"] buffer):
    """Process byte buffer"""
    process_buffer(&buffer[0], buffer.shape[0])

def cy_checksum(np.ndarray[unsigned char, ndim=1, mode="c"] buffer):
    """Calculate checksum"""
    return checksum(&buffer[0], buffer.shape[0])

# ============================================================================
# 9. POINTER-INTENSIVE OPERATIONS
# ============================================================================

def cy_list_operations(int size):
    """Create, sum, and free linked list"""
    cdef Node* head = create_list(size)
    cdef int total = sum_list(head)
    free_list(head)
    return total

# ============================================================================
# 10. BITWISE OPERATIONS
# ============================================================================

def cy_popcount(unsigned int n):
    """Count set bits"""
    return popcount(n)

def cy_bitwise_reduce(np.ndarray[unsigned int, ndim=1, mode="c"] arr):
    """Bitwise operations on array"""
    return bitwise_reduce(&arr[0], arr.shape[0])

