#!/usr/bin/env python3

import itertools
import logging
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

kmers_set_cache = dict()
def kmers_set(s, k):
    key = (s, k)
    if not key in kmers_set_cache:
        kmers_set_cache[key] = set(kmers(s, k))
    return kmers_set_cache[key]

def reconstruct():
    n, k = map(int, stdin.readline().split())
    origkmers = set((stdin.readline().rstrip() for _ in range(n)))
    assert all(len(kmer) == k for kmer in origkmers)
    state = list(origkmers)
    def mergekmers():
        for i in range(len(state)):
            for j in range(len(state)):
                if i == j:
                    continue
                # TODO: try different overlap lenghts
                s = overlap(state[i], state[j])
                skmers = kmers_set(s, k)
                if not skmers.issubset(origkmers):
                    continue
                if any(not skmers.isdisjoint(kmers_set(state[m], k)) \
                       for m in range(len(state)) if m != i and m != j):
                    continue
                return (s, i, j)
        return None
    # TODO
    stop = False
    while len(state) > 1 and not stop:
        res = mergekmers()
        if res:
            s, i, j = res
            del(state[max(i, j)])
            del(state[min(i, j)])
            state.insert(0, s)
        else:
            stop = True
    print(len(state))
    print('\n'.join(state))

if __name__ == '__main__':
    try:
        while True:
            reconstruct()
    except ValueError:
        pass
