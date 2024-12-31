# AES from scratch
# @author - venupulagam

import numpy as np
from itertools import chain

check = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]

def bintohex (bin) :
    hexs = hex(int(bin, 2))[2:]
    return hexs

def hextobin (hex) :
    bins = bin(int(hex, 16))
    return bins

def dectohex (dec) :
    bins = hex(int(dec))[2:]
    if len(bins) != 2 :
        bins = '0' + bins
    return bins

def hextodec (hex) :
    decs = int(hex, 16)
    return decs

sbox = [
    ["63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
    ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
    ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
    ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
    ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
    ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
    ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
    ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
    ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
    ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
    ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
    ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
    ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
    ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
    ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
    ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]]

invsbox = [
    ["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
    ["7C", "E3", "39", "82", "9B", "2F", "FF", "87", "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
    ["54", "7B", "94", "32", "A6", "C2", "23", "3D", "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
    ["08", "2E", "A1", "66", "28", "D9", "24", "B2", "76", "5B", "A2", "49", "6D", "8B", "D1", "25"],
    ["72", "F8", "F6", "64", "86", "68", "98", "16", "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
    ["6C", "70", "48", "50", "FD", "ED", "B9", "DA", "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
    ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A", "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
    ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02", "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
    ["3A", "91", "11", "41", "4F", "67", "DC", "EA", "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
    ["96", "AC", "74", "22", "E7", "AD", "35", "85", "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
    ["47", "F1", "1A", "71", "1D", "29", "C5", "89", "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
    ["FC", "56", "3E", "4B", "C6", "D2", "79", "20", "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
    ["1F", "DD", "A8", "33", "88", "07", "C7", "31", "B1", "12", "10", "59", "27", "80", "EC", "5F"],
    ["60", "51", "7F", "A9", "19", "B5", "4A", "0D", "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
    ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0", "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
    ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"]]

roundconst = ["01", "02", "04", "08", "10", "20", "40", "80", "1B", "36"]

mix =  [[0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]]

invmix = [[0x0E, 0x0B, 0x0D, 0x09],
          [0x09, 0x0E, 0x0B, 0x0D],
          [0x0D, 0x09, 0x0E, 0x0B],
          [0x0B, 0x0D, 0x09, 0x0E]]

test = [[0x63, 0x47, 0xa2, 0xf0],
        [0x9c, 0x63, 0xc5, 0xf2],
        [0x7b, 0x7c, 0xf0, 0xab],
        [0xca, 0xaf, 0x76, 0x76]]

def subbytes (string) :
    subs = sbox[check.index(string[0])][check.index(string[1])]
    return subs

def shiftrows (key) :
    output = []
    for i in range(0,len(key)) :
        out = key[i][i:len(key)]
        [out.append(key[i][j]) for j in range(0, i)]
        output.append(out)
    return output

def mixcol (mat) :
    out = [[0, 0, 0, 0] for i in range (0,4)]
    outs = [["", "", "", ""] for i in range (0,4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                out[i][j] ^= galois_field_multiply(mix[i][k], int(mat[k][j],16))
                outs[i][j] = dectohex(out[i][j])
    return outs

def galois_field_multiply(a, b):
    result = 0
    while a and b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return result

def g(word, iter) :
        rc = [roundconst[iter], 0, 0, 0]
        bdash = word[1:4]
        bdash.append(word[0])
        sub = []
        wdash = []
        for i in bdash:
            sub.append(subbytes(i))
        for i in range(0, len(sub)) :
            var = xor(sub[i], rc[i])
            wdash.append(var)
        return wdash

def keyexpand (strkey) :
    key = []
    for i in strkey :
        key.append(hex(ord(i))[2:])
    
    w0 = key[0:4]
    w1 = key[4:8]
    w2 = key[8:12]
    w3 = key[12:16]
    
    w = [w0, w1, w2, w3]
    
    iter = 0
    
    while iter < len(roundconst) :
        gout = g(w[len(w)-1], iter)
        w.append(xorar(gout, w[len(w)-1-3]))
        nums = 1
        while nums <= 3:
            w.append(xorar(w[len(w)-1], w[len(w)-1-3]))
            nums += 1
        iter += 1
    
    num = 0
    mat = []

    while num <= len(w)-4:
        row = []
        for j in range (0, 4):
            row.append(w[num+j])
        mat.append(row)
        num = num+4
        
    return mat

def xor(hex_str1, hex_str2):
    int_val1 = int(str(hex_str1), 16)
    int_val2 = int(str(hex_str2), 16)
    
    result = int_val1 ^ int_val2
    result_hex = hex(result)[2:]
    if len(result_hex) != 2:
        result_hex = '0' + result_hex

    return result_hex

def xorar (list1, list2) :
    out = []
    for i in range (0, len(list1)) :
        out.append(xor(list1[i], list2[i]))
    return out

def xormat (mat1, mat2) :
    out = []
    for i in range(0, len(mat1)) :
        out.append(xorar(mat1[i], mat2[i]))
    return out

def twofromone (inlist) :
    out = [inlist[i:i+4] for i in range(0, len(inlist), 4)]
    return out

def twotoone (inlist) :
    out = list(chain(*inlist))
    return out

def transpose(matrix):
    transposed_matrix = list(map(list, zip(*matrix)))
    return transposed_matrix

def invshiftrows (mat) :
    output = []
    for i in range (0,len(mat)) :
        out = mat[i][len(mat)-i:len(mat)]
        [out.append(mat[i][j]) for j in range(0, len(mat)-i)]
        output.append(out)
    return output

def invsubbytes (string) :
    subs = invsbox[check.index(string[0])][check.index(string[1])]
    return subs

def invmixcol (mat) :
    out = [[0, 0, 0, 0] for i in range (0,4)]
    outs = [["", "", "", ""] for i in range (0,4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                out[i][j] ^= galois_field_multiply(invmix[i][k], int(mat[k][j], 16))
                outs[i][j] = dectohex(out[i][j])
    return outs

def key16 (key) :
    if len(key) < 16 :
        key = key + " " * (16 - len(key))
    return key
    
def encrypt (message, key) :
    mlist = []
    key = key16(key)
    klist = keyexpand(key)
    
    for i in message :
        mlist.append(hex(ord(i))[2:])
        
    mess = np.array(mlist).reshape(4,4)
    mess = np.transpose(mess)
    
    # intial transformation :
    r0 = xormat(mess, np.transpose(klist[0]))
    r0 = list(chain(*r0))

    round = 0

    while round < 10 :
        sb = []
        for i in range(0, len(r0)):
            sb.append(subbytes(r0[i]))
        sr = shiftrows(twofromone(sb))
        if round != 9 :
            mc = mixcol(sr)
        else :
            mc = sr
        round = round + 1
        r1 = xormat(mc, np.transpose(klist[round]))
        r0 = list(chain(*r1))
        
    r1 = twotoone(transpose(r1))
    cipher = ""
    for i in r1: cipher += chr(int(i, 16))
    
    return cipher

def decrypt (cipher, key):
    key = key16(key)
    klist = keyexpand(key)
    clist = [dectohex(ord(char)) for char in cipher]
    clist = transpose(np.array(clist).reshape(4,4))
    
    # initial transformation
    ar = xormat(clist, transpose(klist[10]))
    round = 0
    
    while round < 10 :
        sr = invshiftrows(ar)
        sr = list(chain(*sr))
        sb = []
        for i in range(0, len(sr)):
            sb.append(invsubbytes(sr[i]))
        sb = twofromone(sb)
        round = round + 1
        ar = xormat(sb, transpose(klist[10-round]))
        if round != 10 :
            mc = invmixcol(ar)
        else :
            mc = ar
        ar = mc
        
        dec = twotoone(transpose(mc))
        message = ""
        for i in dec :
            message = message + chr(hextodec(i))
    
    return message

def enc (message, key) :
    l = len(message)
    message = message + " "*((16 - l) % 16)
    crypt = ""
    i = 0
    while i <= len(message)-16 :
        word = message[i:i+16]
        crypt = crypt + encrypt(word, key)
        i = i+16
    return crypt

def dec (crypt, key) :
    message = ""
    i = 0
    while i <= len(crypt)-16 :
        word = crypt[i:i+16]
        message = message + decrypt(word, key)
        i = i+16
    return message

'''msg = "I have checked the code and its working"
cr = enc(msg, "Thats my Kung Fu")
print(cr)
ms = dec(cr, "Thats my Kung Fu")
print(ms)'''