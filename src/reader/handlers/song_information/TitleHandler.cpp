// TitleHandler.cpp

#include <string>

#include "reader/handlers/song_information/TitleHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::TitleHandler;

void TitleHandler::load_data(const std::string& value, famitracker::Project& project){
    project.title = value;
}

