import instruction as instr


def load_bin_file(path):
    with open(path) as f:
        return f.read()

def get_instruction(inst):
    res = None
    if " "in inst:
        i = inst.index(" ")
        temp = inst[:i].upper()
        args = inst[i+1:]
        if temp == "LI":
            res =  instr.LIInstr(args)
    else:
        res = instr.HLTInstr()
    return res
def get_reg_index_from_str(src_reg):
    return src_reg[1]