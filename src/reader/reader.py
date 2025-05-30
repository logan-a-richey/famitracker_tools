#!/usr/bin/env python3

# TODO
#Track, Columns, Order, Pattern, Row

import re
from typing import Dict, List, Any

from data.macro import Macro
from data.dpcm import Dpcm
from data.groove import Groove
from data.instruments import Inst2A03, InstN163, InstVRC7, InstFDS
from data.key_dpcm import KeyDpcm
from data.track import Track

#import logging
#logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

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
            
            # TODO
            "TRACK"         : self.handle_track,
            "COLUMNS"       : self.handle_columns,
            "ORDER"         : self.handle_order,
            "PATTERN"       : self.handle_pattern,
            "ROW"           : self.handle_row
        }
        # private
        self.last_dpcm_index = 0
        self.last_pattern_index = 0
        self.last_track_index = 0
    

    def handle_song_information(self, line: str):
        # TAG "[STRING]"
        match = re.match(r'^\s*(\w+)\s+"(.*)"$', line)
        if not match:
            #logging.warn("Could not match line: {}".format(line))
            print("[W] Could not match line: {}".format(line))
            return

        tag = match.group(1).lower()
        val = match.group(2)

        if hasattr(self.project, tag):
            setattr(self.project, tag, val)
        else:
            print(f"[W] Unknown song info tag: {tag}")

    def handle_comment(self, line: str):
        # COMMENT "[STRING]"
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
        # TAG [INT]
        match = re.match(r'^\s*(\w+)\s+(\d+)$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return

        tag = match.group(1).lower()
        val = int(match.group(2))

        if hasattr(self.project, tag):
            setattr(self.project, tag, val)
        else:
            print(f"[W] Unknown global setting tag: {tag}")
    
    def handle_macro(self, line: str):
        # MACRO [type] [index] [loop] [release] [setting] : [macro]
        match = re.match(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\:\s*(.*)', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return 

        tag = match.group(1)
        _type, _index, _loop, _release, _setting = list(map( int, match.group(2, 3, 4, 5, 6)))
        _sequence = list(map(int, line.split(":")[1].strip().split()))
        _label = Macro.generate_macro_label(tag, _type, _index)
         
        # create <Macro>
        myMacro = Macro(_label, _type, _index, _loop, _release, _setting, _sequence)
        
        # add macro to <Project> dictionary
        self.project.macros[_label] = myMacro 
    
    def handle_dpcm_def(self, line: str):
        # DPCMDEF [index] [size] "[name]"
        match = re.match(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s*\"(.*)\"$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return
        tag = match.group(1)
        index, size = list(map(int, match.group(2, 3)))
        name = match.group(4)

        myDpcm = Dpcm(index, size, name)
        self.project.samples[index] = myDpcm
        self.last_dpcm_index = index

    def handle_dpcm_data(self, line: str):
        # DPCM : [data]
        try:
            nums = list(map(lambda x: int(x, 16), line.split(":")[1].strip().split()))
            self.project.samples[self.last_dpcm_index].data.extend(nums)
        except Exception as e:
            print("[E] {} Line: {}".format(e, line))
            return

    def handle_groove(self, line: str):
        # GROOVE [index] [sizeof] : [groove_sequence]
        try:
            index, size = list(map(int, line.strip().split()[1:3]))
            sequence = list(map(int, line.split(":")[1].strip().split()))
            myGroove = Groove(index, size, sequence)
            self.project.grooves[index] = myGroove

        except Exception as e:
            print("[E] {} Line: {}".format(e, line))
            return

    def handle_usegroove(self, line: str):
        # USEGROOVE : []
        try:
            self.project.usegroove = list(map(int, line.split(":")[1].strip().split()))
        except Exception as e:
            print("[E] {} Line: {}".format(e, line))
            exit(1)

    def handle_inst_2a03(self, line: str):
        # INST2A03 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_dut] "[name]"
        match = re.match(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return 
    
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
        # INSTN163 [index] [seq_vol] [seq_arp] [seq_pit] [seq_hpi] [seq_wav] [w_size] [w_pos] [w_count] "[name]"
        match = re.match(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s*\"(.*)\"$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return 
    
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
        match = re.match(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s+([0-9A-F]{2})\s*\"(.*)\"$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return
        
        tag = match.group(1)
        index, patch = list(map(int, match.group(2, 3)))
        r0, r1, r2, r3, r4, r5, r6, r7 = list(map(lambda x: int(x, 16), match.group(4, 5, 6, 7, 8, 9, 10, 11)))
        name = match.group(12)
        registers = [r0, r1, r2, r3, r4, r5, r6, r7]
        myInst = InstVRC7(tag, index, patch, registers, name)
        
        self.project.instruments[index] = myInst

    def handle_inst_fds(self, line: str):
        # INSTFDS [index] [mod_enable] [mod_speed] [mod_depth] [mod_delay] "[name]"
        match = re.match(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return
        tag = match.group(1)
        index, mod_enable, mod_speed, mod_depth, mod_delay = list(map(int, match.group(2, 3, 4, 5, 6)))
        name = match.group(7)

        myInst = InstFDS(tag, index, mod_enable, mod_speed, mod_depth, mod_delay, name)

        self.project.instruments[index] = myInst

    def handle_key_dpcm(self, line: str):
        # KEYDPCM [inst] [octave] [note] [sample] [pitch] [loop] [loop_point] [delta]
        match = re.match(r'^\s*(\w+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)\s+(\-?\d+)$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return

        inst, octave, note, sample, pitch, loop, loop_point, delta = list(map(
            int, match.group(2, 3, 4, 5, 6, 7, 8, 9)))

        myKeyDpcm = KeyDpcm(inst, octave, note, sample, pitch, loop, loop_point, delta)

        instLookup = self.project.instruments.get(inst)
        if not instLookup:
            print("[W] Could not load KeyDpcm. Failed to find Inst index {}".format(inst))
            return
        if not hasattr(instLookup, "sample_keys"):
            print("[W] Could not load KeyDpcm. Inst does not have attr \'sample_keys\'")
            return
        midi_pitch = octave * 12 + note
        instLookup.sample_keys[midi_pitch] = myKeyDpcm
        #print("[DEBUG] Loaded KeyDPCM!")

    def handle_fds_wave(self, line: str):
        # FDSWAVE [inst] : [data]
        try:
            inst = int(line.strip().split()[1])
            lst = list(map(int, line.split(":")[1].strip().split()))
            instLookup = self.project.instruments.get(inst, None)            
            if not instLookup:
                print("[E] Could not find inst index. {}".format(line))
                return
            if not hasattr(instLookup, "fds_wave"):
                print("[E] Couldn't add fds_wave to non-fds inst {}".format(line))
                return
            instLookup.fds_wave = lst
        except Exception as e:
            print("[E] {} Line: {}".format(e, line))
            return       

    def handle_fds_mod(self, line: str):
        # FDSMOD [inst] : [data]
        try:
            inst = int(line.strip().split()[1])
            lst = list(map(int, line.split(":")[1].strip().split()))
            instLookup = self.project.instruments.get(inst, None)            
            if not instLookup:
                print("[E] Could not find inst index. {}".format(line))
                return
            if not hasattr(instLookup, "fds_mod"):
                print("[E] Couldn't add fds_mod to non-fds inst {}".format(line))
                return
            instLookup.fds_mod = lst
        except Exception as e:
            print("[E] {} Line: {}".format(e, line))
            return       

    def handle_fds_macro(self, line: str):
        # FDSMACRO [inst] [type] [loop] [release] [setting] : [macro]
        match = re.match(r'^\s*(\w+)\s+(\d+)\s+([012])\s+(\-?\d+)\s+(\-?\d+)\s+(\d+)\s*\:\s*(.*)$', line)
        if not match:
            print("[W] Could not match line: {}".format(line))
            return  
        
        tag = match.group(1)
        _inst, _type, _loop, _release, _setting = list(map(
            int, match.group(2, 3, 4, 5, 6)))
        
        instLookup = self.project.instruments.get(_inst, None)
        if not instLookup:
            print("[E] Could not find inst index. {}".format(line))

        _sequence = list(map(int, line.split(":")[1].strip().split()))
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
            print("[E] Invalid macro type. {}".format(line))
            return

        setattr(instLookup, target, myMacro)
        self.project.macros[label] = myMacro
        #print("[INFO] Added FDS MACRO!")

    def handle_n163_wave(self, line: str):
        # N163WAVE [inst] [wave] : [data]
        inst_index, wave_index = list(map(int, line.strip().split()[1:3]))
        lst = list(map(int, line.split(":")[1].strip().split()))

        instLookup = self.project.instruments.get(inst_index, None)
        if not instLookup:
            print("[E] Failed to find N163 instrument: index {} : {}".format(
                inst_index, line))
            return
        
        if not hasattr(instLookup, "n163_waves"):
            print("[E] Cannot add n163_wave to non-n163 instrument. {}".format(line))
            return

        instLookup.n163_waves[wave_index] = lst
        print("Added N163 wave! {}".format(lst))

    def handle_track(self, line: str):
        match = re.match(r'^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\"(.*)\"$', line)
        if not match:
            print("[E] Could not match line: {}".format(line))
            return
        
        tag = match.group(1)
        num_rows, speed, tempo = list(map(int, match.group(2, 3, 4)))
        name = match.group(5)

        myTrack = Track()
        myTrack.num_rows = num_rows
        myTrack.speed = speed
        myTrack.tempo = tempo
        myTrack.name = name
         
        idx = myTrack.index
        self.project.tracks[idx] = myTrack
        print("A track was created. {}".format(myTrack))


    # TODO
    def handle_columns(self, line: str):
        pass

    # TODO
    def handle_order(self, line: str):
        pass

    # TODO
    def handle_pattern(self, line: str):
        pass

    # TODO
    def handle_row(self, line: str):
        pass

#*******************************************************************************

    def handle_line(self, line: str):
        if not line or line.startswith("#"):
            return

        first_word = line.split()[0]
        func = self.command_map.get(first_word, None)
        if func:
            func(line)
        else:
            # TODO
            # print(f"[W] Unknown line: {line}")
            pass

    def read_file(self, infile: str, project: Any):
        self.project = project

        with open(infile, 'r') as file:
            for line in file:
                self.handle_line(line.strip())

#    def handle_groove(self, line: str): pass
#    def handle_usegroove(self, line: str): pass

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

