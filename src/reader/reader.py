#!/usr/bin/env python3

import re
from typing import Dict, List, Any

from data.macro import Macro
from data.instruments import Inst2A03

# class Dpcm: pass
# class KeyDpcm: pass
# class Groove: pass
# class Track: pass

class Reader:
    def __init__(self):
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
            "INST2A03"      : self.handle_inst_basic,
            "INSTVRC6"      : self.handle_inst_basic,
            "INSTS5B"       : self.handle_inst_basic,
            #"INSTN163"      : self.handle_inst_n163,
            #"INSTVRC7"      : self.handle_inst_vrc7,
            #"INSTFDS"       : self.handle_inst_fds
        }

    def handle_song_information(self, line: str):
        match = re.match(r'^\s*(\w+)\s+"(.*)"$', line)
        if not match:
            print(f"[W] Could not match line: {line}")
            return

        tag = match.group(1).lower()
        val = match.group(2)

        if hasattr(self.project, tag):
            setattr(self.project, tag, val)
        else:
            print(f"[W] Unknown song info tag: {tag}")

    def handle_comment(self, line: str):
        match = re.match(r'^\s*(\w+)\s+"(.*)"$', line)
        if not match:
            print(f"[W] Could not match line: {line}")
            return
        
        tag = match.group(1)
        val = match.group(2)

        if self.project.comment:
            self.project.comment += "\n{}".format(val)
        else:
            self.project.comment = val

    def handle_global_settings(self, line: str):
        match = re.match(r'^\s*(\w+)\s+(\d+)$', line)
        if not match:
            print(f"[W] Could not match line: {line}")
            return

        tag = match.group(1).lower()
        val = int(match.group(2))

        if hasattr(self.project, tag):
            setattr(self.project, tag, val)
        else:
            print(f"[W] Unknown global setting tag: {tag}")
    
    def handle_macro(self, line: str):
        match = re.match(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\:\s*(.*)', line)
        if not match:
            print(f"[W] Could not match line: {line}")
            return 

        tag = match.group(1)
        _type, _index, _loop, _release, _setting = list(map( int, match.group(2, 3, 4, 5, 6)))
        _sequence = list(map(int, line.split(":")[1].strip().split()))
        _label = Macro.generate_macro_label(tag, _type, _index)
         
        # create <Macro>
        myMacro = Macro(_label, _type, _index, _loop, _release, _setting, _sequence)
        
        # add macro to <Project> dictionary
        self.project.macros[_label] = myMacro 

    def handle_inst_basic(self, line: str):
        # INST2A03 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_dut] [name]
        match = re.match(r'\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"$',line)
        if not match:
            print(f"[W] Could not match line: {line}")
            return 
    
        tag = match.group(1) 
        index, vol, arp, pit, hpi, dut = list(map(int, match.group(2, 3, 4, 5, 6, 7)))
        name = match.group(8)

        myInst = Inst2A03(tag, index, vol, arp, pit, hpi, dut, name)
        inst_to_macro = {
            "INST2A03": "MACRO",
            "INSTVRC6": "MACROVRC6",
            "INSTN163": "MACRON163",
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

#*******************************************************************************

    def handle_line(self, line: str):
        if not line or line.startswith("#"):
            return

        first_word = line.split()[0]
        func = self.command_map.get(first_word, None)
        if func:
            func(line)
        else:
            # print(f"[W] Unknown line: {line}")
            pass

    def read_file(self, infile: str, project: Any):
        self.project = project

        with open(infile, 'r') as file:
            for line in file:
                self.handle_line(line.strip())

#    def handle_dpcmdef(self, line: str): pass
#    def handle_dpcm(self, line: str): pass
#    def handle_groove(self, line: str): pass
#    def handle_usegroove(self, line: str): pass

#    def handle_inst2a03(self, line: str): pass
#    def handle_instvrc6(self, line: str): pass
#    def handle_instvrc7(self, line: str): pass
#    def handle_instfds(self, line: str): pass
#    def handle_instn163(self, line: str): pass
#    def handle_insts5b(self, line: str): pass

#    def handle_keydpcm(self, line: str): pass
#    def handle_fdswave(self, line: str): pass
#    def handle_fdsmod(self, line: str): pass
#    def handle_fdsmacro(self, line: str): pass
#    def handle_n163wave(self, line: str): pass

#    def handle_track(self, line: str): pass
#    def handle_columns(self, line: str): pass
#    def handle_order(self, line: str): pass
#    def handle_pattern(self, line: str): pass
#    def handle_row(self, line: str): pass

