from fp_type import FPType
import constants
import utils


class Instruction():
    def __init__(self):
        self.src_op = None
        self.dest_op = None
        self.third_op = None
        self.have_label = None
        pass

    def decode_instr(self, args):
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
    def __init__(self, args, have_label=None):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 2
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()

    def print_instr(self):
        s = ""
        if self.have_label:
            s = "{}: {} {}, {}".format(self.have_label, constants.LD_INSTR, self.src_op, self.dest_op)
        else:
            s = "{} {}, {}".format(constants.LD_INSTR, self.src_op, self.dest_op)
        print(s)


class SDInstr(Instruction):
    def __init__(self):
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 2


class ADDDInstr(Instruction):
    def __init__(self, args, have_label=None):
        self.processing_unit = FPType.FPAdder
        self.exec_stage_cycle = 2
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op , self.third_op = utils.parse_args(args)
        self.print_instr()

    def print_instr(self):
        s = ""
        if self.have_label:
            s = "{}: {} {}, {}, {}".format(self.have_label, constants.ADDD_INSTR, self.src_op, self.dest_op, self.third_op)
        else:
            s = "{} {}, {}, {}".format(constants.ADDD_INSTR, self.src_op, self.dest_op, self.third_op)
        print(s)


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
        self.src_op, self.dest_op = utils.parse_args(args)
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
        self.decode_instr(None)

    def decode_instr(self, args):
        self.print_instr()

    def print_instr(self):
        print("{}".format(constants.HLT_INSTR))
