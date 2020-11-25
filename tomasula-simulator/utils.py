import instruction as instr


def load_bin_file(path):
    with open(path) as f:
        return f.read()


def get_instruction(inst):
    #print("decoding instr: ", inst)
    res = None
    if inst:
        if " " in inst:
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
            elif "L.D" == temp:
                res = instr.LDInstr(args, have_label=label)
            elif "ADD.D" in temp:
                res = instr.ADDDInstr(args, have_label=label)
        else:
            res = instr.HLTInstr()
    return res


def get_reg_index_from_str(src_reg):
    return src_reg[1]


def parse_args(args):
    return list(map(lambda x: x.strip(), args.split(",")))
