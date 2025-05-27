// AbstractSongInformationStrategy.cpp

#include <regex>
#include <string>

// handle regex
void AbstractSongInformationStrategy::handle(
    const std::string& line, 
    Project& project
){
    static const std::regex pattern("^\\s*(\\w+)\\s+(\\d+)$");
    std::smatch match;
    if (std::regex_match(line, match, pattern)) {
        // const std::string& key = match[1];
        const std::string& value = match[2];
        handle_match(key, value, project);
    } else {
        std::cerr << "[E] Could not match pattern! Line: " << line << std::endl;
    }
}


