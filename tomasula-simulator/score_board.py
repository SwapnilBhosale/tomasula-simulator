from fp_type import FPType
from cpu import CPU
import constants


class ScoreBoard:

    def __init__(self, chip):
        self.fetch = []
        self.issue = []
        self.read = []
        self.exec = []
        self.chip = chip
        self.res = []
        self.cleanup_fu = []

    def fetch_stage(self, instr):
        if not instr:
            self.chip.cpu.reg_pc += 1
            return
        print("*********** 1 Fetch\n")
        # if we can not issue next nstruction,
        # we should not fetch next instruction
        if len(self.fetch) == 0:
            print(" instr : {}".format(
                instr.print_instr(is_print=False)))
            instr.res.append(self.chip.cpu.curr_clock)
            self.fetch.append(instr)
            self.chip.cpu.reg_pc += 1

        else:
            print("WARN: Can not fetch, fetch buffer is busy")

    def issue_stage(self):
        print("********** 2 Issue\n")
        if len(self.fetch) == 0:
            #print("No instruction to issue")
            return
        else:
            next_instr = self.fetch[0]
            res = self.__assign_processing_unit(next_instr)
            if res:
                # add fetch complete cycle number
                next_instr.res.append(self.chip.cpu.curr_clock)
                print("Assigned to FP: {}, instr: {}".format(next_instr.processing_unit,
                                                             next_instr.print_instr(is_print=False)))
                self.issue.append(next_instr)
                # next_instr.execute_instr(self.chip)
                # self.chip.print_cpu()
                # print("")
                self.fetch.pop()
                # self.chip.print_memory()
            else:

                if len(next_instr.struct_hazard) == 0:
                    next_instr.struct_hazard.append(self.chip.cpu.curr_clock)
                if len(next_instr.waw_hazard) == 0:
                    next_instr.waw_hazard.append(self.chip.cpu.curr_clock)

    def read_stage(self):
        print("********** 3 Read\n")
        temp = []
        for i, next_instr in enumerate(self.issue):
            raw_harards = self.check_raw_hazards(next_instr)
            if not raw_harards:
                next_instr.res.append(self.chip.cpu.curr_clock)
                self.read.append(next_instr)
                print("instr: {}".format(
                    next_instr.print_instr(is_print=False)))
                temp.append(i)
            else:
                print("^^^ RAW hazard for instr: {}".format(
                    next_instr.print_instr(is_print=False)))

        # remove isntructions from read stage since added to the exe stage
        self.issue = [next_instr for i, next_instr in enumerate(
            self.issue) if i not in temp]

    def exec_stage(self):
        print("********* 4 Exec,  ", self.read)
        temp = []
        for i, next_instr in enumerate(self.read):
            if next_instr.processing_unit == FPType.IntALU:
                if next_instr.is_load_store_instr():
                    if next_instr.total_cycles == next_instr.exec_stage_cycle:
                        next_instr.res.append(self.chip.cpu.curr_clock-1)
                        next_instr.execute_instr(self.chip)
                        self.exec.append(next_instr)
                        print("instr: {}".format(
                            next_instr.print_instr(is_print=False)))
                        temp.append(i)
                        self.cleanup_fu.append((FPType.IntALU, 1))
                    else:
                        self.read[i].total_cycles += 1
                else:

                    if self.chip.cpu.int_alu[0][1] and self.chip.cpu.int_alu[0][0].remain_time == 0:
                        next_instr.res.append(self.chip.cpu.curr_clock-1)
                        # execute instruction
                        next_instr.execute_instr(self.chip)
                        self.exec.append(next_instr)
                        #self.chip.cpu.int_alu[0] = (self.chip.cpu.int_alu[0][0], False)
                        print("instr: {}".format(
                            next_instr.print_instr(is_print=False)))
                        temp.append(i)
                        self.cleanup_fu.append((FPType.IntALU, 0))
                    else:
                        print("decrementing int alu time by 1: ",
                              self.chip.cpu.int_alu[0][0].remain_time)
                        self.chip.cpu.int_alu[0][0].remain_time -= 1
            elif next_instr.processing_unit == FPType.FPAdder:
                occupied_adders = [i for i, adder in enumerate(
                    self.chip.cpu.fp_adder) if adder[1]]
                print("Occupied headers: {} {}".format(occupied_adders, [
                      adder[0].__dict__ for adder in self.chip.cpu.fp_adder]))
                for adder in occupied_adders:
                    if self.chip.cpu.fp_adder[adder][0].instr == next_instr:
                        if self.chip.cpu.fp_adder[adder][0].remain_time == 0:
                            next_instr.res.append(self.chip.cpu.curr_clock-1)
                            # execute instruction
                            next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_adder[adder] = (self.chip.cpu.fp_adder[adder][0], False)
                            print("adder instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)
                            self.cleanup_fu.append((FPType.FPAdder, adder))
                        else:
                            self.chip.cpu.fp_adder[adder][0].remain_time -= 1
            elif next_instr.processing_unit == FPType.FPDiv:
                occupied_div = [i for i, divider in enumerate(
                    self.chip.cpu.fp_divider) if divider[1]]
                for divider in occupied_div:
                    if self.chip.cpu.fp_divider[divider][0].instr == next_instr:
                        if self.chip.cpu.fp_divider[divider][0].remain_time == 0:
                            next_instr.res.append(self.chip.cpu.curr_clock-1)
                            # execute instruction
                            next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_divider[divider] = (self.chip.cpu.fp_divider[divider][0], False)
                            print("instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)
                            self.cleanup_fu.append((FPType.FPDiv, divider))
                        else:
                            self.chip.cpu.fp_divider[divider][0].remain_time -= 1
            elif next_instr.processing_unit == FPType.FPMul:
                occupied_mul = [i for i, mul in enumerate(
                    self.chip.cpu.fp_mul) if mul[1]]
                for mul in occupied_mul:
                    if self.chip.cpu.fp_mul[mul][0].instr == next_instr:
                        if self.chip.cpu.fp_mul[mul][0].remain_time == 0:
                            next_instr.res.append(self.chip.cpu.curr_clock-1)
                            # execute instruction
                            next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_mul[mul] = (self.chip.cpu.fp_mul[mul][0], False)
                            print("instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)
                            self.cleanup_fu.append((FPType.FPMul, mul))
                        else:
                            self.chip.cpu.fp_mul[mul][0].remain_time -= 1

        self.read = [next_instr for i, next_instr in enumerate(
            self.read) if i not in temp]

    def set_fu_active(self):

        while self.cleanup_fu:
            fu_type, index = self.cleanup_fu.pop(-1)
            if fu_type == FPType.IntALU:
                if index == 1:
                    self.chip.cpu.int_alu[0][0].load_store = None
                    self.chip.cpu.int_alu[0] = (
                        self.chip.cpu.int_alu[0][0], False)
                else:
                    if self.chip.cpu.int_alu[0][0].load_store and self.chip.cpu.int_alu[0][1]:
                        self.chip.cpu.int_alu[0] = (
                            self.chip.cpu.int_alu[0][0], True)
                    else:
                        self.chip.cpu.int_alu[0] = (
                            self.chip.cpu.int_alu[0][0], False)
            if fu_type == FPType.FPAdder:
                self.chip.cpu.fp_adder[index] = (
                    self.chip.cpu.fp_adder[index][0], False)
            if fu_type == FPType.FPMul:
                self.chip.cpu.fp_mul[index] = (
                    self.chip.cpu.fp_mul[index][0], False)
            if fu_type == FPType.FPDiv:
                self.chip.cpu.fp_divider[index] = (
                    self.chip.cpu.fp_divider[index][0], False)

    def write_stage(self):
        print("************** 5 Write \n")
        while self.exec:
            next_instr = self.exec.pop()
            next_instr.res.append(self.chip.cpu.curr_clock-1)
            self.res.append(next_instr)
            print(
                "-----------------------------------------------------------------------------")
            print("==================", end=" ")
            print("Finished Instruction {} score: {}".format(
                next_instr.print_instr(is_print=False), next_instr.res), end=" ")
            print("==================")
            print(
                "-----------------------------------------------------------------------------")

    def check_waw_hazards(self, next_instr):
        res = False
        if next_instr.inst_str == constants.LW_INSTR or next_instr.inst_str == constants.SD_INSTR:
            if self.check_raw_hazards(next_instr.src_op):
                res = True
        print("WAW hazard for instr ", next_instr)
        return res

    def check_raw_hazards(self, next_instr):
        res = False
        if next_instr.third_op is not None:
            if self.chip.cpu.is_raw_hazard(next_instr, next_instr.dest_op) or self.chip.cpu.is_raw_hazard(next_instr, next_instr.third_op):
                next_instr.raw_hazard.append(self.chip.cpu.curr_clock)
                res = True
        elif next_instr.inst_str == constants.LW_INSTR or next_instr.inst_str == constants.SD_INSTR:
            start_ind, end_ind = next_instr.dest_op.index(
                "("), next_instr.dest_op.index(")")
            reg = next_instr.dest_op[start_ind+1: end_ind]
            if self.chip.is_raw_hazard(next_instr, reg):
                res = True
        return res

    def __assign_processing_unit(self, next_instr):

        #print("***** Assigning unit for inst: {}".format(next_instr.print_instr(is_print=False)))
        pu_type = next_instr.processing_unit
        #print("processing unit: ", pu_type.name)
        res = False
        # if next instr RUNs in IntALU then no Hazards given in problem statement
        if pu_type == FPType.IntALU:
            print("alu: ", self.chip.cpu.int_alu[0][0].print())
            if next_instr.is_load_store_instr() and self.chip.cpu.int_alu[0][1] and self.chip.cpu.int_alu[0][0].instr.inst_str == constants.LI_INSTR and not self.chip.cpu.int_alu[0][0].load_store and not self.check_waw_hazards(next_instr):
                print("assigning because of exception")
                self.chip.cpu.int_alu[0][0].load_store = next_instr
                res = True
            else:
                if not self.chip.cpu.int_alu[0][1] and not self.check_waw_hazards(next_instr) and not self.chip.cpu.int_alu[0][0].load_store:
                    self.chip.cpu.int_alu[0][0].set_instruction(next_instr)
                    self.chip.cpu.int_alu[0] = (
                        self.chip.cpu.int_alu[0][0], True)
                    res = True
                else:
                    print("WARN: Structural HAZARD: NO Int alu available: {}".format(
                        next_instr.print_instr(is_print=False)))
        elif pu_type == FPType.FPAdder:
            free_adders = [i for i, adder in enumerate(
                self.chip.cpu.fp_adder) if not adder[1]]
            if len(free_adders) == 0:
                print("WARN: Structural HAZARD: NO FP adder available: {}".format(
                    next_instr.print_instr(is_print=False)))
            else:
                if not self.check_waw_hazards(next_instr):
                    selected_adder, taken = self.chip.cpu.fp_adder[free_adders[0]]
                    selected_adder.set_instruction(next_instr)
                    self.chip.cpu.fp_adder[free_adders[0]] = (
                        selected_adder, not taken)
                    print("Added adder: ", self.chip.cpu.fp_adder)
                    res = True
                else:
                    print("WAW hazards {}".format(
                        next_instr.print_instr(is_print=False)))
        elif pu_type == FPType.FPDiv:
            free_dividers = [i for i, divider in enumerate(
                self.chip.cpu.fp_divider) if not divider[1]]
            if len(free_dividers) == 0:
                print("WARN: Structural HAZARD: NO FP dividers available: {}".format(
                    next_instr.print_instr(is_print=False)))
            else:
                if not self.check_waw_hazards(next_instr):
                    selected_divider, taken = self.chip.cpu.fp_divider[free_dividers[0]]
                    selected_divider.set_instruction(next_instr)
                    self.chip.cpu.fp_divider[free_dividers[0]] = (
                        selected_divider, not taken)
                    res = True
                else:
                    print("WAW hazards {}".format(
                        next_instr.print_instr(is_print=False)))
        elif pu_type == FPType.FPMul:
            free_multipliers = [i for i, multiplier in enumerate(
                self.chip.cpu.fp_mul) if not multiplier[1]]
            if len(free_multipliers) == 0:
                print("WARN: Structural HAZARD: NO FP free_multipliers available: {}".format(
                    next_instr.print_instr(is_print=False)))
            else:
                if not self.check_waw_hazards(next_instr):
                    selected_multiplier, taken = self.chip.cpu.fp_mul[free_multipliers[0]]
                    selected_multiplier.set_instruction(next_instr)
                    self.chip.cpu.fp_mul[free_multipliers[0]] = (
                        selected_multiplier, not taken)
                    res = True
                else:
                    print("WAW hazards {}".format(
                        next_instr.print_instr(is_print=False)))

        return res
