#!/usr/bin/python
# -*- coding: utf-8 -*-

##### A3-1 #####
P = 467
G = 2
A = [2, 400, 228]
B = [5, 134, 57]


# Get public single key
def get_pk(p, g, x):
    pk = (g**x) % p
    return pk


# Get secret shared key
def get_sk(g, p, a, b, ):
    sk = (g**(a * b)) % p
    return sk

print('################')
print('##### A3-1 #####')
print('################')
for i in range(0, 3, 1):
    apk = get_pk(P, G, A[i])
    bpk = get_pk(P, G, B[i])
    sk = get_sk(P, G, apk, bpk)
    print('{3}. : A = {0}; B = {1}; K = {2}'.format(apk, bpk, sk, i))

print('################')
print('##### A3-2 #####')
print('################')
M = 9
P = 5
Q = 11
E = 3


def x_euklid(a, b):
    if b == 0:
        return (a, 1, 0)
    (d2, s2, t2) = x_euklid(b, a % b)
    (d, s, t) = (d2, t2, s2 - (a / b) * t2)
    return d, s, t


def encrypt_rsa(e, p, q, m):
    n = p * q
    y = (m ** e) % n
    print('Verschluesselung: n = {0}, y = {1}'.format(n, y))
    return y


def decrypt_rsa(e, p, q, y):
    n = p * q
    phiN = (p-1) * (q-1)
    # (e * d) % phiN = 1
    # 3 * 107 = 321 = phiN * 8 + 1
    d = x_euklid(phiN, e)[2]
    while d < 0:
        d += phiN
    m = (y ** d) % n
    print('Entschluesselung: n = {0}, phiN = {1} d = {2}, m = {3}'.format(n, phiN, d, m))


decrypt_rsa(E, P, Q, encrypt_rsa(E, P, Q, M))


print('################')
print('##### A3-3 #####')
print('################')


def calcD(p, q, e):
    n = p * q
    phiN = (p - 1) * (q - 1)
    d = x_euklid(phiN, e)
    print('n = {0}; phiN = {1};'.format(n, phiN))
    print('Für p = {0}, q = {1} und e = {2}'.format(p, q, e))
    print('..ist n = {0}, phiN = {1};'.format(n, phiN))
    print('..ist der private Exponent d = {}'.format(d[2]))


calcD(41, 17, 39)
