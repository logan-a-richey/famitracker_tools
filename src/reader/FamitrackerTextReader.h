// famitracker_text_reader.h

#pragma once

#include <map>
#include <string>
#include <memory>

#include "strategies/AbstractReaderStrategy.h"
#include "project/Project.h"

class FamitrackerTextReader {
public:
    FamitrackerTextReader();    
    void read_file(Project& project, const std::string& input_file);

private:
    std::map<std::string, std::unique_ptr<AbstractReaderStrategy>> dispatch;
    void load_dispatch();

    int current_dpcm_index;
    int current_track_index;
    int current_pattern_index;
};
