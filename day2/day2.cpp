#include <bits/stdc++.h> 

enum class dice {
    RED,
    GREEN,
    BLUE
};

class Bag {
    public:
    Bag(const std::string& inputStringIn) : inputString(inputStringIn) {}

    private:
        inputString{};
        std::unordered_map<dice, int> data{};
        static std::unordered_map<dice, int> limit{{dice::RED, 12},
                                                   {dice::GREEN, 13},
                                                   {dice::BLUE, 14}};

        void parse();
};


std::vector<std::string> Bag::parse() {
    inputString
}