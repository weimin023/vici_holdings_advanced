#include <vector>
#include <stdexcept>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 

template<typename T>
static double calculateMeanKahan(const std::vector<T>& numbers) {
    if (numbers.empty()) {
        throw std::invalid_argument("The input vector is empty.");
    }

    double totalSum = 0.0;
    double correction = 0.0;

    for (const auto& value : numbers) {
        double adjustedValue = static_cast<double>(value) - correction;
        double newSum = totalSum + adjustedValue;
        correction = (newSum - totalSum) - adjustedValue;
        totalSum = newSum;
    }

    size_t totalCount = numbers.size();
    return totalSum / static_cast<double>(totalCount);
}

PYBIND11_MODULE(Q2_func, m) {
    // Float
    m.def("calculate_mean_kahan_float", &calculateMeanKahan<float>, "Calculate mean using Kahan summation for float");
    
    // Double
    m.def("calculate_mean_kahan_double", &calculateMeanKahan<double>, "Calculate mean using Kahan summation for double");
    
    // Signed Integer
    m.def("calculate_mean_kahan_int32", &calculateMeanKahan<int32_t>, "Calculate mean using Kahan summation for int32_t");
    m.def("calculate_mean_kahan_int64", &calculateMeanKahan<int64_t>, "Calculate mean using Kahan summation for int64_t");
    
    // Unsigned Integer
    m.def("calculate_mean_kahan_uint32", &calculateMeanKahan<uint32_t>, "Calculate mean using Kahan summation for uint32_t");
    m.def("calculate_mean_kahan_uint64", &calculateMeanKahan<uint64_t>, "Calculate mean using Kahan summation for uint64_t");
}
