
from fp_type import FPType
from int_alu import IntAlu
from fp_adder import FPAdder
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
import constants


class CPU:

    def __init__(self, data, inst, config):
        self.gpr = [0] * 32
        self.fpr = [0] * 32
        self.int_alu = None
        self.fp_adder = None
        self.fp_divider = None
        self.fp_mul = None
        self.main_memory = [0] * 0x200
        self.__load_instructions(inst)
        self.__load_data(data)
        self.__load_config(config)


    def __load_instructions(self, instructions):
        inst = instructions.split("\n")
        init_address = constants.INSTRUCTION_START_ADDRESS
        for val in inst:
            self.main_memory[init_address] = val
            init_address += 1

    def __load_data(self, datas):
        data = datas.split("\n")
        init_address = constants.DATA_START_ADDRESS
        for val in data:
            self.main_memory[init_address] = int(val, 2)
            init_address += 1

    def __load_config(self, configs):
        config = configs.split("\n")
        for val in config:
            temp  = val.split(":")
            fp_unit = temp[0].strip().lower()
            n, latency = list(map(lambda x: x.strip(), temp[1].split(",")))
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
        self.add_fp_unit(fp_unit_to_add, 1, 1)           #integer ALU is not given in config, so add here to the CPU
    
        

    def add_fp_unit(self, fp_type, n, latency):
        if fp_type == FPType.FPAdder:
            self.FPAdder = [FPAdder("FP-Adder" + (i+1), latency) for i in range(n)]
        if fp_type == FPType.FPDiv:
            self.FPDivider = [FPDivider("FP-Divider" + (i+1), latency) for i in range(n)]
        if fp_type == FPType.FPMul:
            self.FPDivider = [FP_Multiply("FP-Multiplyer" + (i+1), latency) for i in range(n)]
        if fp_type == FPType.IntALU:
            self.IntALU = [IntAlu("ALU" + (i+1), latency) for i in range(n)]

    