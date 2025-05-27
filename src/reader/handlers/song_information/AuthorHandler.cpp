// AuthorHandler.cpp

#include <string>

#include "reader/handlers/song_information/AuthorHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::AuthorHandler;

void TitleHandler::load_data(const std::string& value, famitracker::Project& project){
    project.author = value;
}

