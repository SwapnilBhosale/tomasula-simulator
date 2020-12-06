import utils
from fp_type import FPType
import constants
from fp_adder import FPAdder
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
from int_alu import IntAlu
from d_cache import DCache


class CPU:

    def __init__(self, config_path):
        self.gpr = [[0 for i in range(3)]
                    for j in range(constants.NUM_REGISTERS+1)]
        self.fpr = [[0 for i in range(3)]
                    for j in range(constants.NUM_REGISTERS+1)]
        self.is_branch = False

        self.fetch = False
        self.issue = False

        self.int_alu = None
        self.fp_adder = None
        self.fp_divider = None
        self.fp_mul = None

        self.fu_load = False
        self.fu_branch = False
        self.config_path = config_path
        self.icache_config = None
        self.__load_config()

    def __load_config(self):
        configs = utils.load_bin_file(self.config_path)
        config = configs.split("\n")
        for val in config:
            if val:
                temp = val.split(":")
                fp_unit = temp[0].strip().lower()
                n, latency = list(
                    map(lambda x: int(x.strip()), temp[1].split(",")))
                fp_unit_to_add = FPType.IntALU

                if "cache" in fp_unit:
                    self.icache_config = (n, latency)
                    continue
                if "adder" in fp_unit:
                    fp_unit_to_add = FPType.FPAdder
                elif "multiplier" in fp_unit:
                    fp_unit_to_add = FPType.FPMul
                elif "divider" in fp_unit:
                    fp_unit_to_add = FPType.FPDiv
                else:
                    print("Error: Wrong functional unit type: {}".format(fp_unit))
                self.add_fp_unit(fp_unit_to_add, n, latency)

        print("adding integer alu")
        # integer ALU is not given in config, so add here to the CPU
        self.add_fp_unit(FPType.IntALU, 1, 1)

    def add_fp_unit(self, fp_type, arg1, arg2):
        if fp_type == FPType.FPAdder:
            self.fp_adder = [FPAdder("FP-Adder" + str(i+1), arg2)
                             for i in range(arg1)]
        elif fp_type == FPType.FPDiv:
            self.fp_divider = [
                FPDivider("FP-Divider" + str(i+1), arg2) for i in range(arg1)]
        elif fp_type == FPType.FPMul:
            self.fp_mul = [FP_Multiply(
                "FP-Multiplyer" + str(i+1), arg2) for i in range(arg1)]
        elif fp_type == FPType.IntALU:
            self.int_alu = [IntAlu("ALU" + str(i+1), arg2)
                            for i in range(arg1)]
        else:
            raise NotImplementedError(
                "Functional unit {} is not supported".format(fp_type))