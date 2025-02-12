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

# Test For Overflow
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
single_vec = [5]
single_mean_numpy = np.mean(single_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, single_vec, single_mean_numpy, "int32")

# Multiple Small Values
multi_vec_small = [-1, 1, 2, -2]
multi_mean_numpy_small = np.mean(multi_vec_small)
test_mean(Q2_func.calculate_mean_kahan_int32, multi_vec_small, multi_mean_numpy_small, "int32")

# Multiple Large Values
multi_vec_large = np.full(100, np.iinfo(np.int64).max, dtype=np.int64)
multi_mean_numpy_large = np.mean(multi_vec_large)
test_mean(Q2_func.calculate_mean_kahan_int64, multi_vec_large, multi_mean_numpy_large, "int64")



min_max_int32_vec = [np.iinfo(np.int32).min, np.iinfo(np.int32).max]
expected_mean_min_max_int32 = np.mean(min_max_int32_vec)
test_mean(Q2_func.calculate_mean_kahan_int32, min_max_int32_vec, expected_mean_min_max_int32, "int32")

min_max_int64_vec = [np.iinfo(np.int64).min, np.iinfo(np.int64).max]
expected_mean_min_max_int64 = np.mean(min_max_int64_vec)
test_mean(Q2_func.calculate_mean_kahan_int64, min_max_int64_vec, expected_mean_min_max_int64, "int64")

uint32_overflow_vec = [np.iinfo(np.uint32).max, np.iinfo(np.uint32).max, 1, 1]
expected_mean_uint32_overflow = np.mean(uint32_overflow_vec)
test_mean(Q2_func.calculate_mean_kahan_uint32, uint32_overflow_vec, expected_mean_uint32_overflow, "uint32")


small_double = np.full(1000000, 1e-8, dtype=np.float64)
expected_mean_small_double = np.mean(small_double)
test_mean(Q2_func.calculate_mean_kahan_double, small_double, expected_mean_small_double, "double")


nan_inf_vec = [1, 2, np.nan, 4, 5]
inf_vec = [1, 2, np.inf, 4, 5]
neg_inf_vec = [1, 2, -np.inf, 4, 5]

try:
    test_mean(Q2_func.calculate_mean_kahan_int64, nan_inf_vec, np.mean(nan_inf_vec), "int64")
except Exception as e:
    print(f"Handled NaN error: {e}")

try:
    test_mean(Q2_func.calculate_mean_kahan_int64, inf_vec, np.mean(inf_vec), "int64")
except Exception as e:
    print(f"Handled Inf error: {e}")

try:
    test_mean(Q2_func.calculate_mean_kahan_int64, neg_inf_vec, np.mean(neg_inf_vec), "int64")
except Exception as e:
    print(f"Handled -Inf error: {e}")
