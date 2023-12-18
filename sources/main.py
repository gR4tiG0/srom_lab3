#!/usr/bin/python3
# from compmath.poly import *
from compmath.gf import *
from random import getrandbits

def main() -> None:
    fld = GF()
    BITS = fld.m
    A,B = getrandbits(BITS),getrandbits(BITS)
    a,b = fld(A),fld(B)
    print("a,b:", a,b)
    print("poly:", fld.poly)
    print("a+b:",a+b)
    print("a*b:",a*b)
    print("a**2:",a**2)
    a_ = a.inv()
    print("a**-1:",a_)
    print("check:",a*a_)
    f = fld(getrandbits(BITS))
    f.reduce()
    print("f:",f)
    print("a**f:",a**f)
    # for i in range(50):
    #     f = fld(i)
    #     print(i,f.trace())
if __name__ == "__main__":
    main()
