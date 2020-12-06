from stage import ScoreBoardStage
from cpu import CPU
import constants


class ScoreBoard:

    def __init__(self, clk, fetch_cycle, instr, instrs, cpu, clock_mgr, mem_bus, dcache):
        self.curr_stage = 0
        self.next_stage = 1
        self.raw_hazard = False
        self.waw_hazard = False
        self.war_hazard = False
        self.struct_hazard = False
        self.should_push = False
        self.finish = False

        self.branch_taken = False

        self.clock = clk
        self.cpu = cpu
        self.fetch_cycle = fetch_cycle
        self.exe_cycles = 0
        self.instr = instr
        self.clock_mgr = clock_mgr
        self.mem_bus = mem_bus
        self.instrs = instrs
        self.dcache = dcache

        self.fetch = 0
        self.issue = 0
        self.read = 0
        self.execute = 0
        self.write = 0
        self.sh = 'N'
        self.h_raw = 'N'
        self.h_waw = 'N'
        self.h_war = 'N'

        self.is_next_free = False
        self.is_fetch_free = False
        self.is_d_cache_hit = False

    def is_et_push(self, current_state):
        self.should_push = False
        if current_state == 0:
            if self.is_next_free:
                self.should_push = True
        elif current_state == 1:
            if not self.struct_hazard and not self.waw_hazard and self.is_next_free:
                self.should_push = True
        elif current_state == 2:
            if not self.raw_hazard and self.is_next_free:
                self.should_push = True
        elif current_state == 3:
            if self.is_next_free:
                self.should_push = True
        elif current_state == 4:
            if self.is_next_free and not self.war_hazard:
                self.should_push = True
        elif current_state == 5:
            if self.is_next_free:
                self.should_push = True

    def is_fp_free(self, instruction):
        if instruction.inst_str == constants.MULD_INSTR:
            self.exe_cycles = self.cpu.fp_mul[0].exec_time
            for i in range(len(self.cpu.fp_mul)):
                if not self.cpu.fp_mul[i].is_occupied():
                    return True
        elif instruction.inst_str == constants.ADDD_INSTR or instruction.inst_str == constants.SUBD_INSTR:
            self.exe_cycles = self.cpu.fp_adder[0].exec_time
            for i in range(len(self.cpu.fp_adder)):
                if not self.cpu.fp_adder[i].is_occupied():
                    return True
        elif instruction.inst_str == constants.DIVD_INSTR:
            self.exe_cycles = self.cpu.fp_divider[0].exec_time
            for i in range(len(self.cpu.fp_divider)):
                if not self.cpu.fp_divider[i].is_occupied():
                    return True
        elif instruction.inst_str == constants.AND_INSTR or instruction.inst_str == constants.ANDI_INSTR or instruction.inst_str == constants.DADD_INSTR or instruction.inst_str == constants.DADDI_INSTR or instruction.inst_str == constants.DSUB_INSTR or instruction.inst_str == constants.DSUBI_INSTR or instruction.inst_str == constants.OR_INSTR or instruction.inst_str == constants.ORI_INSTR or instruction.inst_str == constants.LUI_INSTR or instruction.inst_str == constants.LI_INSTR:
            self.exe_cycles = self.cpu.int_alu[0].exec_time
            for i in range(len(self.cpu.int_alu)):
                if not self.cpu.int_alu[i].is_occupied():
                    return True
        elif instruction.is_load_store_instr():
            self.exe_cycles = 1
            if not self.cpu.fu_load:
                return True
        elif instruction.is_branch_instr() or instruction.inst_str == constants.HLT_INSTR:
            self.exe_cycles = 1
            if not self.cpu.fu_branch:
                return True
        else:
            print("WARN: Can not decode instuction. Invalid Instructions")
        return False

    def set_fp_busy(self, instr):
        aa = instr.inst_str
        if aa == constants.MULD_INSTR:
            for i in range(len(self.cpu.fp_mul)):
                if not self.cpu.fp_mul[i].is_occupied():
                    self.cpu.fp_mul[i].set_occupied(True)
                    break
        elif aa == constants.ADDD_INSTR or aa == constants.SUBD_INSTR:
            for i in range(len(self.cpu.fp_adder)):
                if not self.cpu.fp_adder[i].is_occupied():
                    self.cpu.fp_adder[i].set_occupied(True)
                    break
        elif aa == constants.DIVD_INSTR:
            for i in range(len(self.cpu.fp_divider)):
                if not self.cpu.fp_divider[i].is_occupied():
                    self.cpu.fp_divider[i].set_occupied(True)
                    break
        elif aa == constants.AND_INSTR or aa == constants.ANDI_INSTR or aa == constants.DADD_INSTR or aa == constants.DADDI_INSTR or aa == constants.DSUB_INSTR or aa == constants.DSUBI_INSTR or aa == constants.OR_INSTR or aa == constants.ORI_INSTR or aa == constants.LUI_INSTR or aa == constants.LI_INSTR:
            self.cpu.int_alu[0].set_occupied(True)
        elif instr.is_load_store_instr():
            self.cpu.fu_load = True
        elif instr.is_branch_instr() or instr.inst_str == constants.HLT_INSTR:
            self.cpu.fu_branch = True

    def set_fp_free(self, instr):
        aa = instr.inst_str
        if aa == constants.MULD_INSTR:
            for i in range(len(self.cpu.fp_mul)):
                if self.cpu.fp_mul[i].is_occupied():
                    self.cpu.fp_mul[i].set_occupied(False)
                    break
        elif aa == constants.ADDD_INSTR or aa == constants.SUBD_INSTR:
            for i in range(len(self.cpu.fp_adder)):
                if self.cpu.fp_adder[i].is_occupied():
                    self.cpu.fp_adder[i].set_occupied(False)
                    break
        elif aa == constants.DIVD_INSTR:
            for i in range(len(self.cpu.fp_divider)):
                if self.cpu.fp_divider[i].is_occupied():
                    self.cpu.fp_divider[i].set_occupied(False)
                    break
        elif aa == constants.AND_INSTR or aa == constants.ANDI_INSTR or aa == constants.DADD_INSTR or aa == constants.DADDI_INSTR or aa == constants.DSUB_INSTR or aa == constants.DSUBI_INSTR or aa == constants.OR_INSTR or aa == constants.ORI_INSTR or aa == constants.LUI_INSTR or aa == constants.LI_INSTR:
            self.cpu.int_alu[0].set_occupied(False)
        elif instr.is_load_store_instr():
            self.cpu.fu_load = False
        elif instr.is_branch_instr():
            self.cpu.fu_branch = False

    def check_and_load_from_cache(self, offset):
        if self.instr.is_load_store_instr():
            r2_open_ind, _ = self.instr.dest_op.index(
                "("), self.instr.dest_op.index(")")

            reg2 = self.instr.get_r2()
            reg1 = self.instr.get_r1()
            addr = self.cpu.gpr[reg2][0] + \
                int(self.instr.dest_op[:r2_open_ind])
            data_block = self.dcache.fetch_data(addr + offset)
            self.exe_cycles += data_block.clock_cycles
            if self.instr.inst_str == constants.LW_INSTR or self.instr.inst_str == constants.SW_INSTR:
                self.exe_cycles -= 1
            if self.instr.inst_str == constants.SW_INSTR:
                self.dcache.update_val(addr + offset, self.cpu.gpr[reg1][0])
            self.is_d_cache_hit = True
            print("############## loaded from clock: {} cache: updated clock to: {} {}- {}".format(
                self.clock, self.instr, self.exe_cycles, data_block.clock_cycles))
            return data_block.data
        return 0

    def update_reg_flags(self, instr):
        if instr.dest_op:
            is_gpr = 'R' in instr.dest_op
            is_fpr = 'F' in instr.dest_op
            reg2 = instr.get_r2()
            if is_gpr and reg2 > 0:
                self.cpu.gpr[reg2][2] = 0
            if is_fpr and reg2 > 0:
                self.cpu.fpr[reg2][2] = 0
        if instr.third_op:
            is_gpr = 'R' in instr.third_op
            is_fpr = 'F' in instr.third_op
            reg3 = instr.get_r3()
            if is_gpr and reg3 > 0:
                self.cpu.gpr[reg3][2] = 0
            if is_fpr and reg2 > 0:
                self.cpu.fpr[reg3][2] = 0

    def update_reg_write_flags(self, instr):
        if instr.src_op:
            is_gpr = 'R' in instr.src_op
            is_fpr = 'F' in instr.src_op
            reg1 = instr.get_r1()
            if is_gpr and reg1 > 0:
                self.cpu.gpr[reg1][1] = 0
            if is_fpr and reg1 > 0:
                self.cpu.fpr[reg1][1] = 0

    def is_waw_hazard(self, instr):

        if instr.src_op and instr.dest_op:
            is_gpr = 'R' in instr.src_op
            is_fpr = 'F' in instr.src_op
            r1 = instr.get_r1()
            if is_gpr:
                if self.cpu.gpr[r1][1] > 0:
                    return True
            if is_fpr:
                if self.cpu.fpr[r1][1] > 0:
                    return True
        else:
            return False

    def is_war_hazard(self, instr, pc):
        if instr.is_load_store_instr():
            if instr.src_op:
                is_gpr = 'R' in instr.src_op
                is_fpr = 'F' in instr.src_op
                r1 = instr.get_r1()
                if is_gpr and r1 > 0:
                    print("&&&& laod and store checking in gpr: ",
                          self.cpu.gpr, " r1: ", r1, " pc: ", pc)
                    if self.cpu.gpr[r1][1] > 0 and self.cpu.gpr[r1][1] < pc:
                        return True
                if is_fpr and r1 > 0:
                    if self.cpu.fpr[r1][1] > 0 and self.cpu.fpr[r1][1] < pc:
                        return True
                else:
                    return False

        if instr.dest_op:
            is_gpr = 'R' in instr.dest_op
            is_fpr = 'F' in instr.dest_op
            r2 = instr.get_r2()
            if is_gpr and r2 > 0:
                print("&&&& checking in gpr: ",
                      self.cpu.gpr, " r2: ", r2, " pc: ", pc)
                if self.cpu.gpr[r2][1] > 0 and self.cpu.gpr[r2][1] < pc and self.instr.src_op != self.instr.dest_op:
                    return True
            if is_fpr and r2 > 0:
                if self.cpu.fpr[r2][1] > 0 and self.cpu.fpr[r2][1] < pc and self.instr.src_op != self.instr.dest_op:
                    return True
        else:
            return False

        if instr.third_op:
            if instr.is_branch_instr():
                print("reg: {}", self.cpu.gpr, " fpr: ", self.cpu.fpr)
            is_gpr = 'R' in instr.third_op
            is_fpr = 'F' in instr.third_op
            r3 = instr.get_r3()
            if is_gpr and r3 > 0:
                if self.cpu.gpr[r3][1] > 0 and self.cpu.gpr[r3][1] < pc and self.instr.src_op != self.instr.third_op:
                    return True
            elif is_fpr and r3 > 0:
                if self.cpu.fpr[r3][1] > 0 and self.cpu.fpr[r3][1] < pc and self.instr.src_op != self.instr.third_op:
                    return True
        return False

    def is_raw_hazard(self, instr):
        if instr.src_op and instr.dest_op:
            is_gpr = 'R' in instr.src_op
            is_fpr = 'F' in instr.src_op
            r1 = instr.get_r1()
            if is_gpr and r1 > 0:
                if self.cpu.gpr[r1][2] == 1:
                    return True
            if is_fpr and r1 > 0:
                if self.cpu.fpr[r1][2] == 1:
                    return True
        else:
            return False

    def branch(self, branch_type, pc, curr_pc):

        res = pc
        r2 = 0
        r1 = 0
        self.cpu.is_branch = False
        flag = False
        print("BBBBBBBBBBBBBBBB branch instr: ", self.instr,
              " gpr: ", self.cpu.gpr, " fpr: ", self.cpu.fpr)
        if branch_type == constants.BNE_INSTR:
            r2 = self.instr.get_r2()
            r1 = self.instr.get_r1()

            if self.cpu.gpr[r1][0] != self.cpu.gpr[r2][0]:
                for i in range(len(self.instrs)-1):
                    if self.instrs[i].have_label and self.instrs[i].have_label in self.instr.third_op:
                        if curr_pc != i:
                            res = i
                            flag = True
        elif branch_type == constants.BEQ_INSTR:
            r2 = self.instr.get_r2()
            r1 = self.instr.get_r1()

            if self.cpu.gpr[r1][0] == self.cpu.gpr[r2][0]:
                for i in range(len(self.instrs)):
                    if self.instrs[i].have_label and self.instrs[i].have_label in self.instr.third_op:
                        if curr_pc != i:
                            res = i
                            flag = True

        elif branch_type == constants.J_INSTR:
            for i in range(len(self.instrs)):
                if self.instrs[i].have_label and self.instrs[i].have_label in self.instr.src_op:
                    if curr_pc != i:
                        res = i
                        flag = True

        print("&&&&&&&&&&&&&& called branch: ",
              branch_type, "pc: ", pc, " new_pc: ", res)
        if not flag:
            self.cpu.is_branch = True
        return res

    def set_reg_write(self, reg, pc, is_gpr=True):
        print("************* Reg ", reg, " pc", pc, " is_gpr: ", is_gpr)
        if reg > 0:
            if is_gpr:
                self.cpu.gpr[reg][1] = pc
            else:
                self.cpu.fpr[reg][1] = pc

    def set_reg_read(self, reg, is_gpr=True):

        if reg > 0:
            if is_gpr:
                self.cpu.gpr[reg][2] = 1
            else:
                self.cpu.fpr[reg][2] = 1

    def update(self, clk_cnt, pc_cnt, war_pc, flag):

        # print()
        if self.finish:
            self.is_et_push(self.curr_stage)

        if self.should_push:
            self.curr_stage = self.next_stage
            self.next_stage += 1

        self.finish = False
        self.is_next_free = False
        self.is_fetch_free = False
        self.should_push = False

        if self.curr_stage == 0:
            print("*********  fetch : {}- {}".format(self.instr, clk_cnt))
            if flag:
                self.branch_taken = True
            self.fetch_cycle -= 1

            if not self.cpu.issue and self.fetch_cycle <= 0 and self.instr.inst_str == constants.HLT_INSTR:
                print("fetched hlt : ", self.instr)
                self.finish = True
                self.is_fetch_free = True
                self.fetch = clk_cnt
                self.is_next_free = True
                return pc_cnt
            elif not self.cpu.issue and self.fetch_cycle <= 0:
                print("fetched: ", self.instr)
                self.finish = True
                self.is_fetch_free = True
                self.fetch = clk_cnt
                self.is_next_free = True

        elif self.curr_stage == 1:
            print("curr stage is issue: {}- {}".format(type(self.instr), clk_cnt))
            self.cpu.issue = True
            self.waw_hazard = self.is_waw_hazard(self.instr)
            has_res = self.is_fp_free(self.instr)

            if self.instr.is_branch_instr():
                self.finish = True
                self.cpu.issue = False
                self.issue = clk_cnt
                self.is_next_free = True
                self.waw_hazard = False
                self.struct_hazard = False
                pc_cnt = self.branch(self.instr.inst_str, pc_cnt, war_pc)
                return pc_cnt
            if self.instr.inst_str == constants.SD_INSTR or self.instr.inst_str == constants.SW_INSTR:
                self.waw_hazard = False
            if not has_res:
                self.sh = 'Y'
            if self.instr.inst_str == constants.HLT_INSTR:
                self.sh = 'N'
            if self.waw_hazard:
                self.h_waw = 'Y'
            if has_res and not self.waw_hazard and not self.cpu.is_branch:
                self.set_fp_busy(self.instr)
                self.finish = True
                self.cpu.issue = False
                if not (self.instr.inst_str == constants.SD_INSTR or self.instr.inst_str == constants.SW_INSTR):
                    print("^^^^^^^^^^^ setting regwrite for instruction: ",
                          self.instr, "gpr : ", self.cpu.gpr)
                    is_gpr = self.instr.src_op and "R" in self.instr.src_op
                    self.set_reg_write(self.instr.get_r1(),
                                       war_pc, is_gpr)
                    print("^^^^^^^^^^^ after regwrite for instruction: ",
                          self.instr, "gpr : ", self.cpu.gpr)
                self.issue = clk_cnt
                self.is_next_free = True
        elif self.curr_stage == 2:
            print("curr stage is read: {}- {}".format(self.instr, clk_cnt))
            if self.instr.inst_str == constants.HLT_INSTR or self.branch_taken:
                self.finish = True
                self.cpu.issue = False
                self.update_reg_write_flags(self.instr)
                self.set_fp_free(self.instr)
                self.is_next_free = True
                self.curr_stage = 4
                self.next_stage = 5
                print("changing hlt instruction stages")
                return pc_cnt

            if self.instr.is_branch_instr():
                self.set_fp_busy(self.instr)
            self.war_hazard = self.is_war_hazard(
                self.instr, war_pc)
            if self.war_hazard:
                self.h_war = 'Y'
            if not self.war_hazard:
                self.finish = True
                self.cpu.fu_branch = False
                self.read = clk_cnt
                r2_is_gpr = True if self.instr.dest_op and "R" in self.instr.dest_op else False
                r3_is_gpr = True if self.instr.third_op and "R" in self.instr.third_op else False
                self.set_reg_read(self.instr.get_r2(), r2_is_gpr)
                print("!!!!!!!!!!!! instr  ", self.instr)
                self.set_reg_read(self.instr.get_r3(), r3_is_gpr)
                self.is_next_free = True
                if not self.is_d_cache_hit:
                    data = self.check_and_load_from_cache(0)
                    print("before executing !!!!!!!!!!!!!!!!!")
                    self.instr.execute_instr(self.cpu, data, self.dcache)
                    self.is_d_cache_hit = True
                    if self.instr.inst_str == constants.LD_INSTR or self.instr.inst_str == constants.SD_INSTR:
                        self.is_d_cache_hit = False
        elif self.curr_stage == 3:
            print("curr stage is exec: {}- {} {}".format(self.instr,
                                                         clk_cnt, self.exe_cycles))
            if self.instr.is_branch_instr():
                print("*********************** this should run:0 ")
                self.cpu.is_branch = False
            if not self.is_d_cache_hit:
                print("*********************** this should run:2 ")
                self.check_and_load_from_cache(4)
                self.is_d_cache_hit = True
                self.exe_cycles -= 1
            if self.exe_cycles == 1:
                print("*********************** this should run3: ")
                self.update_reg_flags(self.instr)
                self.finish = True
                self.execute = clk_cnt
                self.is_next_free = True
                return pc_cnt
            self.exe_cycles -= 1

        elif self.curr_stage == 4:
            print("curr stage is wb: {}- {}".format(self.instr, clk_cnt))
            if self.raw_hazard:
                self.h_raw = 'Y'
            else:
                self.finish = True
                self.write = clk_cnt
                self.is_next_free = True
        elif self.curr_stage == 5:
            self.update_reg_write_flags(self.instr)
            self.set_fp_free(self.instr)
            self.finish = True
            self.is_next_free = True
            if self.instr.is_branch_instr():
                self.write = 0
                self.execute = 0
        return pc_cnt
