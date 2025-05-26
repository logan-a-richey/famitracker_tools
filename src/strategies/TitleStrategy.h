// title_strategy.h

#pragma once

#include <string>
#include <regex>

#include "strategies/AbstractReaderStrategy.h"

class TitleStrategy : public AbstractReaderStrategy {
public:
    void handle(const std::string& line, Project&) override; 
};
