// VibratoHandler.cpp

#include <iostream>
#include <string>

#include "reader/handlers/global_settings/VibratoHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::VibratoHandler;

void VibratoHandler::load_data(const std::string& line, const int value, famitracker::Project& project){
    static const int lower = 0;
    static const int upper = 1;

    if (value < lower || value > upper){
        std::cerr << "[W] VIBRATO value should be between " << lower << " and " << upper << "Line: " << line << std::endl;
    }
    project.vibrato = value;
}


