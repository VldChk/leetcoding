import math
# from day_8_input import real_input

test_input = [
    (162, 817, 812),
    (57, 618, 57),
    (906, 360, 560),
    (592, 479, 940),
    (352, 342, 300),
    (466, 668, 158),
    (542, 29, 236),
    (431, 825, 988),
    (739, 650, 466),
    (52, 470, 668),
    (216, 146, 977),
    (819, 987, 18),
    (117, 168, 530),
    (805, 96, 715),
    (346, 949, 466),
    (970, 615, 88),
    (941, 993, 340),
    (862, 61, 35),
    (984, 92, 344),
    (425, 690, 689),
]


def sort_by_distance(point1, point2):
    dist = math.sqrt(sum([(point1[i] - point2[i]) ** 2 for i in range(len(point1))]))

    return dist


def generate_all_possible_pairs(points_input):
    all_possible_pairs = list(
        set(
            [
                tuple(sorted([points_input[i], points_input[j]]))
                for i in range(len(points_input))
                for j in range(len(points_input))
                if i != j
            ]
        )
    )

    all_possible_pairs.sort(key=lambda pair: sort_by_distance(pair[0], pair[1]))
    # print(len(all_possible_pairs))
    return all_possible_pairs


def part_one(all_possible_pairs, break_point):

    circuits = []
    i = 0

    while i < break_point:
        point1, point2 = all_possible_pairs[i]
        other_points_circuit = set()
        for circuit in circuits:
            if point1 in circuit:
                if not other_points_circuit:
                    circuit.add(point2)
                    other_points_circuit = circuit
                else:
                    other_points_circuit.update(circuit)
                    circuits.remove(circuit)
            elif point2 in circuit:
                if not other_points_circuit:
                    circuit.add(point1)
                    other_points_circuit = circuit
                else:
                    other_points_circuit.update(circuit)
                    circuits.remove(circuit)
        if not other_points_circuit:
            circuits.append(set([point1, point2]))
        i += 1
    # print(f"Circuits: {circuits}")
    circuits.sort(key=lambda c: -len(c))
    # print([len(circuit) for circuit in circuits[:3]])
    return math.prod(len(circuit) for circuit in circuits[:3])


def part_two(all_possible_pairs, break_point):
    circuits = []
    i = 0
    while True:
        point1, point2 = all_possible_pairs[i]
        other_points_circuit = set()
        for circuit in circuits:
            if point1 in circuit:
                if not other_points_circuit:
                    circuit.add(point2)
                    other_points_circuit = circuit
                else:
                    other_points_circuit.update(circuit)
                    circuits.remove(circuit)
            elif point2 in circuit:
                if not other_points_circuit:
                    circuit.add(point1)
                    other_points_circuit = circuit
                else:
                    other_points_circuit.update(circuit)
                    circuits.remove(circuit)
        if not other_points_circuit:
            circuits.append(set([point1, point2]))
        i += 1
        circuits.sort(key=lambda c: -len(c))
        if len(circuits[0]) >= break_point:
            return point1[0] * point2[0]


if __name__ == "__main__":
    all_possible_pairs = generate_all_possible_pairs(test_input)
    break_point = len(test_input)
    print(part_one(all_possible_pairs, 10))
    print(part_two(all_possible_pairs, break_point))
