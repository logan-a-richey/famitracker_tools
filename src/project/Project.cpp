// Project.cpp

#include <iostream>
#include "project/Project.h"

void Project::print_self(){
    std::cout   << "title = " << title << "\n"
                << "author = ? \n"
                << "copyright = ? \n"
                << "comment = ?\n";
    
}
