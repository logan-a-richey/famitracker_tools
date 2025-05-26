// FamitrackerTextReader.cpp

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include <map>
#include <memory>
#include <algorithm>
#include <cctype>

#include "reader/FamitrackerTextReader.h"

#include "strategies/AbstractReaderStrategy.h"

#include "strategies/TitleStrategy.h"
#include "strategies/AuthorStrategy.h"
#include "strategies/CopyrightStrategy.h"
#include "strategies/CommentStrategy.h"

// TODO

FamitrackerTextReader::FamitrackerTextReader(){
    load_dispatch();
}

void FamitrackerTextReader::load_dispatch(){
    dispatch["TITLE"] = std::make_unique<TitleStrategy>();
    dispatch["AUTHOR"] = std::make_unique<AuthorStrategy>();
    dispatch["COPYRIGHT"] = std::make_unique<CopyrightStrategy>();
    dispatch["COMMENT"] = std::make_unique<CommentStrategy>();
    /* TODO
    dispatch["MACHINE"] = std::make_unique<MACHINEStrategy>();
    dispatch["FRAMERATE"] = std::make_unique<FRAMERATEStrategy>();
    dispatch["EXPANSION"] = std::make_unique<EXPANSIONStrategy>();
    dispatch["VIBRATO"] = std::make_unique<VIBRATOStrategy>();
    dispatch["SPLIT"] = std::make_unique<SPLITStrategy>();
    dispatch["N163CHANNELS"] = std::make_unique<N163CHANNELSStrategy>();
    */
    /* TODO
    dispatch["MACRO"] = std::make_unique<MACROStrategy>();
    dispatch["MACROVRC6"] = std::make_unique<MACROVRC6Strategy>();
    dispatch["MACRON163"] = std::make_unique<MACRON163Strategy>();
    dispatch["MACROS5B"] = std::make_unique<MACROS5BStrategy>();
    */
    /* TODO
    dispatch["DPCMDEF"] = std::make_unique<DPCMDEFStrategy>();
    dispatch["DPCM"] = std::make_unique<DPCMStrategy>();
    */
    /* TODO
    dispatch["GROOVE"] = std::make_unique<GROOVEStrategy>();
    dispatch["USEGROOVE"] = std::make_unique<USEGROOVEStrategy>();
    */
    /* TODO
    dispatch["INST2A03"] = std::make_unique<INST2A03Strategy>();
    dispatch["INSTVRC6"] = std::make_unique<INSTVRC6Strategy>();
    dispatch["INSTVRC7"] = std::make_unique<INSTVRC7Strategy>();
    dispatch["INSTFDS"] = std::make_unique<INSTFDSStrategy>();
    dispatch["INSTN163"] = std::make_unique<INSTN163Strategy>();
    dispatch["INSTS5B"] = std::make_unique<INSTS5BStrategy>();
    */
    /* TODO
    dispatch["KEYDPCM"] = std::make_unique<KEYDPCMStrategy>();
    dispatch["FDSWAVE"] = std::make_unique<FDSWAVEStrategy>();
    dispatch["FDSMOD"] = std::make_unique<FDSMODStrategy>();
    dispatch["FDSMACRO"] = std::make_unique<FDSMACROStrategy>();
    dispatch["N163WAVE"] = std::make_unique<N163WAVEStrategy>();
    */
    /* TODO
    dispatch["TRACK"] = std::make_unique<TRACKStrategy>();
    dispatch["COLUMNS"] = std::make_unique<COLUMNSStrategy>();
    dispatch["ORDER"] = std::make_unique<ORDERStrategy>();
    dispatch["PATTERN"] = std::make_unique<PATTERNStrategy>();
    dispatch["ROW "] = std::make_unique<ROWStrategy>();
    */
}

std::string FamitrackerTextReader::clean_line(const std::string& input){
    std::string output;
    std::copy_if(input.begin(), input.end(), std::back_inserter(output),
        [](unsigned char c) {
            return c == '\n' || (c >= 32 && c <= 126);
        });
    return output;
}

void FamitrackerTextReader::read_file(Project& project, const std::string& input_file) {
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
