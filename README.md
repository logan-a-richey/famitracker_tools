# Famitracker Tools
A suite of utilities designed to enhance and streamline music composition in [Famitracker](http://famitracker.com/), the standard tracker for authentic NES-style chiptune music.
As a dedicated Famitracker user, I have often run into the limitations of manual editing and repetitive tasks. 
This project provides tools that operate directly on Famitracker's text export format, enabling more powerful manipulation, automation, and creative control.

---

## 🚀 Project Objectives
* Encapsulate Famitracker’s text export data in a structured `Project` class.
* Accelerate the NES-style composition process through programmatic editing tools.
* Provide a clean, extensible codebase suitable for showcasing software engineering skills and for building additional features.

## Roadmap
> [!NOTE]
> This is a work in progress. Features incomplete, active development ongoing.

<br>

Python Version:
- [x] Reader
- [x] TrackFormatter
- [ ] TextToMidi
- [ ] MidiToText
- [ ] AutoVibrato
- [ ] AutoDrums
- [ ] Add additional Logging
- [ ] Add additional Error Handling
- [ ] Add Unit Testing Regex pattern 

<br>

C++ Version:
- [ ] Refactor coming soon. I decided that the Gang-Of-Four approach may be too much for a simple text parser. Considering a map of lambda functions instead.

---

## 🔧 Technical Highlights
This project demonstrates:
* Modular and maintable code, designed to be easy to extend new features.
* Advanced regex parsing with Python's `re` module and C++'s `#include regex>`.
* Input and output file handling
* Complex list and dictionary data structures / use of `std::vector`, `std::map`
* Focus on Separation of Concerns and proper use of design patterns.
* Type-hinting and memory management in mind, using Python's `typing` module and C++ smart pointers / RAII and move semantics.
* Custom `MidiWriter` class in both Python and C++, imported as a git submodule.
* Exception handling throughout
* Logging advanced features
<br>
* Simple CLI argparsing (coming soon)
* UnitTesting (coming soon)

---

## 🧰 Tools Overview
| Tool Name         | Status     | Description                                                          | Key Usage / Notes                                                               |
| ----------------- | ---------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `Reader`          | ✅ Complete | Loads `.txt` export into structured `Project` object                 | Foundation for all other tools                                                  |
| `TrackFormatter`  | ✅ Complete | Returns unscrambled version of scrambled Famitracker lines           | Improves readability and further processing                                     |
| `UncompressScore` | 🔄 In Dev  | Flattens pattern data into a linear score view                       | Useful for debugging and transformation prep                                    |
| `AutoVibrato`     | 🔜 Planned | Replaces 4XY vibrato effects with uniform vibrato macros             | Automates vibrato styling with `<steps> <setting>` configuration                |
| `AutoDrums`       | 🔜 Planned | Adds triangle wave drum macros where drum-named instruments are used | Automates triangle-based percussion juggling, preserves DPCM purity             |
| `MidiToText`      | 🔄 In Dev  | Converts MIDI to Famitracker text format                             | Maps MIDI tracks to FT channels, applies arpeggios, supports expansions via CLI |

---

### ✅ `Reader`
**Status**: Complete
Parses Famitracker `.txt` export files and loads them into a structured `Project` class. 
Acts as the foundation for all subsequent tools by converting the flat text into manipulable data.

### ✅ `TrackFormatter`
**Status**: Complete
Provides utilities for working with scrambled/obfuscated track data. 
Main method returns a list of clean, unscrambled lines to improve readability and facilitate analysis or transformation.

### 🔄 `UncompressScore`
**Status**: In Development
Exports the full pattern order as a linear, human-readable score. Example output:
```plaintext
ORDER 00 : 00 00 00
ORDER 01 : 01 01 01
ORDER 02 : 02 02 02
```
Useful for debugging or pre-processing before applying further transformations like automation or MIDI conversion.

### 🔜 `AutoVibrato`
**Status**: Planned
Replaces all native 4XY vibrato effects in sustained notes with a custom vibrato macro for consistency.
Usage:
* Specify `number_of_steps: int` and `vib_setting: str`.
* Tool auto-injects vibrato macros across all sustained notes.

Benefits:
* Ensures uniform vibrato styling across patterns.
* Removes manual vibrato placement tedium.

### 🔜 `AutoDrums`
**Status**: Planned
Injects triangle-wave-based drum macros alongside basslines to mimic realistic percussion.

Behavior:
* Detects instruments with names like `"kick"`, `"snare"`, `"tom1"`, etc.
* Applies triangle sweep macros at matching note locations.

Context:
* Especially useful for purist NES composers who avoid DPCM and prefer triangle/noise for drums.
* Automates the time-consuming triangle juggling technique.

### 🔜 `MidiToText`
**Status**: In Development
Converts a standard MIDI file into a Famitracker `.txt` file that can be imported directly into the tracker.
Planned Features:
* Assign one or more MIDI tracks to Famitracker channels.
* Specify expansion chips via flags (`--vrc6`, `--vrc7`, etc.).
* Support for arpeggio effects when multiple sustained notes overlap in a single column.
* Optional: Apply volume macros to enhance arpeggiated textures.

Usage Tips:
* Best results when exporting MIDI from a DAW with clean quantization and clear track separation.
* A future GUI interface may make track-channel mapping easier for non-technical users.

## License
MIT Public License


