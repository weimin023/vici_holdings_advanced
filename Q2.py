import build.Q2_func as Q2_func
import numpy as np

# Test with int64 data type
int64_vec = [np.iinfo(np.int64).max, np.iinfo(np.int64).max - 1, np.iinfo(np.int64).max - 2]
mean_int64 = Q2_func.calculate_mean_kahan_int64(int64_vec)
expected_mean_int64 = np.mean(int64_vec)  # Calculate expected mean using numpy for comparison
assert abs(mean_int64 - expected_mean_int64) < 1e-9, f"Expected {expected_mean_int64}, got {mean_int64}"
print(f"Mean (int64): {mean_int64}")

# Test with int32 data type
int32_vec = [np.iinfo(np.int32).max, np.iinfo(np.int32).max - 1, np.iinfo(np.int32).max - 2]
mean_int32 = Q2_func.calculate_mean_kahan_int32(int32_vec)
expected_mean_int32 = np.mean(int32_vec)  # Calculate expected mean using numpy for comparison
assert abs(mean_int32 - expected_mean_int32) < 1e-9, f"Expected {expected_mean_int32}, got {mean_int32}"
print(f"Mean (int32): {mean_int32}")


uint32_vec = [np.iinfo(np.uint32).max, 1]
mean_uint32 = Q2_func.calculate_mean_kahan_uint32(uint32_vec)
expected_mean_uint32 = np.mean(uint32_vec)  # Calculate expected mean using numpy for comparison
assert abs(mean_uint32 - expected_mean_uint32) < 1e-9, f"Expected {expected_mean_uint32}, got {mean_uint32}"
print(f"Mean (uint32): {mean_uint32}")