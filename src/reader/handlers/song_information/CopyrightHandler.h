// CopyrightHandler.h

#include "reader/handlers/song_information/AbstractSongInformation.h"

namespace famitracker::reader::handler {

    class CopyrightHandler : public famitracker::reader::handler::AbstractSongInformation {
    protected:
        void load_data(const std::string& value, famitracker::Project& project) override final;
    };

}
