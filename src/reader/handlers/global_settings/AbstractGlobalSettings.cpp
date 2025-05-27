// AbstractGlobalSettings.cpp

#include <iostream>
#include <string>
#include <regex>

#include "reader/handlers/global_settings/AbstractGlobalSettings.h"
#include "core/Project.h"

using famitracker::reader::handler::AbstractGlobalSettings;

void AbstractGlobalSettings::handle( const std::string& line, famitracker::Project& project){
    // FIELD <integer>
    // (1) grab the first word
    // (2) grab the number that follows, optional leading negative sign
    static const std::regex pattern("\\s*(\\w+)\\s+(\\-?\\d+)$");

    std::smatch match;
    if (std::regex_match(line, match, pattern)){
        std::string str_num = match[2];
        int int_num = std::stoi(str_num);
        load_data(line, int_num, project);
    } else {
        std::cout << "[E] Could match Global Setings line: " << line << std::endl;
    }
}
