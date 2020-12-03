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
        self.total_cycles = 0

    def __repr__(self):
        return self.print_instr(is_print=False)

    def decode_instr(self, args):
        raise NotImplementedError()

    def execute_instr(self, cpu, data):
        raise NotImplementedError()

    def print_instr(self, is_print=True):
        if type(self) == HLTInstr:
            # print("HLT")
            return "HLT"
        args = [self.src_op, self.dest_op]
        if self.third_op is not None:
            args.append(self.third_op)
        s = ""
        if self.have_label:
            s = "{}: {} {}".format(
                self.have_label, self.inst_str, ", ".join(args),)
        else:
            s = "{} {}".format(self.inst_str, ", ".join(
                args))
        if is_print:
            print(s)
        else:
            return s

    def __eq__(self, other):
        return self.inst_str == other.inst_str and self.src_op == other.src_op and self.dest_op == other.dest_op

    def is_load_store_instr(self):
        return self.inst_str == constants.LW_INSTR or self.inst_str == constants.LD_INSTR or self.inst_str == constants.SW_INSTR or self.inst_str == constants.SD_INSTR

    def get_r1(self):
        raise NotImplementedError()

    def get_r2(self):
        #print("instr str: ",self.inst_str)
        raise NotImplementedError()

    def get_r3(self):
        raise NotImplementedError()

    def is_branch_instr(self):
        return self.inst_str == constants.BNE_INSTR or self.inst_str == constants.BEQ_INSTR or self.inst_str == constants.J_INSTR


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        cpu.gpr[r1][0] = data

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        return int(self.dest_op[open_ind+2: clos_ind])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        cpu.gpr[r1][0] = data
        data1 = cpu.gpr[r1]
        offset = int(self.dest_op[:self.dest_op.index("(")])
        addr = cpu.gpr[r2][0] + offset
        dcache.update_val(addr, data1)

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        return int(self.dest_op[open_ind+2: clos_ind])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        return int(self.dest_op[open_ind+2: clos_ind])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, chip, data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        open_ind, clos_ind = self.dest_op.index("("), self.dest_op.index(")")
        return int(self.dest_op[open_ind+2: clos_ind])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, chip,  data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, chip,  data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, chip,  data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, chip,  data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, cpu,  data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = self.get_r3()
        cpu.gpr[r1][0] = cpu.gpr[r2][0] + cpu.gpr[r3][0]

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = int(self.third_op)
        cpu.gpr[r1][0] = cpu.gpr[r2][0] + r3

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = self.get_r3()
        cpu.gpr[r1][0] = cpu.gpr[r2][0] - cpu.gpr[r3][0]

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = int(self.third_op)
        cpu.gpr[r1][0] = cpu.gpr[r2][0] - r3

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = self.get_r3()
        cpu.gpr[r1][0] = cpu.gpr[r2][0] & cpu.gpr[r3][0]

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = int(self.dest_op)
        cpu.gpr[r1][0] = cpu.gpr[r2][0] & r3

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, chip):
        # print("instr:{} src register: {} , dst val: {} third_op: {}".format(self.inst_str,
        #    self.src_op, self.dest_op, self.third_op))
        chip.cpu.gpr[int(self.src_op[1])-1] = chip.cpu.gpr[int(self.dest_op[1]
                                                               )-1] | chip.cpu.gpr[int(self.third_op[1])-1]

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return int(self.third_op[1:])


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = self.get_r2()
        r3 = int(self.dest_op)
        cpu.gpr[r1][0] = cpu.gpr[r2][0] | r3

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        print("before executing: ", cpu.gpr)
        r1 = self.get_r1()
        r2 = int(self.dest_op)
        cpu.gpr[r1][0] = r2
        print("************ executed instruction LI: ", cpu.gpr, " r2: ", r2)

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return -1

    def get_r3(self):
        return -1


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
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = int(self.dest_op)
        cpu.gpr[r1][0] = r2 << 16

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return -1

    def get_r3(self):
        return -1


class HLTInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.HLT_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 0
        self.decode_instr(None)
        self.have_label = have_label

    def get_r1(self):
        return -1

    def get_r2(self):
        return -1

    def get_r3(self):
        return -1

    def decode_instr(self, args):
        pass
        # self.print_instr()

    def execute_instr(self, cpu):
        pass


class BNEInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.BNE_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return -1


class BEQInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.BEQ_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op, self.dest_op, self.third_op = utils.parse_args(args)
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        pass

    def get_r1(self):
        return int(self.src_op[1:])

    def get_r2(self):
        return int(self.dest_op[1:])

    def get_r3(self):
        return -1


class JInstr(Instruction):
    def __init__(self, args, have_label=None):
        super().__init__()
        self.inst_str = constants.J_INSTR
        self.processing_unit = FPType.IntALU
        self.exec_stage_cycle = 1
        self.have_label = have_label
        self.decode_instr(args)

    def decode_instr(self, args):
        self.src_op = utils.parse_args(args)
        # self.print_instr()

    def execute_instr(self, cpu, data, dcache):
        r1 = self.get_r1()
        r2 = int(self.dest_op)
        cpu.gpr[r1][0] = r2 << 16

    def get_r1(self):
        return self.src_op

    def get_r2(self):
        return -1

    def get_r3(self):
        return -1
