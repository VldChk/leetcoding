# from day_6_input import input

test_input = ["123 328  51 64 ", " 45 64  387 23 ", "  6 98  215 314", "*   +   *   + "]


def parse_input(input_lines):
    operations = [op for op in input_lines[-1].strip().split() if op]
    count_of_numbers = len(operations)
    numbers_per_line = []
    for line in input_lines[:-1]:
        line_numbers = [int(num) for num in line.strip().split() if num]
        if len(line_numbers) != count_of_numbers:
            raise ValueError(
                "Mismatch between number of operations and numbers in line."
            )
        numbers_per_line.append(line_numbers)
    numbers = []
    for i in range(len(operations)):
        line = [n[i] for n in numbers_per_line]
        numbers.append(line)
    print(f"Numbers: {numbers}")
    print(f"Operations: {operations}")
    return numbers, operations


def perform_operations(numbers, operations):
    results = []
    for nums, op in zip(numbers, operations):
        if op == "*":
            result = 1
            for n in nums:
                result *= n
        elif op == "+":
            result = sum(nums)
        else:
            raise ValueError(f"Unsupported operation: {op}")
        results.append(result)
    print(f"Results: {results}")
    return sum(results)


def parse_input_part_two(input_lines):
    numbers, operations = parse_input(input_lines)
    len_of_numbers = [max([len(str(n)) for n in nums]) for nums in numbers]
    print(f"Length of numbers per operation: {len_of_numbers}")
    curr_idx = 0
    lines = []
    for line in input_lines[:-1]:
        parsed_line = []
        for i in len_of_numbers:
            segment = line[curr_idx : curr_idx + i]
            parsed_line.append(segment)
            curr_idx += i + 1  # +1 for the space
        lines.append(parsed_line)
        curr_idx = 0
    numbers_str = []
    for i in range(len(operations)):
        line = [n[i] for n in lines]
        numbers_str.append(line)
    print(f"Parsed lines for part two: {numbers_str}")
    return numbers_str, operations


def part_two(numbers, operations):
    results = []
    for nums, op in zip(numbers, operations):
        ln = len(nums[0])
        reconstructed_numbers = [0] * ln
        while ln > 0:
            print(ln, nums)
            for i, n in enumerate(nums):
                if n[ln - 1].isdigit():
                    reconstructed_numbers[ln - 1] = reconstructed_numbers[
                        ln - 1
                    ] * 10 + int(n[ln - 1])
                nums[i] = n[:-1]
            ln -= 1
        print(f"Reconstructed Numbers: {reconstructed_numbers} for operation {op}")
        if op == "*":
            result = 1
            for n in reconstructed_numbers:
                result *= n
        elif op == "+":
            result = sum(reconstructed_numbers)
        else:
            raise ValueError(f"Unsupported operation: {op}")
        results.append(result)
    print(f"Results: {results}")
    return sum(results)


if __name__ == "__main__":
    numbers, operations = parse_input(test_input)
    print(perform_operations(numbers, operations))
    numbers_str, operations = parse_input_part_two(test_input)
    print(part_two(numbers_str, operations))
