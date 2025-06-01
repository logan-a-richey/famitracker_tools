# instruments.py
from abc import ABC
from typing import List, Dict, Optional

from data.macro import Macro
from data.key_dpcm import KeyDpcm

#*******************************************************************************
class BaseInst(ABC):
    def __init__(self, index: int, tag: str, name: str):
        self.index = index
        self.tag = tag
        self.name = name

        # Optional macros shared by most instruments
        self.macro_vol: Optional[Macro] = None
        self.macro_arp: Optional[Macro] = None
        self.macro_pit: Optional[Macro] = None
        self.macro_hpi: Optional[Macro] = None
        self.macro_dut: Optional[Macro] = None

    def _format_str(self, field_names: List[str]) -> str:
        fields = [str(getattr(self, name)) for name in field_names]
        name_str = "\"{}\"".format(self.name)
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join(fields + [name_str]))

    def __str__(self) -> str:
        return self._format_str(["tag", "index", "name"])

    def __repr__(self) -> str:
        return self.__str__()

#*******************************************************************************
class Inst2A03(BaseInst):
    def __init__(self,
                 tag: str,
                 index: int,
                 vol: int,
                 arp: int,
                 pit: int,
                 hpi: int,
                 dut: int,
                 name: str):
        super().__init__(index, tag, name)
        self.seq_vol = vol
        self.seq_arp = arp
        self.seq_pit = pit
        self.seq_hpi = hpi
        self.seq_dut = dut

        self.sample_keys: Dict[int, KeyDpcm] = {}

    def __str__(self) -> str:
        return self._format_str([
            "tag", "index", "seq_vol", "seq_arp", "seq_pit", "seq_hpi", "seq_dut"
        ])

#*******************************************************************************
class InstN163(BaseInst):
    def __init__(self,
                 tag: str,
                 index: int,
                 vol: int,
                 arp: int,
                 pit: int,
                 hpi: int,
                 dut: int,
                 w_size: int,
                 w_pos: int,
                 w_count: int,
                 name: str):
        super().__init__(index, tag, name)
        self.seq_vol = vol
        self.seq_arp = arp
        self.seq_pit = pit
        self.seq_hpi = hpi
        self.seq_dut = dut

        self.wave_size = w_size
        self.w_pos = w_pos
        self.w_count = w_count

        self.n163_waves: Dict[int, List[int]] = {}

    def __str__(self) -> str:
        return self._format_str([
            "tag", "index", "seq_vol", "seq_arp", "seq_pit",
            "seq_hpi", "seq_dut", "wave_size", "w_pos", "w_count"
        ])

#*******************************************************************************
class InstVRC7(BaseInst):
    def __init__(self,
                 tag: str,
                 index: int,
                 patch: int,
                 registers: List[int],
                 name: str):
        super().__init__(index, tag, name)
        self.patch = patch
        self.registers = registers

    def __str__(self) -> str:
        return self._format_str(["tag", "index", "patch", "registers"])

#*******************************************************************************
class InstFDS(BaseInst):
    def __init__(self,
                 tag: str,
                 index: int,
                 mod_enable: int,
                 mod_speed: int,
                 mod_depth: int,
                 mod_delay: int,
                 name: str):
        super().__init__(index, tag, name)
        self.mod_enable = mod_enable
        self.mod_speed = mod_speed
        self.mod_depth = mod_depth
        self.mod_delay = mod_delay

        self.fds_wave: List[int] = []
        self.fds_mod: List[int] = []

        # FDS uses only vol/arp/pit macros
        self.macro_hpi = None
        self.macro_dut = None

    def __str__(self) -> str:
        return self._format_str([
            "tag", "index", "mod_enable", "mod_speed", "mod_depth", "mod_delay"
        ])
