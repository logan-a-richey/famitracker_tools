// Project.cpp

#include <iostream>
#include "project/Project.h"

void Project::print_self(){
    std::cout   << "title = " << title << std::endl
                << "author = " << author << std::endl
                << "copyright = " << copyright << std::endl
                << "comment = " << comment << std::endl;
}
