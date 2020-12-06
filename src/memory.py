import utils
import constants

'''
    This class represents the Main Memory of the System
    This stores the data loaded for the data file in the argument
'''
class Memory:

    def __init__(self, data_file):

        self.data = []
        self.data_file = data_file
        self.start_addr = constants.DATA_START_ADDRESS
        self.__load_data()

    def __load_data(self):
        datas = utils.load_bin_file(self.data_file)
        data = datas.split("\n")
        curr_block = [0]*4
        #print("curr_blocm: ",curr_block)
        for i, val in enumerate(data):
            if val:
                #print("val: ",val)
                int_val = int(val, 2)
                if (i+1) % 4 == 0:
                    curr_block[i % 4] = int_val
                    self.data.append(curr_block)
                    curr_block = [0] * 4
                else:
                    curr_block[i % 4] = int_val
            #print("curr_blocm: ",curr_block)

    def get_data(self, addr):
        idx = (addr - self.start_addr) // 4
        idx = idx // 4
        return self.data[idx]

    def update_and_get_data(self, addr, offset, data):
        idx = (addr - self.start_addr) // 4
        idx = idx // 4
        temp = self.data[idx]
        temp[offset] = data
        return temp

    def update_memory_data(self, addr, data):
        idx = (addr - self.start_addr) // 4
        idx = idx // 4
        self.data[idx] = data

    def update_store_instruction_data(self, addr, data):
        idx = (addr - self.start_addr) // 4
        idx1 = idx // 4
        offset = idx % 4
        temp = self.data[idx1]
        temp[offset] = data
        self.data[idx1] = temp
