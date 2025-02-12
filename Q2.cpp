#include <iostream>
#include <vector>
#include <stdexcept>
#include <numeric>
#include <limits>
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
    m.def("calculate_mean_kahan_int", &calculateMeanKahan<int>, "Calculate mean using Kahan summation for int");
    m.def("calculate_mean_kahan_float", &calculateMeanKahan<float>, "Calculate mean using Kahan summation for float");
    m.def("calculate_mean_kahan_double", &calculateMeanKahan<double>, "Calculate mean using Kahan summation for double");
    m.def("calculate_mean_kahan_int64", &calculateMeanKahan<int64_t>, "Calculate mean using Kahan summation for int64_t");
    m.def("calculate_mean_kahan_int32", &calculateMeanKahan<int32_t>, "Calculate mean using Kahan summation for int32_t");
    m.def("calculate_mean_kahan_uint32", &calculateMeanKahan<uint32_t>, "Calculate mean using Kahan summation for uint32_t");
    m.def("calculate_mean_kahan_uint64", &calculateMeanKahan<uint64_t>, "Calculate mean using Kahan summation for uint64_t");
}

/*int main() {
    try {
        // 1. Empty Vector
        std::vector<int> emptyVec;
        std::cout << "Mean (Empty Vector): ";
        try {
            std::cout << calculateMeanKahan(emptyVec) << std::endl;
        } catch (const std::invalid_argument& e) {
            std::cout << "Caught exception: " << e.what() << std::endl;
        }

        //
        std::vector<uint32_t> exampleValue{ std::numeric_limits<uint32_t>::max(), 1 };
        std::cout << "Mean (Example): " << calculateMeanKahan(exampleValue) << std::endl;

        std::vector<int> exampleValue2{ std::numeric_limits<int>::max(), 1 };
        std::cout << "Mean (int max): " << calculateMeanKahan(exampleValue2) << std::endl;

        // 2. Single Element Vector
        std::vector<int> singleElementVec = {42};
        std::cout << "Mean (Single Element): " << calculateMeanKahan(singleElementVec) << std::endl;

        // 3. All Equal Values
        std::vector<int> equalValuesVec = {5, 5, 5, 5};
        std::cout << "Mean (All Equal Values): " << calculateMeanKahan(equalValuesVec) << std::endl;

        // 4. Large Positive Values
        std::vector<uint64_t> largePosVec = {static_cast<uint64_t>(1e18), static_cast<uint64_t>(1e18 + 1), static_cast<uint64_t>(1e18 + 2), static_cast<uint64_t>(1e18 + 3)};
        std::cout << "Mean (Large Positive Values): " << calculateMeanKahan(largePosVec) << std::endl;

        // 5. Large Negative Values
        std::vector<int64_t> largeNegVec = {static_cast<int64_t>(-1e18), static_cast<int64_t>(-1e18 - 1), static_cast<int64_t>(-1e18 - 2), static_cast<int64_t>(-1e18 - 3)};
        std::cout << "Mean (Large Negative Values): " << calculateMeanKahan(largeNegVec) << std::endl;

        // 7. Small Values
        std::vector<int> smallValuesVec = {1, -1, 2, -2};
        std::cout << "Mean (Small Values): " << calculateMeanKahan(smallValuesVec) << std::endl;

        // 8. Very Large Vector
        std::vector<int> largeVector(1e6, 10);  // 1 million elements, all equal to 10
        std::cout << "Mean (Very Large Vector): " << calculateMeanKahan(largeVector) << std::endl;

        // 9. Floating-Point Numbers
        std::vector<double> floatVec = {1.0000000001, 1.0000000002, 1.0000000003};
        std::cout << "Mean (Floating-Point Numbers): " << calculateMeanKahan(floatVec) << std::endl;

        // 10. Extreme Range of Values
        std::vector<int64_t> extremeRangeVec = {INT64_MAX, 0, INT64_MIN};
        std::cout << "Mean (Extreme Range of Values): " << calculateMeanKahan(extremeRangeVec) << std::endl;

        // 11. Varying Element Counts
        std::vector<int> smallCountVec = {1, 2, 3};
        std::cout << "Mean (Varying Element Count - Small): " << calculateMeanKahan(smallCountVec) << std::endl;

        std::vector<int> largeCountVec(1000, 10);
        std::cout << "Mean (Varying Element Count - Large): " << calculateMeanKahan(largeCountVec) << std::endl;

    } catch (const std::exception& e) {
        std::cout << "General exception caught: " << e.what() << std::endl;
    }

    return 0;
}*/