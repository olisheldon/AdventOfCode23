from collections import OrderedDict, defaultdict
import string

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
        return value
    
    @staticmethod
    def preprocess_strings(lines: list[str]) -> list[int]:
        new_lines = []
        for line in lines:
            new_lines.append(Day1.string_preprocessing(line))
        return new_lines
    
    @staticmethod
    def string_preprocessing(line: str) -> int:
        min_char_string_length = min([len(key) for key in Day1.char_string_map])
        max_char_string_length = max([len(key) for key in Day1.char_string_map])
        new_line = []
        l, r = 0, min_char_string_length
        while l < len(line):
            if line[l] in string.digits:
                new_line.append(int(line[l]))
            else:
                for number in Day1.char_string_map:
                    r = l + min_char_string_length
                    while r - l <= max_char_string_length:
                        if r > len(line):
                            r = len(line)
                        print(l, r, line[l:r], number)
                        if number == line[l:r]:
                            new_line.append(Day1.char_string_map[number])
                            l = r
                            r = l + min_char_string_length
                            break
                        r += 1
            l += 1
            r = l + min_char_string_length
        return new_line

        # for line in lines:
        #     digit_pos = 1
        #     while digit_pos:
        #         digit_strings = defaultdict(list)
        #         for digit in Day1.char_string_map:
        #             digit_pos = line.find(digit)
        #             if digit_pos:
        #                 digit_strings[digit_pos].append(digit)
        #         if digit_strings:
        #             for i in len(line):
        #                 if i in digit_strings:
        #                     line = line[:i] + str(digit_strings) + line[i + len(Day1.char_string_map[digit_strings]):]

            
                    


                
                


    @staticmethod
    def sum_outer_strings(lines: list[str]) -> int:
        pass


    @staticmethod
    def get_input() -> list[str]:
        with open("input.txt", 'r') as f:
            lines = f.read().splitlines()
        return lines

if __name__ == '__main__':
    day1 = Day1()
    print(day1.string_preprocessing("9sixsevenz3"))

    