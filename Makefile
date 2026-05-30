# SENTINEL COMPANY - R+ COMPILER v3.0 Makefile
# Kullanim:
#   make              - test_kodu.rsp dosyasini derle
#   make run          - derle ve calistir
#   make test         - test suite'ini calistir
#   make clean        - .asm ve binary dosyalarini temizle

NASM = nasm
LD = ld
PYTHON = python3
RSP_FILE = test_kodu.rsp
ASM_FILE = $(RSP_FILE:.rsp=.asm)
OBJ_FILE = $(RSP_FILE:.rsp=.o)
BIN_FILE = $(RSP_FILE:.rsp=)

all: $(ASM_FILE)

$(ASM_FILE): $(RSP_FILE)
	$(PYTHON) compiler.py $(RSP_FILE)

$(OBJ_FILE): $(ASM_FILE)
	$(NASM) -f elf64 $(ASM_FILE) -o $(OBJ_FILE)

$(BIN_FILE): $(OBJ_FILE)
	$(LD) $(OBJ_FILE) -o $(BIN_FILE)

run: $(BIN_FILE)
	./$(BIN_FILE)

asm: $(ASM_FILE)

test:
	$(PYTHON) tests/test_compiler.py

clean:
	rm -f *.asm *.o $(BIN_FILE)
	rm -rf __pycache__ src/__pycache__ tests/__pycache__

.PHONY: all run test clean asm
