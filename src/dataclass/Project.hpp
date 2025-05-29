// Project.hpp

#pragma once
#include <string>
#include <vector>
#include <map>
#include <memory>

namespace ft::dataclass {
    class Project {
    public:
        std::string title = "";
        std::string author = "";
        std::string copyright = "";
        std::string comment = "";
        int machine = 0;
        int framerate = 0;
        int expansion = 0;
        int vibrato = 1;
        int split = 32;
        int n163channels = 0;

        /*
        std::map<std::string, Macro> macros;
        std::map<int, DPCM> dpcm_samples;
        std::map<int, Groove> grooves;
        std::map<int, Inst> instruments;
        std::map<int, Track> tracks;
        */

        std::string get_str();
    };
}
