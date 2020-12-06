
from fp_type import FPType
from int_alu import IntAlu
from fp_adder import FPAdder, BranchUnit, LoadStoreUnit
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
from cache import ICache, DCache
import constants
from memory_bus import MemoryBus


class CPU:

    def __init__(self, config, clk_mgr):
        self.gpr = [[0 for i in range(3)]
                    for j in range(constants.NUM_REGISTERS+1)]
        self.fpr = [[0 for i in range(3)]
                    for j in range(constants.NUM_REGISTERS+1)]
        self.int_alu = None
        self.fp_adder = None
        self.fp_divider = None
        self.fp_mul = None
        self.load_store_unit = None
        self.branch_unit = None

        self.icache = None
        self.dcache = None
        self.reg_pc = constants.PC_START_ADD
        self.memory_bus = MemoryBus()
        self.clk_mgr = clk_mgr

        
        self.curr_clock = 0

    
    def load_config(self, config):
        self.__load_config(config)

    def set_chip(self, chip):
        self.chip = chip

    def set_clock(self, clk_no):
        self.curr_clock = clk_no


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

        print("adding integer alu")
        # integer ALU is not given in config, so add here to the CPU
        self.add_fp_unit(FPType.IntALU, 1, 1)
        self.add_fp_unit(FPType.LoadStoreUnit, 1, 1)
        self.add_fp_unit(FPType.BranchUnit, 1, 0)
        self.add_fp_unit(FPType.DCache, 1, 0)


    def add_fp_unit(self, fp_type, arg1, arg2):
        if fp_type == FPType.FPAdder:
            self.fp_adder = [ FPAdder("FP-Adder" + str(i+1), arg2) for i in range(arg1)]
        elif fp_type == FPType.FPDiv:
            self.fp_divider = [ FPDivider("FP-Divider" + str(i+1), arg2) for i in range(arg1)]
        elif fp_type == FPType.FPMul:
            self.fp_mul = [ FP_Multiply("FP-Multiplyer" + str(i+1), arg2) for i in range(arg1)]
        elif fp_type == FPType.IntALU:
            self.int_alu = [ IntAlu("ALU" + str(i+1), arg2)for i in range(arg1)]
        elif fp_type == FPType.ICache:
            self.icache = ICache(arg1, arg2, self.memory_bus, self.clk_mgr)
        elif fp_type == FPType.DCache:
            self.dcache = DCache(arg1, arg2, self.chip, self.memory_bus, self.clk_mgr)
        elif fp_type == FPType.LoadStoreUnit:
            self.load_store_unit = [ LoadStoreUnit("LoadStoreUnit" + str(i+1), arg2) for i in range(arg1)]
        elif fp_type == FPType.BranchUnit:
            self.branch_unit = [ BranchUnit("BranchUnit" + str(i+1), arg2) for i in range(arg1)]
        else:
            raise NotImplementedError(
                "Functional unit {} is not supported".format(fp_type))

    def __is_gpr(self, reg):
        return True if reg[0] == "R" else False

    def __check_int_alu(self, instr, reg):
        res = False
        assigned_adder, taken = self.int_alu[0]
        if taken:
            if assigned_adder.instr.inst_str != constants.SW_INSTR or assigned_adder.instr.inst_str != constants.SD_INSTR:
                res = (
                    instr != assigned_adder.instr and reg in assigned_adder.instr.src_op)
        return res

    def __check_fp_adder(self, instr, reg):
        assigned_adders = [adder for adder, taken in self.fp_adder if taken]
        raw_hazards = [True for adder in assigned_adders if instr !=
                       adder.instr and reg in adder.instr.src_op]
        return True in raw_hazards

    def __check_fp_mul(self, instr, reg):
        assigned_mul = [mul for mul, taken in self.fp_mul if taken]
        raw_hazards = [True for mul in assigned_mul if instr !=
                       mul.instr and reg in mul.instr.src_op]
        return True in raw_hazards

    def __check_fp_div(self, instr, reg):
        assigned_div = [divider for divider, taken in self.fp_divider if taken]
        raw_hazards = [True for divider in assigned_div if instr !=
                       divider.instr and reg in divider.instr.src_op]
        return True in raw_hazards

    def is_raw_hazard(self, instr, reg, is_gpr):
        res = False
        if reg > 0:
            if is_gpr:
                if self.cpu.gpr[r2][1] > 0:
                    res =  True
            if is_fpr and r2 > 0:
                if self.cpu.fpr[r2][1] > 0:
                    res =  True
        return res
