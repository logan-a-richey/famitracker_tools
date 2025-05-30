# track.py

from typing import List, Dict

class Track:
    def __init__(self):
        self.num_rows  = 64
        self.num_cols = 5
        self.eff_cols = []
        self.tempo = 150
        self.speed = 6
        self.name = "DefaultTrack"

        self.orders: Dict[int, List[int]] = {}
        self.tokens = Dict[str, str]

    # TODO print self

