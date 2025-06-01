// Project.h

#pragma once

#include <string>
#include <map>

/* TODO
class Macro;
class DPCM;
class Groove;
class BaseInst;
class Track;
*/

namespace famitracker {

    class Project {
    public:
        void print_self();

        std::string title = "";
        std::string author = "";
        std::string copyright = "";
        std::string comment = "";
        
        int machine = 0;
        int framerate = 60;
        int expansion = 0;
        int vibrato = 1;
        int split = 32;
        int n163channels = 0;

        /* TODO
        std::map<std::string, Macro> macros;
        std::map<int, BaseInst> instruments;
        std::map<int, DPCM> dpcm_samples;
        std::map<int, Groove> grooves;
        std::map<int, Track> tracks;
        */
    };

}
