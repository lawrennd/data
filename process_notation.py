#!/usr/bin/env python

import re
import os
import yaml
file_name = 'notation_def'
match_macro = re.compile(r"""\\global\\long\\def\\(\w+)\{(.*)\}""")
text = open(file_name + '.tex', 'r').read()
macro_matches = match_macro.findall(text)
notation_def = {}
for m in macro_matches:
    notation_def[m[0]] = {}
    notation_def[m[0]]['macro'] = m[1]
    notation_def[m[0]]['args'] = 0
    

match_macro = re.compile(r"""\\global\\long\\def\\(\w+)#[^\{]*([0-9])\{(.*)\}""")
macro_matches = match_macro.findall(text)
for m in macro_matches:
    notation_def[m[0]] = {}
    notation_def[m[0]]['macro'] = m[2]
    notation_def[m[0]]['args'] = int(m[1])
    
with open(file_name + '.yml', 'w') as outfile:
    outfile.write(yaml.dump(notation_def,default_flow_style=False))

