# Famitracker Tools (C++ Version)

## 🛠 Build Instructions
### 🐧 Linux (Tested on Ubuntu 24.04)

1. Ensure you have `g++` with C++17 support installed:
```bash
sudo apt update
sudo apt install build-essential
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

## ▶️  Usage
### Linux
```bash
./bin/main.exe <input_file.txt>
```

### Windows
```bash
bin\main.exe <input_file.txt>
```

