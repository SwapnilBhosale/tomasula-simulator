import sys
from cpu import CPU
from fp_adder import FPAdder
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
from int_alu import IntAlu
from fp_type import FPType
from chip import Chip
import utils
from clock_mgr import ClockMgr

class App:

    def __init__(self):
        args = sys.argv
        
        #self.inst_file = args[1]
        #self.data_file = args[2]
        #self.config_file = args[3]
        self.inst_file = "..//tc//tc1//inst.txt"
        self.data_file = "..//tc//tc1//data.txt"
        self.config_file = "..//tc//tc1//config.txt"
        self.result_file = "..//tc//tc1//mine.txt"
        
        self.chip = None
        self.clk_mgr = ClockMgr()
        self.init_chip()

    def init_chip(self):
        print("inside init chip")
        data_file = utils.load_bin_file(self.data_file)
        inst_file = utils.load_bin_file(self.inst_file)
        config_file = utils.load_bin_file(self.config_file)
        cpu = CPU(config_file, self.clk_mgr)
        self.chip = Chip(cpu, inst_file, data_file)
        cpu.set_chip(self.chip)
        cpu.load_config(config_file)

    def start_cpu(self):
        #print("**************** before starting cpu: ", self.chip.cpu.__dict__)
        while True:
            print("-------------------")
            print("Running cycle number: {}".format(self.clk_mgr.get_clock()))
            res = self.chip.execute()
            self.clk_mgr.increament_clock()

            if res == -1:
                break

            print("-------------------\n\n")


app = App()
app.start_cpu()
