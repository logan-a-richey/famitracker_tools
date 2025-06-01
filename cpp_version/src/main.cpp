// #include <iostream>
// main.py

#include <iostream>

#include "core/Project.h"
#include "reader/TextReader.h"

int main(int argc, char** argv){
    std::cout << "Hello Famitracker" << std::endl;
    
    if (argc != 2){
        std::cout << "Usage: ./main.exe input.txt" << std::endl;
        return 1;
    }
    const std::string input_file = argv[1];

    famitracker::Project my_project;
    famitracker::reader::TextReader reader;
    reader.read_file(input_file, my_project);

    my_project.print_self();

    return 0;
}