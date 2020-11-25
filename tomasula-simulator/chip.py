import constants
import utils


class Chip():

    def __init__(self, cpu, instructions, data):
        self.cpu = cpu
        self.main_memory = [0] * constants.MAIN_MEMORY_SIZE
        self.__load_instructions(instructions)
        self.__load_data(data)

    def __load_instructions(self, instructions):
        inst = instructions.split("\n")
        init_address = constants.INSTRUCTION_START_ADDRESS
        for val in inst:
            if val:
                instr = utils.get_instruction(val)
                self.main_memory[init_address] = instr
                init_address += 1
        self.print_memory()

    def print_memory(self):
        print("memory is: ", self.main_memory)

    def __load_data(self, datas):
        data = datas.split("\n")
        init_address = constants.DATA_START_ADDRESS
        for val in data:
            if val:
                self.main_memory[init_address] = int(val, 2)
                init_address += 1
        self.print_memory()
