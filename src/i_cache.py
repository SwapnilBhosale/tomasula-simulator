from cache import Cache

class ICache(Cache):

    def __init__(self, num_of_blocks, block_size, clock_mgr, memory_bus):
        self.num_of_blocks = num_of_blocks
        self.block_size = block_size
        self.clock_mgr = clock_mgr
        self.memory_bus = memory_bus

        self.cache = {}
        self.hits = 0
        self.requests = 0
        self.block_offset_mask = 0
        self.offset_cnt = 0
        self.__set_offset_mask()

    def __set_offset_mask(self):
        temp = self.block_size
        while temp:
            temp = temp // 2
            self.block_offset_mask = self.block_offset_mask << 1
            self.block_offset_mask = self.block_offset_mask | 1
            self.offset_cnt += 1
        self.block_offset_mask = self.block_offset_mask >> 1
        self.offset_cnt = self.offset_cnt - 1

    def get_stats_total_requests(self):
        return self.requests

    def get_stats_total_hits(self):
        return self.hits

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
        block_num = (addr >> self.offset_cnt) % self.num_of_blocks
        tag = addr >> self.offset_cnt
        self.requests += 1
        print("**** tag: {}, block_nul: {}, cache: {} ".format(tag,
                                                               block_num, self.cache))
        if block_num in self.cache:
            if self.cache[block_num] == tag:
                self.hits += 1
                return 1
            else:
                self.cache[block_num] = tag
                return self.num_cycle_needed(self.block_size * 3) + 1
        else:
            self.cache[block_num] = tag
            return self.num_cycle_needed(self.block_size * 3) + 1
