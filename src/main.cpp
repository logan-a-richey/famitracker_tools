// main.cpp

#include <iostream>

#include "project/Project.h"
#include "reader/FamitrackerTextReader.h"

int main(int argc, char** argv){
    if  (argc != 2){
        std::cout << "Usage: ./main input.txt" << std::endl;
        return 1;
    }
    const std::string input_file = argv[1];

    Project my_project;
    FamitrackerTextReader my_text_reader;
    my_text_reader.read_file(my_project, input_file);

    return 0;
}
