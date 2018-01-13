#!/usr/bin/env python3

import logging
import math
import sys

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def readchromosome(f):
    n = int(f.readline())
    def readmatrix():
        return [list(map(int, f.readline().split())) for _ in range(n)]
    h00 = readmatrix()
    f.readline()
    h01 = readmatrix()
    f.readline()
    h10 = readmatrix()
    f.readline()
    h11 = readmatrix()
    return (h00, h01, h10, h11)

def numgenes(ch):
    return len(ch[0b00])

def numorganism(ch, a, b):
    return sum((ch[i][a][b] for i in [0b00, 0b01, 0b10, 0b11]))

# p(d) := 0.5 * d;
# h11(d) := 3/4 * (1 - p(d))^2 + p(d) * (1 - p(d)) + 1/2 * p(d)^2;
# h01(d) := 1/2 * (1 - p(d)) * p(d) + 1/4 * p(d)^2;
# h10(d) := h01(d);
# h00(d) := 1/4 * (1 - p(d))^2;
# solve(h11(d) = m/n, d);
# solve(h10(d) = m/n, d);
# solve(h01(d) = m/n, d);
# solve(h00(d) = m/n, d);

def solve11(m, n):
    d1 = -(2**(3/2) * math.sqrt(2 * m * n - n**2) - 2 * n) / n
    d2 =  (2**(3/2) * math.sqrt(2 * m * n - n**2) + 2 * n) / n
    return (d1, d2)

def solve10(m, n):
    d1 = -(2 * math.sqrt(n**2 - 4 * m * n) - 2 * n) / n
    d2 =  (2 * math.sqrt(n**2 - 4 * m * n) + 2 * n) / n
    return (d1, d2)

def solve01(m, n):
    return solve10(m, n)

def solve00(m, n):
    d1 = -(4 * math.sqrt(m * n) - 2 * n) / n
    d2 =  (4 * math.sqrt(m * n) + 2 * n) / n
    return (d1, d2)

def genesdist(ch, a, b):
    n = numorganism(ch, a, b)
    logging.debug('numorganism %d %d = %d', a, b, n)

    m = ch[0b00][a][b]
    logging.debug('ch[0b00][%d][%d] %d %s', a, b, m, solve00(m, n))

    m = ch[0b01][a][b]
    logging.debug('ch[0b01][%d][%d] %d %s', a, b, m, solve01(m, n))

    m = ch[0b10][a][b]
    logging.debug('ch[0b10][%d][%d] %d %s', a, b, m, solve10(m, n))

    m = ch[0b11][a][b]
    logging.debug('ch[0b11][%d][%d] %d %s', a, b, m, solve11(m, n))

    pass

def genesorder(ch):
    logging.debug('ch %s', ch)
    n = numgenes(ch)
    logging.debug('numgenes %d', n)
    dist = dict()
    for a in range(n - 1):
        for b in range(a + 1, n):
            dist.setdefault(a, dict())[b] = genesdist(ch, a, b)
            dist.setdefault(b, dict())[a] = dist[a][b]
    # TODO
    return list(range(n))

for _ in range(int(sys.stdin.readline())):
    order = genesorder(readchromosome(sys.stdin))
    print(' '.join(map(str, order)))
