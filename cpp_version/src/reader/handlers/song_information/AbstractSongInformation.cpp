// AbstractSongInformation.cpp

#include <iostream>
#include <string>
#include <regex>

#include "reader/handlers/song_information/AbstractSongInformation.h"
#include "core/Project.h"

using famitracker::reader::handler::AbstractSongInformation;

void AbstractSongInformation::handle( const std::string& line, famitracker::Project& project){
    // FIELD "VALUE"
    // (1) grab the first word 
    // (2) grab the text inside of quotes
    static const std::regex pattern("^\\s*(\\w+)\\s+\"(.*)\"$");

    std::smatch match;
    if (std::regex_match(line, match, pattern)){
        std::string value = match[2];
        load_data(value, project);
    } else {
        std::cout << "[E] Could not match Song Information line: " << line << std::endl;
    }
}
