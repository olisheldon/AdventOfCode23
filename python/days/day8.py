from overrides import override
from aoc23_base import DayBase
from enum import StrEnum, auto
from itertools import cycle
from functools import reduce
import math


class MoveInstruction(StrEnum):
    L = auto()
    R = auto()


class Node:

    def __init__(self, node_name: str):
        self.node_name: str = node_name
        self.left: Node
        self.right: Node
        self.starting_node: bool = False
        self.ending_node: bool = False

    def add_left(self, left: 'Node'):
        self.left = left

    def add_right(self, right: 'Node'):
        self.right = right

    def move_once(self, mi: MoveInstruction) -> 'Node':
        match mi:
            case MoveInstruction.L:
                return self.left
            case MoveInstruction.R:
                return self.right
            case _:
                raise RuntimeError(f"{mi} is not a recognised move")


class NodesBase:

    def __init__(self, nodes: list[tuple[str, str, str]], move_instructions: list[MoveInstruction]):
        self.node_instances: list[tuple[Node, str, str]] = [
            (Node(node[0]), node[1], node[2]) for node in nodes]
        node_dict: dict[str, Node] = {
            node[0].node_name: node[0] for node in self.node_instances}
        self.nodes: dict[str, Node] = self._add_nodes(node_dict)
        self.move_instructions = move_instructions
        self.cycle: cycle[MoveInstruction] = cycle(move_instructions)

    def _add_nodes(self, node_dict: dict[str, Node]) -> dict[str, Node]:
        nodes: dict[str, Node] = {}
        for node_instance, left, right in self.node_instances:
            node_instance.add_left(node_dict[left])
            node_instance.add_right(node_dict[right])
            nodes[node_instance.node_name] = node_instance
        return nodes


class Nodes(NodesBase):

    def __init__(self, nodes: list[tuple[str, str, str]], move_instructions: list[MoveInstruction]):
        super().__init__(nodes, move_instructions)

    def move(self, starting_node: Node) -> int:
        curr_node: Node = starting_node

        moves = 0
        while not curr_node.ending_node:
            moves += 1
            curr_node = curr_node.move_once(next(self.cycle))
        return moves


class SimultaneousNodes(NodesBase):

    def __init__(self, nodes: list[tuple[str, str, str]], move_instructions: list[MoveInstruction]):
        super().__init__(nodes, move_instructions)

    def move(self, starting_nodes: list[Node]) -> int:
        moves = 0
        first_hit_per_node = [0] * len(starting_nodes)

        while not all(first_hit_per_node):
            moves += 1
            next_move = next(self.cycle)
            for i in range(len(starting_nodes)):
                starting_nodes[i] = starting_nodes[i].move_once(next_move)
            for i, starting_node in enumerate(starting_nodes):
                if not first_hit_per_node[i] and starting_node.ending_node:
                    first_hit_per_node[i] = moves

        prime_factors = []
        for num_of_moves in first_hit_per_node:
            prime_factors += SimultaneousNodes._prime_factors(num_of_moves)
        return reduce(lambda x, y: x * y, set(prime_factors))

    @staticmethod
    def _prime_factors(n: int) -> list[int]:
        factors: list[int] = []
        while n % 2 == 0:
            n = n // 2

        for i in range(3, int(math.sqrt(n)) + 1, 2):
            while n % i == 0:
                factors.append(i)
                n = n // i
        if n > 2:
            factors.append(n)
        return factors


class Day8(DayBase):

    def __init__(self):
        super().__init__()
        instructions, nodes = self.parse()
        self.instructions: list[MoveInstruction] = [
            MoveInstruction[i] for i in instructions]
        self.nodes: list[tuple[str, str, str]] = nodes

    def parse(self) -> tuple[str, list[tuple[str, str, str]]]:
        instructions: str = str(self.input[0])
        nodes: list[tuple[str, str, str]] = []
        for line in self.input[2:]:
            line_split = line.split()
            nodes.append((line_split[0], line_split[2]
                         [1:-1], line_split[3][:-1]))
        return instructions, nodes

    @override
    def part_1(self) -> int:
        nodes = Nodes(self.nodes, self.instructions)
        for node, _, _ in nodes.node_instances:
            if node.node_name == "AAA":
                node.starting_node = True
                starting_node: Node = node
            if node.node_name == "ZZZ":
                node.ending_node = True
        return nodes.move(starting_node)

    @override
    def part_2(self) -> int:
        simultaneous_nodes = SimultaneousNodes(self.nodes, self.instructions)
        starting_nodes = []
        ending_nodes = []
        for node, _, _ in simultaneous_nodes.node_instances:
            if node.node_name.endswith("A"):
                node.starting_node = True
                starting_nodes.append(node)
            if node.node_name.endswith("Z"):
                node.ending_node = True
                ending_nodes.append(node)
        return simultaneous_nodes.move(starting_nodes)


if __name__ == "__main__":
    day8 = Day8()
    print(day8.part_1())
    print(day8.part_2())
