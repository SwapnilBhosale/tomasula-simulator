import constants
import math


class Cache():
    def put_in_cache(self, addr, data):
        raise NotImplementedError()

    def get_from_cache(self, addr):
        raise NotImplementedError()


class SetAssociateCache(Cache):

    def __init__(self, no_of_sets, block_size_words):
        self.no_of_sets = no_of_sets
        self.block_size_words = block_size_words


class DirectCache(Cache):
    def __init__(self, num_of_blocks, block_size_words):
        self.num_of_blocks = num_of_blocks
        self.block_size_words = block_size_words
        self.cache = [] * num_of_blocks
        self.byte_offset = None
        self.no_index_bits = None

    def get_byte_offset(self):
        res = None
        if self.byte_offset is None:
            no_of_bytes = self.block_size_words * constants.WORD_SIZE_IN_BYTES
            res = int(math.log2(no_of_bytes))
            self.byte_offset = res
        else:
            res = self.byte_offset
        return res

    def get_index_bits(self):
        res = None
        if self.no_index_bits is None:
            res = int(math.log2(self.num_of_blocks))
            self.no_index_bits = res
        else:
            res = self.no_index_bits
        return res


class ICache(DirectCache):

    def __init__(self, num_of_blocks, block_size_words):
        super().__init__(num_of_blocks, block_size_words)


class DCache(SetAssociateCache):

    def __init__(self, num_of_sets, block_size_words):
        super().__init__(num_of_sets, block_size_words)


#c = ICache(4, 4)
# print(c.get_index_bits())
# print(c.get_byte_offset())
