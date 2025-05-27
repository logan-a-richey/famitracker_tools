// AbstractSongInformation.h

#include <string>

#include "reader/handlers/BaseHandler.h"
#include "core/Project.h"

namespace famitracker::reader::handler {
    
    class AbstractSongInformation : public famitracker::reader::handler::BaseHandler {
    public:
        void handle( const std::string& line, famitracker::Project& project) override final;

    protected:
        virtual void load_data( const std::string& value, famitracker::Project& project) = 0;
    };

}
