#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The .XCompose file requires us to specify the names of the keys we want to
press. That's easy enough for letters and numbers, but some symbols need to be
specified by their name, such as `colon` or `overline` or whatever.

This script parses the linux keysymdef.h given to it, finds all possible keys
that could be pressed based on their XK_ definitions, gets the unicode
representation of them based on the U+nnnn representation in the comment,
and generates a list of symbol→keyname mappins that can be used by the main
NXCompose script.
"""

import sys
import datetime
import re

def read_keysyms(fname):
    """
    Get all keysyms from the given file which have a representation
    specified as a unicode codepoint.
    """
    # Map of user key representations to XK_ names.
    XComposeNames = dict()
    xk_re = re.compile('^#define\sXK_(\S+)\s.*/\*\sU\+([0-9A-F]+)\s')
    with open(fname, "rt") as f:
        for line in f:
            m = xk_re.search(line)
            if not m: continue
            k = chr(int(m.group(2), 16))
            v = m.group(1)
            XComposeNames[k] = v
    return XComposeNames

def write_keysyms(syms, fname="keysyms.py"):
    """
    Update the python file which specifies keysyms and their
    mappings.
    """
    with open(fname, "wt") as f:
        f.write("""\
# -*- coding: utf-8 -*-

\"\"\"
This file is automatically generated by the `regen_keysyms.py` script
in this directory. Editing is not recommended.

Last generated date: {thisdate}
\"\"\"

XComposeNames = {lbrace}
""".format(thisdate=datetime.date.today().strftime('%Y-%m-%d'), lbrace='{'))
        for k in sorted(syms.keys()):
            v = syms[k]
            if k in ('"', '\\'):
                k = '\\'+k
            f.write('\tu"{k}": "{v}",\n'.format(k=k, v=v))
        f.write("}\n")

if __name__ == "__main__":
    infile = "/usr/include/X11/keysymdef.h"
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    syms = read_keysyms(infile)
    write_keysyms(syms)

#
# Editor modelines - http://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# End:
#
# vi:set shiftwidth=4 tabstop=4 expandtab:
# indentSize=4:tabSize=4:noTabs=true:
