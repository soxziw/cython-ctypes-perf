#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

// ============================================================================
// 1. FUNCTION CALL OVERHEAD TESTS
// ============================================================================

// Minimal function to measure pure call overhead
int noop(int x) {
    return x;
}

// Simple arithmetic operation
int add_numbers(int a, int b) {
    return a + b;
}

// Multiple parameter function
double calculate_simple(int a, double b, int c, double d) {
    return (a + b) * (c - d);
}

// ============================================================================
// 2. COMPUTE-INTENSIVE WORKLOADS
// ============================================================================

// Fibonacci (recursive) - measures call stack overhead
long long fibonacci_recursive(int n) {
    if (n <= 1) return n;
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2);
}

// Fibonacci (iterative) - measures loop performance
long long fibonacci_iterative(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1, temp;
    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Prime number checking - compute intensive
int is_prime(long long n) {
    if (n <= 1) return 0;
    if (n <= 3) return 1;
    if (n % 2 == 0 || n % 3 == 0) return 0;
    
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0)
            return 0;
    }
    return 1;
}

// Count primes in range
int count_primes(int start, int end) {
    int count = 0;
    for (int i = start; i <= end; i++) {
        if (is_prime(i)) count++;
    }
    return count;
}

// Matrix multiplication - compute intensive
void matrix_multiply(double* A, double* B, double* C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i * n + j] = 0;
            for (int k = 0; k < n; k++) {
                C[i * n + j] += A[i * n + k] * B[k * n + j];
            }
        }
    }
}

// Mathematical operations - transcendental functions
double compute_math_intensive(double x, int iterations) {
    double result = x;
    for (int i = 0; i < iterations; i++) {
        result = sin(result) + cos(result * 1.5) + sqrt(fabs(result) + 1.0);
        result = result / (1.0 + fabs(result));
    }
    return result;
}

// ============================================================================
// 3. MEMORY-INTENSIVE WORKLOADS
// ============================================================================

// Array sum - memory read intensive
double sum_array(double* arr, int size) {
    double sum = 0.0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

// Array operations - read and write
void scale_array(double* arr, int size, double factor) {
    for (int i = 0; i < size; i++) {
        arr[i] *= factor;
    }
}

// Memory copy operation
void copy_array(double* src, double* dst, int size) {
    memcpy(dst, src, size * sizeof(double));
}

// Array dot product
double dot_product(double* a, double* b, int size) {
    double result = 0.0;
    for (int i = 0; i < size; i++) {
        result += a[i] * b[i];
    }
    return result;
}

// Array manipulation with complex access pattern
void array_reverse(double* arr, int size) {
    for (int i = 0; i < size / 2; i++) {
        double temp = arr[i];
        arr[i] = arr[size - 1 - i];
        arr[size - 1 - i] = temp;
    }
}

// Strided access pattern
double sum_strided(double* arr, int size, int stride) {
    double sum = 0.0;
    for (int i = 0; i < size; i += stride) {
        sum += arr[i];
    }
    return sum;
}

// ============================================================================
// 4. DATA MARSHALLING TESTS
// ============================================================================

// String length (measures string marshalling)
int string_length(const char* str) {
    return strlen(str);
}

// String concatenation (allocates memory)
char* string_concat(const char* s1, const char* s2) {
    int len1 = strlen(s1);
    int len2 = strlen(s2);
    char* result = (char*)malloc(len1 + len2 + 1);
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

// Free string allocated by C
void free_string(char* str) {
    free(str);
}

// Struct marshalling test
typedef struct {
    int id;
    double value;
    char name[32];
} DataPoint;

// Process struct
double process_datapoint(DataPoint* dp) {
    return dp->id * dp->value;
}

// Array of structs
double sum_datapoints(DataPoint* points, int count) {
    double sum = 0.0;
    for (int i = 0; i < count; i++) {
        sum += points[i].value;
    }
    return sum;
}

// ============================================================================
// 5. MIXED WORKLOADS
// ============================================================================

// Simulate a Monte Carlo calculation (compute + random access)
double monte_carlo_pi(int iterations) {
    int inside = 0;
    unsigned int seed = 42;
    
    for (int i = 0; i < iterations; i++) {
        double x = (double)rand_r(&seed) / RAND_MAX;
        double y = (double)rand_r(&seed) / RAND_MAX;
        if (x * x + y * y <= 1.0) {
            inside++;
        }
    }
    
    return 4.0 * inside / iterations;
}

// Image processing simulation - blur operation
void blur_array(double* input, double* output, int width, int height) {
    for (int i = 1; i < height - 1; i++) {
        for (int j = 1; j < width - 1; j++) {
            double sum = 0.0;
            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    sum += input[(i + di) * width + (j + dj)];
                }
            }
            output[i * width + j] = sum / 9.0;
        }
    }
}

// Sorting - quicksort implementation
int compare_doubles(const void* a, const void* b) {
    double diff = *(double*)a - *(double*)b;
    return (diff > 0) - (diff < 0);
}

void sort_array(double* arr, int size) {
    qsort(arr, size, sizeof(double), compare_doubles);
}

// ============================================================================
// 6. MEMORY ALLOCATION TESTS
// ============================================================================

// Allocate array and fill with pattern
double* allocate_array(int size) {
    double* arr = (double*)malloc(size * sizeof(double));
    for (int i = 0; i < size; i++) {
        arr[i] = (double)i;
    }
    return arr;
}

// Free allocated array
void free_array(double* arr) {
    free(arr);
}

// ============================================================================
// 7. CALLBACK SIMULATION (for measuring FFI round-trip overhead)
// ============================================================================

// Apply a simple operation repeatedly (simulates callbacks)
double apply_operation(double initial, int iterations) {
    double result = initial;
    for (int i = 0; i < iterations; i++) {
        result = result * 1.1 + 0.5;
    }
    return result;
}

// ============================================================================
// 8. BUFFER PROCESSING
// ============================================================================

// Process byte buffer
void process_buffer(unsigned char* buffer, int size) {
    for (int i = 0; i < size; i++) {
        buffer[i] = (buffer[i] + 13) % 256;
    }
}

// Calculate checksum
unsigned int checksum(unsigned char* buffer, int size) {
    unsigned int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += buffer[i];
    }
    return sum;
}

// ============================================================================
// 9. POINTER-INTENSIVE OPERATIONS
// ============================================================================

// Linked list node
typedef struct Node {
    int data;
    struct Node* next;
} Node;

// Create linked list
Node* create_list(int size) {
    Node* head = NULL;
    Node* current = NULL;
    
    for (int i = 0; i < size; i++) {
        Node* node = (Node*)malloc(sizeof(Node));
        node->data = i;
        node->next = NULL;
        
        if (head == NULL) {
            head = node;
            current = node;
        } else {
            current->next = node;
            current = node;
        }
    }
    
    return head;
}

// Sum linked list
int sum_list(Node* head) {
    int sum = 0;
    Node* current = head;
    while (current != NULL) {
        sum += current->data;
        current = current->next;
    }
    return sum;
}

// Free linked list
void free_list(Node* head) {
    Node* current = head;
    while (current != NULL) {
        Node* next = current->next;
        free(current);
        current = next;
    }
}

// ============================================================================
// 10. BITWISE OPERATIONS
// ============================================================================

// Count set bits
int popcount(unsigned int n) {
    int count = 0;
    while (n) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}

// Bitwise operations on array
unsigned int bitwise_reduce(unsigned int* arr, int size) {
    unsigned int result = 0;
    for (int i = 0; i < size; i++) {
        result ^= arr[i];
    }
    return result;
}

