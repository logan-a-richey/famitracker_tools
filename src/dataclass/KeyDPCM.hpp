// KeyDPCM.hpp

#pragma once
#include <string>

namespace ft::dataclass {
    class KeyDPCM {
    public:
        int inst;
        int octave;
        int note;
        int sample;
        int pitch;
        int loop;
        int loop_point;
        int delta;

        // TODO
        // std::string get_str();
    };
}
