#ifndef BENCHMARK_LIB_H
#define BENCHMARK_LIB_H

// Function call overhead
int noop(int x);
int add_numbers(int a, int b);
double calculate_simple(int a, double b, int c, double d);

// Compute-intensive
long long fibonacci_recursive(int n);
long long fibonacci_iterative(int n);
int is_prime(long long n);
int count_primes(int start, int end);
void matrix_multiply(double* A, double* B, double* C, int n);
double compute_math_intensive(double x, int iterations);

// Memory-intensive
double sum_array(double* arr, int size);
void scale_array(double* arr, int size, double factor);
void copy_array(double* src, double* dst, int size);
double dot_product(double* a, double* b, int size);
void array_reverse(double* arr, int size);
double sum_strided(double* arr, int size, int stride);

// Data marshalling
int string_length(const char* str);
char* string_concat(const char* s1, const char* s2);
void free_string(char* str);

// Struct definition
typedef struct {
    int id;
    double value;
    char name[32];
} DataPoint;

double process_datapoint(DataPoint* dp);
double sum_datapoints(DataPoint* points, int count);

// Mixed workloads
double monte_carlo_pi(int iterations);
void blur_array(double* input, double* output, int width, int height);
void sort_array(double* arr, int size);

// Memory allocation
double* allocate_array(int size);
void free_array(double* arr);

// Callback simulation
double apply_operation(double initial, int iterations);

// Buffer processing
void process_buffer(unsigned char* buffer, int size);
unsigned int checksum(unsigned char* buffer, int size);

// Pointer-intensive
typedef struct Node {
    int data;
    struct Node* next;
} Node;

Node* create_list(int size);
int sum_list(Node* head);
void free_list(Node* head);

// Bitwise operations
int popcount(unsigned int n);
unsigned int bitwise_reduce(unsigned int* arr, int size);

#endif // BENCHMARK_LIB_H

