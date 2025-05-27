# Famitracker Tools

A suite of utilities designed to enhance and streamline music composition in [Famitracker](http://famitracker.com/), the standard tracker for authentic NES-style chiptune music.
As a dedicated Famitracker user, I have often run into the limitations of manual editing and repetitive tasks. 
This project provides tools that operate directly on Famitracker's text export format, enabling more powerful manipulation, automation, and creative control.

---

## 🚀 Project Objectives

* Encapsulate Famitracker’s text export data in a structured `Project` class.
* Accelerate the NES-style composition process through programmatic editing tools.
* Provide a clean, extensible codebase suitable for showcasing software engineering skills and for building additional features.

---

## 🔧 Technical Highlights

This project demonstrates:

* **Modular architecture**, with a professional directory structure and `Makefile`-based build system.
* Implementation of **design patterns** including *Facade*, *Strategy*, and *Abstract Factory* for maintainable and scalable code.
* Use of **advanced regular expressions** for precise parsing and tokenization.
* Robust **file I/O** for efficient handling of large, text-based song data.
* Integrated **logging** for transparency and debugging.
* A growing suite of **unit tests** to ensure stability and correctness as development progresses.

---

## 🧰 Tools Overview

### 1. **Famitracker Text Export Parser** *(In Progress)*

Parses `.txt` exports from Famitracker into a structured, navigable intermediate format.
Captures pattern data, instruments, macros, and control codes.

### 2. **Famitracker to MIDI Converter** *(In Progress)*

Converts Famitracker project data into a MIDI sequence using a custom `MidiWriter` engine.
Enables playback in modern DAWs and facilitates further production and synthesis.

### 3. **Auto-Inject Vibrato Tool** *(In Progress)*

Automatically inserts vibrato macros into sustained notes across patterns.
Eliminates the need for tedious, manual vibrato placement.

---

## 🛠 Build Instructions

### 🐧 Linux (Tested on Ubuntu 24.04)

Ensure you have `g++` with C++17 support installed:

```bash
sudo apt update
sudo apt install build-essential
```

Then build the project with:

```bash
make
```

### 🪟 Windows (Tested with MinGW + MSYS2)

#### Prerequisites

* Install [MSYS2](https://www.msys2.org/)
* Open an MSYS2 shell and install the necessary tools:

```bash
pacman -Syu
pacman -S mingw-w64-x86_64-gcc make
```

#### Building

From a **MinGW64 shell** (not the default MSYS shell):

```bash
make
```

This will produce the output binary in the `bin/` directory.

---

## ▶️  Usage

### Linux

```bash
./bin/main.exe <input_file.txt>
```

### Windows

```bash
bin\main.exe <input_file.txt>
```

(Ensure `main.exe` and your input `.txt` file are in the correct working directory.)

