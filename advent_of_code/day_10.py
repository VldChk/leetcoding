from collections import deque
from typing import Deque, List, Sequence, Tuple, Union
import pulp

from day_10_input import real_input

# Sample data kept for quick ad-hoc checks
state = (0, 1, 1, 0)
buttons = [(1, 3), (3), (2), (2, 3), (0, 2), (0, 1)]


test_input = [
    ([0, 1, 1, 0], (3,), (1, 3), (2,), (2, 3), (0, 2), (0, 1), [3, 5, 4, 7]),
    ([0, 0, 0, 1, 0], (0, 2, 3, 4), (2, 3), (0, 4), (0, 1, 2), (1, 2, 3, 4), [7, 5, 12, 7, 2]),
    ([0, 1, 1, 1, 0, 1], (0, 1, 2, 3, 4), (0, 3, 4), (0, 1, 2, 4, 5), (1, 2), [10, 11, 11, 5, 10, 5]),
    ([0, 1, 1, 1, 0, 0], (2, 3, 4, 5), (1, 4, 5), (1, 3, 4), (0, 4), [10, 19, 6, 23, 35, 8]),
    ([0, 0, 0, 1], (1,), (1, 3), (0, 1, 2), (0, 2), (3,), [18, 21, 18, 15]),
]

INPUT = real_input

Button = Union[int, Sequence[int]]


def _bfs(queue: Deque[Tuple[Button, Tuple[int, ...]]], state: Sequence[int], buttons: Sequence[Button], memory: set) -> bool:
    target_state = tuple(state)
    current_cycle: List[Tuple[Button, Tuple[int, ...]]] = []
    while queue:
        current_button, current_state = queue.popleft()
        for button in buttons:
            if button == current_button:
                continue
            new_state = list(current_state)
            if isinstance(button, int):
                new_state[button] ^= 1
            else:
                for b in button:
                    new_state[b] ^= 1
            new_state_tuple = tuple(new_state)
            if new_state_tuple == target_state:
                return True
            if new_state_tuple in memory:
                continue
            memory.add(new_state_tuple)
            current_cycle.append((button, new_state_tuple))
    queue.extend(current_cycle)
    return False


def _button_to_vector(button: Button, size: int) -> List[int]:
    vec = [0] * size
    if isinstance(button, int):
        vec[button] = 1
    else:
        for idx in button:
            vec[idx] = 1
    return vec


def _min_presses_ilp(num_counters: int, buttons: Sequence[Button], target: Sequence[int]) -> int:
    effects = [_button_to_vector(btn, num_counters) for btn in buttons]

    # Quick feasibility sanity check: every counter with demand must be covered.
    for idx, needed in enumerate(target):
        if needed and all(effect[idx] == 0 for effect in effects):
            raise ValueError(f"Counter {idx} cannot be reached with available buttons")

    presses = [
        pulp.LpVariable(f"press_{i}", lowBound=0, cat="Integer")
        for i in range(len(buttons))
    ]

    problem = pulp.LpProblem("machine", pulp.LpMinimize)
    problem += pulp.lpSum(presses)

    for counter_idx in range(num_counters):
        problem += pulp.lpSum(
            presses[j] * effects[j][counter_idx] for j in range(len(buttons))
        ) == target[counter_idx]

    status = problem.solve(pulp.PULP_CBC_CMD(msg=False))
    if status != pulp.LpStatusOptimal:
        raise RuntimeError(f"ILP solver failed with status {pulp.LpStatus[status]}")

    return int(round(pulp.value(problem.objective)))


def part_one(input):
    total_count = 0
    for line in input:
        state = line[0]
        buttons = line[1:-1]
        base_state = tuple([0] * len(state))
        queue: Deque[Tuple[Button, Tuple[int, ...]]] = deque([(-1, base_state) for _ in buttons])
        found = False
        iterations = 0
        memory = set()
        while not found:
            iterations += 1
            found = _bfs(queue, state, buttons, memory)
        total_count += iterations
    return total_count


def part_two(input):
    total_count = 0
    for line in input:
        state = line[0]
        voltage = line[-1]  # target counts
        buttons = line[1:-1]
        total_count += _min_presses_ilp(len(state), buttons, voltage)
    return total_count


if __name__ == "__main__":
    print("Part One:", part_one(INPUT))
    print("Part Two:", part_two(INPUT))
