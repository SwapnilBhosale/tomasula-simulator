
class Resource:

    def __init(self):
        self.fetch = False
        self.issue = False

        self.fp_mult = []
        self.fp_add = []
        self.fp_div = []
        self.int_alu = False
        self.fp_load = False
        self.fp_branch = False

        self.fp_mul_cycles = 0
        self.fp_add_cycles = 0
        self.fp_div_cycles = 0
