

class MemoryBus:

    def __init__(self, busy_until=0):
        self.busy_until = busy_until

    def is_busy(self, clk):
        return self.busy_until > clk

    def set_busy_until(self, clk):
        self.busy_until = clk

    def get_busy_until(self):
        return self.busy_until
