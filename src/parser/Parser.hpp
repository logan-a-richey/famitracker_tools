// Parser.hpp

#pragma once
#include "dataclass/Project.hpp"

namespace ft::parser {

    class Parser {
    public:
        void read_file(
            const std::string& input_file,
            ft::dataclass::Project& project
        );
    private:
        void read_line(
            const std::string& line, 
            ft::dataclass::Project& project
        );
    }; 
}
