#!/usr/bin/env python3

from random import randint

# n = randint(290, 300)
# m = randint(290, 300)
n = 300
m = 300
print(n, m)

# Case 1

# for i in range(n):
#     k = 0 + randint(0, 100)
#     ivlist = []
#     for j in range(334):
#         ivlist.append(k + randint(0, 10))
#         ivlist.append(ivlist[-1] + randint(0, 10))
#         k = ivlist[-1]
#     print(' '.join(map(str, ivlist)))
#
# for i in range(m):
#     k = 0 + randint(0, 100)
#     ivlist = []
#     for j in range(334):
#         ivlist.append(k + randint(0, 10))
#         ivlist.append(ivlist[-1] + randint(0, 10))
#         k = ivlist[-1]
#     print(' '.join(map(str, ivlist)))

# Case 2

# k = 0 + randint(0, 100)
# ivlist = []
# for j in range(10**5 - n):
#     ivlist.append(k + randint(0, 10))
#     ivlist.append(ivlist[-1] + randint(0, 10))
#     k = ivlist[-1]
# print(' '.join(map(str, ivlist)))
# for i in range(n):
#     ivlist = []
#     ivlist.append(randint(0, 100) + randint(0, 10))
#     ivlist.append(ivlist[-1] + randint(0, 10))
#     print(' '.join(map(str, ivlist)))
#
# k = 0 + randint(0, 100)
# ivlist = []
# for j in range(10**5 - m):
#     ivlist.append(k + randint(0, 10))
#     ivlist.append(ivlist[-1] + randint(0, 10))
#     k = ivlist[-1]
# print(' '.join(map(str, ivlist)))
# for i in range(m):
#     ivlist = []
#     ivlist.append(randint(0, 100) + randint(0, 10))
#     ivlist.append(ivlist[-1] + randint(0, 10))
#     print(' '.join(map(str, ivlist)))

# Case 3

for i in range(n):
    ivlist = []
    for j in range(10**5 // n):
        ivlist.append(j)
        ivlist.append(j)
    print(' '.join(map(str, ivlist)))

for i in range(m):
    ivlist = []
    for j in range(10**5 // m):
        ivlist.append(j + 1)
        ivlist.append(j + 1)
    print(' '.join(map(str, ivlist)))
