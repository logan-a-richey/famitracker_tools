// ExpansionHandler.cpp

#include <iostream>
#include <string>

#include "reader/handlers/global_settings/ExpansionHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::ExpansionHandler;

void ExpansionHandler::load_data(const std::string& line, const int value, famitracker::Project& project){
    static const int lower = 0;
    static const int upper = 255;
    
    if (value < lower || value > upper){
        std::cerr << "[W] EXPANSION value should be between " << lower << " and " << upper << "Line: " << line << std::endl;
    }
    project.expansion = value;
}

