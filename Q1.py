import unittest
from collections import deque

current_day = 0
last_timestamp = 0

def parse_timestamp(timestamp: str):
    global current_day, last_timestamp
    
    try:
        # Split the timestamp and check if it's well-formed
        raw_data_list = timestamp.split()
        if len(raw_data_list) != 4:
            raise ValueError(f"Malformed data: {timestamp} <sequence_number> <timestamp> <type> <details>")
        
        raw_sequence_number = raw_data_list[0]
        raw_timestamp = raw_data_list[1]
        raw_type = raw_data_list[2]
        raw_details = raw_data_list[3]

        # Parse order details
        order_info = raw_details.split("|")
        order_dict = {}
        for item in order_info:
            if ":" not in item:
                raise ValueError(f"Malformed data: {order_info} <details> value missing")
            
            key, value = item.split(":", 1)

            if not value:
                raise ValueError(f"Malformed data: {order_info} <details> value missing")
            
            order_dict[key] = value
        
        required_keys = {"OrderID", "Side", "Price", "Lots"}
        if not required_keys.issubset(order_dict.keys()):
            raise ValueError(f"Malformed order data: {order_info} <details> missing fields")

        # Parse timestamp and handle exceptions
        try:
            timestamp_ns = time_to_nanoseconds(raw_timestamp)
        except ValueError as e:
            print(f"Error parsing timestamp: {e}")
            return -1  # Return -1 or any default value indicating failure

        # Handle cross-day offset
        if timestamp_ns < last_timestamp:
            current_day += 1

        last_timestamp = timestamp_ns
        
        return timestamp_ns + current_day * 86400 * int(1e9)
    
    except ValueError as e:
        print(f"Error processing record: {e}")
        return -1  # Return -1 to indicate that this record has an error and can be skipped

def time_to_nanoseconds(raw_time):
    # Split the time into hours, minutes, seconds, and nanoseconds
    processed_list = raw_time.split(":")

    # Check if time format is correct
    if len(processed_list) != 3:
        raise ValueError(f"Malformed order data: {raw_time} Invalid timestamp format")
    
    h, m, s = processed_list
    s, ns = s.split(".")

    # Convert time to nanoseconds
    return (int(h) * 3600 + int(m) * 60 + int(s)) * int(1e9) + int(ns)

def detect_throttle_violations(filename):
    violations = []
    window = deque() 

    with open(filename, 'r') as file:
        for line in file:
            timestamp = parse_timestamp(line)

            if timestamp == -1:
                violations.append(line)
                continue
            
            while window and timestamp - window[0] >= 1e9:
                window.popleft()

            window.append(timestamp)

            if len(window) > 4:
                violations.append(line)
                window.pop()

    return violations

class TestThrottleViolations(unittest.TestCase):

### violated logs are in the list of "violations_log", print out if it is necessary
    def test_empty(self):
        print("==================Test 1==================")
        violations_log = detect_throttle_violations("./Q1_testcase/Q1_test_empty_file.txt")
        self.assertEqual(violations_log, [])

    def test_no_violation_exact_boundary(self):
        print("==================Test 2==================")
        violations_log = detect_throttle_violations("./Q1_testcase/Q1_test_no_violation.txt")
        self.assertEqual(violations_log, [])

    def test_one_violation(self):
        print("==================Test 3==================")
        violations_log = detect_throttle_violations("./Q1_testcase/Q1_test_one_violation.txt")
        self.assertEqual(len(violations_log), 1)

    def test_cross_day_violation(self):
        print("==================Test 4==================")
        violations_log = detect_throttle_violations("./Q1_testcase/Q1_test_cross_day.txt")
        self.assertEqual(violations_log, [])

    def test_malformed_entries(self):
        print("==================Test 5==================")
        violations_log = detect_throttle_violations("./Q1_testcase/Q1_test_dirty_data.txt")
        self.assertEqual(len(violations_log), 6)
    
    def test_a_log_file(self):
        print("==================Test 6==================")
        violations_log = detect_throttle_violations("./Q1_testcase/Q1_test_large_file.txt")
        self.assertEqual(len(violations_log), 17)

    def run(self, result=None):
        super().run(result)
        if result.wasSuccessful():
            print("Test Success")


if __name__ == '__main__':
    unittest.main()