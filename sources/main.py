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
    BITS = 100#GF179.m 
    A,B = getrandbits(BITS), getrandbits(BITS)
    # A,B = 6,7
    # print(GF179.poly)
    print(hex(A),hex(B))
    print(A.bit_length(),B.bit_length())
    # tmp = GFelement([1,0,0,0,0,0])
    # print(tmp.bitLen())
    # A = 1 
    # a = GF179(A)
    # b = a.lshift(66)
    # print(b)
    # print(bin(b.getBase())[2:])

    # A,B = 7,6
    a,b = GF179(A),GF179(B)
    print(a,b)
    # C = (A ^ B)
    # c = a + b 

    C = gf2_multiply([int(i) for i in list(bin(A)[2:])], [int(i) for i in list(bin(B)[2:])])
    print(C > 13)
    c = a*b
    print("results C,c")
    print(hex(C))
    print(c)
    print("calling reduce on c from main")
    c.reduce()
    c_ = GF179(C)
    print("python main results c_,c")
    print(c_)
    print(c)

if __name__ == "__main__":
    main()
