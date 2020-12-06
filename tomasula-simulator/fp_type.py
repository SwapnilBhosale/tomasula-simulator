from enum import Enum


class FPType(Enum):

    IntALU = 0
    FPAdder = 1
    FPMul = 2
    FPDiv = 3
    ICache = 4
    DCache = 5
    LoadStoreUnit = 6
    BranchUnit = 7
