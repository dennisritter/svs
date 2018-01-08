import sys
import os
from xtea import *
import hashlib, binascii
#import hmac

from PIL import Image


def encrypt(img_file, txt_file, xtea, auth):

    # Image preparation
    img = Image.open(img_file)
    img_width, img_height = img.size
    pixel_map = img.load()

    for w in range(0, img_width, 1):
        for h in range(0, img_height, 1):
            pixel = pixel_map[w, h]
            pixel_new = [0, 0, 0]
            pixel_new[0] = int(bin(pixel[0])[:-1] + '0', 2)
            pixel_new[1] = int(bin(pixel[1])[:-1] + '0', 2)
            pixel_new[2] = int(bin(pixel[2])[:-1] + '0', 2)
            pixel_map[w, h] = tuple(pixel_new)

    ## Text preparation
    txt = open(txt_file, 'r').read()
    # add padding to get blocks of 16
    txt = txt.ljust(len(txt) + (64 - len(txt) % 64), '\0')
    #print('textlength', msgLength)
    txt = getMac(auth, txt) + txt
    print(txt, len(txt))
    enc_txt = xtea.encrypt(txt)
    # encode msg length in 16bit
    msgLength = format(len(txt), '016b')
    print('encrypted text', enc_txt, len(enc_txt))

    img_width, img_height = img.size

    # binary String
    temp_txt_bits_str = ''.join([format(int(x, 2), '008b') for x in map(bin, bytearray(enc_txt))])
    temp_txt_bits_str = msgLength + temp_txt_bits_str
    print(int(msgLength, 2))
    print('compare length', len(temp_txt_bits_str) - 16, len(txt), len(temp_txt_bits_str) / len(txt))
    # n-bit array
    n = 3
    txt_tri_bits = [temp_txt_bits_str[i:i+n] for i in range(0, len(temp_txt_bits_str), n)]
    # fill up last element if length is not
    while len(txt_tri_bits[-1]) < n:
        txt_tri_bits[-1] += '0'

    # replace last rgb-bits with text-bits
    for i in range(0, len(txt_tri_bits), 1):
        txt_tri_bit = txt_tri_bits[i]
        pixel = pixel_map[i % img_width, i / img_width]
        pixel_new = [0, 0, 0]
        pixel_new[0] = int(bin(pixel[0])[:-1] + txt_tri_bit[0], 2)
        pixel_new[1] = int(bin(pixel[1])[:-1] + txt_tri_bit[1], 2)
        pixel_new[2] = int(bin(pixel[2])[:-1] + txt_tri_bit[2], 2)
        pixel_map[i % img_width, i / img_width] = tuple(pixel_new)

    # save ste file
    dirname = 'ste'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    img.save('./ste/' + img_file)
    os.rename('ste/' + img_file, 'ste/' + img_file + '.ste')


def decrypt(img_file, xtea, auth):
    img = Image.open(img_file)
    img_width, img_height = img.size
    pixel_map = img.load()

    txt_bits = ''

    for i in range(0, (img_width * img_height), 1):
        pixel = pixel_map[i % img_width, i / img_width]
        for j in range(0, len(pixel), 1):
            txt_bits += bin(pixel[j])[-1]

    # cut off msgLength
    msg_length = int(txt_bits[:16], 2)*8
    print(txt_bits[:16])
    print(msg_length)
    txt_bits = txt_bits[16:]
    txt_bits = txt_bits[:msg_length]

    n = 8
    # split to bytes
    txt_bytes = [txt_bits[i:i+n] for i in range(0, len(txt_bits), n)]
    # filter bytes with no text
    #txt_bytes = filter(lambda byte: byte != '00000000', txt_bytes) #HHHHHIIIIEEEERRRR

    # reformat
    txt_bytes = [format(int(x, 2), '008b') for x in txt_bytes]
    #print(txt_bytes)
    # create bytearray
    txt_bytes = str(bytearray([int(x, 2) for x in txt_bytes]))

    #txt_bytes = txt_bytes.ljust(len(txt_bytes) + (16 - len(txt_bytes) % 16), '\0')
    print(len(str(txt_bytes)) % 64)
    print('text to decrypt', txt_bytes, len(txt_bytes))
    text = xtea.decrypt(txt_bytes)

    mac = getMac(auth, text[64:])
    txt_mac = text[:64]
    print('ENCRYPT MAC', txt_mac)
    print('DECRYPT MAC', mac)
    if txt_mac == mac:
        text = text[64:]
        print(text)
        txt_file = open('text.txt_restored', 'w')
        txt_file.write(text)
        txt_file.close()
    else:
        print('Mooop, wrong MAC')


def getMac(pw, msg):
    testmac = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', bytes(hashlib.sha256(pw).hexdigest()), msg, 100000))
    print('hmac:', testmac, len(testmac))
    return testmac


def getXtea(p):
    k = hashlib.sha256(p).digest()[:16]
    return new(k, mode=MODE_CFB, IV="12345678")


print(sys.argv)
mode = str(sys.argv[1])
print('mac pw', str(sys.argv[3]))
auth = str(sys.argv[3])
xt = getXtea(str(sys.argv[5]))
if mode == '-e':
    text_par = str(sys.argv[6])
    img_par = str(sys.argv[7])
    encrypt(text_par, img_par, xt, auth)

elif mode == '-d':
    img_par = str(sys.argv[6])
    decrypt(img_par, xt, auth)
