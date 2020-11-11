

class FUnit:

    def __init__(self, name, exec_time):
        self.name = name
        self.exec_time = exec_time

    
    def execute(self):
        raise NotImplementedError

    
