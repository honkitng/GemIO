# GemIO

**G**raphically **e**liminate **m**icrographs **I**nhibiting **O**perations

>*Finding gems in your data because sometimes your micrographs are a diamond in the rough.*

## Overview

GemIO can be used to remove movies, micrographs (with associated relion generated files) and jpeg files following motion correction.

## Requirements
### GemIO.py file (Recommended)
* python3.8
* PIL module - install using "pip3.8 install pillow"
* flask module - install using "pip3.8 install flask"

## Usage
### Linux
GemIO uses JPEG files to select micrographs and move those selected micrograph to dedicated trash directories. Star files can also be edited and imported into RELION which do not contain any removed micrographs.
* Use e2proc2d.py to generate the JPEG files from the motion corrected MRC files if they do not already exist.

Notes:
- TIF directory is required as an input, but the tiffs are not required to be in the directory
- Only input star files if you wish to remove selected micrographs from the star files
