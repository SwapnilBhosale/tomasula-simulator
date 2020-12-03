
from func_unit import FUnit


class IntAlu(FUnit):

    def __init__(self, name, latency):
        super().__init__(name, latency)
        self.load_store = None

    def execute(self):
        pass

    def print(self):
        return "load_store: {} , instr: {}".format(self.load_store, self.instr)
