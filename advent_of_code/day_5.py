test_input_ranges = [
    "3-5",
    "10-14",
    "16-20",
    "12-18",
]

test_input_vals = [
    1,
    5,
    8,
    11,
    17,
    32,
]


def process_ranges (ranges):
    processed = []
    for r in ranges:
        start, end = map(int, r.split("-"))
        processed.append((start, end))
    return processed


def find_fresh_products(ranges, values):
    total_count = 0
    for val in values:
        for start, end in ranges:
            if start <= val <= end:
                total_count += 1
                break
    return total_count


def find_all_fresh_products_part_two(ranges):
    merged_ranges = []
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    current_start, current_end = sorted_ranges[0]

    for start, end in sorted_ranges[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            merged_ranges.append((current_start, current_end))
            current_start, current_end = start, end
    merged_ranges.append((current_start, current_end))

    total_count = 0
    for start, end in merged_ranges:
        total_count += (end - start + 1)
    return total_count


if __name__ == "__main__":
    processed_ranges = process_ranges(test_input_ranges)
    part_two_result = find_all_fresh_products_part_two(processed_ranges)
    print(part_two_result)