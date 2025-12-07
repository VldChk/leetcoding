# from collections import deque
# from day_3_input import batteries

test_input = [
    987654321111111,
    811111111111119,
    234234234234278,
    818181911112111,
]

def largest_battery_part_one(batteries):
    total_count = 0
    for battery in batteries:
        battery_str = str(battery)
        max_digit = int(battery_str[0])
        max_sum = 0
        for i in range(1, len(battery_str)):
            current_digit = int(battery_str[i])
            if max_digit * 10 + current_digit > max_sum:
                max_sum = max_digit * 10 + current_digit
            if current_digit > max_digit:
                max_digit = current_digit
        total_count += max_sum
    return total_count


def largest_battery_part_two(batteries):
    def _sum_queue(queue):
        total = 0
        for idx, val in enumerate(reversed(queue)):
            total += val * (10 ** idx)
        return total
    total_count = 0
    for battery in batteries:
        battery_str = str(battery)
        max_digits = [int(battery_str[0])]
        max_sum = 0
        for i in range(1, len(battery_str)):
            current_digit = int(battery_str[i])
            if len(max_digits) < 12:
                max_digits.append(current_digit)
                max_sum = max(max_sum, _sum_queue(max_digits))
            else:
                curr_idx = 1
                while curr_idx < 12:
                    if max_digits[curr_idx] > max_digits[curr_idx - 1]:
                        max_digits.pop(curr_idx - 1)
                        max_digits.append(current_digit)
                        break
                    if curr_idx == 11:
                        if current_digit > max_digits[11]:
                            max_digits.pop()
                            max_digits.append(current_digit)
                    curr_idx += 1
                max_sum = max(max_sum, _sum_queue(max_digits))
        print(f"Battery: {battery}, Max Sum: {max_sum}")
        total_count += max_sum
    return total_count

if __name__ == "__main__":
    print(largest_battery_part_one(test_input))
    print(largest_battery_part_two(test_input))