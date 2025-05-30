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

    def __str__(self) -> str:
        return "{}".format(self.__dict__)
    
    def __repr__(self) -> str:
        return self.__str__()


