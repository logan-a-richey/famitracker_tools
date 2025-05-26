// CopyrightStrategy.cpp

#include <iostream>
#include <string>
#include <regex>

#include "project/Project.h"
#include "strategies/CopyrightStrategy.h"

void CopyrightStrategy::handle(const std::string& line, Project& project){
    static const std::regex pattern("^\\s*(\\w+)\\s+\"(.*)\"$");
    std::smatch match;
    if (std::regex_match(line, match, pattern)){
        std::string val = match[2];
        project.copyright = val;
    } else {
        std::cerr << "[E] Could not match pattern! Line: " << line << std::endl;
    }
}

