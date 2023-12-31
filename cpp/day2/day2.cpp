#include <unordered_map>
#include <set>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <iterator>
#include <numeric>

#include <iostream>

namespace DiceEnum {

    enum Type {
        RED,
        GREEN,
        BLUE
    };

    static const Type All[] = {RED,
                            GREEN,
                            BLUE
    };

    static const std::unordered_map<char, Type> charToDiceType {{'r', RED},
                                                                {'g', GREEN},
                                                                {'b', BLUE}};

};

class DiceMap {
public:

    static const std::unordered_map<DiceEnum::Type, int> maximum_bag_contents;

    const bool valid() {
        for ( const auto dieType : DiceEnum::All ) {
            if (mDiceMap.at(dieType) > DiceMap::maximum_bag_contents.at(dieType)) {
                return false;
            }
        }
        return true;
    }

    void update_max(DiceMap diceSet) {
        for ( const auto dieType : DiceEnum::All ) {
            if (diceSet.getDiceMap().at(dieType) > mDiceMap.at(dieType)) {
                mDiceMap[dieType] = diceSet.getDiceMap()[dieType];
        }
    }
    }

    std::unordered_map<DiceEnum::Type, int> getDiceMap() {
        return mDiceMap;
    }

    int getMaxRequiredNumOfDice() {
        int sum{};
        for (auto const& [dieType, num] : maximum_bag_contents) {
            sum += num;
        }
        return sum;
    }

// private:
    std::unordered_map<DiceEnum::Type, int> mDiceMap{{DiceEnum::Type::RED, 0},
                                           {DiceEnum::Type::GREEN, 0},
                                           {DiceEnum::Type::BLUE, 0}};
};


const std::unordered_map<DiceEnum::Type, int> DiceMap::maximum_bag_contents = {{DiceEnum::Type::RED, 12},
                                                                               {DiceEnum::Type::GREEN, 13},
                                                                               {DiceEnum::Type::BLUE, 14}};

class Game {
public:
    Game(int idIn) {
        id = idIn;
    }

    void add_set(DiceMap diceSet) {
        maxDiceSet.update_max(diceSet);
        diceSets.push_back(diceSet);
    }

    bool valid() {
        for (auto& diceSet : diceSets) {
            if (!diceSet.valid()) {
                return false;
            }
        }
        return true;
    }

    std::vector<DiceMap> getDiceMaps() {
        return diceSets;
    }

    int getId() {
        return id;
    }

// private:
    int id{};
    std::vector<DiceMap> diceSets{};
    DiceMap maxDiceSet{};
};

class Day2 {

public:

    Day2() {
        input = getInput();
        games = parse();
    }

    int part1() {
        int sum{};
        for (auto& game : games) {
            if (game.valid()) {
                sum += game.getId();
            }
        }
        return sum;
    }

    int part2() {
        std::vector<std::vector<int>> max_dice_required_per_game{};
        int power{1};
        for (auto& game : games) {
            for (auto& diceMap : game.getDiceMaps()) {
                power *= diceMap.getMaxRequiredNumOfDice();
            }
        }
        return power;
    }

    
// private:
    std::vector<std::string> input{};
    std::vector<Game> games{};

    
    std::vector<std::string> getInput() {
        std::ifstream myfile("input.txt");
        std::string line;
        std::vector<std::string> input;
        while (std::getline(myfile, line))
        {
            input.push_back(line);
        }
        return input;
    }

    std::vector<Game> parse() {
        games = std::vector<Game>{};
        for (const auto& line : input) {
            std::istringstream iss(line);
            std::vector<std::string> splitLine((std::istream_iterator<std::string>(iss)), std::istream_iterator<std::string>());
            int id = std::stoi(splitLine[1].substr(0, splitLine[1].size() - 1));
            Game game(id);

            std::stringstream ss;
            std::copy(splitLine.begin() + 2, splitLine.end(),std::ostream_iterator<std::string>(ss," "));

            std::string test{};
            int num{};
            DiceEnum::Type diceType;
            DiceMap diceMap;
            while (ss >> test) {
                if (!num) {
                    num = std::stoi(test);
                } else {
                    diceType = DiceEnum::charToDiceType.at(test[0]);
                    diceMap.getDiceMap()[diceType] = num;

                    num = 0;
                    if (test.find(';') != std::string::npos) {
                        game.add_set(diceMap);
                        DiceMap diceMap{};
                    }
                }
            }
            games.push_back(game);
        }
        return games;
    }

};

int main() {
    Day2 day2;

    std::cout << "C++ Solution:" << std::endl;
    std::cout << "\tPart 1: " << day2.part1() << std::endl;
    std::cout << "\tPart 2: " << day2.part2() << std::endl;

}