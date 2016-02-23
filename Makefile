CC = g++
CFLAGS = -c -Wall -std=c++11

LIBS = -lzmq
LDFLAGS = $(LIBS)

BROKER = queue_broker
BROKER_SOURCES = queue_broker.cpp
BROKER_OBJECTS = $(BROKER_SOURCES:.cpp=.o)

SOURCES = $(BROKER_SOURCES)
OBJECTS = $(BROKER_OBJECTS)
EXECUTABLES = $(BROKER)

OBJECTS_DIR = obj
BIN_DIR = bin

all: $(SOURCES) $(EXECUTABLES)

$(BROKER): $(BROKER_OBJECTS)
	$(CC) $(LDFLAGS) $(patsubst %, $(OBJECTS_DIR)/%, $(BROKER_OBJECTS)) -o $(BIN_DIR)/$@

.cpp.o:
	$(CC) $(CFLAGS) $< -o  $(OBJECTS_DIR)/$@

.PHONY: clean
clean:
	rm -f $(OBJECTS_DIR)/* $(BIN_DIR)/*
