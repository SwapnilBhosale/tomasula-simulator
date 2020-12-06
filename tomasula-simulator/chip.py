import constants
import score_board
import utils


class Chip():

    def __init__(self, cpu, instructions, data):
        self.cpu = cpu
        self.instr = []
        self.data = []
        self.main_memory_access_time = 3
        self.__load_instructions(instructions)
        self.__load_data(data)
        self.sb = score_board.ScoreBoard(self)

    def __load_instructions(self, instructions):
        inst = instructions.split("\n")
        for val in inst:
            if val:
                instr = utils.get_instruction(val)
                self.instr.append(instr)

    def __load_data(self, datas):
        data = datas.split("\n")
        for val in data:
            if val:
                self.data.append(int(val, 2))

        # self.print_memory()
    def fetch_data_for_d_cache(self, addr):
        idx = (addr - 256) // 4
        idx = idx // 4
        return self.data[idx]
    
    def update_data_for_d_cache(self, address, data):
        idx = (address - 256) // 4
        idx = idx // 4
        for i in len(data):
            self.data[idx][i] = data[i]

    def update_sw_data_for_d_cache(self, addr, data):
        idx = (addr - 256) // 4
        idx1 = idx // 4
        offset = idx % 4
        temp = self.data[idx1]
        temp[offset] = data
        self.data[idx1] = temp

    def update_get_data_for_d_cache(self, addr, offset, data):
        idx = (addr - 256) // 4
        idx = idx // 4
        temp = self.data[idx]
        temp[offset] = data
        return temp

    def update_data_for_d_cache(self, addr, data):
        idx = (addr - 256) // 4
        idx = idx // 4
        self.data[idx] = data

    def execute(self, cycle_no=0):
        self.sb.write_stage()
        self.sb.exec_stage()
        self.sb.read_stage()
        self.sb.issue_stage()
        self.sb.fetch_stage()
        self.sb.set_fu_active()
        return 1
