// TextReader.cpp

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include <map>
#include <memory>
#include <algorithm>
#include <cctype>

#include "reader/TextReader.h"

#include "reader/handlers/song_information/TitleHandler.h"
#include "reader/handlers/song_information/AuthorHandler.h"
#include "reader/handlers/song_information/CopyrightHandler.h"
#include "reader/handlers/song_information/CommentHandler.h"

#include "reader/handlers/global_settings/MachineHandler.h"
#include "reader/handlers/global_settings/FramerateHandler.h"
#include "reader/handlers/global_settings/ExpansionHandler.h"
#include "reader/handlers/global_settings/VibratoHandler.h"
#include "reader/handlers/global_settings/SplitHandler.h"
#include "reader/handlers/global_settings/N163ChannelsHandler.h"

using famitracker::reader::TextReader;

TextReader::TextReader(){
    load_dispatch();
}

void TextReader::load_dispatch(){
    // -- Song Information ---
    dispatch["TITLE"] = std::make_unique<famitracker::reader::handler::TitleHandler>();
    dispatch["AUTHOR"] = std::make_unique<famitracker::reader::handler::AuthorHandler>();
    dispatch["COPYRIGHT"] = std::make_unique<famitracker::reader::handler::CopyrightHandler>();
    dispatch["COMMENT"] = std::make_unique<famitracker::reader::handler::CommentHandler>();
    
    // --- Global Settings ---
    dispatch["MACHINE"] = std::make_unique<famitracker::reader::handler::MachineHandler>();
    dispatch["FRAMERATE"] = std::make_unique<famitracker::reader::handler::FramerateHandler>();
    dispatch["EXPANSION"] = std::make_unique<famitracker::reader::handler::ExpansionHandler>();
    dispatch["VIBRATO"] = std::make_unique<famitracker::reader::handler::VibratoHandler>();
    dispatch["SPLIT"] = std::make_unique<famitracker::reader::handler::SplitHandler>();
    dispatch["N163CHANNELS"] = std::make_unique<famitracker::reader::handler::N163ChannelsHandler>();
    
    // --- Macros ---
    // TODO

    // --- DPCM ---
    // TODO
    
    // --- Groove ---
    // TODO
    
    // --- Instruments ---
    // TODO
    
    // --- KeyDPCM ---
    // TODO

    // --- Other ---
    // TODO

    // --- Tracks ---
    // TODO
    
}

std::string TextReader::clean_line(const std::string& input){
    std::string output;
    std::copy_if(input.begin(), input.end(), std::back_inserter(output),
        [](unsigned char c) {
            return c == '\n' || (c >= 32 && c <= 126);
        });
    return output;
}

void TextReader::read_file(const std::string& input_file, Project& project) {
    // std::cout << "Reading file!" << std::endl;
    std::ifstream infile(input_file);
    if (!infile.is_open()) {
        std::cerr << "[E] Could not open file " << input_file << std::endl;
        return;
    }

    std::string line;
    while (std::getline(infile, line)) {
        line = clean_line(line);
        std::istringstream iss(line);
        
        std::string token;
        iss >> token;
        
        if (token.empty()) continue; // skip empty lines
        
        auto it = dispatch.find(token);
        if (it != dispatch.end()){
            it->second->handle(line, project);
        }


    }
}

