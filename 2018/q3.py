#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin
from time import time

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

def hamm_dist(s, t):
    assert(len(s) == len(t))
    return sum(si != ti for si, ti in zip(s, t))

# def edit_dist(s, t, l=None):
#     n = len(s)
#     m = len(t)
#     d = [[0] * (m + 1) for _ in range(2)]
#     for j in range(1, m + 1):
#         d[0][j] = j
#     for i in range(1, n + 1):
#         d[i % 2][0] = i
#         for j in range(1, m + 1):
#             cost = 0 if s[i - 1] == t[j - 1] else 1
#             delt = d[(i - 1) % 2][j] + 1
#             ins = d[i % 2][j - 1] + 1
#             subst = d[(i - 1) % 2][j - 1] + cost
#             dist = min(delt, ins, subst)
#             if l and dist > l:
#                 raise RuntimeError
#             d[i % 2][j] = dist
#     return d[n % 2][m]

def find_repeats_hamm(s, t_max):
    ans = []
    for k in range(1, len(s) // 2):
        debug("k = %d", k)
        for i in range(0, len(s) - k * 2 + 1):
            d = hamm_dist(s[i:i + k], s[i + k:i + 2 * k])
            if d <= (0.1 * k):
                ans.append((i, k, k))
                break
        if time() >= t_max:
            break
    return ans

def tandem_repeat(s):
    return max(find_repeats_hamm(s, time() + 60), key=lambda r: r[1] + r[2])

while True:
    header = stdin.readline()
    dna = stdin.readline().strip().upper()
    if header == "" and dna == "":
        break
    debug("dna = '%s', len = %d", dna, len(dna))
    print(" ".join(map(str, tandem_repeat(dna))))
