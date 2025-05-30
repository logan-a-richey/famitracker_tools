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

    def get_str(self):
        out = "{}| ".format("<{}>".format(self.__class__.__name__).ljust(12))
        #out += "label = {},\t".format(self.label)
   
        m_spacing = 14
        for field in ["macro_vol", "macro_arp", "macro_pit", "macro_hpi", "macro_dut"]:
            obj = getattr(self, field)
            if obj:
                out += "{} = {}| ".format(field, str(obj.label).ljust(m_spacing))
            else:
                out += "{} = {}| ".format(field, "None".ljust(m_spacing))
        
        out +="name = {}".format(self.name)
        return out

    def __str__(self) -> str:
        return "{}".format(self.__dict__)
    
    def __repr__(self) -> str:
        return self.__str__()

