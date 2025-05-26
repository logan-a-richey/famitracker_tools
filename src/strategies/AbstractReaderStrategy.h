// abstract_reader_strategy.h

#pragma once

#include <string>
#include "project/Project.h"

class AbstractReaderStrategy {
public:
    virtual ~AbstractReaderStrategy() = default; // destructor for polymorphism
    virtual void handle(const std::string& line, Project&) = 0; // pure virtual function; must be overriden
};

