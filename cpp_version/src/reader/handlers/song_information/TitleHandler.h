// TitleHandler.h

#pragma once

#include <string>

#include "reader/handlers/song_information/AbstractSongInformation.h"
#include "core/Project.h"

namespace famitracker::reader::handler {

    class TitleHandler : public famitracker::reader::handler::AbstractSongInformation {
    protected:
        void load_data(const std::string& value, famitracker::Project& project) override final;
    };

}

