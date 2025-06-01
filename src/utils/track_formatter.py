# track_formatter.py

import re
from typing import Optional, List
from utils.helpers import get_next_item
from utils.helpers import get_token_key

from core.color_logger import ColorLogger
logger = ColorLogger("TrackFormatter").get()
logger.setLevel(ColorLogger.DEBUG)

class RegexPatterns:
    ''' Contains precompiled regex patterns '''
    BXX = re.compile(r'B[0-9A-F]{2}')
    CXX = re.compile(r'C[0-9A-F]{2}')
    DXX = re.compile(r'D[0-9A-F]{2}')
    NOTE_ON     = re.compile(r'[A-G][\-#b][0-9]')
    NOTE_NOISE  = re.compile(r'[0-9A-F]\-\#')
    NOTE_OFF    = re.compile(r'\-{3}')
    NOTE_REL    = re.compile(r'\={3}')
    NOTE_ECHO   = re.compile(r'\^\-[0-3]')


class EchoBuffer:
    ''' FIFO type data structure to store echo buffer ^-N strings '''
    def __init__(self):
        self.max_size = 4
        self.lst: List[str] = []
    
    def push_front(self, item: str):
        self.lst.insert(0, item)
        if len(self.lst) >= self.max_size:
            self.lst.pop()

    def peek(self, idx: int):
        if len(self.lst) == 0:
            return None
        ridx = min(max(idx, 0), len(self.lst) - 1)
        return self.lst[ridx]


class TrackFormatter:
    ''' 
    Use method `def unscramble(self, track) -> List[str]` 
    Return a list of lines (Track tokens unscrambled): 
    '''

    def __init__(self, project):
        self.lines: List[str] = []

        # access <Project> state
        self.project = project
     
        # keep track of <Track> state
        self.track: Optional["Track"] = None
        self.target_row: int = 0
        self.target_order: int = 0
        self.lst_orders: Optional[List[int]] = None
        self.lst_cols: Optional[List[int]] = None

        self.echo_buffers: List[EchoBuffer] = None
    
    def handle_control_flow(self, line: str) -> Optional[str]:
        # stop song
        cxx = RegexPatterns.CXX.match(line)
        if cxx:
            return "CXX"

        # go to order xx
        bxx = RegexPatterns.BXX.findall(line)
        if bxx:
            self.target_row = 0
            last_match = bxx[-1]
            next_order = int(last_match[1:], 16)
            if next_order not in self.lst_orders:
                self.target_order = self.lst_orders[-1]
            else:
                self.target_order = next_order
            return "BXX"

        # go to next order at row xx
        dxx = RegexPatterns.DXX.findall(line)
        if dxx:
            last_match = dxx[-1]
            next_row = min(int(last_match[1:], 16), self.track.num_rows - 1)
            self.target_row = 0
            self.target_order = get_next_item(self.target_order, self.lst_orders)
            return "DXX"

        return None
    
    # TODO
    def classify_note_event(self, token: str) -> str:
        note_part = token.strip().split()[0]
        for name in ["NOTE_ON", "NOTE_OFF", "NOTE_NOISE", "NOTE_REL", "NOTE_ECHO"]:
            myRegex = getattr(RegexPatterns, name)
            if myRegex.match(note_part):
                return name
        return "OTHER"

    def handle_echo_buffer(self, token: str, col: int) -> Optional[str]:
        note_event_type = self.classify_note_event(token)
        if note_event_type in ["NOTE_ON", "NOTE_OFF", "NOTE_NOISE"]:
            # add to echo buffer
            self.echo_buffers[col].push_front(token[0:3])
            return None
        elif note_event_type == "NOTE_ECHO":
            # get echo note, if there is one
            echo_value = int(token[2])
            lookup = self.echo_buffers[col].peek(echo_value)
            if not lookup:
                return "...{}".format(token[3:])
            # return new string
            self.echo_buffers[col].push_front(lookup)
            return "{}{}".format(lookup, token[3:])
        # OTHER
        return None

    def parse_order(self) -> None:
        self.lst_cols = self.track.orders[self.target_order]
        tokens: List[str] = []

        if self.target_order not in self.lst_orders:
            raise ValueError("Target order {} not in keys {}".format(self.target_order, self.lst_orders))

        for row in range(self.target_row, self.track.num_rows):
            tokens.clear()
            for col in range(self.track.num_cols):
                col_lookup = self.lst_cols[col]
                
                token_key = get_token_key(col_lookup, row, col)
                token = self.track.tokens.get(token_key, None)
                
                # Handle null token
                if not token:
                    token = "... .. .{}".format(" ..." * self.track.eff_cols[col])
                
                ## Handle echo buffer
                res = self.handle_echo_buffer(token, col)
                if res:
                    token = res
                
                tokens.append(token)
            
            line = "{} : ".format(str(self.target_order).rjust(2, '0')) + " : ".join(tokens)
            self.lines.append(line)

            # Handle control flow Bxx Cxx Dxx
            res  = self.handle_control_flow(line)
            if res:
                #logger.info("Frame Skip: {}. Line {}".format(res, line))
                return
        
        # get next order
        self.target_order = get_next_item(self.target_order, self.lst_orders) 

    def print_lines(self):
        for line in self.lines:
            logger.debug(line)

    def unscramble(self, track) -> List[str]:
        self.lines.clear()

        self.track = track
        self.target_order = 0
        self.target_row = 0
        self.lst_orders: List[int] = list(self.track.orders.keys())
        self.echo_buffers = [EchoBuffer() for _ in range(self.track.num_cols)]

        seen_order = set()
        while self.target_order not in seen_order:
            seen_order.add(self.target_order)
            self.parse_order()
        
        self.print_lines()

        # TODO does this return a deepcopy or reference?
        return self.lines

