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

        std::string title;
        std::string author;
        std::string copyright;
        std::string comment;
        
        bool machine;
        int framerate;
        int expansion;
        bool vibrato;
        int namco_channels;

        /* TODO
        std::map<std::string, Macro> macros;
        std::map<int, BaseInst> instruments;
        std::map<int, DPCM> dpcm_samples;
        std::map<int, Groove> grooves;
        std::map<int, Track> tracks;
        */
    };

}
