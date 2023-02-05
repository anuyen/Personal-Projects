"""
Load text file as a list

Arguments:
    -text file name (+ path if needed)

Exceptions:
    -IOError if filename not found

Returns:
    -words from dictionary text file as a list in lowercase

Requires:
    -import sys
"""

import sys

def load(file):
    """Open text file and return a list of lowercase strings"""
    try:
        with open(file,'r',encoding='utf8') as in_file:
            loaded_txt = in_file.read().strip().split('\n')
            loaded_txt = [x.lower() for x in loaded_txt]
            return loaded_txt
    except IOError as error:
        print(f"{error}\nError opening {file}\nTerminating program.",file=sys.stderr)
        sys.exit(1)