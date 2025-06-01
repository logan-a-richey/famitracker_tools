// BaseHandler.h

#pragma once

#include <string>

#include "core/Project.h"

namespace famitracker::reader::handler {
    
    class BaseHandler {
    public:
        virtual ~BaseHandler() = default;
        virtual void handle(const std::string& line, famitracker::Project& project) = 0;
    };

}