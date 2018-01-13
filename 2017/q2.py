#!/usr/bin/env python3

from sys import stdin

comp = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}

def matchbonds(s):
    stack = []
    for c in s:
        if stack and stack[-1] == comp[c]:
            stack.pop()
        else:
            stack.append(c)
    return stack

s = stdin.readline().strip().upper()
s = matchbonds(s)
if not s:
    print('perfect')
elif len(s) % 2 == 1:
    del(s[len(s) // 2])
    s = matchbonds(s)
    if not s:
        print('almost perfect')
    else:
        print('imperfect')
else:
    print('imperfect')
