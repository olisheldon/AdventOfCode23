#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <set>
#include <cctype>

int sumOuterStrings(std::vector<std::string> input) {
    std::unordered_map<std::string, int> wordsToInt{{"one",   1},
                                                    {"two",   2},
                                                    {"three", 3},
                                                    {"four",  4},
                                                    {"five",  5},
                                                    {"six",   6},
                                                    {"seven", 7},
                                                    {"eight", 8},
                                                    {"nine",  9}};
    std::vector<std::string> words;
    for (const auto& pair : wordsToInt) {
        words.push_back(pair.first);
    }

    int sum{};
    std::vector<int> integers;
    for (const auto& line : input) {
        for (const auto& word : words) {
            int pos{};
            while (pos < line.size()){
                pos = line.find(word);
                if (pos != std::string::npos) {
                    integers.push_back(wordsToInt[word]);
                }
            }
        }
    }
    return sum;
}

int sumOuterNumbers(std::vector<std::string> input) {
    int sum{};
    for (const auto& line : input) {
        for (const char& c : line) {
            if (std::isdigit(c)) {
                sum += 10 * static_cast<int>(c - '0');
                break;
            }
        }
        for (auto it = line.crbegin(); it != line.crend(); ++it) {
            if (std::isdigit(*it)) {
                sum += static_cast<int>(*it - '0');
                break;
            }
        }
    }
    return sum;
}

int main(int argc, char* argv[]) {
    std::ifstream myfile("input.txt");
    std::string line;
    std::vector<std::string> myLines;
    while (std::getline(myfile, line))
    {
        myLines.push_back(line);
    }

    int result = sumOuterNumbers(myLines);
    std::cout << "Task 1: " << result << std::endl;
    
    return 1;
}