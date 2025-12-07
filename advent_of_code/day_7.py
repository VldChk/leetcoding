# from day_7_input import real_input

test_input = [
    ".......S.......",
	"...............",
	".......^.......",
	"...............",
	"......^.^......",
	"...............",
	".....^.^.^.....",
	"...............",
	"....^.^...^....",
	"...............",
	"...^.^...^.^...",
	"...............",
	"..^...^.....^..",
	"...............",
	".^.^.^.^.^...^.",
	"..............."
]

def _bfs(line, queue):
    cycle = []
    counter = 0
    while queue:
        idx = queue.pop(0)
        if line[idx] == ".":
            cycle.append(idx)
            line[idx] = "|"
        elif line[idx] == "^":
            counter += 1
            if idx - 1 >= 0:
                cycle.append(idx - 1)
                line[idx-1] = "|"
            if idx + 1 < len(line):
                cycle.append(idx + 1)
                line[idx+1] = "|"
    queue.extend(cycle)
    return counter, line

def part_one(input_lines):
    total_count = 0
    start_idx = input_lines[0].index("S")
    parsed_input_lines = [input_lines[0][:]]
    queue = [start_idx]
    for line in input_lines[1:]:
        count, new_line = _bfs(list(line), queue)
        total_count += count
        parsed_input_lines.append("".join(new_line))
    # print (f"Parsed lines for part one: {parsed_input_lines}")
    return total_count, parsed_input_lines


debug_counter = 0
memory = {}

def _dfs(input, line_idx, stack) -> int:
    if line_idx >= len(input):
        global debug_counter
        debug_counter += 1
        if debug_counter % 1000 == 0:
            print(f"Reached the end, debug_counter: {debug_counter}")
        return 1
    if (line_idx, stack[-1]) in memory:
        return memory[(line_idx, stack[-1])]
    line = input[line_idx]
    next_idx = stack.pop()
    res = 0
    if line[next_idx] == ".":
        stack.append(next_idx)
        res += _dfs(input, line_idx + 1, stack)

    elif line[next_idx] == "^":
        if next_idx - 1 >= 0:
            stack.append(next_idx - 1)
            res += _dfs(input, line_idx + 1, stack)
        if next_idx + 1 < len(line):
            stack.append(next_idx + 1)
            res += _dfs(input, line_idx + 1, stack)
    memory[(line_idx, next_idx)] = res
    return res



if __name__ == "__main__":
    result, processed_lines = part_one(test_input)
    print(f"Part one result: {result}")
    result_part_two = _dfs(test_input, 1, [test_input[0].index("S")])
    print(f"Part two result: {result_part_two}")