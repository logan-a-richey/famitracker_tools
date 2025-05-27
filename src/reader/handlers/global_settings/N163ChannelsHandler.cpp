// N163ChannelsHandler.cpp

#include <iostream>
#include <string>

#include "reader/handlers/global_settings/N163ChannelsHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::N163ChannelsHandler;

void N163ChannelsHandler::load_data(const std::string& line, const int value, famitracker::Project& project){
    static const int lower = 1;
    static const int upper = 8;

    if (value < lower || value > upper){
        std::cerr << "[W] N163CHANNELS value should be between " << lower << " and " << upper << "Line: " << line << std::endl;
    }
    project.n163channels = value;
}

