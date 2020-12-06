import instruction as instr


def load_bin_file(path):
    try: 
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print("ERROR: File not found at location: ",path)
        import sys
        sys.exit(1)



def get_instruction(inst):
    #print("decoding instr: ", inst)
    res = None
    if inst:
        print("inst is: ", inst)
        if inst and not ("hlt" in inst or "HLT" in inst):
            label = None
            if ":" in inst:  # label
                i = inst.index(":")
                label = inst[:i].strip()
                inst = inst[i+2:]
            i = inst.index(" ")
            temp = inst[:i].upper()
            args = inst[i+1:]
            if "LI" in temp:
                res = instr.LIInstr(args, have_label=label)
            elif "LUI" in temp:
                res = instr.LUIInstr(args, have_label=label)
            elif "LW" in temp:
                res = instr.LWInstr(args, have_label=label)
            elif "SW" in temp:
                res = instr.SWInstr(args, have_label=label)
            elif "L.D" == temp:
                res = instr.LDInstr(args, have_label=label)
            elif "S.D" in temp:
                res = instr.SDInstr(args, have_label=label)
            elif "DADDI" in temp:
                res = instr.DADDIInstr(args, have_label=label)
            elif "DADD" == temp:
                res = instr.DADDInstr(args, have_label=label)
            elif "DSUBI" in temp:
                res = instr.DSUBIInstr(args, have_label=label)
            elif "DSUB" == temp:
                res = instr.DSUBInstr(args, have_label=label)
            elif "ANDI" in temp:
                res = instr.ANDIInstr(args, have_label=label)
            elif "AND" == temp:
                res = instr.ANDInstr(args, have_label=label)
            elif "ORI" in temp:
                res = instr.ORIInstr(args, have_label=label)
            elif "OR" == temp:
                res = instr.ORInstr(args, have_label=label)
            elif "ADD.D" in temp:
                res = instr.ADDDInstr(args, have_label=label)
            elif "SUB.D" == temp:
                res = instr.SUBDInstr(args, have_label=label)
            elif "MUL.D" in temp:
                res = instr.MULDInstr(args, have_label=label)
            elif "DIV.D" == temp:
                res = instr.DIVDInstr(args, have_label=label)
            elif "BNE" in temp:
                res = instr.BNEInstr(args, have_label=label)
            elif "BEQ" in temp:
                res = inst.BEQInstr(args, have_label=label)
            elif "J" in temp:
                res = inst.JInstr(args, have_label=label)
        else:
            res = instr.HLTInstr(None)
    return res


def get_reg_index_from_str(src_reg):
    return src_reg[1]


def parse_args(args):
    return list(map(lambda x: x.strip(), args.split(",")))
