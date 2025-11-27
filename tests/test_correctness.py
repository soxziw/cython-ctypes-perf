"""
Unit tests to verify that Cython and ctypes wrappers produce identical results
"""

import unittest
import numpy as np
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))  # For ctypes_wrapper
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # For cython_wrapper (built in root)

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


@unittest.skipIf(not (CYTHON_AVAILABLE and CTYPES_AVAILABLE), 
                 "Both Cython and ctypes wrappers must be available")
class TestCorrectness(unittest.TestCase):
    """Test that Cython and ctypes produce identical results"""
    
    def test_noop(self):
        """Test noop function"""
        for x in [0, 1, 42, -10, 1000]:
            self.assertEqual(cy.cy_noop(x), ct.ct_noop(x))
    
    def test_add_numbers(self):
        """Test add_numbers function"""
        test_cases = [(1, 2), (100, 200), (-5, 10), (0, 0)]
        for a, b in test_cases:
            self.assertEqual(cy.cy_add_numbers(a, b), ct.ct_add_numbers(a, b))
    
    def test_calculate_simple(self):
        """Test calculate_simple function"""
        test_cases = [(1, 2.5, 3, 4.5), (10, 1.1, 5, 2.2)]
        for a, b, c, d in test_cases:
            cy_result = cy.cy_calculate_simple(a, b, c, d)
            ct_result = ct.ct_calculate_simple(a, b, c, d)
            self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_fibonacci_recursive(self):
        """Test recursive fibonacci"""
        for n in [0, 1, 5, 10, 15]:
            cy_result = cy.cy_fibonacci_recursive(n)
            ct_result = ct.ct_fibonacci_recursive(n)
            self.assertEqual(cy_result, ct_result)
    
    def test_fibonacci_iterative(self):
        """Test iterative fibonacci"""
        for n in [0, 1, 10, 100, 1000]:
            cy_result = cy.cy_fibonacci_iterative(n)
            ct_result = ct.ct_fibonacci_iterative(n)
            self.assertEqual(cy_result, ct_result)
    
    def test_is_prime(self):
        """Test prime checking"""
        test_cases = [2, 3, 4, 17, 100, 1000003]
        for n in test_cases:
            cy_result = cy.cy_is_prime(n)
            ct_result = ct.ct_is_prime(n)
            self.assertEqual(cy_result, ct_result)
    
    def test_count_primes(self):
        """Test counting primes in range"""
        test_cases = [(1, 10), (1, 100), (1, 1000)]
        for start, end in test_cases:
            cy_result = cy.cy_count_primes(start, end)
            ct_result = ct.ct_count_primes(start, end)
            self.assertEqual(cy_result, ct_result)
    
    def test_matrix_multiply(self):
        """Test matrix multiplication"""
        for size in [2, 5, 10]:
            A = np.random.rand(size, size)
            B = np.random.rand(size, size)
            
            cy_result = cy.cy_matrix_multiply(A.copy(), B.copy())
            ct_result = ct.ct_matrix_multiply(A.copy(), B.copy())
            
            np.testing.assert_array_almost_equal(cy_result, ct_result)
    
    def test_compute_math_intensive(self):
        """Test math intensive computation"""
        test_cases = [(1.5, 100), (2.0, 1000)]
        for x, iterations in test_cases:
            cy_result = cy.cy_compute_math_intensive(x, iterations)
            ct_result = ct.ct_compute_math_intensive(x, iterations)
            self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_sum_array(self):
        """Test array sum"""
        for size in [10, 100, 1000]:
            arr = np.random.rand(size)
            cy_result = cy.cy_sum_array(arr.copy())
            ct_result = ct.ct_sum_array(arr.copy())
            self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_scale_array(self):
        """Test array scaling"""
        arr = np.random.rand(100)
        factor = 2.5
        
        cy_arr = arr.copy()
        ct_arr = arr.copy()
        
        cy.cy_scale_array(cy_arr, factor)
        ct.ct_scale_array(ct_arr, factor)
        
        np.testing.assert_array_almost_equal(cy_arr, ct_arr)
    
    def test_copy_array(self):
        """Test array copy"""
        arr = np.random.rand(100)
        
        cy_result = cy.cy_copy_array(arr.copy())
        ct_result = ct.ct_copy_array(arr.copy())
        
        np.testing.assert_array_almost_equal(cy_result, ct_result)
        np.testing.assert_array_almost_equal(cy_result, arr)
    
    def test_dot_product(self):
        """Test dot product"""
        for size in [10, 100, 1000]:
            a = np.random.rand(size)
            b = np.random.rand(size)
            
            cy_result = cy.cy_dot_product(a.copy(), b.copy())
            ct_result = ct.ct_dot_product(a.copy(), b.copy())
            
            self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_array_reverse(self):
        """Test array reversal"""
        arr = np.random.rand(100)
        original = arr.copy()
        
        cy_arr = arr.copy()
        ct_arr = arr.copy()
        
        cy.cy_array_reverse(cy_arr)
        ct.ct_array_reverse(ct_arr)
        
        np.testing.assert_array_almost_equal(cy_arr, ct_arr)
        np.testing.assert_array_almost_equal(cy_arr, original[::-1])
    
    def test_sum_strided(self):
        """Test strided sum"""
        arr = np.random.rand(100)
        for stride in [1, 2, 5, 10]:
            cy_result = cy.cy_sum_strided(arr.copy(), stride)
            ct_result = ct.ct_sum_strided(arr.copy(), stride)
            self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_string_length(self):
        """Test string length"""
        test_strings = ["", "hello", "Hello, World!", "x" * 100]
        for s in test_strings:
            cy_result = cy.cy_string_length(s)
            ct_result = ct.ct_string_length(s)
            self.assertEqual(cy_result, ct_result)
            self.assertEqual(cy_result, len(s))
    
    def test_string_concat(self):
        """Test string concatenation"""
        test_cases = [("hello", "world"), ("foo", "bar"), ("", "test")]
        for s1, s2 in test_cases:
            cy_result = cy.cy_string_concat(s1, s2)
            ct_result = ct.ct_string_concat(s1, s2)
            self.assertEqual(cy_result, ct_result)
            self.assertEqual(cy_result, s1 + s2)
    
    def test_process_datapoint(self):
        """Test datapoint processing"""
        test_cases = [(1, 2.5, "test"), (42, 3.14, "foo")]
        for id, value, name in test_cases:
            cy_result = cy.cy_process_datapoint(id, value, name)
            ct_result = ct.ct_process_datapoint(id, value, name)
            self.assertAlmostEqual(cy_result, ct_result, places=10)
            self.assertAlmostEqual(cy_result, id * value, places=10)
    
    def test_sum_datapoints(self):
        """Test sum of datapoint array"""
        points = [(i, float(i), f"point_{i}") for i in range(10)]
        cy_result = cy.cy_sum_datapoints(points)
        ct_result = ct.ct_sum_datapoints(points)
        self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_monte_carlo_pi(self):
        """Test Monte Carlo pi estimation"""
        # Results won't be identical due to RNG, but should be close to pi
        iterations = 100000
        cy_result = cy.cy_monte_carlo_pi(iterations)
        ct_result = ct.ct_monte_carlo_pi(iterations)
        
        # Both should be close to pi
        self.assertAlmostEqual(cy_result, np.pi, delta=0.1)
        self.assertAlmostEqual(ct_result, np.pi, delta=0.1)
    
    def test_blur_array(self):
        """Test blur operation"""
        img = np.random.rand(10, 10)
        cy_result = cy.cy_blur_array(img.copy())
        ct_result = ct.ct_blur_array(img.copy())
        np.testing.assert_array_almost_equal(cy_result, ct_result)
    
    def test_sort_array(self):
        """Test array sorting"""
        arr = np.random.rand(100)
        
        cy_arr = arr.copy()
        ct_arr = arr.copy()
        
        cy.cy_sort_array(cy_arr)
        ct.ct_sort_array(ct_arr)
        
        np.testing.assert_array_almost_equal(cy_arr, ct_arr)
        np.testing.assert_array_almost_equal(cy_arr, np.sort(arr))
    
    def test_allocate_and_sum(self):
        """Test allocation and sum"""
        size = 1000
        cy_result = cy.cy_allocate_and_sum(size)
        ct_result = ct.ct_allocate_and_sum(size)
        self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_apply_operation(self):
        """Test repeated operation"""
        test_cases = [(1.0, 100), (2.5, 1000)]
        for initial, iterations in test_cases:
            cy_result = cy.cy_apply_operation(initial, iterations)
            ct_result = ct.ct_apply_operation(initial, iterations)
            self.assertAlmostEqual(cy_result, ct_result, places=10)
    
    def test_process_buffer(self):
        """Test buffer processing"""
        buffer = np.random.randint(0, 256, 100, dtype=np.uint8)
        
        cy_buffer = buffer.copy()
        ct_buffer = buffer.copy()
        
        cy.cy_process_buffer(cy_buffer)
        ct.ct_process_buffer(ct_buffer)
        
        np.testing.assert_array_equal(cy_buffer, ct_buffer)
    
    def test_checksum(self):
        """Test checksum calculation"""
        buffer = np.random.randint(0, 256, 100, dtype=np.uint8)
        cy_result = cy.cy_checksum(buffer.copy())
        ct_result = ct.ct_checksum(buffer.copy())
        self.assertEqual(cy_result, ct_result)
    
    def test_list_operations(self):
        """Test linked list operations"""
        for size in [10, 100, 1000]:
            cy_result = cy.cy_list_operations(size)
            ct_result = ct.ct_list_operations(size)
            self.assertEqual(cy_result, ct_result)
            # Verify result is correct: sum of 0 to size-1
            expected = sum(range(size))
            self.assertEqual(cy_result, expected)
    
    def test_popcount(self):
        """Test popcount"""
        test_cases = [0, 1, 0xFF, 0xFFFF, 0xFFFFFFFF]
        for n in test_cases:
            cy_result = cy.cy_popcount(n)
            ct_result = ct.ct_popcount(n)
            self.assertEqual(cy_result, ct_result)
    
    def test_bitwise_reduce(self):
        """Test bitwise reduction"""
        arr = np.random.randint(0, 2**32, 100, dtype=np.uint32)
        cy_result = cy.cy_bitwise_reduce(arr.copy())
        ct_result = ct.ct_bitwise_reduce(arr.copy())
        self.assertEqual(cy_result, ct_result)


if __name__ == '__main__':
    unittest.main()

