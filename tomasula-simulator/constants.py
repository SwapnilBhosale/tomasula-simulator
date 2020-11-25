
INSTRUCTION_START_ADDRESS = 0
DATA_START_ADDRESS = 32
MAIN_MEMORY_SIZE = 64
PC_START_ADD = 32
NUM_REGISTERS = 32

LI_INSTR = "LI"
HLT_INSTR = "HLT"


from enum import Enum


class FPType(Enum):

    IntALU = 0
    FPAdder = 1
    FPMul = 2
    FPDiv = 3
    ICache = 4
