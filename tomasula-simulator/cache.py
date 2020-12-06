import constants
import math


class Cache():
    def __init__(self):
        self.hit_time = 1
        self.hits = 0
        self.requests = 0
        self.memory_bus = None

    def put_in_cache(self, addr, data):
        raise NotImplementedError()

    def get_from_cache(self, addr):
        raise NotImplementedError()

    def get_stats_requests(self):
        return self.requests
    
    def get_stats_hits(self):
        return self.hits

class SetAssociateCache(Cache):

    def __init__(self, num_of_sets, number_of_blocks, chip, memory_bus, clk_mgr):
        super().__init__()
        self.no_of_sets = num_of_sets
        self.block_size_words = 4
        self.cache_size = 4
        self.valid = [False] * self.cache_size
        self.lru_cnt = [False] * self.cache_size
        self.dirty = [False] * self.cache_size
        self.tag = [0] * self.cache_size
        self.clk_mgr = clk_mgr
        #self.memory = memory
        self.memory_bus = memory_bus
        self.chip = chip

        self.cache = [[0 for i in range(self.block_size_words)] for j in range(self.cache_size)]

    def num_cycle_needed(self, clock_cycle):
        if not self.memory_bus.is_busy(self.clk_mgr.get_clock()):
            self.memory_bus.set_busy_until(
                self.clk_mgr.get_clock() + clock_cycle)
            return clock_cycle
        else:
            busy_cnt = self.memory_bus.get_busy_until(
            ) - self.clk_mgr.get_clock() + clock_cycle
            self.memory_bus.set_busy_until(
                self.memory_bus.get_busy_until() + clock_cycle)
            return busy_cnt

class DirectCache(Cache):
    def __init__(self, num_of_blocks, block_size_words, memory_bus, clk_mgr):
        super().__init__()
        self.num_of_blocks = num_of_blocks
        self.block_size_words = block_size_words
        self.cache = {}
        self.memory_bus = memory_bus
        self.block_offset_mask = 0
        self.offset_cnt = 0
        self.clk_mgr = clk_mgr
        self.__set_offset_mask()
    
    def __set_offset_mask(self):
        temp = self.block_size_words
        while temp:
            temp = temp // 2
            self.block_offset_mask = self.block_offset_mask << 1
            self.block_offset_mask = self.block_offset_mask | 1
            self.offset_cnt += 1
        self.block_offset_mask = self.block_offset_mask >> 1
        self.offset_cnt = self.offset_cnt - 1

        print("Block_offset_mask: ",self.block_offset_mask, " offset_cnt: ", self.offset_cnt)

    def num_cycle_needed(self, clock_cycle):
        if not self.memory_bus.is_busy(self.clk_mgr.get_clock()):
            self.memory_bus.set_busy_until(
                self.clk_mgr.get_clock() + clock_cycle)
            return clock_cycle
        else:
            busy_cnt = self.memory_bus.get_busy_until(
            ) - self.clk_mgr.get_clock() + clock_cycle
            self.memory_bus.set_busy_until(
                self.memory_bus.get_busy_until() + clock_cycle)
            return busy_cnt

    
class ICache(DirectCache):

    def __init__(self, num_of_blocks, block_size_words, memory_bus, clk_mgr):
        super().__init__(num_of_blocks, block_size_words, memory_bus, clk_mgr)

    
    def fetch_instruction(self, address):
        block_num = (address >> self.offset_cnt) % self.num_of_blocks
        tag = address >> self.offset_cnt
        self.requests += 1
        print("**** tag: {}, block_nul: {}, cache: {} ".format(tag,block_num, self.cache))
        cycles_required = 0                                                       
        if block_num in self.cache:
            if self.cache[block_num] == tag:
                self.hits += 1
                cycles_required =  self.hit_time
            else:
                self.cache[block_num] = tag
                cycles_required =  self.num_cycle_needed(self.block_size_words * 3)
        else:
            self.cache[block_num] = tag
            cycles_required =  self.num_cycle_needed(self.block_size_words * 3)
        return cycles_required



