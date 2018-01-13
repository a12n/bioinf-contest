#!/usr/bin/env python3

import sys
import random

# print(1)
# for i in range(50000, 1, -1):
#     print(i, '->', (i - 1), sep='')

# print(1)
# l = [1]
# for i in range(2,

# initonly.in

init = list(map(str, range(1, 100000)))
random.shuffle(init)
print(' '.join(init))
print('+'.join(init), '->', 100000, sep='')
print(' '.join(map(str, sorted(init) + [100000])))
