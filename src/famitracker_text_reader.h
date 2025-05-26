// famitracker_text_reader.h

#include <string>
class Project;

class FamitrackerTextReader {
public:
    void read_file(Project& p, std::string input_file);

private:
    int current_dpcm_index;
    int current_track_index;
    int current_pattern_index;
};
