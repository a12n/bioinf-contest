#!/usr/bin/env python3

from sys import stdin

import numpy
import matplotlib.pyplot as plot

def gccontent(s):
    return (s.count('C') + s.count('G')) / len(s)

_ = stdin.readline()
s = ''.join(map(str.rstrip, stdin))
assert sum([s.count(c) for c in 'ACGT']) == len(s)

def parts(s, n):
    i = 0
    while True:
        t = s[(i * n):((i + 1) * n)]
        if not t:
            break
        yield t
        i += 1

# print(s)
# print(gccontent(s))
# print(list(map(gccontent, parts(s, 10))))

k = 100
subs = list(parts(s, k))
mean = gccontent(s)
std = numpy.std(list(map(gccontent, subs)))
print('mean', mean, 'std', std)

x = [k * i for i in range(len(subs))]
plot.grid(True)                 # TODO: grin on y for mean and std multiplies
plot.plot(x, list(map(gccontent, subs)), '-r', \
          x, [mean - std] * len(x), '-g', \
          x, [mean] * len(x), '-b', \
          x, [mean + std] * len(x), '-g' \
)
plot.show()

# def weirdgc(subs, mean, std, alpha=2.2):
#     for i in range(len(subs)):
#         gc = gccontent(subs[i])
#         if abs(gc - mean) > (alpha * std):
#             yield (i, gc)
#
# weird = list(weirdgc(subs, mean, std))
#
# for i, gc in weird:
#     print('Part at', k * i, 'GC content', gc, 'is weird')
#
# first, _ = weird[0]
# last, _ = weird[-1]

# print('first', k * first, 'last', k * last)
