

'''

    This is the base class for cache
    defines get and put methods
'''
class Cache:
    def __init__(self, name):
        self.name = name

    def get_from_cache(self, address):
        raise NotImplementedError()

    def put_into_cache(self, address, data):
        raise NotImplementedError()