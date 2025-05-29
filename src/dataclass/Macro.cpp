// Macro.cpp

#include <string>
#include <sstream>
#include <vector>

#include "dataclass/Macro.hpp"

std::string ft::dataclass::Macro::get_str(){
    std::ostringstream oss;

    oss << label << " " 
        << type << " " 
        << index << " " 
        << loop << " " 
        << release << " " 
        << setting
        << " : [";
    
    for (long unsigned int i = 0; i < sequence.size(); ++i) {
        if (i == sequence.size() - 1){
            oss <<  sequence[i] << " ";
        } else {
            oss << sequence[i] << "]";
        }
    }

    return oss.str();
}
