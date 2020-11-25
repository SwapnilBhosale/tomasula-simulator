import sys
from cpu import CPU
from fp_adder import FPAdder
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
from int_alu import IntAlu
from fp_type import FPType
import utils

from chip import Chip


class App:

    def __init__(self):
        args = sys.argv
        self.inst_file = args[1]
        self.data_file = args[2]
        self.config_file = args[3]
        self.result_file = "result.txt"
        self.chip = None
        self.init_chip()

    def init_chip(self):
        print("inside init chip")
        data_file = utils.load_bin_file(self.data_file)
        inst_file = utils.load_bin_file(self.inst_file)
        config_file = utils.load_bin_file(self.config_file)
        cpu = CPU(config_file)
        self.chip = Chip(cpu, inst_file, data_file)


app = App()

app.init_chip()
