# Famitracker Tools

A suite of utilities designed to enhance and streamline composition in [Famitracker](http://famitracker.com/), the premier tracker for authentic NES-style chiptune music.

As a dedicated Famitracker user, I've often run into the limitations of manual editing and repetitive tasks. This project addresses that by providing tools that operate directly on Famitracker’s text export format — enabling more powerful manipulation, automation, and creative control.

---

## 🚀 Project Goals

This project aims to:
- Accelerate the NES-style composition process
- Provide a clean, extensible codebase as a technical showcase
- Serve as a launchpad for experimental tooling in tracker-based music

---

## Technical Highlights

This project demonstrates:
- **Modular architecture** with a professional code layout and `Makefile`-based build system
- Use of **Design Patterns**: *Facade*, *Strategy*, *Abstract Factory*
- **Advanced Regex** techniques for parsing and tokenization
- Robust **file I/O** operations for reading/writing large text-based music formats
- Integrated **logging** for traceability and debugging
- **Unit tests** to ensure correctness and prevent regressions

---

## Tools Overview

### 1. **Famitracker Text Export Parser** *(WIP)*  
Parses `.txt` exports from Famitracker into structured, navigable data.  
Encapsulates pattern data, instruments, macros, and control codes into a usable intermediate format.

### 2. **Famitracker to MIDI Converter** *(WIP)*  
Translates parsed Famitracker data into a MIDI sequence using a custom `MidiWriter` engine.  
Allows playback and interoperability with modern DAWs or synthesis tools.

### 3. **Auto-Inject Vibrato Tool** *(WIP)*  
Automatically adds vibrato macros to long notes across patterns.  
A massive time-saver — no more manually entering vibrato hundreds of times.

---

## 🛠️ Build Instructions

```bash
make