class DCache(SetAssociateCache):

    def __init__(self, num_of_sets, number_of_blocks,  chip, memory_bus,  clk_mgr):
        super().__init__(num_of_sets, number_of_blocks,  chip, memory_bus, clk_mgr)

    def num_cycle_needed(self, clock_cycle):
        res = clock_cycle
        if not self.memory_bus.is_busy(self.clk_mgr.get_clock()):
            self.memory_bus.set_busy_until(
                self.clk_mgr.get_clock() + clock_cycle)
        else:
            res  = self.memory_bus.get_busy_until(
            ) - self.clk_mgr.get_clock() + clock_cycle
            self.memory_bus.set_busy_until(
                self.memory_bus.get_busy_until() + clock_cycle)
        return res

    def fetch_data(self, address):

        self.requests += 1

        old_address = address
        address = address >> 2
        # extract last 2 bits
        offset_mask = 3

        block_offset = address & offset_mask
        # extract last 2 bits again for set number
        address = address >> 2
        set_no = address % 2

        idx = set_no * self.no_of_sets

        print("idx: {} , set: {} , block_offset: {}".format(
            idx, set_no, block_offset))
        temp_lru_cnt = [False] * 4
        temp_lru_cnt[idx] = self.lru_cnt[idx]
        temp_lru_cnt[idx+1] = self.lru_cnt[idx+1]
        self.lru_cnt[idx] = False
        self.lru_cnt[idx+1] = False

        if self.valid[idx] and self.tag[idx] == address:
            self.lru_cnt[idx] = True
            self.hits += 1
            return DCacheInfo(self.cache[idx][block_offset], 1)

        if self.valid[idx+1] and self.tag[idx+1] == address:
            self.lru_cnt[idx+1] = True
            self.hits += 1
            return DCacheInfo(self.cache[idx+1][block_offset], 1)

        #data not found in cache so load from memory
        data = self.chip.fetch_data_for_d_cache(old_address)
        print("########################### $$$$$$$$$$$$$$$$$$$$$$ data fetched: ", data)
        if not self.valid[idx]:
            self.valid[idx] = True
            self.lru_cnt[idx] = True
            self.dirty[idx] = False
            self.tag[idx] = address
            for i in range(len(data)):
                self.cache[idx][i] = data[i]
            return DCacheInfo(self.cache[idx][block_offset], self.num_cycle_needed(12)+1)
        if not self.valid[idx+1]:
            self.valid[idx+1] = True
            self.lru_cnt[idx+1] = True
            self.dirty[idx+1] = False
            self.tag[idx+1] = address
            for i in range(len(data)):
                self.cache[idx+1][i] = data[i]
            return DCacheInfo(self.cache[idx+1][block_offset], self.num_cycle_needed(12)+1)
        if not temp_lru_cnt[idx]:
            self.valid[idx] = True
            self.lru_cnt[idx] = True
            extra_cycle = 0
            if self.dirty[idx]:
                extra_cycle = 12
                self.chip.update_data_for_d_cache(old_address, self.cache[idx])
            self.dirty[idx] = False
            self.tag[idx] = address
            for i in range(len(data)):
                self.cache[idx][i] = data[i]
            return DCacheInfo(self.cache[idx][block_offset], self.num_cycle_needed(12+extra_cycle)+1)
        if not temp_lru_cnt[idx+1]:
            self.valid[idx+1] = True
            self.lru_cnt[idx+1] = True
            extra_cycle = 0
            if self.dirty[idx+1]:
                extra_cycle = 12
                self.chip.update_data_for_d_cache(old_address, self.cache[idx])
            self.dirty[idx+1] = False
            self.tag[idx+1] = address
            for i in range(len(data)):
                self.cache[idx+1][i] = data[i]
            return DCacheInfo(self.cache[idx+1][block_offset], self.num_cycle_needed(12+extra_cycle)+1)
        return None

    def update_val(self, address, data):
        old_address = address
        address = address >> 2
        # extract last 2 bits
        offset_mask = 3

        block_offset = address & offset_mask
        address = address >> 2
        set_no = address % 2

        idx = set_no * self.no_of_sets
        temp_lru_cnt = [False] * 4
        self.chip.update_sw_data_for_d_cache(old_address, data)

        temp_lru_cnt[idx] = self.lru_cnt[idx]
        temp_lru_cnt[idx+1] = self.lru_cnt[idx+1]
        self.lru_cnt[idx] = False
        self.lru_cnt[idx+1] = False
        if self.valid[idx] and self.tag[idx] == address:
            self.lru_cnt[idx] = True
            self.dirty[idx] = True
            self.cache[idx][block_offset] = data
            return 1
        if self.valid[idx+1] and self.tag[idx+1] == address:
            self.lru_cnt[idx+1] = True
            self.dirty[idx+1] = True
            self.cache[idx+1][block_offset] = data
            return 1

        new_data = self.chip.update_get_data_for_d_cache(old_address, block_offset, data)

        if not self.valid[idx]:
            self.valid[idx] = True
            self.lru_cnt[idx] = True
            self.dirty[idx] = False
            self.tag[idx] = address
            for i in range(len(new_data)):
                self.cache[idx][i] = new_data[i]
            return self.num_cycle_needed(12)+1

        if not self.valid[idx+1]:
            self.valid[idx+1] = True
            self.lru_cnt[idx+1] = True
            self.dirty[idx+1] = False
            self.tag[idx+1] = address
            for i in range(len(new_data)):
                self.cache[idx+1][i] = new_data[i]
            return self.num_cycle_needed(12)+1
        if not temp_lru_cnt[idx]:
            self.valid[idx] = True
            self.lru_cnt[idx] = True
            extra_cycle = 0
            if self.dirty[idx]:
                extra_cycle = 12
                self.chip.update_data_for_d_cache(old_address, self.cache[idx])
            self.dirty[idx] = False
            self.tag[idx] = address
            for i in range(len(new_data)):
                self.cache[idx][i] = new_data[i]
            return self.num_cycle_needed(12+extra_cycle)+1
        if not temp_lru_cnt[idx+1]:
            self.valid[idx+1] = True
            self.lru_cnt[idx+1] = True
            extra_cycle = 0
            if self.dirty[idx+1]:
                extra_cycle = 12
                self.chip.update_data_for_d_cache(old_address, self.cache[idx])
            self.dirty[idx+1] = False
            self.tag[idx+1] = address
            for i in range(len(new_data)):
                self.cache[idx+1][i] = new_data[i]
            return self.num_cycle_needed(12+extra_cycle)+1
        return -1
#c = ICache(4, 4)
# print(c.get_index_bits())
# print(c.get_byte_offset())

class DCacheInfo:

    def __init__(self, data, clock_cycles):
        self.data = data
        self.clock_cycles = clock_cycles