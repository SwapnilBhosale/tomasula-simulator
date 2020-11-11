
from .fp_type import FPType
from int_alu import IntAlu
from fp_adder import FPAdder
from fp_divider import FPDivider
from fp_multiply import FP_Multiply
class CPU:

    def __init__(self):
        self.gpr = [0] * 32
        self.fpr = [0] * 32
        self.IntALU = IntAlu()
        self.FPAdder = None
        self.FPDivider = None
        self.FPMul = None

    def add_fp_unit(self, fp_type, n, latency):
        if fp_type == FPType.FPAdder:
            self.FPAdder = [FPAdder("FP-Adder" + (i+1), latency) for i in range(n)]
        if fp_type == FPType.FPDiv:
            self.FPDivider = [FPDivider("FP-Divider" + (i+1), latency) for i in range(n)]
        if fp_type == FPType.FPMul:
            self.FPDivider = [FP_Multiply("FP-Multiplyer" + (i+1), latency) for i in range(n)]

    