from fp_type import FPType
import constants
import utils
from cpu import CPU


class Instruction():
    def __init__(self):
        self.inst_str = None
        self.src_op = None
        self.dest_op = None
        self.third_op = None
        self.have_label = None
        self.raw_hazard = []
        self.waw_hazard = []
        self.struct_hazard = []
        self.res = []

    def decode_instr(self, args):
        raise NotImplementedError()

    def execute_instr(self):
        raise NotImplementedError()

    def print_instr(self, is_print=True):
        if type(self) == HLTInstr:
            print("HLT")
            return
        args = [self.src_op, self.dest_op]
        if self.third_op is not None:
            args.append(self.third_op)
        s = ""
        if self.have_label:
            s = "{}: {} {}".format(
                self.have_label, self.inst_str, ", ".join(args))
        else:
            s = "{} {}".format(self.inst_str, ", ".join(args))
        if is_print:
            print(s)
        else:
            return s


class LWInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.LW_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()


class SWInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.SW_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()


class LDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.LD_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 2
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()


class SDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.SD_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 2
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()


class ADDDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.ADDD_INSTR
        self.processing_unit = FPType.FPAdder
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class SUBDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.SUBD_INSTR
        self.processing_unit = FPType.FPAdder
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class MULDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.MULD_INSTR
        self.processing_unit = FPType.FPMul
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class DIVDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.DIVD_INSTR
        self.processing_unit = FPType.FPDiv
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class DADDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.DADD_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class DADDIInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.DADDI_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class DSUBInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.DSUB_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class DSUBIInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.DSUBI_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class ANDInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.AND_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class ANDIInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.ANDI_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class ORInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.OR_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class ORIInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.ORI_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        self.print_instr()


class LIInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.LI_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()

    def execute_instr(self, cpu):
        print("src register: {} , immediate val: {}".format(
            self.src_op, self.dest_op))
        cpu.gpr[int(self.src_op[1])-1] = int(self.dest_op)
        print("added to GPR : ", cpu.__dict__)


class LUIInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.LUI_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = None
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op = utils.parse_args(args)
        self.print_instr()


class HLTInstr(Instruction):
    def __init__(self):
        super().__init__()
        self.inst_str = constants.HLT_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 0
        self.decode_instr(None)

    def decode_instr(self, args):
        self.print_instr()
