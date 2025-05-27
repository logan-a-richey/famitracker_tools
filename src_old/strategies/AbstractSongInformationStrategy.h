// AbstractSongInformationStrategy.h

#include "reader/AbstractReaderStrategy.h"

class AbstractSongInformationStrategy : AbstractReaderStrategy {
public:
    void handle(const std::string& line, Project& project) final override;

protected:
    virtual void handle_match(
        // const std::string& key,
        const std::string& value,
        Project& project
    ) = 0;
};

