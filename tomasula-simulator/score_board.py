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
        self.cpu = chip.cpu
        self.res = []
        self.cleanup_fu = []

        self.fetch_stall = False
        self.fetch_cycles = 0

    def fetch_stage(self):
        if len(self.fetch) == 0:
            if not self.fetch_stall:
                fetch_cycles = self.chip.cpu.icache.fetch_instruction(
                    self.chip.cpu.reg_pc)
                print("*** from cache: ", fetch_cycles, " reg pc : ",
                      self.cpu.reg_pc, "clokc: ", self.cpu.clk_mgr.get_clock())
                if fetch_cycles > 1:
                    self.fetch_stall = True
                    self.fetch_cycles = fetch_cycles
                else:
                    print(self.chip.instr, " &&& reg_pc: ", self.cpu.reg_pc)
                    self.fetch.append(self.chip.instr[self.chip.cpu.reg_pc])
                    self.fetch[0].res.append(self.cpu.clk_mgr.get_clock())
                    self.cpu.reg_pc += 1

                    print("Fetched instruction: ",
                          self.fetch[0], " at clock: ", self.cpu.clk_mgr.get_clock())

            else:
                print("in else not stall : ", self.fetch_cycles)
                if self.fetch_cycles == 1:
                    print(self.chip.instr, " &&& reg_pc: ", self.cpu.reg_pc)
                    self.fetch.append(self.chip.instr[self.chip.cpu.reg_pc])
                    self.fetch_stall = False
                    self.fetch[0].res.append(self.cpu.clk_mgr.get_clock())
                    print("Fetched instruction else: ",
                          self.fetch[0], " at clock: ", self.cpu.clk_mgr.get_clock())
                    self.cpu.reg_pc += 1
                else:
                    self.fetch_cycles -= 1

    def issue_stage(self):
        print("********** 2 Issue ", self.fetch)
        if len(self.fetch) == 0:
            print("No instruction to issue")
            return
        else:
            next_instr = self.fetch[0]
            res = self.__can_assign_processing_unit(next_instr)
            is_waw_hazard = self.check_waw_hazards(next_instr)
            if res:
                if not is_waw_hazard:
                    # add fetch complete cycle number
                    next_instr.res.append(self.cpu.clk_mgr.get_clock())
                    print("Assigned to FP: {}, instr: {}".format(next_instr.processing_unit,
                                                                 next_instr.print_instr(is_print=False)))
                    self.set_fp_busy(next_instr)
                    self.issue.append(next_instr)
                    if not (next_instr.inst_str == constants.SD_INSTR or next_instr.inst_str == constants.SW_INSTR):
                        self.set_reg_write(
                            next_instr.get_r1(), "R" in next_instr.src_op)
                    self.fetch.pop()
                else:
                    if len(next_instr.waw_hazard) == 0:
                        next_instr.waw_hazard.append(
                            self.chip.cpu.clk_mgr.get_clock())
            else:
                if len(next_instr.struct_hazard) == 0:
                    next_instr.struct_hazard.append(
                        self.chip.cpu.clk_mgr.get_clock())

    def read_stage(self):
        print("********** 3 Read\n")
        temp = []
        for i, next_instr in enumerate(self.issue):
            if len(next_instr.raw_hazard) == 0:
                raw_harards = self.check_raw_hazards(next_instr)
                if not raw_harards:
                    next_instr.res.append(self.chip.cpu.clk_mgr.get_clock())
                    temp.append(i)
                    if next_instr.is_load_store_instr() and not next_instr.d_cache_hit:
                        data_block = self.check_and_load_from_cache(
                            0, next_instr)
                        self.cpu.load_store_unit[0].add_remain_time(
                            data_block.clock_cycles)

                    self.read.append(next_instr)
                    print("instr: {}".format(
                        next_instr.print_instr(is_print=False)))
                else:
                    if len(next_instr.raw_hazard) == 0:
                        next_instr.raw_hazard.append(
                            self.chip.cpu.clk_mgr.get_clock())
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
                occupied_int_alu = [i for i, alu in enumerate(
                    self.chip.cpu.int_alu) if alu.is_occupied()]
                print("Occupied headers: {} {}".format(occupied_int_alu, [
                      alu.__dict__ for alu in self.chip.cpu.int_alu]))
                for alu in occupied_int_alu:
                    if self.chip.cpu.int_alu[alu].instr == next_instr:
                        if self.chip.cpu.int_alu[alu].remain_time == 1:
                            next_instr.res.append(
                                self.chip.cpu.clk_mgr.get_clock())
                            # execute instruction
                            # next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_adder[adder] = (self.chip.cpu.fp_adder[adder][0], False)
                            temp.append(i)
                            print("adder instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                        else:
                            print("Decrementing integer remain time")
                            self.chip.cpu.int_alu[alu].remain_time -= 1
            elif next_instr.processing_unit == FPType.FPAdder:
                occupied_adders = [i for i, adder in enumerate(
                    self.chip.cpu.fp_adder) if adder.is_occupied()]
                print("Occupied headers: {} {}".format(occupied_adders, [
                      adder[0].__dict__ for adder in self.chip.cpu.fp_adder]))
                for adder in occupied_adders:
                    if self.chip.cpu.fp_adder[adder][0].instr == next_instr:
                        if self.chip.cpu.fp_adder[adder][0].remain_time == 1:
                            next_instr.res.append(
                                self.chip.cpu.clk_mgr.get_clock())
                            # execute instruction
                            # next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_adder[adder] = (self.chip.cpu.fp_adder[adder][0], False)
                            print("adder instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)
                        else:
                            self.chip.cpu.fp_adder[adder].remain_time -= 1
            elif next_instr.processing_unit == FPType.FPDiv:
                occupied_div = [i for i, divider in enumerate(
                    self.chip.cpu.fp_divider) if divider.is_occupied()]
                for divider in occupied_div:
                    if self.chip.cpu.fp_divider[divider].instr == next_instr:
                        if self.chip.cpu.fp_divider[divider].remain_time == 1:
                            next_instr.res.append(
                                self.chip.cpu.clk_mgr.get_clock())
                            # execute instruction
                            # next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_divider[divider] = (self.chip.cpu.fp_divider[divider][0], False)
                            print("instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)

                        else:
                            self.chip.cpu.fp_divider[divider].remain_time -= 1
            elif next_instr.processing_unit == FPType.FPMul:
                occupied_mul = [i for i, mul in enumerate(
                    self.chip.cpu.fp_mul) if mul.is_occupied()]
                for mul in occupied_mul:
                    if self.chip.cpu.fp_mul[mul].instr == next_instr:
                        if self.chip.cpu.fp_mul[mul].remain_time == 0:
                            next_instr.res.append(
                                self.chip.cpu.clk_mgr.get_clock())
                            # execute instruction
                            # next_instr.execute_instr(self.chip)
                            self.exec.append(next_instr)
                            #self.chip.cpu.fp_mul[mul] = (self.chip.cpu.fp_mul[mul][0], False)
                            print("instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)
                        else:
                            self.chip.cpu.fp_mul[mul].remain_time -= 1
            elif next_instr.processing_unit == FPType.LoadStoreUnit:
                occupied_load_store = [i for i, load_store in enumerate(
                    self.chip.cpu.load_store_unit) if load_store.is_occupied()]
                for load_store in occupied_load_store:
                    if self.chip.cpu.load_store_unit[load_store].instr == next_instr:
                        if self.chip.cpu.load_store_unit[load_store].remain_time == 1:
                            next_instr.res.append(
                                self.chip.cpu.clk_mgr.get_clock())
                            # execute instruction
                            next_instr.execute_instr(self.chip)
                            # self.exec.append(next_instr)
                            #self.chip.cpu.fp_mul[mul] = (self.chip.cpu.fp_mul[mul][0], False)
                            print("instr: {}".format(
                                next_instr.print_instr(is_print=False)))
                            temp.append(i)
                        else:
                            self.chip.cpu.load_store_unit[load_store].remain_time -= 1

        self.read = [next_instr for i, next_instr in enumerate(
            self.read) if i not in temp]

    def check_and_load_from_cache(self, offset, instr):
        r2_open_ind, _ = instr.dest_op.index(
            "("), instr.dest_op.index(")")

        reg2 = instr.get_r2()
        reg1 = instr.get_r1()
        addr = self.cpu.gpr[reg2][0] + \
            int(instr.dest_op[:r2_open_ind])
        data_block = self.cpu.dcache.fetch_data(addr + offset)
        instr.exec_stage_cycle += data_block.clock_cycles
        if instr.inst_str == constants.SW_INSTR:
            self.cpu.dcache.update_val(addr + offset, self.cpu.gpr[reg1][0])
        instr.is_d_cache_hit = True
        print("############## loaded from clock: {} cache: updated clock to: {} {}- {}".format(
            self.cpu.clk_mgr.get_clock(), instr, instr.exec_stage_cycle, data_block.clock_cycles))
        return data_block

    def set_reg_write(self, reg, pc, is_gpr=True):
        if reg and reg > 0:
            if is_gpr:
                self.cpu.gpr[reg][1] = pc
            else:
                self.cpu.fpr[reg][1] = pc

    def set_fp_busy(self, instr):
        pu_type = instr.processing_unit

        if pu_type == FPType.IntALU:
            for i in range(len(self.cpu.int_alu)):
                if not self.cpu.int_alu[i].is_occupied():
                    self.cpu.int_alu[i].set_occupied(True)
                    self.cpu.int_alu[i].set_instruction(instr)
                    instr.assigned_index = i
        elif pu_type == FPType.FPAdder:
            for i in range(len(self.cpu.fp_adder)):
                if not self.cpu.fp_adder[i].is_occupied():
                    self.cpu.fp_adder[i].set_occupied(True)
                    self.cpu.fp_adder[i].set_instruction(instr)
                    instr.assigned_index = i
        elif pu_type == FPType.FPDiv:
            for i in range(len(self.cpu.fp_divider)):
                if not self.cpu.fp_divider[i].is_occupied():
                    self.cpu.fp_divider[i].set_occupied(True)
                    self.cpu.fp_divider[i].set_instruction(instr)
                    instr.assigned_index = i
        elif pu_type == FPType.FPMul:
            for i in range(len(self.cpu.fp_mul)):
                if not self.cpu.fp_mul[i].is_occupied():
                    self.cpu.fp_mul[i].set_occupied(True)
                    self.cpu.fp_mul[i].set_instruction(instr)
                    instr.assigned_index = i
        elif pu_type == FPType.LoadStoreUnit:
            for i in range(len(self.cpu.load_store_unit)):
                if not self.cpu.load_store_unit[i].is_occupied():
                    self.cpu.load_store_unit[i].set_occupied(True)
                    self.cpu.load_store_unit[i].set_instruction(instr)
                    instr.assigned_index = i
        elif pu_type == FPType.BranchUnit:
            for i in range(len(self.cpu.branch_unit)):
                if not self.cpu.branch_unit[i].is_occupied():
                    self.cpu.branch_unit[i].set_occupied(True)
                    self.cpu.branch_unit[i].set_instruction(instr)
                    instr.assigned_index = i

    def set_fu_active(self):
        while self.cleanup_fu:
            instr = self.cleanup_fu.pop(-1)
            pu_type = instr.processing_unit
            if pu_type == FPType.IntALU:
                self.cpu.int_alu[instr.assigned_index].cleanup()
            elif pu_type == FPType.FPAdder:
                self.cpu.fp_adder[instr.assigned_index].cleanup()
            elif pu_type == FPType.FPDiv:
                self.cpu.fp_divider[instr.assigned_index].cleanup()
            elif pu_type == FPType.FPMul:
                self.cpu.fp_mul[instr.assigned_index].cleanup()
            elif pu_type == FPType.LoadStoreUnit:
                self.cpu.load_store_unit[instr.assigned_index].cleanup()
            elif pu_type == FPType.BranchUnit:
                self.cpu.branch_unit[instr.assigned_index].cleanup()

    def write_stage(self):
        print("************** 5 Write \n")
        while self.exec:
            next_instr = self.exec.pop()
            next_instr.res.append(self.cpu.clk_mgr.get_clock())
            self.cleanup_fu.append(next_instr)
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
        if next_instr.src_op and next_instr.dest_op:
            is_gpr = 'R' in next_instr.src_op
            r1 = next_instr.get_r1()
            if is_gpr:
                if self.cpu.gpr[r1][1] > 0:
                    return True
            else:
                if self.cpu.fpr[r1][1] > 0:
                    return True
        return res

    def check_raw_hazards(self, next_instr):
        res = False
        if next_instr.third_op:
            r3 = next_instr.get_r3()
            r2 = next_instr.get_r2()
            r3_str = next_instr.get_r3()
            r2_str = next_instr.get_r2()
            if self.chip.cpu.is_raw_hazard(next_instr, r3, "R" in r3_str) or self.chip.cpu.is_raw_hazard(next_instr, r2, "R" in r2_str):
                res = True
        else:
            r2_str = next_instr.dest_op
            r2 = next_instr.get_r2()
            if self.chip.cpu.is_raw_hazard(next_instr, r2, "R" in r2_str):
                res = True
        return res

    def __can_assign_processing_unit(self, next_instr):

        pu_type = next_instr.processing_unit
        res = False
        # if next instr RUNs in IntALU then no Hazards given in problem statement
        if pu_type == FPType.IntALU:
            for i in range(len(self.cpu.int_alu)):
                if not self.cpu.int_alu[i].is_occupied():
                    res = True
        elif pu_type == FPType.FPAdder:
            for i in range(len(self.cpu.fp_adder)):
                if not self.cpu.fp_adder[i].is_occupied():
                    res = True
        elif pu_type == FPType.FPDiv:
            for i in range(len(self.cpu.fp_divider)):
                if not self.cpu.fp_divider[i].is_occupied():
                    res = True
        elif pu_type == FPType.FPMul:
            for i in range(len(self.cpu.fp_mul)):
                if not self.cpu.fp_mul[i].is_occupied():
                    res = True
        elif pu_type == FPType.LoadStoreUnit:
            for i in range(len(self.cpu.load_store_unit)):
                if not self.cpu.load_store_unit[i].is_occupied():
                    res = True
        elif pu_type == FPType.BranchUnit:
            for i in range(len(self.cpu.branch_unit)):
                if not self.cpu.branch_unit[i].is_occupied():
                    res = True

        '''
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
        '''
        return res
