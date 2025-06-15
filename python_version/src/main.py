#!/usr/bin/env python3
# main.py

'''
# TODO ideal usage:
./app --txt2mid <input.txt> <output_path>
./app --flatten <input.txt> <output_path>
./app --vibrato <input.txt> <output_path>
./app --auto_tri_drums <input.txt> <output_path>
./app --mid2txt <input.mid> <output_path>
'''

import sys
sys.dont_write_bytecode = True 

from typing import List

from core.color_logger import ColorLogger
logger = ColorLogger("Main").get()
logger.setLevel(ColorLogger.INFO)

from data.project import Project

from utils.reader import Reader
from utils.track_formatter import TrackFormatter
from utils.midi_exporter import MidiExporter

#*******************************************************************************
# main program
def main():
    try:
        infile = sys.argv[1]
    except Exception as e:
        logger.error("Could not open file. Usage: ./main <input.txt>")
        sys.exit(1)

    project = Project()
    
    reader = Reader()
    reader.read_file(infile, project)
    
    track_formatter = TrackFormatter(project) 
    exporter = MidiExporter()

    for track_index, track in project.tracks.items():
        lines: List[str] = track_formatter.unscramble(track)
        exporter.export_track(track, lines, "output_name.mid")
        logger.info("Created file output.mid")

    # logger.debug(proj)
    
    logger.info("Program ran successfully.")


if __name__ == "__main__":
    main()

