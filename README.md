# GemIO

**G**raphically **e**liminate **m**icrographs **I**nhibiting **O**perations

>*Finding gems in your data because sometimes your micrographs are a diamond in the rough.*




## Overview

This program can be used to remove movies, micrographs (with associated relion generated files) and jpeg files following motion correction.

## Requirements
### cleanup.py file (Recommended)
* python3.6
* PyQt5 (5.9.2) module - install using "pip3.6 install PyQt5" after installing python3.6

### Precompiled binaries (only available for Windows and Linux)
* None

Note:
- Only use if cannot install python3.6 or the PyQt5 module. Otherwise, the python file is more reliable and up to date.

## Usage
### Linux
This program is intended to run on Linux with full functionality. This program uses JPEG files to view and delete micrographs. Log files are generated after each run and can be imported (from Linux or Windows sessions) to continue previous sessions.
* Use e2proc2d.py to generate the JPEG files from the MRC files if they do not already exist (can be done through the GUI).

Notes:
- Only input TIF directory if you wish to remove TIF files
- This program assumes the use of .tif, .mrc, and .jpeg file extensions for movies, corrected micrographs and jpeg files, respectively.

### Windows and Mac
This program can be run on Windows and Mac to generate the log files ONLY. This file can be imported into the program when it is run on a Linux machine with all the data.
* To generate the log file on Windows and Mac, select all micrographs you wish to remove and close the program when you are done.
