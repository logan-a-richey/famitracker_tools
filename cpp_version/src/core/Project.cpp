// Project.cpp

#include <iostream>

#include "core/Project.h"

void famitracker::Project::print_self(){
    std::cout 
    << "--- Project Data ---" << "\n" 
    << "--- Song Information ---" << "\n" 
    << "TITLE        : \'" << title << "\'" << "\n" 
    << "AUTHOR       : \'" << author << "\'" << "\n" 
    << "COPYRIGHT    : \'" << copyright << "\'" << "\n" 
    << "COMMENT      : \'" << comment << "\'" << "\n"
    << "\n"
    << "--- Global Settings ---" << "\n"
    << "MACHINE      : " << machine << "\n"
    << "FRAMERATE    : " << framerate << "\n"
    << "EXPANSION    : " << expansion << "\n"
    << "VIBRATO      : " << vibrato << "\n"
    << "SPLIT        : " << split << "\n"
    << "N163CHANNELS : " << n163channels << "\n"
    << std::endl;
    
    /* TODO */

}

