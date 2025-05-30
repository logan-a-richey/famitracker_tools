# instruments.py

from typing import List, Dict

#*******************************************************************************
class BaseInst:
    def __init__(self, _index: int, _tag: str, _name: str):
        self.index = _index
        self.tag = _tag
        self.name = _name

#*******************************************************************************
class Inst2A03:
    def __init__(self, _tag: str, _index: int, _vol: int, _arp: int, _pit: int, _hpi: int, _dut: int, _name: str):
        self.tag = _tag
        self.index = _index
        self.seq_vol = _vol
        self.seq_arp = _arp
        self.seq_pit = _pit
        self.seq_hpi = _hpi
        self.seq_dut = _dut
        self.name = _name

        self.macro_vol = None # <Macro>
        self.macro_arp = None
        self.macro_pit = None
        self.macro_hpi = None
        self.macro_dut = None
        
        self.sample_keys = {} # Dict[int, <KeyDpcm>]

    def __str__(self):
        fields = [
            self.tag, self.index, self.seq_vol, self.seq_arp, 
            self.seq_pit, self.seq_hpi, self.seq_dut, self.name
        ]
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([
            str(field) for field in fields]))
        
    def __repr__(self) -> str:
        return self.__str__()

#*******************************************************************************

class InstN163:
    def __init__(self, _tag: str, _index: int, _vol: int, _arp: int, _pit: int, _hpi: int, _dut: int, w_size: int, w_pos: int, w_count: int, _name: str):
        self.tag = _tag
        self.index = _index
        self.seq_vol = _vol
        self.seq_arp = _arp
        self.seq_pit = _pit
        self.seq_hpi = _hpi
        self.seq_dut = _dut
        self.name = _name

        self.macro_vol = None # <Macro>
        self.macro_arp = None
        self.macro_pit = None
        self.macro_hpi = None
        self.macro_dut = None

        self.waves: Dict[int, List[int]] = {}

    def __str__(self):
        fields = [
            self.tag, self.index, self.seq_vol, self.seq_arp, 
            self.seq_pit, self.seq_hpi, self.seq_dut, self.name
        ]
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([
            str(field) for field in fields]))
        
    def __repr__(self) -> str:
        return self.__str__()

#*******************************************************************************
class InstVRC7:
    def __init__(self, _tag: str, _index: int, _patch: int, _registers: List[int], _name: str):
        self.tag = _tag
        self.index = _index
        self.registers = _registers
        self.name = _name
    
    def __str__(self):
        fields = [self.tag, self.index, self.registers, self.name]
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([
            str(field) for field in fields]))
    
    def __repr__(self) -> str:
        return self.__str__()

#*******************************************************************************
class InstFDS:
    def __init__(self, _tag: str, _index: int, _mod_enable: int, _mod_speed: int, _mod_depth: int, _mod_delay: int, _name: str):
        self.tag = _tag
        self.index = _index
        self.mod_enable = _mod_enable
        self.mod_speed = _mod_speed
        self.mod_depth = _mod_depth
        self.mod_delay = _mod_delay
        self.name = _name
        
        self.macro_vol = None # <Macro>
        self.macro_arp = None
        self.macro_pit = None

    def __str__(self):
        fields = [
            self.tag, self.index, self.mod_enable, \
            self.mod_speed, self.mod_depth, self.mod_delay, self.name
        ]
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([
            str(field) for field in fields]))
 
