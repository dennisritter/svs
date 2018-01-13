

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


def encrypt_rsa(e, p, q, m):
    n = p * q
    y = (m ** e) % n
    print('Verschlüsselung: n = {0}, y = {1}'.format(n, y))
    return y


def decrypt_rsa(e, p, q, y):
    n = p * q
    phiN = (p-1) * (q-1)
    # (e * d) % phiN = 1
    # 3 * 107 = 321 = phiN * 8 + 1
    d = 107
    m = (y ** d) % n
    print('Entschlüsselung: n = {0}, phiN = {1} d = {2}, m = {3}'.format(n, phiN, d, m))


decrypt_rsa(E, P, Q, encrypt_rsa(E, P, Q, M))


print('################')
print('##### A3-3 #####')
print('################')
