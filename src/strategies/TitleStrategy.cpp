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
    std::cout << "In TitleStrategy: " << line << std::endl;
}
