rotations = [
    "L68",
    "L30",
    "R48",
    "L5",
    "R60",
    "L55",
    "L1",
    "L99",
    "R14",
    "L82",
]

# from day_1_rotations import all_rotations


def calculate_zero_positions(rotations):
    current_position = 50
    count = 0

    for rotation in rotations:
        direction = rotation[0]
        degrees = int(rotation[1:]) % 100
        if direction == "L":
            current_position -= degrees
            if current_position < 0:
                current_position += 100
        else:
            current_position += degrees
            if current_position >= 100:
                current_position -= 100
        if current_position == 0:
            count += 1
    return count


def calculate_rotations_through_zero(rotations):
    current_position = 50
    prev_position = 50
    count = 0

    for rotation in rotations:
        direction = rotation[0]
        degrees = int(rotation[1:]) % 100
        count += int(rotation[1:]) // 100
        prev_position = current_position
        if direction == "L":
            current_position -= degrees
            if current_position < 0:
                current_position += 100
                if prev_position > 0:
                    count += 1
            elif current_position == 0 and prev_position > 0:
                count += 1
        else:
            current_position += degrees
            if current_position >= 100:
                current_position -= 100
                if prev_position > 0:
                    count += 1
            elif current_position == 0 and prev_position > 0:
                count += 1
        #print (current_position, count)
    return count


if __name__ == "__main__":
    result = calculate_rotations_through_zero(rotations)
    print(result)