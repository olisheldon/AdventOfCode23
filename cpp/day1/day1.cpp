#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <string>
#include <unordered_map>

class Day1 {

public:

    Day1() {
        lines = getLines();
    }

    int part1() {
        std::vector<std::vector<int>> processedLines = preprocessStringsPart1();
        return sumOuterNumbers(processedLines);
    }

    int part2() {
        std::vector<std::vector<int>> processedLines = preprocessStringsPart2();
        return sumOuterNumbers(processedLines);
    }

private:

    std::vector<std::string> lines;
    std::unordered_map<std::string, int> wordsToInt{{"one",   1},
                                                    {"two",   2},
                                                    {"three", 3},
                                                    {"four",  4},
                                                    {"five",  5},
                                                    {"six",   6},
                                                    {"seven", 7},
                                                    {"eight", 8},
                                                    {"nine",  9}};
    std::vector<std::string> words = {"one",
                                      "two",
                                      "three",
                                      "four",
                                      "five",
                                      "six",
                                      "seven",
                                      "eight",
                                      "nine"};

    std::vector<char> digits = {'1',
                                '2',
                                '3',
                                '4',
                                '5',
                                '6',
                                '7',
                                '8',
                                '9'};

    std::vector<std::string> getLines() {
        std::ifstream myfile("input.txt");
        std::string line;
        std::vector<std::string> input;
        while (std::getline(myfile, line))
        {
            input.push_back(line);
        }
        return input;
    }

    std::vector<std::vector<int>> preprocessStringsPart1() {
        std::vector<std::vector<int>> processedLines{};
        std::vector<int> processedLine{};
        for (const auto& line : lines) {
            processedLine = {};
            for (const auto& c : line) {
                if (std::isdigit(c)) {
                    processedLine.push_back(static_cast<int>(c - '0'));
                }
            }
            processedLines.push_back(processedLine);
        }
        return processedLines;
    }

    std::vector<std::vector<int>> preprocessStringsPart2() {
        std::vector<std::vector<int>> processedLines{};
        int l;
        std::vector<int> processedLine;
        for (const auto& line : lines) {
            processedLine = {};
            l = {};
            while (l < line.size()) {
                if (std::find(digits.begin(), digits.end(), line[l]) != std::end(digits))
                    processedLine.push_back(static_cast<int>(line[l] - '0'));
                else {
                    int answer = isStringRangeValid(line, l);
                    if (answer != 0) 
                        processedLine.push_back(answer);
                }
                l++;
            }
            processedLines.push_back(processedLine);
        }
        return processedLines;
    }

    int isStringRangeValid(std::string line, int l) {
        int r = l + 2;
        while (r - l <= 5 && r < line.size() + 1) {
            if (wordsToInt.find( line.substr(l, r - l + 1) ) != wordsToInt.end())
                return wordsToInt.at(line.substr(l, r - l + 1));
            r++;
        }
        return 0;
    }

    int sumOuterNumbers(std::vector<std::vector<int>> processedLines) {
        int sum{};
        for (const auto& line : processedLines) {
            sum += 10 * line.front() + line.back();
        }
        return sum;
    }

};

int main(int argc, char* argv[]) {

    Day1 day1{};

    std::cout << "C++ Solution:" << std::endl;
    std::cout << "\tPart 1: " << day1.part1() << std::endl;
    std::cout << "\tPart 2: " << day1.part2() << std::endl;
}