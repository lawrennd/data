#!/usr/bin/env python

import os
import yaml


def write(macros, filename, dir, **kwargs):
    """Reads notation from a latex include file."""
    ext = os.path.splitext(filename)[1]
    if ext == '.tex':
        write_tex(macros, filename, dir, **kwargs)
    else:
        write_yaml(macros, filename, dir)

def write_yaml(macros, filename, dir):
    """Writes notation to a yaml file."""
    with open(os.path.join(dir, filename),  'w') as outfile:
        outfile.write(yaml.dump(macros, default_flow_style=False))

def write_tex(macros, filename, dir, style='newcommand'):
    """Writes notation to a latex format."""
    out = '% Macro listing created by write_tex\n'
    out += '% from source file {filename}\n'.format(filename=filename)
    out += '% in style {style}\n\n'.format(style=style)
    out += '% WARNING: you may edit this file but your edits are likely to be overwritten.\n\n'
    out += '% Try finding the source file from which it was generated.\n\n\n'.format(style=style)
    for key, val in macros.items():
        if style=='newcommand':
            if 'args' in val and val['args']>0:
                out += "\\newcommand{\\" + key + r'}[' + str(val['args']) + ']{' + val['latex'] + '}'
            else:
                out += "\\newcommand{\\" + key + r'}{' + val['latex'] + '}'

        elif style == 'global':
            if 'args' in val and val['args']>0:
                arg_string = ''
                for i in range(val['args']):
                    arg_string += '#' + str(i+1)
                out += '\\global\\long\\def\\{key}{arg_string}{{{macro}}}'.format(key=key, macro=val['latex'], arg_string=arg_string)
            else:
                out += '\\global\\long\\def\\{key}{{{macro}}}'.format(key=key, macro=val['latex'])
        if 'description' in val:
            out += ' % ' + val['description']
        out += '\n'
    open(os.path.join(dir,filename), 'w').write(out)

def read(filename, dir):
    """Reads notation from a latex include file."""
    ext = os.path.splitext(filename)[1]
    if ext == '.tex':
        return read_tex(filename, dir)
    else:
        return read_yaml(filename, dir)

def read_tex(filename, dir):
    """Reads notation from a latex macro file."""
    text = open(os.path.join(dir, filename), 'r').read()

    match_macro = re.compile(r"""\\global\\long\\def\\(\w+)\{(.*)\}\s*#( """)
    macro_matches = match_macro.findall(text)
    macros = {}
    for m in macro_matches:
        macros[m[0]] = {}
        macros[m[0]]['latex'] = m[1]

    match_macro = re.compile(r"""\\newcommand\{(\w+)\}\{(.*)\}""")
    text = open(os.path.join(dir, filename), 'r').read()
    macro_matches = match_macro.findall(text)
    macros = {}
    for m in macro_matches:
        macros[m[0]] = {}
        macros[m[0]]['latex'] = m[1]


    match_macro = re.compile(r"""\\global\\long\\def\\(\w+)#[^\{]*([0-9])\{(.*)\}""")
    macro_matches = match_macro.findall(text)
    for m in macro_matches:
        macros[m[0]] = {}
        macros[m[0]]['latex'] = m[2]
        macros[m[0]]['args'] = int(m[1])

    match_macro = re.compile(r"""\\newcommand\{(\w+)\}\[(0-9+)]\{(.*)\}""")
    text = open(os.path.join(dir, filename), 'r').read()
    macro_matches = match_macro.findall(text)
    macros = {}
    for m in macro_matches:
        macros[m[0]] = {}
        macros[m[0]]['args'] = int(m[1])
        macros[m[0]]['latex'] = m[2]

    return macros

def read_yaml(filename, dir):
    """Read macros from a yaml file."""
    text = open(os.path.join(dir, filename), 'r').read()
    return yaml.load(text)
