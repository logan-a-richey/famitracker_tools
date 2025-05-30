# macro.py

from typing import List

class Macro:
    @staticmethod
    def generate_macro_label(chip: str, macro_type: int, macro_index: int) -> str:
        ''' chip is either MACRO, MACROVRC6, MACRON163, MACROSB5 '''
        return "{}.{}.{}".format(chip, macro_type, macro_index)

    def __init__(self, _label: str, _type: int, _index: int, _loop: int, _release: int, _setting: int, _sequence: List[int]):
        self.label = _label
        self.type = _type
        self.index = _index
        self.loop = _loop
        self.release = _release
        self.setting = _setting
        self.sequence =  _sequence

    def __str__(self):
        return "{}".format(self.__dict__)
    
    def __repr__(self):
        return self.__str__()
