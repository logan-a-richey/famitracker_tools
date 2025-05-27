// N163ChannelsHandler.h

#pragma once

#include <string>

#include "reader/handlers/global_settings/AbstractGlobalSettings.h"
#include "core/Project.h"

namespace famitracker::reader::handler {

    class N163ChannelsHandler : public famitracker::reader::handler::AbstractGlobalSettings {
    protected: 
        void load_data(const std::string& line, const int value, famitracker::Project& project) override final;
    };

}
