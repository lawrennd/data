#!/usr/bin/env python

import re
import os
import yaml

file_name = 'definitions'
text = open(file_name + '.yml', 'r')
macros = yaml.load(text)
out = ''
for key, val in macros.items():
    if int(val['args']) == 0:
        out += "\\newcommand{\\" + key + r'}{' + val['macro'] + '}\n'
    elif int(val['args']) > 0:
        out += "\\newcommand{\\" + key + r'}[' + str(val['args']) + ']{' + val['macro'] + '}\n'

print(out)
