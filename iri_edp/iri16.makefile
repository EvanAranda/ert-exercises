OBJ_DIR:=./build/iri16
BIN_DIR:=./bin
SRC_DIR:=./lib/iri16/src

TARGET:=$(BIN_DIR)/libiri16.so
SRC:=irisub.for irifun.for iritec.for iridreg.for igrf.for iriflip.for cira.for
OBJ:=$(SRC:%.for=$(OBJ_DIR)/%.o)

FC=gfortran
FFLAGS:=-std=legacy -w -O2 -fPIC -finit-local-zero -fno-automatic -fno-backtrace

.PHONY: all clean

all: $(TARGET)

# make the shared lib
$(TARGET): $(OBJ) | $(BIN_DIR)
	$(FC) -shared $(FFLAGS) -o $@ $^

# make the object files
# -finit-local-zero: initialize local variables to zero (avoid NaNs)
# -fno-automatic: recommended in FAQ
# -fPIC: needed for shared lib
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.for | $(OBJ_DIR)
	$(FC) $(FFLAGS) -o $@ -c $<

$(OBJ_DIR) $(BIN_DIR):
	mkdir -p $@

clean:
	rm -rf $(OBJ_DIR)
	rf -f $(TARGET)