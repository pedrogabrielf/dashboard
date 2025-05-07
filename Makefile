# Compilador
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -I./include

# Diretórios
SRC_DIR = src
CONTROLLER_DIR = $(SRC_DIR)/controller
MODEL_DIR = $(SRC_DIR)/model
VIEW_DIR = $(SRC_DIR)/view
BUILD_DIR = build
APP_DIR = app

# Arquivos fonte
CONTROLLER_SRC = $(CONTROLLER_DIR)/controller.cpp
MODEL_SRC = $(MODEL_DIR)/model.cpp
VIEW_SRC = $(VIEW_DIR)/view.cpp
MAIN_SRC = main.cpp

# Arquivos objeto
CONTROLLER_OBJ = $(BUILD_DIR)/controller.o
MODEL_OBJ = $(BUILD_DIR)/model.o
VIEW_OBJ = $(BUILD_DIR)/view.o
MAIN_OBJ = $(BUILD_DIR)/main.o

# Executável final
TARGET = $(APP_DIR)/app

.PHONY: tudo limpar pastas

tudo: pastas $(TARGET)

pastas:
	mkdir -p $(BUILD_DIR) $(APP_DIR)

$(MAIN_OBJ): $(MAIN_SRC)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(CONTROLLER_OBJ): $(CONTROLLER_SRC)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(MODEL_OBJ): $(MODEL_SRC)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(VIEW_OBJ): $(VIEW_SRC)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(TARGET): $(MAIN_OBJ) $(CONTROLLER_OBJ) $(MODEL_OBJ) $(VIEW_OBJ)
	$(CXX) $^ -o $@

limpar:
	rm -rf $(BUILD_DIR)/*.o $(TARGET)