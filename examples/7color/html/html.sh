#!/bin/bash

CWD=`pwd`
filename=$1

firefox --headless --screenshot --window-size=600,448 https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdc02EyCEZ5LLvjO51V_1FXXjjTvDxyagqJyqqbwyr295uxu5Hlluy_gWrkLLSMRyQStE&usqp=CAU
../image.py screenshot.png
