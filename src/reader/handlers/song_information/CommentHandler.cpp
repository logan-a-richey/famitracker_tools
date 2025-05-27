// CommentHandler.cpp

#include <string>

#include "reader/handlers/song_information/CommentHandler.h"
#include "core/Project.h"

using famitracker::reader::handler::CommentHandler;

void CommentHandler::load_data(const std::string& value, famitracker::Project& project){
    if (project.comment.empty()){
        project.comment = value;
    } else {
        project.comment += "\n" + value;
    }
}
