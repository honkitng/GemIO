# RELION cleaup

This program can be used to remove movies, micrographs and jpeg files following motion correction.
This program uses JPEG files to view and delete micrographs; use e2proc2d.py (i.e. e2proc2d.py *.mrc jpeg/@.jpeg --apix={pixel size} --process filter.lowpass.gauss:cutoff_freq=20 --meanshrink=4) to low pass filter and generate the JPEG files from the MRC files if they do not already exist.

## Requirements
* python3.6
* PyQt5 (5.9.2) module - install using "pip3.6 install PyQt5" after installing python3.6


## Usage
This script is intended to run on a Linux machine with full functionality.
* Only input TIF directory if you wish to remove TIF files
* This program assumes the use of .tif, .mrc, and .jpeg file extensions for movies, corrected micrographs and jpeg files, respectively.

This script can be run on a Windows machine to generate the log files ONLY. This file can be imported into the program when it is run on a Linux machine with all the data.
* To generate the log file on a Windows machine, simply select all micrographs you wish to remove and close the program when you are done.
