// CopyrightHandler.cpp

#include <string>

#include "reader/handlers/song_information/CopyrightHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::CopyrightHandler;

void CopyrightHandler::load_data(const std::string& value, famitracker::Project& project){
    project.copyright = value;
}

