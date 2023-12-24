class Day1:

    char_string_map = {"one"   : 1,
                       "two"   : 2,
                       "three" : 3,
                       "four"  : 4,
                       "five"  : 5,
                       "six"   : 6,
                       "seven" : 7,
                       "eight" : 8,
                       "nine"  : 9,
                       }

    inverse_char_string_map = {k[::-1] : v for k, v in char_string_map.items()}

    def __init__(self):
        self.input = Day1.get_input()

    def part_1(self) -> int:
        return Day1.sum_outer_numbers(self.input)
    
    def part_2(self) -> int:
        pass

    @staticmethod
    def sum_outer_numbers(lines: list[str]) -> int:
        value = 0
        for line in lines:
            for c in line:
                if c.isdigit():
                    value += 10 * int(c)
                    break
            for c in line[::-1]:
                if c.isdigit():
                    value += int(c)
                    break
        return 
    
    @staticmethod
    def string_preprocessing(lines: list[str]) -> list[str]:
        min_char_string_length = min([key for key in Day1.char_string_map])
        max_char_string_length = max([key for key in Day1.char_string_map])
        new_lines = []
        new_line = []
        for line in lines:
            l, r = 0, 3
            while r - l + 1 < max_char_string_length:
                for digit in Day1.char_string_map:
                    pos = line[l:r].find(digit)
                    if pos:
                        new_line += Day1.char_string_map[digit]
                        
                r += 1
            l += 1
            r = l + 2

                
                


    @staticmethod
    def sum_outer_strings(lines: list[str]) -> int:


    @staticmethod
    def get_input() -> list[str]:
        with open("input.txt", 'r') as f:
            lines = f.readlines()
        return lines

if __name__ == '__main__':
    pass
    