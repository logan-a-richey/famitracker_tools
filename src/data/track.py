# track.py

from typing import List, Dict

class Track:
    count = 0
    def __init__(self):
        # update class variable
        self.index = Track.count
        Track.count += 1
        
        # sensible defaults
        self.num_rows  = 64
        self.num_cols = 5
        self.tempo = 150
        self.speed = 6
        self.name = "DefaultTrack"
        
        # data
        self.eff_cols = [1 for i in range(self.num_cols)]
        self.orders: Dict[int, List[int]] = {}
        self.tokens: Dict[str, str] = {}

    def __str__(self):
        return "<{}> : \'{}\'".format(self.__class__.__name__, self.name)

    def __repr__(self):
        return self.__str__()


