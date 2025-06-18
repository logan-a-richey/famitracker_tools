# midi_exporter.py

import re

from core.color_logger import ColorLogger
logger = ColorLogger("TrackFormatter").get()
logger.setLevel(ColorLogger.INFO)

INST_PATTERN = re.compile(r'^([0-9A-F]{2})')
VOL_PATTERN = re.compile(r'^([0-9A-F])')

PITCH_PATTERN = re.compile(r'^([A-G][\-#b][0-9])')
NOTE_MAPPING = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11
}

class ColContext:
    def __init__(self):
        self.last_pitch = -1
        self.last_vol = 15
        self.last_inst = 0
        self.last_time = 0
    
class MidiExporter:
    def __init__(self):
        self.col_contexts = []

    def get_note_str_to_int(self, token: str) -> int:
        ''' Return midi pitch '''
        note_match = PITCH_PATTERN.match(token)
        if not note_match:
            return -1

        note_str = note_match.group(1)
        note_pitch = 0
        
        # note letter offset
        note_pitch = NOTE_MAPPING.get(note_str[0], 0)
        
        # handle accidental
        if note_str[1] == '#':
            note_pitch += 1
        elif note_str[2] == 'b':
            note_pitch -= 1
        
        # note octave
        note_octave = int(note_str[2])
        note_pitch = note_pitch + (note_octave * 12)
        return note_pitch
    
    def get_inst_str_to_int(self, token: str) -> int:
        inst_match = INST_PATTERN.match(token)
        if not inst_match:
            return -1
        inst_int = int(inst_match.group(1), 16)
        return inst_int

    def get_vol_str_to_int(self, token: str) -> int:
        vol_match = VOL_PATTERN.match(token)
        if not vol_match:
            return -1
        vol_int = int(vol_match.group(1), 16)
        return vol_int
    
    def export_track(self, track: "Track", lines: str, output_name: str):
        self.col_contexts = [ColContext() for _ in range(track.num_cols)] 
        
        step = -1
        for line in lines:
            if not line.startswith("ROW"):
                continue
            
            logger.debug(line)
            
            step += 1

            cols = [token.strip() for token in line.split(":")[1:]]
            
            for ci, col in enumerate(cols):
                cc = self.col_contexts[ci]

                note_part, inst_part, vol_part = col.split()[0:3]
                eff_part = col.split()[3:]
                
                # --- update inst ---
                inst_int = self.get_inst_str_to_int(inst_part)
                if inst_int >= 0:
                    cc.last_inst = inst_int

                # --- update vol ---
                vol_int = self.get_vol_str_to_int(vol_part)
                if vol_int >= 0:
                    cc.last_vol = vol_int

                # --- update note --- 
                # note_off
                if note_part == "---":
                    if cc.last_pitch >= 0:
                        # add note
                        print("add note: {} @ {}".format(cc.last_pitch, step))
                        pass
                    cc.last_pitch = -1
                
                # note on
                note_pitch = self.get_note_str_to_int(note_part)
                if note_pitch >= 0:
                    if cc.last_pitch >= 0:
                        # add note
                        print("add note: {} @ {}".format(cc.last_pitch, step))
                        pass
                    cc.last_pitch = note_pitch
                
