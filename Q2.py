import build.Q2_func as Q2_func
import numpy as np

def test_mean(function, input_vec, expected_mean, dtype_name):
    mean_result = function(input_vec)
    error = abs(mean_result - expected_mean)
    
    assert error < 1e-9, f"Expected {expected_mean}, got {mean_result}"
    
    print(f"[Success] Test Overflow ({dtype_name}), Mean of {input_vec}")
    print(f"    - C++   Result: {mean_result}")
    print(f"    - Numpy Result: {expected_mean}")
    print(f"    - Error       : {error}")


# Test For Empty
# This case is tested in C++ function, throw std::invalid_argument("The input vector is empty.")

import numpy as np

# Test for Overflow
int32_vec = [np.iinfo(np.int32).max, 1]
expected_mean_int32 = np.mean(int32_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, int32_vec, expected_mean_int32, "int32")

int64_vec = [np.iinfo(np.int64).max, 1]
expected_mean_int64 = np.mean(int64_vec)
test_mean(Q2_func.calculate_mean_kahan_int64, int64_vec, expected_mean_int64, "int64")

uint32_vec = [np.iinfo(np.uint32).max, 1]
expected_mean_uint32 = np.mean(uint32_vec)
test_mean(Q2_func.calculate_mean_kahan_uint32, uint32_vec, expected_mean_uint32, "uint32")

# Test Single Value
single_value_vec = [5]
expected_mean_single_value = np.mean(single_value_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, single_value_vec, expected_mean_single_value, "int32")

# Test Small Values with Negative and Positive Numbers
small_values_vec = [-1, 1, 2, -2]
expected_mean_small_values = np.mean(small_values_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, small_values_vec, expected_mean_small_values, "int32")

# Test Large Values
large_values_vec = np.full(100, np.iinfo(np.int64).max, dtype=np.int64)
expected_mean_large_values = np.mean(large_values_vec)
test_mean(Q2_func.calculate_mean_kahan_int64, large_values_vec, expected_mean_large_values, "int64")

# Test Min and Max Integer Values for Symmetry
min_max_int32_vec = [np.iinfo(np.int32).min, np.iinfo(np.int32).max]
expected_mean_min_max_int32 = np.mean(min_max_int32_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, min_max_int32_vec, expected_mean_min_max_int32, "int32")

min_max_int64_vec = [np.iinfo(np.int64).min, np.iinfo(np.int64).max]
expected_mean_min_max_int64 = np.mean(min_max_int64_vec)
test_mean(Q2_func.calculate_mean_kahan_int64, min_max_int64_vec, expected_mean_min_max_int64, "int64")

# Test Unsigned Integer Overflow Case
uint32_overflow_vec = [np.iinfo(np.uint32).max, np.iinfo(np.uint32).max, 1, 1]
expected_mean_uint32_overflow = np.mean(uint32_overflow_vec)
test_mean(Q2_func.calculate_mean_kahan_uint32, uint32_overflow_vec, expected_mean_uint32_overflow, "uint32")

# Test Small Floating-Point Values for Underflow
small_double_vec = np.full(1000000, 1e-8, dtype=np.float64)
expected_mean_small_double = np.mean(small_double_vec)
test_mean(Q2_func.calculate_mean_kahan_double, small_double_vec, expected_mean_small_double, "double")

# Additional Test Cases

# Test Very Small Floating-Point Values (Precision Loss Check)
tiny_double_vec = np.full(1000000, 1e-308, dtype=np.float64)
expected_mean_tiny_double = np.mean(tiny_double_vec)
test_mean(Q2_func.calculate_mean_kahan_double, tiny_double_vec, expected_mean_tiny_double, "double")

# Test Mix of Very Large and Very Small Values (Loss of Precision Test)
mixed_scale_double_vec = [1e20, 1, 1e-20]
expected_mean_mixed_scale_double = np.mean(mixed_scale_double_vec)
test_mean(Q2_func.calculate_mean_kahan_double, mixed_scale_double_vec, expected_mean_mixed_scale_double, "double")

# Test Alternating Sign Values
alternating_sign_vec = np.tile([-1, 1], 500000)
expected_mean_alternating_sign = np.mean(alternating_sign_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, alternating_sign_vec, expected_mean_alternating_sign, "int32")

# Test Exponentially Growing Values
exponential_growth_vec = np.array([10**i for i in range(10)], dtype=np.float64)
expected_mean_exponential_growth = np.mean(exponential_growth_vec)
test_mean(Q2_func.calculate_mean_kahan_double, exponential_growth_vec, expected_mean_exponential_growth, "double")

# Test Random Integer Values
random_int32_vec = np.random.randint(-1000, 1000, 1000000, dtype=np.int32)
expected_mean_random_int32 = np.mean(random_int32_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, random_int32_vec, expected_mean_random_int32, "int32")

random_int64_vec = np.random.randint(-10**12, 10**12, 1000000, dtype=np.int64)
expected_mean_random_int64 = np.mean(random_int64_vec)
test_mean(Q2_func.calculate_mean_kahan_int64, random_int64_vec, expected_mean_random_int64, "int64")
