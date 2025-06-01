# dpcm.py

from typing import List

class Dpcm:
    def __init__(self, _index: int, _size: int, _name):
        self.index = _index
        self.size = _size
        self.name = _name
        self.data: List[int] = []
    
    def __str__(self):
        fields = [self.index, self.size, self.name, self.data]
        return "<{}> \'{}\': {}\n".format(self.__class__.__name__, self.name, self.data)
        
    def __repr__(self) -> str:
        return self.__str__()


