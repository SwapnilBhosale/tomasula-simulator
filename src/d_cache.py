
import constants
from cache import Cache



'''

    This class repesents the Data Cache
    Data cache is a 2 way Set Associative with 2 sets and 4 blocks
    Implements the LRU replacement stratergy in case of cache miss
'''
class DCache(Cache):

    def __init__(self, clock_mgr, memory_bus, memory):
        super().__init__("Dcache")
        self.clock_mgr = clock_mgr
        self.memory_bus = memory_bus
        self.memory = memory
        self.cache_size = constants.D_CACHE_SIZE
        self.block_size = constants.WORD_SIZE_IN_BYTES
        self.no_of_sets = constants.NO_OF_SETS_D_CACHE
        self.cache = [[0 for i in range(self.block_size)]
                      for j in range(self.cache_size)]
        self.valid = [False] * self.cache_size
        self.lru_cnt = [False] * self.cache_size
        self.dirty = [False] * self.cache_size
        self.tag = [0] * self.cache_size

        self.requests = 0
        self.hits = 0

    '''
        Returns the total number of request received to the DCache so fat
    '''
    def get_stats_total_requests(self):
        return self.requests


    '''
        Returns the total number of cache HITS
    '''
    def get_stats_total_hits(self):
        return self.hits

    '''
        Returns the Cycles needed
    '''
    def num_cycle_needed(self, clock_cycle):
        if not self.memory_bus.is_busy(self.clock_mgr.get_clock()):
            self.memory_bus.set_busy_until(
                self.clock_mgr.get_clock() + clock_cycle)
            return clock_cycle
        else:
            busy_cnt = self.memory_bus.get_busy_until(
            ) - self.clock_mgr.get_clock() + clock_cycle
            self.memory_bus.set_busy_until(
                self.memory_bus.get_busy_until() + clock_cycle)
            return busy_cnt

    
    def get_from_cache(self, addr):
        print("addr: ", addr)
        temp = addr
        addr = addr >> 2
        # extract last 2 bits
        offset_mask = 3

        block_offset = addr & offset_mask
        address = addr >> 2
        set_no = address % 2

        idx = set_no * self.no_of_sets

        print("idx: {} , set: {} , block_offset: {}".format(
            idx, set_no, block_offset))
        temp_lru_cnt = [False] * 4
        temp_lru_cnt[idx] = self.lru_cnt[idx]
        temp_lru_cnt[idx+1] = self.lru_cnt[idx+1]
        self.lru_cnt[idx] = False
        self.lru_cnt[idx+1] = False
        self.requests += 1
        if self.valid[idx] and self.tag[idx] == address:
            self.lru_cnt[idx] = True
            self.hits += 1
            return DCacheInfo(self.cache[idx][block_offset], 1)
        if self.valid[idx+1] and self.tag[idx+1] == address:
            self.lru_cnt[idx+1] = True
            self.hits += 1
            return DCacheInfo(self.cache[idx+1][block_offset], 1)

        data = self.memory.get_data(temp)
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
                self.memory.update_memory_data(temp, self.cache[idx])
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
                self.memory.update_memory_data(temp, self.cache[idx])
            self.dirty[idx+1] = False
            self.tag[idx+1] = address
            for i in range(len(data)):
                self.cache[idx+1][i] = data[i]
            return DCacheInfo(self.cache[idx+1][block_offset], self.num_cycle_needed(12+extra_cycle)+1)
        return None

    def put_into_cache(self, addr, data):
        temp = addr
        addr = addr >> 2
        # extract last 2 bits
        offset_mask = 3

        block_offset = addr & offset_mask
        temp1 = addr >> 2
        set_no = temp1 % 2

        idx = set_no * self.no_of_sets
        temp_lru_cnt = [False] * 4
        self.memory.update_store_instruction_data(temp, data)

        temp_lru_cnt[idx] = self.lru_cnt[idx]
        temp_lru_cnt[idx+1] = self.lru_cnt[idx+1]
        self.lru_cnt[idx] = False
        self.lru_cnt[idx+1] = False
        if self.valid[idx] and self.tag[idx] == addr:
            self.lru_cnt[idx] = True
            self.dirty[idx] = True
            self.cache[idx][block_offset] = data
            return 1
        if self.valid[idx+1] and self.tag[idx+1] == addr:
            self.lru_cnt[idx+1] = True
            self.dirty[idx+1] = True
            self.cache[idx+1][block_offset] = data
            return 1

        data = self.memory.update_and_get_data(temp, block_offset, data)

        if not self.valid[idx]:
            self.valid[idx] = True
            self.lru_cnt[idx] = True
            self.dirty[idx] = False
            self.tag[idx] = addr
            for i in range(len(data)):
                self.cache[idx][i] = data[i]
            return self.num_cycle_needed(12)+1

        if not self.valid[idx+1]:
            self.valid[idx+1] = True
            self.lru_cnt[idx+1] = True
            self.dirty[idx+1] = False
            self.tag[idx+1] = addr
            for i in range(len(data)):
                self.cache[idx+1][i] = data[i]
            return self.num_cycle_needed(12)+1
        if not temp_lru_cnt[idx]:
            self.valid[idx] = True
            self.lru_cnt[idx] = True
            extra_cycle = 0
            if self.dirty[idx]:
                extra_cycle = 12
                self.memory.update_memory_data(temp, self.cache[idx])
            self.dirty[idx] = False
            self.tag[idx] = addr
            for i in range(len(data)):
                self.cache[idx][i] = data[i]
            return self.num_cycle_needed(12+extra_cycle)+1
        if not temp_lru_cnt[idx+1]:
            self.valid[idx+1] = True
            self.lru_cnt[idx+1] = True
            extra_cycle = 0
            if self.dirty[idx+1]:
                extra_cycle = 12
                self.memory.update_memory_data(temp, self.cache[idx])
            self.dirty[idx+1] = False
            self.tag[idx] = addr
            for i in range(len(data)):
                self.cache[idx][i] = data[i]
            return self.num_cycle_needed(12+extra_cycle)+1
        return -1


class DCacheInfo:

    def __init__(self, data, clock_cycles):
        self.data = data
        self.clock_cycles = clock_cycles
