# macro.py

from typing import List

class Macro:

    def __init__(self, _label: str, _type: int, _index: int, _loop: int, _release: int, _setting: int, _sequence: List[int]):
        self.label = _label
        self.type = _type
        self.index = _index
        self.loop = _loop
        self.release = _release
        self.setting = _setting
        self.sequence =  _sequence
    
    def __str__(self):
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([str(field) for field in [self.label, self.type, self.index, self.loop, self.release, self.setting, self.sequence]]))

    def __repr__(self):
        return self.__str__()
