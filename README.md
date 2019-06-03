# Second Task

### Steps:
* First, the raw GCode file is normalized, i.e. comments are removed along with extraneous spaces, etc. This is accomplished by `normalize.py`
* The next step is parsing this normalized Gcode. The normalized GCode is temporarily held in `tmp.txt`. So far, only `G1`, `G28`, `M0`, `M112` and `M117` are parseable.

### To run:
* cd parser
* python3 parser.py tester.txt

Build failing

I feel like I should mention that I did not have sufficient time to figure out the problem owing to a medical emergency. Additionally, I wanted to make a parser capable of parsing all GCode syntax but have limited myself to the commands in the doc due to the aforementioned reason. However, I believe the design is correct.