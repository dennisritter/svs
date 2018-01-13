import sys
import os
import hashlib
from xtea import *
import datetime
import base64


##########################
##### Diffie-Hellman #####
##########################


def calcDHK(others_shared_key, my_secret_key, p):
    k = (others_shared_key ** my_secret_key) % p
    return k


G = 123
P = 401

a = 8347
b = 42

A = (G ** a) % P
B = (G ** b) % P

# 357
K = calcDHK(A, b, P)
print('xtea_pw: [{0}]'.format(K))


##########################
##### Send Mail ##########
##########################


def getXtea(p):
    k = hashlib.sha256(p).digest()[:16]
    return new(k, mode=MODE_CFB, IV="12345678")


##########################
##### Send Mail ##########
##########################


def sendMail(from_mail, to_mail, msg, xtea_pw):
    print('Sending mail to {0}...'.format(to_mail))
    msg = from_mail + ': ' + msg
    if not os.path.exists(to_mail):
        os.makedirs(to_mail)
    #filename = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    if xtea_pw is None:
        filename = 'key' + '.txt'
    else:
        filename = 'mail' + '.txt'
        xt = getXtea(xtea_pw)
        msg = xt.encrypt(msg.ljust(len(msg) + (64 - len(msg) % 64), '\0'))

    file = open('./' + to_mail + '/' + filename, 'w')

    b64_msg = base64.b64encode(msg)
    file.write(b64_msg)
    print('Mail sent.')

##########################
##### Receive Mail #######
##########################


def receiveMail(for_mail, xtea_pw):
    print('Receiving mail...')

    if not os.path.exists(for_mail):
        print('No directory [{0}] present...'.format(for_mail))
        print('Aborting')

    if xtea_pw is None:
        filename = 'key' + '.txt'
    else:
        filename = 'mail' + '.txt'

    file = open('./' + for_mail + '/' + filename, 'r')
    b64_msg = file.read()
    msg = base64.b64decode(b64_msg)
    print('enc_msg:', msg)

    if xtea_pw is not None:
        xt = getXtea(xtea_pw)
        msg = xt.decrypt(msg)

    print('Received mail:')
    print(msg)

##########################
##### Check Args #########
##########################

print(str(sys.argv))

xtea_pw_param = None
to_mail_param = None
msg_param = None
from_mail_param = 'my@mail.de'

if str(sys.argv[1]) == '-s':
    if str(sys.argv[2]) != '-k':
        to_mail_param = str(sys.argv[3])
        msg_param = str(sys.argv[4])
        sendMail(from_mail_param, to_mail_param, msg_param, xtea_pw_param)
    else:
        xtea_pw_param = str(sys.argv[3])
        to_mail_param = str(sys.argv[5])
        msg_param = str(sys.argv[6])
        sendMail(from_mail_param, to_mail_param, msg_param, xtea_pw_param)

if str(sys.argv[1]) == '-r':
    if len(sys.argv) >= 3 and str(sys.argv[2]) == '-k':
        xtea_pw_param = str(sys.argv[3])
    receiveMail('my@mail.de', xtea_pw_param)
