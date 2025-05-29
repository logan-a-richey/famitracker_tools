// Parser.cpp

#include "parser/Parser.hpp"

#include <iostream>

void ft::parser::Parser::read_file(
    [[maybe_unused]] const std::string& input_file,
    [[maybe_unused]] ft::dataclass::Project& project
){
    std::cout << "Reading file!" << std::endl;
    // TODO read file line by line
}

void ft::parser::Parser::read_line(
    [[maybe_unused]] const std::string& line,
    [[maybe_unused]] ft::dataclass::Project& project
){
    std::cout << "Reading line: " << line << "\n";
}
