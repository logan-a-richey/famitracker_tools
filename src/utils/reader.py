#!/usr/bin/env python3

import re
import sys
from typing import Dict, List, Any

from data.macro import Macro
from data.dpcm import Dpcm
from data.groove import Groove
from data.instruments import Inst2A03, InstN163, InstVRC7, InstFDS
from data.key_dpcm import KeyDpcm
from data.track import Track

from core.color_logger import ColorLogger
logger = ColorLogger("Reader").get()
logger.setLevel(ColorLogger.DEBUG)


class RegexPatterns:
    SONG_INFO = re.compile(r'^\s*(\w+)\s+"(.*)"$')
    COMMENT = re.compile(r'^\s*(COMMENT)\s+"(.*)"$')
    GLOBAL_SETTINGS = re.compile(r'^\s*(\w+)\s+(\d+)$')
    MACRO = re.compile(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\:\s*(.*)')
    DPCMDEF = re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s*\"(.*)\"$')
    # TODO DPCM = re.compile()
    INST2A03 = re.compile(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"$')
    INSTN163 = re.compile(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"$')
    INSTVRC7 = re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s*\"(.*)\"$')
    INSTFDS = re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"$')
    KEYDPCM = re.compile(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)$')
    FDSWAVE = re.compile(r'^\s*(\w+)\s+(\d+)\s*:\s*(.*)$')
    FDSMOD =  re.compile(r'^\s*(\w+)\s+(\d+)\s*:\s*(.*)$')
    FDSMACRO = re.compile(r'^\s*(\w+)\s+(\d+)\s+([012])\s+(\-?\d+)\s+(\-?\d+)\s+(\d+)\s*\:\s*(.*)$')
    N163WAVE = re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s*:\s*(.*)$')
    TRACK = re.compile(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"$')
    ORDER = re.compile(r'^\s*(ORDER)\s*([0-9A-F]{2})\s*:\s*(.*)$')
    ROW = re.compile(r'^\s*ROW\s*([0-9A-F]{2})\s*:\s*(.*)$')
    #BLANK_TOKEN = re.compile(r'[.\s]')
    BLANK_TOKEN = re.compile(r'^[\s\.]+$')

class Reader:
    def __init__(self):
        # contain a reference to project
        self.project = None

        self.command_map = {
            "TITLE"         : self.handle_song_information,
            "AUTHOR"        : self.handle_song_information,
            "COPYRIGHT"     : self.handle_song_information,
            "COMMENT"       : self.handle_comment,
            
            "MACHINE"       : self.handle_global_settings,
            "FRAMERATE"     : self.handle_global_settings,
            "EXPANSION"     : self.handle_global_settings,
            "VIBRATO"       : self.handle_global_settings,
            "SPLIT"         : self.handle_global_settings,
            "N163CHANNELS"  : self.handle_global_settings,
            
            "MACRO"         : self.handle_macro,
            "MACROVRC6"     : self.handle_macro,
            "MACRON163"     : self.handle_macro,
            "MACROS5B"      : self.handle_macro,
            
            "DPCMDEF"       : self.handle_dpcm_def,
            "DPCM"          : self.handle_dpcm_data,
            "GROOVE"        : self.handle_groove,
            "USEGROOVE"     : self.handle_usegroove,
            
            "INST2A03"      : self.handle_inst_2a03,
            "INSTVRC6"      : self.handle_inst_2a03,
            "INSTS5B"       : self.handle_inst_2a03,
            "INSTN163"      : self.handle_inst_n163,
            "INSTVRC7"      : self.handle_inst_vrc7,
            "INSTFDS"       : self.handle_inst_fds,

            "KEYDPCM"       : self.handle_key_dpcm,
            "FDSWAVE"       : self.handle_fds_wave,
            "FDSMOD"        : self.handle_fds_mod,
            "FDSMACRO"      : self.handle_fds_macro,
            "N163WAVE"      : self.handle_n163_wave,
            
            "TRACK"         : self.handle_track,
            "COLUMNS"       : self.handle_columns,
            "ORDER"         : self.handle_order,
            "PATTERN"       : self.handle_pattern,
            "ROW"           : self.handle_row
        }
        
        self.last_dpcm_index = 0
        self.last_pattern_index = 0
        self.last_track_index = 0

    def handle_song_information(self, line: str):
        # TAG "[STRING]"
        match = RegexPatterns.SONG_INFO.match(line)
        if not match:
            raise ValueError("Regex failed")

        tag = match.group(1).lower()
        val = match.group(2)

        if not hasattr(self.project, tag):
            raise ValueError("Invalid SongInformation tag \"{}\"".format(tag))
        
        setattr(self.project, tag, val)

    def handle_comment(self, line: str):
        # COMMENT "[STRING]"
        match = RegexPatterns.COMMENT.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        tag = match.group(1)
        val = match.group(2)

        if self.project.comment:
            self.project.comment += "\n{}".format(val)
        else:
            self.project.comment = val

    def handle_global_settings(self, line: str):
        # TAG [INT]
        match = RegexPatterns.GLOBAL_SETTINGS.match(line)
        if not match:
            raise ValueError("Regex failed")

        tag = match.group(1).lower()
        val = int(match.group(2))

        if not hasattr(self.project, tag):
            raise ValueError("Invalid GlobalSettings tag \"{}\"".format(tag))
        
        setattr(self.project, tag, val)
    
    def handle_macro(self, line: str):
        # MACRO [type] [index] [loop] [release] [setting] : [macro]
        match = RegexPatterns.MACRO.match(line)
        if not match:
            raise ValueError("Regex failed")

        tag = match.group(1)
        _type, _index, _loop, _release, _setting = list(map( int, match.group(2, 3, 4, 5, 6)))
        _int_list = match.group(7).strip().split()

        try:
            _sequence = list(map(int, _int_list))
        except Exception as e:
            raise ValueError("Could not parse IntList")

        # create <Macro>
        _label = Macro.generate_macro_label(tag, _type, _index)
        myMacro = Macro(_label, _type, _index, _loop, _release, _setting, _sequence)
        
        # add macro to <Project> dictionary
        self.project.macros[_label] = myMacro 
    
    def handle_dpcm_def(self, line: str):
        # DPCMDEF [index] [size] "[name]"
        match = RegexPatterns.DPCMDEF.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        tag = match.group(1) 
        index, size = list(map(int, match.group(2, 3)))
        name = match.group(4)

        myDpcm = Dpcm(index, size, name)
        self.project.samples[index] = myDpcm
        self.last_dpcm_index = index

    def handle_dpcm_data(self, line: str):
        # DPCM : [data]
        # TODO regex for better checking
        try:
            nums = list(map(lambda x: int(x, 16), line.split(":")[1].strip().split()))
            self.project.samples[self.last_dpcm_index].data.extend(nums)
        except Exception as e:
            raise ValueError("Could not parse HexList")

    def handle_groove(self, line: str):
        # TODO - regex for better checking
        # GROOVE [index] [sizeof] : [groove_sequence]
        try:
            index, size = list(map(int, line.strip().split()[1:3]))
            sequence = list(map(int, line.split(":")[1].strip().split()))
            myGroove = Groove(index, size, sequence)
            self.project.grooves[index] = myGroove

        except Exception as e:
            raise ValueError("Could not parse IntList")

    def handle_usegroove(self, line: str):
        # TODO - regex for better checking
        # USEGROOVE : []
        try:
            self.project.usegroove = list(map(int, line.split(":")[1].strip().split()))
        except Exception as e:
            raise ValueError("Could not parse IntList")

    def handle_inst_2a03(self, line: str):
        # INST2A03 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_dut] "[name]"
        match = RegexPatterns.INST2A03.match(line)
        if not match:
            raise ValueError("Regex failed")
    
        tag = match.group(1) 
        index, vol, arp, pit, hpi, dut = list(map(int, match.group(2, 3, 4, 5, 6, 7)))
        name = match.group(8)

        myInst = Inst2A03(tag, index, vol, arp, pit, hpi, dut, name)
        inst_to_macro = {
            "INST2A03": "MACRO",
            "INSTVRC6": "MACROVRC6",
            "INSTS5B": "MACROS5B"
        }

        macro_vol_label = Macro.generate_macro_label(inst_to_macro.get(tag, "XYZ"), 0, vol)
        macro_arp_label = Macro.generate_macro_label(inst_to_macro.get(tag, "XYZ"), 1, arp)
        macro_pit_label = Macro.generate_macro_label(inst_to_macro.get(tag, "XYZ"), 2, pit)
        macro_hpi_label = Macro.generate_macro_label(inst_to_macro.get(tag, "XYZ"), 3, hpi)
        macro_dut_label = Macro.generate_macro_label(inst_to_macro.get(tag, "XYZ"), 4, dut)
        
        macro_vol_obj = self.project.macros.get(macro_vol_label, None)
        macro_arp_obj = self.project.macros.get(macro_arp_label, None)
        macro_pit_obj = self.project.macros.get(macro_pit_label, None)
        macro_hpi_obj = self.project.macros.get(macro_hpi_label, None)
        macro_dut_obj = self.project.macros.get(macro_dut_label, None)

        if macro_vol_obj: 
            myInst.macro_vol = macro_vol_obj
        if macro_arp_obj: 
            myInst.macro_arp = macro_arp_obj
        if macro_pit_obj: 
            myInst.macro_pit = macro_pit_obj
        if macro_hpi_obj: 
            myInst.macro_hpi = macro_hpi_obj
        if macro_dut_obj: 
            myInst.macro_dut = macro_dut_obj
        
        # add <Inst2A03> to project
        self.project.instruments[index] = myInst

    def handle_inst_n163(self, line: str):
        match = RegexPatterns.INSTN163.match(line)
        # INSTN163 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_wav] [w_size] [w_pos] [w_count] "[name]"
        if not match:
            raise ValueError("Regex failed")

        tag = match.group(1) 
        index, vol, arp, pit, hpi, dut = list(map(int, match.group(2, 3, 4, 5, 6, 7)))
        w_size, w_pos, w_count = list(map(int, match.group(8, 9, 10)))
        name = match.group(11)

        myInst = InstN163(tag, index, vol, arp, pit, hpi, dut, w_size, w_pos, w_count, name)

        macro_vol_label = Macro.generate_macro_label("MACRON163", 0, vol)
        macro_arp_label = Macro.generate_macro_label("MACRON163", 1, arp)
        macro_pit_label = Macro.generate_macro_label("MACRON163", 2, pit)
        macro_hpi_label = Macro.generate_macro_label("MACRON163", 3, hpi)
        macro_dut_label = Macro.generate_macro_label("MACRON163", 4, dut)
        
        macro_vol_obj = self.project.macros.get(macro_vol_label, None)
        macro_arp_obj = self.project.macros.get(macro_arp_label, None)
        macro_pit_obj = self.project.macros.get(macro_pit_label, None)
        macro_hpi_obj = self.project.macros.get(macro_hpi_label, None)
        macro_dut_obj = self.project.macros.get(macro_dut_label, None)

        if macro_vol_obj: 
            myInst.macro_vol = macro_vol_obj
        if macro_arp_obj: 
            myInst.macro_arp = macro_arp_obj
        if macro_pit_obj: 
            myInst.macro_pit = macro_pit_obj
        if macro_hpi_obj: 
            myInst.macro_hpi = macro_hpi_obj
        if macro_dut_obj: 
            myInst.macro_dut = macro_dut_obj
        
        # add <InstN163> to project
        self.project.instruments[index] = myInst

    def handle_inst_vrc7(self, line: str):
        # INSTVRC7 [index] [patch] [r0] [r1] [r2] [r3] [r4] [r5] [r6] [r7] "[name]"
        match = RegexPatterns.INSTVRC7.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        tag = match.group(1)
        index, patch = list(map(int, match.group(2, 3)))
        r0, r1, r2, r3, r4, r5, r6, r7 = list(map(lambda x: int(x, 16), match.group(4, 5, 6, 7, 8, 9, 10, 11)))
        name = match.group(12)
        registers = [r0, r1, r2, r3, r4, r5, r6, r7]
        myInst = InstVRC7(tag, index, patch, registers, name)
        
        self.project.instruments[index] = myInst

    def handle_inst_fds(self, line: str):
        # INSTFDS [index] [mod_enable] [mod_speed] [mod_depth] [mod_delay] "[name]"
        match = RegexPatterns.INSTFDS.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        tag = match.group(1)
        index, mod_enable, mod_speed, mod_depth, mod_delay = list(map(int, match.group(2, 3, 4, 5, 6)))
        name = match.group(7)

        myInst = InstFDS(tag, index, mod_enable, mod_speed, mod_depth, mod_delay, name)

        self.project.instruments[index] = myInst

    def handle_key_dpcm(self, line: str):
        # KEYDPCM [inst] [octave] [note] [sample] [pitch] [loop] [loop_point] [delta]
        match = RegexPatterns.KEYDPCM.match(line)
        if not match:
            raise ValueError("Regex failed")

        inst, octave, note, sample, pitch, loop, loop_point, delta = list(map(
            int, match.group(2, 3, 4, 5, 6, 7, 8, 9)))

        myKeyDpcm = KeyDpcm(inst, octave, note, sample, pitch, loop, loop_point, delta)

        instLookup = self.project.instruments.get(inst)
        
        if not isinstance(instLookup, Inst2A03):
            raise ValueError("`instLookup` is not type <Inst2A03>")

        midi_pitch = octave * 12 + note
        instLookup.sample_keys[midi_pitch] = myKeyDpcm

    def handle_fds_wave(self, line: str):
        # FDSWAVE [inst] : [data]
        match = RegexPatterns.FDSWAVE.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        # tag = match.group(1)
        inst = int(match.group(2))
        
        try:
            lst = list(map(int, match.group(3).strip().split()))
        except:
            raise ValueError("Failed to parse List[int]")
        
        instLookup = self.project.instruments.get(inst, None)            
        
        if not instLookup:
            raise ValueError("Could not find Instrument index {}".format(inst))
        
        if not isinstance(instLookup, InstFDS):
            raise ValueError("`instLookup` is not of type <InstFDS>")

        instLookup.fds_wave = lst

    def handle_fds_mod(self, line: str):
        # FDSMOD [inst] : [data]
        match = RegexPatterns.FDSMOD.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        # tag = match.group(1)
        inst = int(match.group(2))
        try:
            lst = list(map(int, match.group(3).strip().split()))
        except:
            raise ValueError("Could not parse List[int]")

        instLookup = self.project.instruments.get(inst, None)            
        if not instLookup:
            raise ValueError("Could not find Instrument index {}".format(inst))
        
        if not isinstance(instLookup, InstFDS):
            raise ValueError("`instLookup` is not of type <InstFDS>")

        instLookup.fds_mod = lst
        
    def handle_fds_macro(self, line: str):
        # FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
        match = RegexPatterns.FDSMACRO.match(line)
        if not match:
            raise ValueError("Regex failed.")
        
        tag = match.group(1)
        _inst, _type, _loop, _release, _setting = list(map(
            int, match.group(2, 3, 4, 5, 6)))
        
        instLookup = self.project.instruments.get(_inst, None)
        if not instLookup:
            raise ValueError("Could not find Instrument index {}".format(inst))
        
        try:
            _sequence = list(map(int, match.group(7).strip().split()))
        except Exception as e:
            raise ValueError("Could not parse List[int]")

        label = Macro.generate_macro_label(tag, _type, 0)
        myMacro = Macro(label, _type, 0, _loop, _release, _setting, _sequence)

        target = ""
        if _type == 0:
            target = "macro_vol" 
        elif _type == 1:
            target = "macro_arp"
        elif _type == 2:
            target = "macro_pit"
        else:
            raise ValueError("Invalid macro type: {}".format(_type))

        setattr(instLookup, target, myMacro)
        self.project.macros[label] = myMacro

    def handle_n163_wave(self, line: str):
        # N163WAVE [inst] [wave] : [data]
        match = RegexPatterns.N163WAVE.match(line)
        if not match:
            raise ValueError("Regex failed.")

        tag = match.group(1)
        inst_index, wave_index = list(map(int, match.group(2, 3)))
        lst = list(map(int, match.group(4).strip().split()))

        instLookup = self.project.instruments.get(inst_index, None)
        
        if not instLookup:
            raise ValueError("Failed to find Instrument {}".format(inst_index))
        
        if not isinstance(instLookup, InstN163):
            raise ValueError("instLookup is not of type <InstN163>")

        instLookup.n163_waves[wave_index] = lst

    def handle_track(self, line: str):
        # TRACK [pattern] [speed] [tempo] [name]
        match = RegexPatterns.TRACK.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        tag = match.group(1)
        num_rows, speed, tempo = list(map(int, match.group(2, 3, 4)))
        name = match.group(5)

        myTrack = Track()
        
        myTrack.num_rows = num_rows
        myTrack.speed = speed
        myTrack.tempo = tempo
        myTrack.name = name
         
        self.project.tracks[myTrack.index] = myTrack
        self.last_track_index = myTrack.index

    def handle_columns(self, line: str):
        # COLUMNS : [columns]
        last_track = self.project.tracks.get(self.last_track_index, None)
        if not last_track:
            raise ValueError("Tried to access null <Track>")

        try:
            lst = list(map(int, line.split(":")[1].strip().split()))
            last_track.num_cols = len(lst)
            last_track.eff_cols = lst
        except Exception as e:
            raise ValueError("Could not parse List[int]")

    def handle_order(self, line: str):
        # ORDER [frame] : [list]
        last_track = self.project.tracks.get(self.last_track_index, None)
        if not last_track:
            raise ValueError("Tried to access null <Track>")
        
        match = RegexPatterns.ORDER.match(line)
        if not match:
            raise ValueError("Regex failed")
        
        # TODO error checking
        tag = match.group(1)
        idx = int(match.group(2), 16)
        lst = list(map(lambda x: int(x, 16), match.group(3).strip().split()))

        last_track.orders[idx] = lst

    def handle_pattern(self, line: str):
        # PATTERN [pattern]
        try:
            idx = int(line.strip().split()[1], 16)
            self.last_pattern_index = idx
        except:
            raise ValueError("Could not get Pattern index.")
       
    # TODO
    def handle_row(self, line: str):
        # ROW [row] : [c0] : [c1] : [c2] ...
        last_track = self.project.tracks.get(self.last_track_index, None)
        if not last_track:
            raise ValueError("Tried to access null <Track>")

        match = RegexPatterns.ROW.match(line)
        if not match:
            raise ValueError("Regex failed.")
        
        row = int(match.group(1), 16)
        tokens = [token.strip() for token in match.group(2).split(":")]
        
        # print(row, tokens)
         
        if len(tokens) != last_track.num_cols:
            raise ValueError("Number of Row tokens does not match Track.num_rows")
        
        for col, token in enumerate(tokens):
            # print(col, token)
            # TODO
            blankMatch = RegexPatterns.BLANK_TOKEN.match(token)
            if blankMatch:
                continue
            
            # TODO - put this in a helpers_function.py
            tokenKey = "PAT={}::ROW={}::COL={}".format(self.last_pattern_index, row, col)
            last_track.tokens[tokenKey] = token
            
            logger.verbose("Added tokens[\'{}\'] = \'{}\'".format(tokenKey, token))
        
#*******************************************************************************

    def handle_line(self, line: str):
        if not line or line.startswith("#"):
            return

        first_word = line.split()[0]
        func = self.command_map.get(first_word, None)
        if not func:
            logger.warning("Unknown Tag \"{}\", Line: {}".format(line.split()[0], line))
            return

        try:
            func(line)
        except Exception as e:
            logger.warning("{}, Line = \"{}\"".format(e, line))
            sys.exit(1)

    def read_file(self, infile: str, project: Any):
        self.project = project
        try:
            with open(infile, 'r') as file:
                for line in file:
                    self.handle_line(line.strip())
        except FileNotFoundError:
            logger.error("File not found.")
            sys.exit(1)
        except IOError as e:
            logging.error("Error: An I/O error occurred: {}".format(e))
            sys.exit(1)
        except Exception as e:
            logging.error("An unexpected error occured: {}".format(e))
            sys.exit(1)
        
