from collections import deque

current_day = 0
last_timestamp = 0

def parse_timestamp(timestamp: str):
    global current_day, last_timestamp
    
    try:
        # Split the timestamp and check if it's well-formed
        raw_data_list = timestamp.split()
        if len(raw_data_list) != 4:
            raise ValueError("Malformed data")
        
        raw_sequence_number = raw_data_list[0]
        raw_timestamp = raw_data_list[1]
        raw_type = raw_data_list[2]
        raw_details = raw_data_list[3]

        # Parse order details
        order_info = raw_details.split("|")
        order_dict = {}
        for item in order_info:
            if ":" not in item:
                raise ValueError("Malformed order data")
            key, value = item.split(":", 1)
            order_dict[key] = value
        
        required_keys = {"OrderID", "Side", "Price", "Lots"}
        if not required_keys.issubset(order_dict.keys()):
            raise ValueError("Malformed order data: Missing fields")

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
        raise ValueError("Malformed order data: Invalid time format")
    
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

def test_detect_throttle_violations():
    test_empty = []
    violations = detect_throttle_violations(test_empty)
    assert len(violations) == 0, "Test Failed @test_empty"
    
    test_no_violation_exact_boundary = [
        "000020 10:15:00.100000000 [ORDER] OrderID:CAA|Side:Buy|Price:3.67|Lots:1",
        "000021 10:15:00.300000000 [ORDER] OrderID:CAB|Side:Sell|Price:3.69|Lots:1",
        "000022 10:15:00.500000000 [ORDER] OrderID:CAC|Side:Buy|Price:3.68|Lots:1",
        "000023 10:15:00.900000000 [ORDER] OrderID:CAD|Side:Sell|Price:3.70|Lots:1",
        "000024 10:15:01.100000000 [ORDER] OrderID:CAE|Side:Buy|Price:3.71|Lots:1",
    ]
    violations = detect_throttle_violations(test_no_violation_exact_boundary)
    assert len(violations) == 0, "Test Failed @test_no_violation_exact_boundary"
    
    test_one_violation = [
        "000001 09:31:03.100000000 [ORDER] OrderID:AAA|Side:Buy|Price:3.67|Lots:1",
        "000002 09:31:03.300000000 [ORDER] OrderID:AAB|Side:Sell|Price:3.69|Lots:1",
        "000003 09:31:03.500000000 [ORDER] OrderID:AAC|Side:Buy|Price:3.68|Lots:1",
        "000004 09:31:03.700000000 [ORDER] OrderID:AAD|Side:Sell|Price:3.70|Lots:1",
        "000005 09:31:03.900000000 [ORDER] OrderID:AAE|Side:Buy|Price:3.71|Lots:1",
        "000006 09:31:04.100000000 [ORDER] OrderID:AAF|Side:Sell|Price:3.72|Lots:1",
    ]
    violations = detect_throttle_violations(test_one_violation)
    assert len(violations) == 2, "Test Failed @test_one_violation"

    test_cross_day_violation = [
        "000011 23:59:59.500000000 [ORDER] OrderID:BAB|Side:Sell|Price:3.69|Lots:1",
        "000012 00:00:00.200000000 [ORDER] OrderID:BAC|Side:Buy|Price:3.68|Lots:1",
        "000013 00:00:00.400000000 [ORDER] OrderID:BAD|Side:Sell|Price:3.70|Lots:1",
        "000014 00:00:01.300000000 [ORDER] OrderID:BAE|Side:Buy|Price:3.71|Lots:1",
        "000015 00:00:02.000000000 [ORDER] OrderID:BAF|Side:Sell|Price:3.72|Lots:1",
    ]
    violations = detect_throttle_violations(test_cross_day_violation)
    assert len(violations) == 0, "Test Failed @test_cross_day_violation"

    test_rolling_window_violation = [
        "000030 11:00:00.100000000 [ORDER] OrderID:DAA|Side:Buy|Price:3.67|Lots:1",
        "000031 11:00:00.600000000 [ORDER] OrderID:DAB|Side:Sell|Price:3.69|Lots:1",
        "000032 11:00:01.000000000 [ORDER] OrderID:DAC|Side:Buy|Price:3.68|Lots:1",
        "000033 11:00:01.200000000 [ORDER] OrderID:DAD|Side:Sell|Price:3.70|Lots:1",
        "000034 11:00:01.300000000 [ORDER] OrderID:DAE|Side:Buy|Price:3.71|Lots:1",
        "000035 11:00:01.800000000 [ORDER] OrderID:DAG|Side:Sell|Price:3.72|Lots:1",
    ]
    violations = detect_throttle_violations(test_rolling_window_violation)
    assert len(violations) == 0, "Test Failed @test_rolling_window_violation"

    test_malformed_entries = [
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
    violations = detect_throttle_violations(test_malformed_entries)
    assert len(violations) == 5, "Test Failed @test_malformed_entries"

    print("Finish.")

test_detect_throttle_violations()
