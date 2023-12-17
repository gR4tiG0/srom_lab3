#main file for compmath lib, implemetation of operation in polynomial basis
import ctypes
import sys
import os
from typing import Any
# get the current directory
curr_dir = os.path.dirname(os.path.realpath(__file__))

# add the current directory to the Python path
sys.path.append(curr_dir)
lib = ctypes.CDLL(curr_dir + '/comp.so')


BASE = 64

class GF:
    def __init__(self, m=179, poly=0x800000000000000000000000000000000000000000017) -> Any:
        self.m = m
        self.p = 2**m
        self.poly = GFelement(poly)
        global POLY 
        POLY = self.poly
    
    def __call__(self, n) -> Any:
        tmp = GFelement(n)        
        tmp.reduce()
        return tmp
    
def parse(n:int) -> list:
    res = []
    m = 2**BASE
    while n:
        res += [n % m]
        n = n // m 
    return res


class GFelement:
    def __init__(self, number):
        if isinstance(number, int):
            self.words = parse(number)
        elif isinstance(number, list):
            while number[-1] == 0 and len(number) > 1:
                number.pop()
            self.words = number
        else:
            raise ValueError("Invalid input")
        self.l = len(self.words)

    def __add__(self, other):
        self_D = list(self.words)
        other_D = list(other.words)
        size = max(len(other_D),len(self_D))
        self_c = (ctypes.c_uint64 * size)(*self_D)
        other_c = (ctypes.c_uint64 * size)(*other_D)
        result_c = (ctypes.c_uint64 * size)() 
        lib.add(result_c,self_c,other_c,size)
        result = list(result_c)
        return GFelement(result)
    
    def __mul__(self, other):
        self_D = list(self.words)
        other_D = list(other.words)
        size = max(len(other_D),len(self_D))
        self_c = (ctypes.c_uint64 * size)(*self_D)
        other_c = (ctypes.c_uint64 * size)(*other_D)
        result_c = (ctypes.c_uint64 * (size*2))() 
        lib.mul(result_c,self_c,other_c,size)
        result_ = list(result_c)
        result = GFelement(result_)
        result.reduce()
        return result

    def getBase(self) -> int:
        res = 0
        for elem in self.words[::-1]:
            res = (res * 2**BASE) + elem
        return res
    
    def reduce(self):
        # print("reduce called")
        # print(self)
        self_D = list(self.words)
        global POLY 
        mod_D = list(POLY.words)
        aSize = len(self_D)
        pSize = len(mod_D)
        self_c = (ctypes.c_uint64 * aSize)(*self_D)
        mod_c = (ctypes.c_uint64 * pSize)(*mod_D)
        result_c = (ctypes.c_uint64 * pSize)()
        lib.reduce(result_c,self_c,mod_c,aSize,pSize)
        result = list(result_c)
        # print("poly.py reduce, res raw", result)
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        # print("poly.py reduce, res cleared", result)
        self.words = result
        self.l = len(self.words)
        # print("poly.py reduce, self.words",self.words)
    
    def lshift(self, n):
        self_D = list(self.words)
        size = len(self_D)
        #print(self_D)
        self_c = (ctypes.c_uint64 * size)(*self_D)
        res_c = (ctypes.c_uint64 * (size+ n//64 + 1))()
        lib.lshift(res_c, self_c,size,n)
        res = list(res_c)
        #print(res)
        return GFelement(res)
    
    def bitLen(self):
        self_D = list(self.words)
        size = len(self_D)
        self_c = (ctypes.c_uint64 * size)(*self_D)
        
        res = lib.bitLen(self_c,size)
        # print(type(res))
        # print(res)
        return int(res)
    
    def __pow__(self,n):
        if n == 2:
            # print(self.words)
            self_D = list(self.words)
            # print("poly.py self.words:",self_D)
            size = len(self_D)
            self_c = (ctypes.c_uint64 * size)(*self_D)
            res_c = (ctypes.c_uint64 * (size*2))()
            lib.sqr(res_c,self_c,size)
            res_ = list(res_c)
            res = GFelement(res_)
            # print(res)
            res.reduce()
            return res
    def __repr__(self):
        return hex(self.getBase())
    
    def __str__(self):
        return hex(self.getBase())

