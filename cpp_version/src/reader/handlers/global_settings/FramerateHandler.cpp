// FramerateHandler.cpp

#include <iostream>
#include <string>

#include "reader/handlers/global_settings/FramerateHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::FramerateHandler;

void FramerateHandler::load_data( const std::string& line, const int value, famitracker::Project& project){
    static const int lower = 0;
    static const int upper = 800;
    
    if (value < lower || value > upper){
        std::cerr << "[W] FRAMERATE value should be between " << lower << " and " << upper << "Line: " << line << std::endl;
    }
    project.framerate = value;
}

