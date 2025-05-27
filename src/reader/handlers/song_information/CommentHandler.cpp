// CommentHandler.cpp

#include <string>

#include "reader/handlers/song_information/CommentHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::TitleHandler;

void CommentHandler::load_data(const std::string& value, famitracker::Project& project){
    if (project.comment.empty()){
        project.comment = value;
    } else {
        project.comment += value;
    }
}

