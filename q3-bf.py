#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def readseq():
    return stdin.readline().strip().upper()

s = readseq()
reads = tuple([readseq() for i in range(int(stdin.readline()))])
# debug('s %s', s)
debug('len(s) %d', len(s))
debug('%d reads', len(reads))
# debug('reads %s', reads)

# nstates = 2**len(reads) - 1
# states = ([reads[i] if (k >> i) & 1 != 0 else None for i in range(len(reads))] for k in range(nstates, 0, -1))
# debug('nstates = %s', nstates)
# debug('states = %s', states)
# for s in states:
#     debug(s)

def findsubseq(s, t, start=None):
    ans = []
    p = start
    for c in t:
        q = s.find(c, p)
        if q == -1:
            return None
        ans.append(q)
        p = q + 1
    return ans

def issubseq(s, t, start=None):
    p = start
    for c in t:
        q = s.find(c, p)
        if q == -1:
            return False
        p = q + 1
    return True

def findallsubseq(s, t):
    start = 0
    while True:
        p = findsubseq(s, t, start)
        if p == None:
            break
        yield p
        start = p[0] + 1

def left(s, k):
    return s[0:k]

def right(s, k):
    return s[-k:]

def comparsestr(s, t, i, j, l):
    for k in range(l):
        if s[i] != t[j]:
            return False
    return True

def overlap(a, b):
    ans = 0
    for i in range(1, min(len(a), len(b))):
        if right(a, i) == left(b, i):
            ans = i
    return ans

def combine(s, t, l=None):
    # debug('combine: "%s" "%s" %s', s, t, l)
    n = len(s)
    if not l:
        l = overlap(s, t)
    assert l >= 0 and l <= n
    return left(s, n - l) + t

def longestoverlap(seqs, skip=set()):
    # debug('longestoverlap seqs %s', seqs)
    debug('longestoverlap %d seqs', len(seqs))
    global s
    ans = [-1, -1, -1, None]
    for i in range(len(seqs)):
        debug('i %s, ans %s', i, ans[0:3])
        for j in range(len(seqs)):
            if i == j or i in skip or j in skip:
                continue
            l = overlap(seqs[i], seqs[j])
            if l > ans[2]:
                t = combine(seqs[i], seqs[j], l)
                if issubseq(s, t):
                    ans[0] = i
                    ans[1] = j
                    ans[2] = l
                    ans[3] = t
    return ans

def run(seqs):
    seqs = list(seqs)
    while True:
        i, j, l, t = longestoverlap(seqs)
        # debug('i %s, j %s, l %s, t %s', i, j, l, t)
        if l != -1:
            i, j = min(i, j), max(i, j)
            seqs[i] = t
            del(seqs[j])
        else:
            break
    return max(seqs, key=len)

t = run(reads)
print(t)
for i in range(len(reads)):
    j = t.find(reads[i])
    if j != -1:
        print(j + 1)
    else:
        print(-1)
