#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def comp(s):
    # FIXME: maketrans once
    return s.translate(str.maketrans('ACGU', 'UGCA'))

def findall(s, sub, start=0):
    while True:
        start = s.find(sub, start)
        if start != -1:
            yield start
            start += len(sub)
        else:
            break

s = stdin.readline().strip()
debug(s)

basepair = dict()
for i in range(len(s) - 2):
    e = set(findall(s, comp(s[i]), i + 2))
    if e:
        basepair[i] = e
debug(basepair)

# TODO
