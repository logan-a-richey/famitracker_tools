// Track.hpp

#pragma once

#include <string>
#include <map>
#include <vector>

namespace ft::dataclass {
    class Track {
    public:
        std::string name;
        int num_rows;
        int num_cols;
        std::vector<int> effect_cols;
        int speed;
        int tempo;
        std::map<int, std::vector<int>> orders;
        std::map<std::string, std::string> tokens;
        
        // TODO implement print self
    };
}

