#!/usr/bin/env python3

from logging import debug
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

def beeskg(n1, a, b):
    i = 0
    try:
        while True:
            n2 = max(a * n1 - b * n1**2, 0)
            diff = abs(n2 - n1)
            if diff < 10E-12:
                return round(n2, 4)
            if i > 100000:
                return round((n1 + n2) / 2, 4)
            n1 = n2
            i += 1
    except OverflowError:
        return -1

n = int(input())
for i in range(n):
    n1, a, b = tuple(map(float, input().split()))
    print(beeskg(n1, a, b))
