#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cctype>

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
    std::cout << result << std::endl;
    
    return 1;
}