
'''

Clock manager holds the current clock value of the system
This class is shared among other system components for clock sharing.
'''
class ClockMgr:

    def __init__(self):
        self.clock = 1

    def get_clock(self):
        return self.clock

    def increament_clock(self):
        self.clock += 1
