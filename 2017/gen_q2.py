#!/usr/bin/env python3

import random

# n = 100001
# print(''.join(random.choice('ACGU') for i in range(n)))

n = 5000
o = False
a = ['A'] * n + ['C'] * n + ['G'] * n + ['U'] * n + [(random.choice('ACGU') if o else '')]
random.shuffle(a)
print(''.join(a))
