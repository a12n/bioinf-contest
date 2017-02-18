#!/usr/bin/env python3

from bisect import bisect_right
from sys import stdin
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def intersects(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

class DIS:
    def __init__(self, ivlist):
        self.first = [iv[0] for iv in ivlist]
        self.last = [iv[1] for iv in ivlist]
        # self.first.sort()
        # self.last.sort()

    def __len__(self):
        return len(self.first)

    def _intersects1(self, iv):
        i = bisect_right(self.first, iv[1])
        if i != 0:
            return intersects((self.first[i - 1], self.last[i - 1]), iv)
        return False

    def _endpoints(self):
        return (self.first[0], self.last[-1])

    def intersects(self, other):
        if len(other) > len(self):
            return other.intersects(self)
        if not intersects(self._endpoints(), other._endpoints()):
            return False
        for iv in zip(other.first, other.last):
            if self._intersects1(iv):
                return True
        # if self._intersects1((other.first[0], other.last[0])):
        #     return True
        # for i in range(1, len(other) // 2 + 1):
        #     if self._intersects1((other.first[+i], other.last[+i])) or \
        #        self._intersects1((other.first[-i], other.last[-i])):
        #         return True
        return False

# --------------------------------------------------------------------------------------

def ivsoflist(l):
    return [(l[2 * i], l[2 * i + 1]) for i in range(len(l) // 2)]

def ivsofstr(s):
    return ivsoflist(list(map(int, s.split())))

if __name__ == '__main__':
    n, m = map(int, stdin.readline().split())
    genes = [DIS(ivsofstr(stdin.readline())) for _ in range(n)]
    reads = [DIS(ivsofstr(stdin.readline())) for _ in range(m)]

    ans = [0] * n
    tmp = [-1] * m

    for j in range(len(reads)):
        for i in range(len(genes)):
            if tmp[j] == -1:
                if reads[j].intersects(genes[i]):
                    tmp[j] = i
            elif tmp[j] != -2:
                if reads[j].intersects(genes[i]):
                    tmp[j] = -2

    for i in tmp:
        if i >= 0:
            ans[i] += 1

    print('\n'.join(map(str, ans)))
