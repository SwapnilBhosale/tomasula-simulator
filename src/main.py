import utils
import sys
import constants
from clock_mgr import ClockMgr
from memory_bus import MemoryBus
from cpu import CPU
from memory import Memory
from d_cache import DCache
from i_cache import ICache
from scoreboard import ScoreBoard


class CDC600:

    def __init__(self):
        args = sys.argv
        #self.inst_file = args[1]
        #self.data_file = args[2]
        #self.config_file = args[3]
        #self.res_file = args[4]

        self.inst_file = "..//tc//tc1//inst.txt"
        self.data_file = "..//tc//tc1//data.txt"
        self.config_file = "..//tc//tc1//config.txt"
        self.res_file = "..//tc//tc1//final_res.txt"
        self.instructions = []

        self.scoreboards = []
        self.clock_mgr = ClockMgr()
        self.memory_bus = MemoryBus()
        self.memory = Memory(self.data_file)

        self.reg_pc = 0
        self.dcache = DCache(self.clock_mgr, self.memory_bus, self.memory)
        self.cpu = CPU(self.config_file)
        self.icache = ICache(
            self.cpu.icache_config[0], self.cpu.icache_config[1], self.clock_mgr, self.memory_bus)
        #print("before calling load")

    def __load_instructions(self):
        instructions = utils.load_bin_file(self.inst_file)
        inst = instructions.split("\n")
        print("all isntgr: ", inst)
        for val in inst:
            val = val.strip()
            if val:
                instr = utils.get_instruction(val)
                print("Got instr: {} - {}".format(type(instr), len(self.instructions)))
                self.instructions.append(instr)
                print("loaded instuctions: ", self.instructions[-1])

    def execute(self):
        self.__load_instructions()
        self.reg_pc = 0
        fetch_cycle = self.icache.fetch_instruction(self.reg_pc)
        clk_cnt = 1
        self.scoreboards.append(ScoreBoard(
            clk_cnt, fetch_cycle, self.instructions[self.reg_pc], self.instructions, self.cpu, self.clock_mgr, self.memory_bus, self.dcache))
        while self.reg_pc < len(self.instructions)-1:
            print("*** curr_pc: ", self.reg_pc)
            flag = False
            for j in range(len(self.scoreboards)):
                temp = self.reg_pc
                self.reg_pc = self.scoreboards[j].update(
                    clk_cnt, self.reg_pc + 1, j+1, flag) - 1
                if self.reg_pc != temp:
                    flag = True
            if self.scoreboards[-1].is_fetch_free:
                self.reg_pc += 1
                fetch_cycle = self.icache.fetch_instruction(self.reg_pc)
                self.scoreboards.append(ScoreBoard(
                    clk_cnt, fetch_cycle, self.instructions[self.reg_pc], self.instructions, self.cpu, self.clock_mgr, self.memory_bus, self.dcache))
            clk_cnt += 1
            self.clock_mgr.increament_clock()

        for _ in range(100):
            for j in range(len(self.scoreboards)):
                self.scoreboards[j].update(clk_cnt, self.reg_pc, j+1, False)
            clk_cnt += 1
            self.clock_mgr.increament_clock()
        print("Writing results after clok: ", clk_cnt)
        self.write_result_file(
            self.scoreboards, self.dcache, self.icache, self.res_file)

    def write_result_file(self, scoreboards, dcache, icache, res_file):
        try:
            with open(res_file, "w") as f:
                f.write(self.__get_res_file_header())
                f.write("\n")
                for i in range(len(scoreboards)):
                    temp = scoreboards[i]
                    inst_str = temp.instr.print_instr(is_print=False)

                    temp1 = "{} \t\t\t {} \t {} \t {} \t {}\t {} \t {} \t {} \t {}".format(
                        inst_str, temp.fetch, temp.issue, temp.read, temp.execute, temp.write, temp.h_war, temp.h_waw, temp.sh)
                    f.write(temp1)
                    f.write("\n")

                f.write("\n")
                f.write("\n")
                f.write("Total number of access requests for instruction cache: {}".format(
                    icache.stats_total_requests()))
                f.write("\n")

                f.write("Number of instruction cache hits: {}".format(
                    icache.stats_total_hits()))
                f.write("\n")

                f.write("Total number of access requests for data cache: {}".format(
                    dcache.stats_total_requests()))
                f.write("\n")

                f.write("Number of data cache hits: {}".format(
                    dcache.stats_total_hits()))
                f.write("\n")

        except Exception as e:
            print("Error occured in writing: ", e)

    def __get_res_file_header(self):

        return "INSTRUCTION \t\t\t FETCH \t ISSUE \t READ \t EXEC \t WRITE \t RAW \t WAW \t STRUCTURAL \t"


main = CDC600()
print("Instructions are: ", main.instructions)
main.execute()
#main.write_result_file(None, None, None, "D://UMBC Courses//ACA//Project//src//swapniil.txt")
