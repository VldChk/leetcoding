from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Optional, Tuple
from day_9_input import real_input
from functools import cached_property

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_tuple(cls, t):
        return cls(t[0], t[1])

    def to_tuple(self):
        return (self.x, self.y)


@dataclass(frozen=True)
class Wall:
    position: int
    range: tuple[int, int]
    end_position: int


@dataclass(frozen=True)
class PointsPair:
    p1: Point
    p2: Point

    @cached_property
    def area(self) -> int:
        return calc_space_square(self.p1, self.p2)

    @cached_property
    def corners(self) -> Tuple[Point, Point, Point, Point]:
        return identify_orientation(self.p1, self.p2)


test_input = [
    Point(7, 1),
    Point(11, 1),
    Point(11, 7),
    Point(9, 7),
    Point(9, 5),
    Point(2, 5),
    Point(2, 3),
    Point(7, 3),
]

INPUT = [Point.from_tuple(p) for p in real_input]


def calc_space_square(point1, point2):
    # type: (Point, Point) -> int
    return (abs(point1.x - point2.x) + 1) * (abs(point1.y - point2.y) + 1)


def generate_all_possible_pairs(points_input: Iterable[Point]) -> List[PointsPair]:
    pairs = [PointsPair(a, b) for a, b in combinations(points_input, 2)]
    pairs.sort(key=lambda pair: pair.area, reverse=True)
    return pairs


def build_lines(points_input: List[Point]) -> Tuple[Dict[int, List[Tuple[int, int]]], Dict[int, List[Tuple[int, int]]]]:
    def _add_segment(
        p1: Point,
        p2: Point,
        horizontal_lines: Dict[int, List[Tuple[int, int]]],
        vertical_lines: Dict[int, List[Tuple[int, int]]],
    ) -> None:
        if p1.x == p2.x:
            x = p1.x
            y_start = min(p1.y, p2.y)
            y_end = max(p1.y, p2.y)
            if x not in vertical_lines:
                vertical_lines[x] = []
            vertical_lines[x].append((y_start, y_end))
        elif p1.y == p2.y:
            y = p1.y
            x_start = min(p1.x, p2.x)
            x_end = max(p1.x, p2.x)
            if y not in horizontal_lines:
                horizontal_lines[y] = []
            horizontal_lines[y].append((x_start, x_end))

    horizontal_lines = {}
    vertical_lines = {}
    prev_point = points_input[0]
    for point in points_input[1:]:
        _add_segment(prev_point, point, horizontal_lines, vertical_lines)
        prev_point = point
    # wrap-around segment between last and first point (the outline is a closed loop)
    _add_segment(prev_point, points_input[0], horizontal_lines, vertical_lines)
    return horizontal_lines, vertical_lines


def identify_orientation(point1: Point, point2: Point) -> Tuple[Point, Point, Point, Point]:
    left_upper = None
    right_lower = None
    left_lower = None
    right_upper = None
    if point1.x <= point2.x: #point1 is left to point2
        if point1.y <= point2.y: # point1 is upper to point2
            left_upper = point1
            right_lower = point2
            left_lower = Point(point1.x, point2.y)
            right_upper = Point(point2.x, point1.y)
        else: # point1 is lower to point2
            left_lower = point1
            right_upper = point2
            left_upper = Point(point1.x, point2.y)
            right_lower = Point(point2.x, point1.y)
    else: # point2 is left to point1
        if point2.y <= point1.y: # point2 is upper to point1
            left_upper = point2
            right_lower = point1
            left_lower = Point(point2.x, point1.y)
            right_upper = Point(point1.x, point2.y)
        else: # point2 is lower to point1
            left_lower = point2
            right_upper = point1
            left_upper = Point(point2.x, point1.y)
            right_lower = Point(point1.x, point2.y)

    return left_upper, right_lower, left_lower, right_upper


def point_in_or_on_polygon(
    point: Point,
    horizontal_lines: Dict[int, List[Tuple[int, int]]],
    vertical_lines: Dict[int, List[Tuple[int, int]]],
) -> bool:
    x, y = point.x, point.y

    # Check if the point lies on any edge.
    if x in vertical_lines:
        for y_start, y_end in vertical_lines[x]:
            if y_start <= y <= y_end:
                return True
    if y in horizontal_lines:
        for x_start, x_end in horizontal_lines[y]:
            if x_start <= x <= x_end:
                return True

    # Ray cast to the right; even/odd rule.
    crossings = 0
    for x_v, segments in vertical_lines.items():
        if x_v > x:
            for y_start, y_end in segments:
                if y_start <= y < y_end:
                    crossings += 1
    return crossings % 2 == 1


def check_line_doesnt_cross_lines(
    line: Wall,
    horizontal_lines: Dict[int, List[Tuple[int, int]]],
    vertical_lines: Dict[int, List[Tuple[int, int]]],
    direction: str,
) -> bool:
    if direction in ("left", "right"):
        x = line.position
        y_start, y_end = line.range
        y_low, y_high = sorted((y_start, y_end))
        for y in [k for k in horizontal_lines if y_low < k < y_high]:
            for x_start, x_end in horizontal_lines[y]:
                if x_start < x < x_end:
                    return False
    else:  # up or down
        y = line.position
        x_start, x_end = line.range
        x_low, x_high = sorted((x_start, x_end))
        for x in [k for k in vertical_lines if x_low < k < x_high]:
            for y_start, y_end in vertical_lines[x]:
                if y_start < y < y_end:
                    return False
    return True


def part_two(
    all_possible_pairs: Iterable[PointsPair],
    horizontal_lines: Dict[int, List[Tuple[int, int]]],
    vertical_lines: Dict[int, List[Tuple[int, int]]],
) -> Optional[int]:
    for pair in all_possible_pairs:
        left_upper, right_lower, left_lower, right_upper = pair.corners
        walls = {
            "down": Wall(left_upper.y, (left_upper.x, right_upper.x), left_lower.y),
            "up": Wall(left_lower.y, (left_lower.x, right_lower.x), left_upper.y),
            "right": Wall(left_upper.x, (left_upper.y, left_lower.y), right_upper.x),
            "left": Wall(right_upper.x, (right_upper.y, right_lower.y), left_upper.x),
        }
        
        if left_upper not in INPUT and not point_in_or_on_polygon(left_upper, horizontal_lines, vertical_lines):
            continue
        if right_lower not in INPUT and not point_in_or_on_polygon(right_lower, horizontal_lines, vertical_lines):
            continue
        if left_lower not in INPUT and not point_in_or_on_polygon(left_lower, horizontal_lines, vertical_lines):
            continue
        if right_upper not in INPUT and not point_in_or_on_polygon(right_upper, horizontal_lines, vertical_lines):
            continue

        # All corners are valid; now ensure rectangle edges stay inside outline.
        if all(
            [
                check_line_doesnt_cross_lines(
                    walls[direction],
                    horizontal_lines,
                    vertical_lines,
                    direction,
                )
                for direction in walls
            ]
        ):
            return pair.area
    return None


if __name__ == "__main__":
    all_possible_pairs = generate_all_possible_pairs(INPUT)
    print(all_possible_pairs[0].area)
    print(part_two(all_possible_pairs, *build_lines(INPUT)))
