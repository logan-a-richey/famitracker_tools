// title_strategy.cpp

#include <iostream>
#include <string>
#include <regex>

#include "project/Project.h"
#include "strategies/TitleStrategy.h"

void TitleStrategy::handle(
    [[maybe_unused]] const std::string& line, 
    [[maybe_unused]] Project& project
){
    static const std::regex pattern("^\\s*(\\w+)\\s+\"(.*)\"$");
    std::smatch match;
    if (std::regex_match(line, match, pattern)){
        std::string val = match[2];
        project.title = val;
    } else {
        std::cerr << "[E] Could not match pattern! Line: " << line << std::endl;
    }
}
