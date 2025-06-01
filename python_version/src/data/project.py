# project.py

from typing import Dict, List

class Project:
    def __init__(self):
        self.title = ""
        self.author = ""
        self.copyright = ""
        self.comment = ""
        self.machine = 0
        self.framerate = 0 
        self.expansion = 0 
        self.vibrato = 1
        self.split = 32
        self.n163channels = 0
        self.macros: Dict[str, object] = {} 
        self.samples: Dict[int, object] = {} 
        self.grooves: Dict[int, object] = {} 
        self.usegroove: List[int] = [] 
        self.instruments: Dict[int, object] = {} 
        self.tracks: Dict[int, object] = {} 
    
    def __str__(self) -> str:
        out = "<Project> Data:\n"
        out += "--- Song Information ---\n"
        for item in ["title", "author", "copyright"]:
            val = getattr(self, item)
            out += "{}: {}\n".format(item.upper().ljust(10), val)
        out += "\n"
        
        out += "--- Comment ---\n"
        out += "{}\n".format(self.comment)
        if self.comment:
            out += "\n"

        out += "--- Macros ---\n"
        for it, val in enumerate(self.macros.values()):
            out += "{}: {}\n".format(str(it).rjust(3), val)
        out += "\n"
        
        out += "--- Grooves ---\n"
        for groove in self.grooves.values():
            out += "<Groove> {} : {}\n".format(groove.index, groove.sequence)
        out += "\n"

        out += "--- Tracks that use Default Groove ---\n"
        out += "{}\n\n".format(self.usegroove)

#       out += "--- DPCM Samples ---\n"
#       for it, val in enumerate(self.samples.values()):
#           out += "{}: {}\n".format(str(it).rjust(3), val)
#       if not(self.samples): out += "\n"
        
        out += "--- Instruments ---\n"
        for key, val in self.instruments.items():
            out += "{}: {}\n".format(str(key).rjust(3), val)
        out += "\n"
        
        out += "--- Tracks ---\n"
        for idx, trk in self.tracks.items():
            out += "<Track> {} : \'{}\'\n".format(idx, trk.name)
        
        return out
    
    def __repr__(self) -> str:
        return self.__str__()


