from fp_type import FPType
import constants


class Instruction():
    def __init__(self):
        self.src_op = None
        self.dest_op = None
        pass

    def decode_instr(self):
        raise NotImplementedError()

    def print_instr(self):
        raise NotImplementedError()


class LWInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1


class SWInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1


class LDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 2


class SDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 2


class ADDDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.FPAdder
        self.exec_stage_cycle = 2


class SUBDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.FPAdder
        self.exec_stage_cycle = None


class MULDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.FPMul
        self.exec_stage_cycle = None


class DIVDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.FPDiv
        self.exec_stage_cycle = None


class DADDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class DADDIInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class DSUBInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class DSUBIInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class ANDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class ANDIInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class ORInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class ORIInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class LIInstr(Instruction):
    def __init__(self, args, have_label=None):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = list(
            map(lambda x: x.strip(), args.split(",")))
        self.print_instr()

    def print_instr(self):
        print("{} {}, {}".format(constants.LI_INSTR, self.src_op, self.dest_op))


class LUIInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None


class HLTInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 0

    def decode_instr(self, args):
        self.print_instr()

    def print_instr(self):
        print("{}".format(constants.HLT_INSTR))
