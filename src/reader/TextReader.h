// TextReader.h

#pragma once

#include <string>
#include <string>
#include <memory>

#include "core/Project.h"
#include "reader/handlers/BaseHandler.h"

namespace famitracker::reader {

    class TextReader {
    public:
        TextReader();
        void read_file(const std::string& input_file, famitracker::Project& project);

    private:
        // functions
        std::map<std::string, std::unique_ptr<famitracker::reader::handler::BaseHandler>> dispatch;
        void load_dispatch();
        std::string clean_line(const std::string& input);

        // attributes
        int current_dpcm_index;
        int current_track_index;
        int current_pattern_index;
    };

}