// Macro.hpp

#pragma once

#include <string>
#include <vector>

namespace ft::dataclass {
    class Macro {
    public:
        std::string label;
        int type;
        int index;
        int loop;
        int release;
        int setting;
        std::vector<int> sequence;
        
        Macro(
            std::string label,
            int m_type,
            int m_index,
            int m_loop,
            int m_release,
            int m_setting,
            std::vector<int> sequence
        );
        std::string get_str();
    };
}

