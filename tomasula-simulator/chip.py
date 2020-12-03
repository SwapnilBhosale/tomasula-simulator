import constants
import score_board
import utils


class Chip():

    def __init__(self, cpu, instructions, data):
        self.cpu = cpu
        self.main_memory = [0] * constants.MAIN_MEMORY_SIZE
        self.main_memory_access_time = 3
        self.__load_instructions(instructions)
        self.__load_data(data)
        self.sb = score_board.ScoreBoard(self)

    def __load_instructions(self, instructions):
        inst = instructions.split("\n")
        init_address = constants.INSTRUCTION_START_ADDRESS
        for val in inst:
            if val:
                instr = utils.get_instruction(val)
                self.main_memory[init_address] = instr
                init_address += 1
        # self.print_memory()

    def print_memory(self):
        print("MAIN Memory: ", self.main_memory)

    def print_cpu(self):
        print("CPU: ", self.cpu.__dict__)

    def __load_data(self, datas):
        data = datas.split("\n")
        init_address = constants.DATA_START_ADDRESS
        for val in data:
            if val:
                self.main_memory[init_address] = int(val, 2)
                init_address += 1
        # self.print_memory()

    def execute(self, cycle_no):
        self.cpu.set_clock(cycle_no)
        cache_block = None
        instr = None
        if self.cpu.icache.get_from_cache[self.cpu.reg_pc]:
            cache_block = self.cpu.icache.get_from_cache[self.cpu.reg_pc]
        else:
            inst = self.main_memory[self.cpu.reg_pc]
            self.sb.write_stage()
            self.sb.exec_stage()
            self.sb.read_stage()
            self.sb.issue_stage()
            self.sb.fetch_stage(inst)
            self.sb.set_fu_active()
        return 1
