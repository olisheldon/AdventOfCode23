#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <set>
#include <cctype>

class Day1 {


public:
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

    Day1() {
        lines = getLines();
    }

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

    int part1() {
        std::vector<std::vector<int>> processedLines = preprocessStrings();
        return sumOuterNumbers(processedLines);
    }

    std::vector<std::vector<int>> preprocessStrings() {
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

    int sumOuterNumbers(std::vector<std::vector<int>> processedLines) {
        int sum{};
        for (const auto& line : processedLines) {
            sum += 10 * line.front();
            sum += line.back();
        }
        return sum;
    }

};

int main(int argc, char* argv[]) {

    Day1 day1{};

    int result = day1.part1();
    std::cout << "Task 1: " << result << std::endl;
    
    return 1;
}