from overrides import override
from aoc23_base import DayBase
from enum import StrEnum, auto
from itertools import cycle
class MoveInstruction(StrEnum):
    L = auto(),
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
                curr_node = self.left
            case MoveInstruction.R:
                curr_node = self.right
            case _:
                raise RuntimeError(f"{mi} is not a recognised move")
        return curr_node

class NodesBase:

    def __init__(self, nodes: list[tuple[str, str, str]], move_instructions: list[MoveInstruction]):
        self.node_instances = [(Node(node[0]), node[1], node[2]) for node in nodes]
        node_dict = {node[0].node_name : node[0] for node in self.node_instances}
        self.nodes: dict[str, Node] = self._add_nodes(node_dict)
        self.move_instructions = move_instructions

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
        cycle_move_instructions: cycle = cycle(self.move_instructions)
        curr_node: Node = starting_node

        moves = 0
        while not curr_node.ending_node: 
            moves += 1
            mi = next(cycle_move_instructions)
            curr_node = curr_node.move_once(mi)
        return moves
    
class SimultaneousNodes(NodesBase):

    def __init__(self, nodes: list[tuple[str, str, str]], move_instructions: list[MoveInstruction]):
        super().__init__(nodes, move_instructions)

    def move(self, starting_nodes: list[Node]) -> int:
        cycle_move_instructions: cycle = cycle(self.move_instructions)
        # starting_nodes: list[Node] = [node for (node_str, node) in self.nodes.items() if node_str.endswith("A")]
        moves = 0
        while (not all(starting_node.ending_node for starting_node in starting_nodes)):
            moves += 1
            next_move = next(cycle_move_instructions)
            for starting_node in starting_nodes:
                starting_node.move_once(next_move)
        return moves
    
class Day8(DayBase):
    
    def __init__(self):
        super().__init__()
        instructions, nodes = self.parse()
        self.instructions: list[MoveInstruction] = [MoveInstruction[i] for i in instructions]
        self.nodes: list[tuple[str, str, str]] = nodes


    def parse(self) -> tuple[str, list[tuple[str, str, str]]]:
        instructions: str = str(self.input[0])
        nodes: list[tuple[str, str, str]] = []
        for line in self.input[2:]:
            line_split = line.split()
            nodes.append((line_split[0], line_split[2][1:-1], line_split[3][:-1]))
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
