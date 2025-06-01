# track_formatter.py

import re
from typing import Optional, List
from utils.helpers import get_next_item, get_token_key, get_hex2d

from core.color_logger import ColorLogger
logger = ColorLogger("TrackFormatter").get()
logger.setLevel(ColorLogger.INFO)

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
    ''' FixedQueue / FIFO type data structure to store echo buffer ^-N strings '''
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
    # Contains a public method for returning a list of formatted lines (Track tokens unscrambled): 
    # Usage:
        TrackFormatter.unscramble(track: Track) -> List[str]:
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
        self.echo_buffers: List["EchoBuffer"] = None
    
    def _handle_control_flow(self, line: str) -> Optional[str]:
        ''' Handle Famitracker's frame-skipping effects:
        BXX: skip to Order XX. If XX is not a valid order, go the last order.
        CXX: simply stop the song. We can return and `target_order` will be in `seen_it`, exiting the loop.
        DXX: skip to the next Order at row XX. XX is bounded by 0 and num_rows - 1.
        '''

        # stop song
        cxx = RegexPatterns.CXX.match(line)
        if cxx:
            return "CXX"

        # go to order xx
        bxx = RegexPatterns.BXX.findall(line)
        if bxx:
            last_match = bxx[-1]
            next_order = int(last_match[1:], 16)
            if next_order not in self.lst_orders:
                self.target_order = self.lst_orders[-1]
            else:
                self.target_order = next_order
            self.target_row = 0
            return "BXX"

        # go to next order at row xx
        dxx = RegexPatterns.DXX.findall(line)
        if dxx:
            last_match = dxx[-1]
            self.target_row = max(min(int(last_match[1:], 16), self.track.num_rows - 1), 0)
            self.target_order = get_next_item(self.target_order, self.lst_orders)
            return "DXX"

        return None
    
    # TODO I might pull this method out of this class since we may need it elsewhere.
    def classify_note_event(self, token: str) -> str:
        ''' 
        Determine the token event type. 
        Returns a string name that corresponds to a RegexPattern.
        We can use getattr to elegantly loop through the RegexPatterns
        '''

        note_part = token.strip().split()[0]
        for name in ["NOTE_ON", "NOTE_OFF", "NOTE_NOISE", "NOTE_REL", "NOTE_ECHO"]:
            myRegex = getattr(RegexPatterns, name)
            if myRegex.match(note_part):
                return name
        return "OTHER"

    def _handle_echo_buffer(self, token: str, col: int) -> str:
        ''' 
        Determine if token should be added to EchoBuffer FixedQueue 
        Return string: unmodified token or modified echo token.
        '''

        note_event_type = self.classify_note_event(token)
        if note_event_type in ["NOTE_ON", "NOTE_OFF", "NOTE_NOISE"]:
            # NOTE that "NOTE_REL" tokens are added to the EchoBuffer, due to the behavior of Famitracker.
            # The reason for this is a note can only be released once. (No reason to echo)
            
            # add token to echo buffer. 
            self.echo_buffers[col].push_front(token[0:3])
            
            # return unmodified token
            return token
        
        elif note_event_type == "NOTE_ECHO":
            # get echo note lookup_value X in ^-X:
            lookup = self.echo_buffers[col].peek(int(token[2]))
            
            # return token but set the note_part to blank
            if not lookup:
                return "...{}".format(token[3:])
            
            # return new string, where ^-X is updated with the actual note being played.
            self.echo_buffers[col].push_front(lookup)
            return "{}{}".format(lookup, token[3:])
        
        # OTHER
        # return unmodified token
        return token

    def _parse_order(self) -> None:
        ''' 
        Read the rows, cols of the order line by line.
        We can use the get_tokek_key() function to generate the lookup needed to uncompress the Famitracker text file format.
        If a token does not exist, we use a token with the value of "... .. . <...>" where <...> is the number of blank effect columns. 
        Once this step is completed, we can join the tokens to create the line string. 
        We can use a regex on this line to scan for frame skipping effects such as Bxx, Cxx, Dxx. (order skip, song skip, and row skip, respectively)
        '''

        # Contains the list of patterns for this order 
        self.lst_cols = self.track.orders[self.target_order]
        
        # Start of order text
        msg = "PATTERN {}".format(get_hex2d(self.target_order))
        self.lines.append(msg)

        if self.target_order not in self.lst_orders:
            raise ValueError("Target order {} not in keys {}".format(self.target_order, self.lst_orders))
        
        tokens: List[str] = []
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
                token = self._handle_echo_buffer(token, col)
                tokens.append(token)
            
            # Add ROW : <line>
            prefix: str = "ROW {} : ".format(get_hex2d(row))
            line: str = prefix + " : ".join(tokens)
            self.lines.append(line)

            # Handle control flow Bxx Cxx Dxx
            res: Optional[str] = self._handle_control_flow(line)
            if res:
                logger.debug("Frame Skip: {}. Line {}".format(res, line))
                return
        
        # Get next order
        self.target_order = get_next_item(self.target_order, self.lst_orders) 

    def unscramble(self, track: "Track") -> List[str]:
        ''' Main method to call. 
        @params : 
            `track` : <Track> reference.
        @return : 
            `lines` : <List[str]>
        '''
        
        # Reset for track reading
        self.lines.clear()

        self.track = track
        self.target_order = 0
        self.target_row = 0

        self.lst_orders: List[int] = list(self.track.orders.keys())
        self.echo_buffers = [EchoBuffer() for _ in range(self.track.num_cols)]

        seen_order = set()
        while self.target_order not in seen_order:
            seen_order.add(self.target_order)
            self._parse_order()
        
        return self.lines

