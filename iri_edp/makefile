BIN_DIR=bin
TARGET=bin/run_iri

LDFLAGS=-Lbin
LDLIBS=-liri16

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(BIN_DIR)
	$(CC) src/run_iri.c -o $@ $(LDFLAGS) $(LDLIBS) -Wall

$(BIN_DIR):
	mkdir -p $@

clean:
	rm -f $(TARGET)