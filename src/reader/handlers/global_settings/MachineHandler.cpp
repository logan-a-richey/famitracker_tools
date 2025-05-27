// MachineHandler.cpp

#include <iostream>

#include "reader/handlers/global_settings/MachineHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::MachineHandler;

void MachineHandler::load_data(
    const std::string& line, 
    const int value, 
    famitracker::Project& project
){
    static const int lower = 0;
    static const int upper = 1;

    if (value < lower || value > upper){
        std::cout << "[W] machine value should be between " << lower << " and " << upper << "Line: " << line << std::endl;
    }
    project.machine = value;
}

