// Project.h

#pragma once

#include <string>
#include <map>
#include <vector>

class Project {
public:
    void print_self();

    // song information settings
    std::string title;
    std::string author;
    std::string copyright;
    std::string comment;
    
    // global settings
    int machine;
    int framerate;
    int expansion;
    int vibrato;
    int split;
    int n163channels;

    /*
    TODO - not implemented yet!
    // macro defs
    std::map<std::string, Macro> macros;
    
    // instrument defs
    std::map<int, BaseInstrument> instruments;
    
    // dpcm defs
    std::map<int, DpcmDef> dpcm_def;
    
    // groove defs
    std::map<int, Groove> grooves;
    std::vector<int> use_groove;

    // track defs
    std::map<int, Track> tracks;
    */
};
    
