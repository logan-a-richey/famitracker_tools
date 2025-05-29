// #include <iostream>
// main.py

#include <iostream>

#include "dataclass/Project.hpp"
#include "parser/Parser.hpp"

int main(int argc, char** argv){
    if (argc == 1){
        std::cout << "Usage: ./main.exe input.txt" << std::endl;
        return 1;
    }
    const std::string input_file = argv[1];

    ft::dataclass::Project my_project;
    ft::parser::Parser my_parser;
    
    my_parser.read_file(input_file, my_project);
    
    std::cout << my_project.get_str() << std::endl;

    return 0;
}

