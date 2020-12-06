

class FUnit:

    def __init__(self, name, exec_time):
        self.name = name
        self.exec_time = exec_time
        self.remain_time = exec_time
        self.instr = None
        self.occupied = False

    def set_instruction(self, instr):
        self.instr = instr
        if instr.exec_stage_cycle:
            self.remain_time = instr.exec_stage_cycle
        else:
            self.remain_time = self.exec_time

    def execute(self):
        raise NotImplementedError


    def set_occupied(self, val):
        self.occupied = val
    
    def is_occupied(self):
        return self.occupied

    def add_remain_time(self, time):
        self.remain_time += time
    
    def cleanup(self):
        self.occupied = False
        self.instr = None
        print("** cleaned up ",self.name)