#!/usr/bin/env python

import macros

latex_macros = macros.read('notation_def.yml', dir='.')
macros.write(latex_macros, filename='notation_def.tex', dir='/Users/neil/SheffieldML/publications/tex_inputs/', style='newcommand')
macros.write(latex_macros, filename='notationDef.tex', dir='/Users/neil/SheffieldML/publications/tex_inputs/', style='global')
