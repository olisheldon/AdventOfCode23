from overrides import override
from aoc23_base import DayBase
from enum import Enum, auto
from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
import math

        
@dataclass
class Position:
    x: int
    y: int
    z: int
        
@dataclass
class Velocity:
    x: int
    y: int
    z: int
        
class Hailstone:

    def __init__(self, position: Position, velocity: Velocity):

        self.position: Position = position
        self.velocity: Velocity = velocity

    def __repr__(self) -> str:
        return f"Hailstone(position={self.position}, velocity={self.velocity})"

    @classmethod
    def from_str(cls, halistone_str: str) -> 'Hailstone':
        position_str, velocity_str = halistone_str.split(' @ ')
        return Hailstone(Position(*map(int, position_str.split(', '))), Velocity(*map(int, velocity_str.split(', '))))
    
    def linearize(self) -> tuple[float, float, float]:
        '''
        Returns hailstone in form ax + by = c for solving
        '''
        return (self.velocity.y , -self.velocity.x, self.velocity.y * self.position.x - self.velocity.x * self.position.y)
    
    def does_intersect(self, other: 'Hailstone', x_lower_bound: int = 200000000000000, x_upper_bound: int = 400000000000000, y_lower_bound: int = 200000000000000, y_upper_bound: int = 400000000000000):
        a1, b1, c1 = self.linearize()
        a2, b2, c2 = other.linearize()

        if a1 * b2 == b1 * a2:
            return False
        
        x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
        y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)

        if x_lower_bound <= x <= x_upper_bound and y_lower_bound <= y <= y_upper_bound:
            if all(hailstone.collides_in_future(x, y) for hailstone in (self, other)):
                return True
        return False
    
    def collides_in_future(self, collision_position_x: float, collision_position_y: float, ) -> bool:
        return (collision_position_x - self.position.x) * self.velocity.x >= 0 and (collision_position_y - self.position.y) * self.velocity.y >= 0
    
class Day24(DayBase):
    
    def __init__(self):
        super().__init__()
        self.hailstones: list[Hailstone] = [Hailstone.from_str(hailstone_str) for hailstone_str in self.parse()]

    def parse(self) -> list[str]:
        return self.input
                      
    @override
    def part_1(self) -> int:
        return sum(hailstone1.does_intersect(hailstone2) for (i, hailstone1) in enumerate(self.hailstones) for hailstone2 in self.hailstones[:i])

    @override
    def part_2(self) -> int:
        pass

if __name__ == "__main__":
    day24 = Day24()
    print(day24.part_1())
    print(day24.part_2())
