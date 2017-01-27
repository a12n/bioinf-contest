#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

s = stdin.readline().strip().upper()
# debug(s)

comp = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}

def matchbonds(s):
    stack = []
    for c in s:
        if stack and stack[-1] == comp[c]:
            stack.pop()
        else:
            stack.append(c)
    return stack

s = matchbonds(s)
# debug('stack %s', s)
if not s:
    print('perfect')
elif len(s) % 2 == 1:
    del(s[len(s) // 2])
    s = matchbonds(s)
    # debug('stack %s', s)
    if not s:
        print('almost perfect')
    else:
        print('imperfect')
else:
    print('imperfect')
