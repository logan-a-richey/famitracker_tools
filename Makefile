# ---- Makefile ----

CXX := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -Isrc

TARGET := bin/main.exe
BUILD_DIR := build
SRC_DIR := src

# Get all .cpp files in src
SRC := $(shell find $(SRC_DIR) -name "*.cpp")
# Turn each .cpp into a corresponding .o in build/
OBJ := $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(SRC))

# Default target
all: $(TARGET)

# Link final binary
$(TARGET): $(OBJ)
	@mkdir -p bin
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compile source to object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# Clean
clean:
	rm -rf $(BUILD_DIR) $(TARGET)

.PHONY: all clean

