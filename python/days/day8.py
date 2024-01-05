from overrides import override
from aoc23_base import DayBase
from enum import StrEnum, auto
from itertools import cycle

class MoveInstruction(StrEnum):
    L = auto(),
    R = auto()

class Node:

    def __init__(self, node_name):
        self.node_name: str = node_name
        self.left: Node
        self.right: Node

    
    def add_left(self, left: 'Node'):
        self.left = left
    
    def add_right(self, right: 'Node'):
        self.right = right

class Nodes:

    def __init__(self, nodes: list[tuple[str, str, str]]):
        node_mapping = [(Node(node[0]), node[1], node[2]) for node in nodes]
        node_dict = {node[0].node_name : node[0] for node in node_mapping}
        self.nodes: dict[str, Node] = self._add_nodes(node_mapping, node_dict)

    def _add_nodes(self, node_mapping: list[tuple[Node, str, str]], node_dict: dict[str, Node]) -> dict[str, Node]:
        nodes: dict[str, Node] = {}
        for node_instance, left, right in node_mapping:
            node_instance.add_left(node_dict[left])
            node_instance.add_right(node_dict[right])
            nodes[node_instance.node_name] = node_instance
        return nodes
    
    def move(self, move_instructions: list[MoveInstruction], starting_node: str) -> int:
        cycle_move_instructions: cycle = cycle(move_instructions)
        curr_node: Node = self.nodes[starting_node]

        moves = 0
        while curr_node.node_name != "ZZZ": 
            moves += 1
            n = next(cycle_move_instructions)
            match n:
                case MoveInstruction.L:
                    curr_node = curr_node.left
                case MoveInstruction.R:
                    curr_node = curr_node.right
                case _:
                    raise RuntimeError(f"{n} is not a recognised move")
        return moves
    
class Day8(DayBase):
    
    def __init__(self):
        super().__init__()
        instructions, nodes = self.parse()
        self.instructions: list[MoveInstruction] = [MoveInstruction[i] for i in instructions]
        self.nodes: Nodes = Nodes(nodes)


    def parse(self) -> tuple[str, list[tuple[str, str, str]]]:
        instructions: str = str(self.input[0])
        nodes: list[tuple[str, str, str]] = []
        for line in self.input[2:]:
            line_split = line.split()
            nodes.append((line_split[0], line_split[2][1:-1], line_split[3][:-1]))
        return instructions, nodes

    
    @override
    def part_1(self) -> int:
        return self.nodes.move(self.instructions, "AAA")



    @override
    def part_2(self) -> int:
        pass
    
if __name__ == "__main__":
    day8 = Day8()
    print(day8.part_1())
    print(day8.part_2())
