# project.py

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
        self.macros = {}
        self.samples = {}
        self.grooves = {}
        self.instruments = {}
        self.tracks = {}
    
    def print_self(self) -> str:
        out = ""
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
        
        out += "--- DPCM Samples ---\n"
        for it, val in enumerate(self.samples.values()):
            out += "{}: {}\n".format(str(it).rjust(3), val)
        
        out += "--- Instruments ---\n"
        for key, val in self.instruments.items():
            out += "{}: {}\n".format(str(key).rjust(3), val)
         
        print(out)
        return out

    def __str__(self) -> str:
        return "{}".format(self.__dict__)
    
    def __repr__(self) -> str:
        return self.__str__()


