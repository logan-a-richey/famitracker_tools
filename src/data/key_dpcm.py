# key_dpcm.py

class KeyDpcm:
    def __init__(self, _inst: int, _octave: int, _note: int, _sample: int, _pitch: int, _loop: int, _loop_point: int, _delta: int):
        self.inst = _inst
        self.octave = _octave
        self.note = _note
        self.sample = _sample
        self.pitch = _pitch
        self.loop = _loop
        self.loop_point = _loop_point
        self.delta = _delta

    def __str__(self):
        fields = [
            self.inst, self.octave, self.note, self.sample, 
            self.pitch, self.loop, self.loop_point, self.delta 
        ]
        return "<{}> : [{}]".format(self.__class__.__name__, ", ".join([
            str(field) for field in fields]))
 
