import sys
from .cpu import CPU
from .fp_adder import FPAdder
from .fp_divider import FPDivider
from .fp_multiply import FP_Multiply
from .int_alu import IntAlu
from fp_type import FPType

class App:

    def __init__(self):


        args = sys.argv
        self.inst_file = args[1]
        self.data_file = args[2]
        self.config_file = args[3]
        self.result_file = "result.txt"


    def init_cpu(self):
        self.cpu = CPU()
        with open(self.config_file) as f:
            data = f.read().split("\n")
            for val in data:
                if "adder" in val:
                    n, cycles = val.split(":")[1].split(",")
                        self.cpu.add_fp_unit()




    def __load_bin_file(self):
        pass
