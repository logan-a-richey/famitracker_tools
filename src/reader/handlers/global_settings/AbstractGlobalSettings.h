// AbstractGlobalSettings.cpp

#pragma once

#include <string>

#include "reader/handlers/BaseHandler.h"
#include "core/Project.h"

namespace famitracker::reader::handler {

    class AbstractGlobalSettings : public famitracker::reader::handler::BaseHandler {
    public:
        void handle(const std::string& line, famitracker::Project& project) override final;
    
    protected:
        virtual void load_data(const int value, famitracker::Project& project) = 0;
    };

}