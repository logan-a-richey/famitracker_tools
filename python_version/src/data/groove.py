# groove.py

from typing import List

class Groove:
    def __init__(self, _index: int, _size: int, _sequence: List[int]):
        self.index = _index
        self.size = _size 
        self.sequence = _sequence
    
    def __str__(self):
        return "<{}> {} : {}".format(self.__class__.__name__, self.index, self.sequence)
        
    def __repr__(self) -> str:
        return self.__str__()
