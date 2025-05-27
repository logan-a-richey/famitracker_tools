// Project.cpp

#include <iostream>

#include "core/Project.h"

void famitracker::Project::print_self(){
    std::cout 
    << "--- Project Data ---" << std::endl 
    << "--- Song Information ---" << std::endl 
    << "TITLE       : \'" << title << "\'" << std::endl 
    << "AUTHOR      : \'" << author << "\'" << std::endl 
    << "COPYRIGHT   : \'" << copyright << "\'" << std::endl 
    << "COMMENT     : \'" << comment << "\'" << std::endl << std::endl
    << "--- Global Settings ---" << std::endl
    << "MACHINE     : " << machine << std::endl;

    /* TODO */

}

