#!/usr/bin/env python3

import itertools
import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def left(s, k):
    return s[0:k]

def right(s, k):
    return s[-k:]

# TODO: memoize
def overlaplen(a, b):
    ans = 0
    for i in range(1, min(len(a), len(b))):
        if right(a, i) == left(b, i):
            ans = i
    return ans

def overlap(s, t, l=None):
    n = len(s)
    if not l:
        l = overlaplen(s, t)
    return left(s, n - l) + t

def kmers(s, k):
    for i in range(len(s) - k + 1):
        yield s[i:(i + k)]

def reconstruct():
    n, k = map(int, stdin.readline().split())
    origkmers = set((stdin.readline().rstrip() for _ in range(n)))
    assert all(len(kmer) == k for kmer in origkmers)
    # TODO
    print(0)

if __name__ == '__main__':
    try:
        while True:
            reconstruct()
    except ValueError:
        pass
