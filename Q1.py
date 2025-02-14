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

def detect_throttle_violations(log_lines):
    violations = []
    window = deque() 

    for line in log_lines:
        timestamp = parse_timestamp(line)

        if timestamp == -1:
            violations.append(line)
            continue
        
        while window and timestamp - window[0] >= 1e9:
            window.popleft()

        window.append(timestamp)

        if len(window) > 4:
            violations.append(line)

    return violations

class TestThrottleViolations(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(detect_throttle_violations([]), [])

    def test_no_violation_exact_boundary(self):
        test_data = [
            "000020 10:15:00.100000000 [ORDER] OrderID:CAA|Side:Buy|Price:3.67|Lots:1",
            "000021 10:15:00.300000000 [ORDER] OrderID:CAB|Side:Sell|Price:3.69|Lots:1",
            "000022 10:15:00.500000000 [ORDER] OrderID:CAC|Side:Buy|Price:3.68|Lots:1",
            "000023 10:15:00.900000000 [ORDER] OrderID:CAD|Side:Sell|Price:3.70|Lots:1",
            "000024 10:15:01.100000000 [ORDER] OrderID:CAE|Side:Buy|Price:3.71|Lots:1",
        ]
        self.assertEqual(detect_throttle_violations(test_data), [])

    def test_one_violation(self):
        test_data = [
            "000001 09:31:03.100000000 [ORDER] OrderID:AAA|Side:Buy|Price:3.67|Lots:1",
            "000002 09:31:03.300000000 [ORDER] OrderID:AAB|Side:Sell|Price:3.69|Lots:1",
            "000003 09:31:03.500000000 [ORDER] OrderID:AAC|Side:Buy|Price:3.68|Lots:1",
            "000004 09:31:03.700000000 [ORDER] OrderID:AAD|Side:Sell|Price:3.70|Lots:1",
            "000005 09:31:03.900000000 [ORDER] OrderID:AAE|Side:Buy|Price:3.71|Lots:1",
            "000006 09:31:04.100000000 [ORDER] OrderID:AAF|Side:Sell|Price:3.72|Lots:1",
        ]
        self.assertEqual(len(detect_throttle_violations(test_data)), 2)

    def test_cross_day_violation(self):
        test_data = [
            "000011 23:59:59.500000000 [ORDER] OrderID:BAB|Side:Sell|Price:3.69|Lots:1",
            "000012 00:00:00.200000000 [ORDER] OrderID:BAC|Side:Buy|Price:3.68|Lots:1",
            "000013 00:00:00.400000000 [ORDER] OrderID:BAD|Side:Sell|Price:3.70|Lots:1",
            "000014 00:00:01.300000000 [ORDER] OrderID:BAE|Side:Buy|Price:3.71|Lots:1",
            "000015 00:00:02.000000000 [ORDER] OrderID:BAF|Side:Sell|Price:3.72|Lots:1",
        ]
        self.assertEqual(detect_throttle_violations(test_data), [])

    def test_malformed_entries(self):
        test_data = [
            "000040 11:30:00.200000000 [ORDER] OrderID:EAA|Side:Buy|Price:3.67|Lots:1",
            "000041 MISSING_TIMESTAMP [ORDER] OrderID:EAB|Side:Sell|Price:3.69|Lots:1",
            "WRONG_FORMAT",
            "000043 11:30:01.100000000 [ORDER] OrderID:EAC|Side:Buy|Price:3.68|Lots:1",
            "000044 11:30:01.500000000 [ORDER] OrderID:EAD|Side:Sell|Price:3.70|Lots:1",
            "000045 11:30:01.600000000 [ORDER] OrderID:EAD|Side:|Price:3.70|Lots:1",
            "000046 11:30:01.700000000 [ORDER] OrderID:EAD|Side|Price:3.70|Lots:1",
            "000047 11:30:01.780000000 [ORDER] OrderID:EAC|Side:Buy|Price:3.68|",
            "000048 11:30:01.790000000 [ORDER] OrderID:EAC|Side:Buy|Price:3.68",
        ]
        self.assertEqual(len(detect_throttle_violations(test_data)), 6)

if __name__ == '__main__':
    unittest.main()