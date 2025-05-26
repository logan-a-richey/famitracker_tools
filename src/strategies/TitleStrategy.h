// TitleStrategy.h

#pragma once

#include <string>

#include "strategies/AbstractReaderStrategy.h"

class TitleStrategy : public AbstractReaderStrategy {
public:
    void handle(const std::string& line, Project&) override; 
};

