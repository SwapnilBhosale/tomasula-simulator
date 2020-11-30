from fp_type import FPType
from cpu import CPU
from instruction import Instruction


class ScoreBoard:

    def __init__(self, cpu):
        self.fetch = []
        self.issue = []
        self.read = []
        self.exec = []
        self.write = []
        self.cpu = cpu

    def fetch_stage(self, instr):
        # if we can not issue next nstruction,
        # we should not fetch next instruction
        if len(self.fetch) == 0:
            print("Fetched instrt : {}".format(
                instr.print_instr(is_print=False)))
            self.fetch.append(instr)
        else:
            print("WARN: Can not fetch, fetch buffer is busy")

    def __assign_processing_unit(self, next_instr):

        #print("***** Assigning unit for inst: {}".format(next_instr.print_instr(is_print=False)))
        pu_type = next_instr.processing_unit
        print("processing unit: ", pu_type.name)
        res = False
        # if next instr RUNs in IntALU then no Hazards given in problem statement
        if pu_type == FPType.IntALU:
            # print(self.cpu.__dict__)
            self.cpu.int_alu[0][0].set_instruction(next_instr)
            res = True
        elif pu_type == FPType.FPAdder:
            free_adders = [i for i, adder in enumerate(
                self.cpu.fp_adder) if not adder[1]]
            if len(free_adders) == 0:
                next_instr.struct_hazard.append(self.cpu.curr_clock)
                print("WARN: Structural HAZARD: NO FP adder available: {}".format(
                    next_instr.print_instr(is_print=False)))
            else:
                selected_adder, taken = self.cpu.fp_adder[free_adders[0]]
                selected_adder.set_instruction(next_instr)
                self.cpu.fp_adder[free_adders[0]] = (selected_adder, not taken)
                print("Added adder: ", self.cpu.fp_adder)
                res = True
        elif pu_type == FPType.FPDiv:
            free_dividers = [i for i, divider in enumerate(
                self.cpu.fp_divider) if not divider[1]]
            if len(free_dividers) == 0:
                print("WARN: Structural HAZARD: NO FP dividers available: {}".format(
                    next_instr.print_instr(is_print=False)))
            else:
                next_instr.struct_hazard.append(self.cpu.curr_clock)
                selected_divider, taken = self.cpu.fp_divider[free_dividers[0]]
                selected_divider.set_instruction(next_instr)
                self.cpu.fp_divider[free_dividers[0]] = (
                    selected_divider, not taken)
                res = True
        elif pu_type == FPType.FPMul:
            free_multipliers = [i for i, multiplier in enumerate(
                self.cpu.fp_mul) if not multiplier[1]]
            if len(free_multipliers) == 0:
                print("WARN: Structural HAZARD: NO FP free_multipliers available: {}".format(
                    next_instr.print_instr(is_print=False)))
            else:
                next_instr.struct_hazard.append(self.cpu.curr_clock)
                selected_multiplier, taken = self.cpu.fp_mul[free_multipliers[0]]
                selected_multiplier.set_instruction(next_instr)
                self.cpu.fp_mul[free_multipliers[0]] = (
                    selected_multiplier, not taken)
                res = True
        if res:
            self.fetch.pop()
            self.cpu.reg_pc += 1

    def issue_stage(self):

        if len(self.fetch) == 0:
            print("No instruction to fetch")
            return
        else:
            next_instr = self.fetch[0]
            self.__assign_processing_unit(next_instr)
            # add fetch complete cycle number
            next_instr.res.append(self.cpu.curr_clock)
            print("Issued instructionm: {}".format(
                next_instr.print_instr(is_print=False)))
            # next_instr.execute_instr(self.cpu)

        '''
        for instr in self.issue:
            ex_unit = instr.processing_unit
            if ex_unit == FPType.IntALU()
            if ex_unit == FPType.FPAdder:
                free_adders = [adder for adder in selc.cpu.fp_adder if not adder[1]]
                free_adders.set_instruction(instr)'''
