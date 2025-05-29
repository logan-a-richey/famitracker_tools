// Project.cpp

#include <string>
#include <sstream>
#include <vector>
#include <map>

#include "dataclass/Project.hpp"

std::string ft::dataclass::Project::get_str(){
    std::ostringstream oss;

    oss << "--- Song Information ---\n";
    oss << "title = " << title << "\n";
    oss << "author = " << author << "\n";
    oss << "copyright = " << copyright << "\n";
    
    oss << "--- Comment ---\n";
    oss << comment << "\n";
    
    oss << "--- Global Settings ---\n";
    oss << "machine = " << machine << "\n";
    oss << "framerate = " << framerate << "\n";
    oss << "expansion = " << expansion << "\n";
    oss << "vibrato = " << vibrato << "\n";
    oss << "split = " << split << "\n";
    oss << "n163channels = " << n163channels << "\n"; 

    // oss << "--- Macros ---\n";
    // oss << "--- Grooves ---\n";
    // oss << "--- DPCM ---\n";
    // oss << "--- KeyDPCM ---\n";
    // oss << "--- Instruments ---\n";
    // oss << "--- Tracks ---\n";
    
    return oss.str();
}
