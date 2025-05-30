# instruments.py

class Inst2A03:
    def __init__(self, _label: str, _index: int, _vol: int, _arp: int, _pit: int, _hpi: int, _dut: int, _name: str):
        self.label = _label
        self.index = _index
        self.seq_vol = _vol
        self.seq_arp = _arp
        self.seq_pit = _pit
        self.seq_hpi = _hpi
        self.seq_dut = _dut
        self.name = _name

        self.macro_vol = None
        self.macro_arp = None
        self.macro_pit = None
        self.macro_hpi = None
        self.macro_dut = None

    def __str__(self):
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([str(field) for field in [self.label, self.index, self.seq_vol, self.seq_arp, self.seq_pit, self.seq_hpi, self.seq_dut, self.name]]))
        
    def __repr__(self) -> str:
        return self.__str__()

