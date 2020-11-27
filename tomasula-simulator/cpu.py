
from fp_type import FPType
from int_alu import IntAlu
from fp_adder import FPAdder
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
import constants


class CPU:

    def __init__(self, config):
        self.gpr = [0] * constants.NUM_REGISTERS
        self.fpr = [0] * constants.NUM_REGISTERS
        self.int_alu = None
        self.fp_adder = None
        self.fp_divider = None
        self.fp_mul = None
        self.reg_pc = constants.PC_START_ADD
        self.__load_config(config)
        self.__add_d_cache()

    def __add_d_cache(self):
        self.add_fp_unit(FPType.DCache, 2, 4)

    def __load_config(self, configs):
        config = configs.split("\n")
        for val in config:
            if val:
                temp = val.split(":")
                fp_unit = temp[0].strip().lower()
                n, latency = list(
                    map(lambda x: int(x.strip()), temp[1].split(",")))
                fp_unit_to_add = FPType.IntALU
                if "adder" in fp_unit:
                    fp_unit_to_add = FPType.FPAdder
                elif "multiplier" in fp_unit:
                    fp_unit_to_add = FPType.FPMul
                elif "divider" in fp_unit:
                    fp_unit_to_add = FPType.FPDiv
                elif "cache" in fp_unit:
                    fp_unit_to_add = FPType.ICache
                else:
                    print("Error: Wrong functional unit type: {}".format(fp_unit))
                self.add_fp_unit(fp_unit_to_add, n, latency)
            # integer ALU is not given in config, so add here to the CPU
            self.add_fp_unit(fp_unit_to_add, 1, 1)

    def add_fp_unit(self, fp_type, n, latency):
        if fp_type == FPType.FPAdder:
            self.FPAdder = [FPAdder("FP-Adder" + str(i+1), latency)
                            for i in range(n)]
        if fp_type == FPType.FPDiv:
            self.FPDivider = [
                FPDivider("FP-Divider" + str(i+1), latency) for i in range(n)]
        if fp_type == FPType.FPMul:
            self.FPDivider = [FP_Multiply(
                "FP-Multiplyer" + str(i+1), latency) for i in range(n)]
        if fp_type == FPType.IntALU:
            self.IntALU = [IntAlu("ALU" + str(i+1), latency) for i in range(n)]
        if fp_type == FPType.ICache:
            self.Ica
