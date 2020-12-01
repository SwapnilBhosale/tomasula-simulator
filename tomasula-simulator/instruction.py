from fp_type import FPType
import constants
import utils


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
            s = "{}: {} {}    {}-{}-{}".format(
                self.have_label, self.inst_str, ", ".join(args), self.raw_hazard, self.waw_hazard, self.struct_hazard)
        else:
            s = "{} {}   {}-{}-{}".format(self.inst_str, ", ".join(
                args), self.raw_hazard, self.waw_hazard, self.struct_hazard)
        if is_print:
            print(s)
        else:
            return s

    def __eq__(self, other):
        return self.inst_str == other.inst_str and self.src_op == other.src_op and self.dest_op == other.dest_op


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , immediate val: {}".format(self.inst_str,
        #    self.src_op, self.dest_op))
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        #print("LW putting to reg: {} value: {}".format(int(self.src_op[1]), chip.main_memory[(int(self.dest_op[:open_ind]) + chip.cpu.gpr[int(self.dest_op[open_ind+2: clos_ind])]) // 4]))
        chip.cpu.gpr[int(self.src_op[1])-1] = chip.main_memory[(int(self.dest_op[:open_ind]
                                                                    ) + chip.cpu.gpr[int(self.dest_op[open_ind+2: clos_ind]) - 1]) // 4]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , immediate val: {}".format(self.inst_str,
        #    self.src_op, self.dest_op))
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        #print("SW putting to memory: {} value: {}".format(chip.main_memory[(int(self.dest_op[:open_ind]) + chip.cpu.gpr[int(self.dest_op[open_ind+2: clos_ind]) - 1]) // 4]), int(self.src_op[1]))
        chip.main_memory[(int(self.dest_op[:open_ind]) + chip.cpu.gpr[int(
            self.dest_op[open_ind+2: clos_ind]) - 1]) // 4] = chip.cpu.gpr[int(self.src_op[1])-1]


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

    def execute_instr(self, chip):

        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        print("LD putting to REG: {} value: {}    {} - {}  {}".format(int(self.src_op[1]), chip.main_memory[(int(self.dest_op[:open_ind]) + chip.cpu.gpr[int(
            self.dest_op[open_ind+2: clos_ind])]) // 4], int(self.dest_op[:open_ind]),  chip.cpu.gpr[int(self.dest_op[open_ind+2: clos_ind]) - 1], chip.main_memory[66]))
        chip.cpu.fpr[int(self.src_op[1])-1] = chip.main_memory[(int(self.dest_op[:open_ind]
                                                                    ) + chip.cpu.gpr[int(self.dest_op[open_ind+2: clos_ind]) - 1]) // 4]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , immediate val: {}".format(self.inst_str,
        #    self.src_op, self.dest_op))
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        chip.main_memory[(int(self.dest_op[:open_ind]) + chip.cpu.gpr[int(
            self.dest_op[open_ind+2: clos_ind]) - 1]) // 4] = chip.cpu.fpr[int(self.src_op[1])-1]
        print("added to memory SW : ", chip.cpu.__dict__)


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, chip.cpu.fpr[int(self.dest_op[1])-1] , chip.cpu.fpr[int(self.third_op[1])-1]))
        chip.cpu.fpr[int(self.src_op[1])-1] = chip.cpu.fpr[int(self.dest_op[1]
                                                               )-1] + chip.cpu.fpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.fpr[int(self.src_op[1])-1] = chip.cpu.fpr[int(self.dest_op[1]
                                                               )-1] - chip.cpu.fpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.fpr[int(self.src_op[1])-1] = chip.cpu.fpr[int(self.dest_op[1]
                                                               )-1] * chip.cpu.fpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.fpr[int(self.src_op[1])-1] = chip.cpu.fpr[int(self.dest_op[1]
                                                               )-1] // chip.cpu.fpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1]
                                                               )-1] + chip.cpu.gpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(
            self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1])-1] + int(self.third_op)


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1]
                                                               )-1] - chip.cpu.gpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(
            self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1])-1] - int(self.third_op)


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1]
                                                               )-1] & chip.cpu.gpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(
            self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1])-1] & int(self.third_op)


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1]
                                                               )-1] | chip.cpu.gpr[int(self.third_op[1])-1]


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

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(
            self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1])-1] | int(self.third_op)


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

    def execute_instr(self, chip):
        # print("src register: {} , immediate val: {}".format(
        #    self.src_op, self.dest_op))
        chip.cpu.gpr[int(self.src_op[1])-1] = int(self.dest_op)
        #print("added to GPR : ", chip.cpu.__dict__)


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

    def execute_instr(self, cpu):
        # print("src register: {} , immediate val: {}".format(
        #    self.src_op, self.dest_op))
        cpu.gpr[int(self.src_op[1])-1] = int(self.dest_op) << 16
        #print("added to GPR : ", cpu.__dict__)


class HLTInstr(Instruction):
    def __init__(self):
        super().__init__()
        self.inst_str = constants.HLT_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 0
        self.decode_instr(None)

    def decode_instr(self, args):
        self.print_instr()

    def execute_instr(self, cpu):
        import sys
        sys.exit(0)
