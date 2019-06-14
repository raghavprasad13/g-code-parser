# G Code Parser

### Steps:
* First, the raw GCode file is normalized, i.e. comments are removed along with extraneous spaces, etc. This is accomplished by `normalize.py`
* The next step is parsing this normalized Gcode. The normalized GCode is temporarily held in `tmp.txt`. So far, only `G1`, `G28`, `M0`, `M112` and `M117` are parseable.

### To run:
* cd parser
* python3 parser.py tester.txt

[![Generic badge](https://img.shields.io/badge/<build>-<failing>-<red>.svg)]