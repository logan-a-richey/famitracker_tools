// AuthorStrategy.h

#pragma once

#include <string>

#include "strategies/AbstractReaderStrategy.h"

class AuthorStrategy : public AbstractReaderStrategy {
public:
    void handle(const std::string& line, Project& project) override; 
};

