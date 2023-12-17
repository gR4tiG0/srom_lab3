#!/usr/bin/python3
from compmath.poly import *
from random import getrandbits
import numpy as np
from sys import exit
def gf2_multiply(a, b):
    # Perform polynomial multiplication in GF(2)
    result = np.convolve(a, b, mode='full') % 2
    return int(''.join([str(i) for i in list(result)]),2)

def main() -> None:
    # GF179 = GF(3,13)
    GF179 = GF()
    BITS = GF179.m 
    # A,B = getrandbits(BITS), getrandbits(BITS)
    A,B = 0x10065cb0425d5a61e16c2de3199c39b4dc33300cc573e, 0x322cf6939d4b453e274bce09d7316747a3926dd062b4a

    # A,B = 6,7
    # print(GF179.poly.words)
    # print(hex(A),hex(B))
    # print(A.bit_length(),B.bit_length())
    # tmp = GFelement([1,0,0,0,0,0])
    # print(tmp.bitLen())
    # A = 1 
    # a = GF179(A)
    # b = a.lshift(66)
    # print(b)
    # print(bin(b.getBase())[2:])

    # A,B = 7,6
    a,b = GF179(A),GF179(B)
    # print(a,b)
    # C = (A ^ B)
    c = a + b 
    print(c)
    # C = gf2_multiply([int(i) for i in list(bin(A)[2:])], [int(i) for i in list(bin(B)[2:])])
    d = a*b
    # print("results C,c")
    # print(hex(C))
    d.reduce()
    # c_ = GF179(C)
    print(d) 
    # print(c_)
if __name__ == "__main__":
    main()
