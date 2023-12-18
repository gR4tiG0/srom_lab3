#main file for compmath lib, implemetation of operation in polynomial basis
from typing import Any


BASE = 64
class GF:
    def __init__(self, m=179, poly=0x800000000000000000000000000000000000000000017) -> Any:
        self.m = m
        self.p = 2**m
        self.poly = GFelement(poly,1,m)

    
    def __call__(self, n) -> Any:
        tmp = GFelement(n,self.poly,self.m)      
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
    def __init__(self, number,p,m):
        if isinstance(number, int):
            if number == 0: words = [0]
            elif number == 1: words = [1]
            else: words = parse(number)
            
        elif isinstance(number, list):
            while number[-1] == 0 and len(number) > 3:
                number.pop()
            words = number
        else:
            raise ValueError("Invalid input")
        self.p = p 
        self.m = m
        self.words = words
        self.l = self.bitLen()
    
   
    def __add__(self, other):
        res_ = []
        for i in range(max(len(self.words), len(other.words))):
            if i >= len(self.words): a = 0
            elif i >= len(other.words): b = 0
            else:
                a,b = self.words[i],other.words[i]
                res_ += [a^b]
        return GFelement(res_,self.p,self.m)
    
    def mulStep(self,a,b):
        tmp = [0,0]
        for i in range(64):
            if (a & (1 <<i)):
                for j in range(64):
                    if (b & (1<<j)):
                        tmp[(i+j)//64] ^= (1 << ((i+j)%64))
        return tmp
    
    def bitLen(self):
        if set(self.words) == {0}:
            return 0
        c = 0
        while self.words[-1-c] == 0: c += 1
        msb = self.words[-1-c]
        bitsize = 0
        while msb > 0:
            msb >>= 1
            bitsize += 1
        return (len(self.words) - 1 - c)*64 + bitsize
    
    def __mul__(self,b_):
        s = max(len(self.words),len(b_.words))
        a_ = self.words + [0]*(s - len(self.words))
        b_ = b_.words + [0]*(s - len(b_.words))
        res = [0]*(len(a_)+len(b_))
        for i,a in enumerate(a_):
            for j,b in enumerate(b_):
                tmp = self.mulStep(a,b)
                res[i+j] ^= tmp[0]
                res[i+j+1] ^= tmp[1]
            
        res = GFelement(res,self.p,self.m)
        res.reduce()
        return res

    def lshift(self, bits):
        word = 64
        res = GFelement(self.words,self.p,self.m)
        b_words = bits // word 
        b_shift = bits % word
        if b_words != 0:
            res.words = [0]*b_words + res.words
            res.l = res.bitLen()
        if b_shift != 0:
            result = res.words + [0]
            for i in range(len(res.words),0,-1):
                curr = (result[i] << b_shift) & ((1 << (64)) - 1)
                result[i] = curr | (result[i-1] >> (word - b_shift))
            result[0] = (result[0] << b_shift) & ((1 << (word)) - 1)
            if set(result) == {0}: result = [0]
            res.words = result
            res.l = res.bitLen()
        return res
    
    def reduce(self):
        global p 
        
        k = self.bitLen()
        n = self.p.l
        if k > n:
            res = GFelement(self.words,self.p,self.m)
            while k >= n:
                tmp = self.p.lshift(k - n)
              
                res = res + tmp
                k = res.bitLen()

            self.words = res.words 
            self.l = self.bitLen()

    def __pow__(self,n):
        if n == 1:
            return self 
        elif n == 0:
            return GFelement([1],self.p,self.m)
        elif n == 2:
            res = [0]*2*len(self.words)
            k = self.bitLen()
            for i in range(k):
                if (self.words[i//64] & (1 << (i%64))):
                    res[(2*i)//64] ^= (1 << (2*i)%64)
            res = GFelement(res,self.p,self.m)
            res.reduce()
            return res
        elif n == -1:
            return self.inv()
        elif isinstance(n,GFelement):
            k = n.bitLen()
            res = GFelement([1,0,0],self.p,self.m)
            a = GFelement(self.words,self.p,self.m)
            for i in range(k):
                if (n.words[i//64] & (1 << (i%64))):
                    res = res * a 
                a = a**2
            return res
            
    def trace(self):
        k = self.p.l
        a = GFelement(self.words,self.p,self.m) 
        res = GFelement([0,0,0],self.p,self.m)
        for _ in range(k-1):
            res += a 
            a = a**2
            #print("Res: ",res)
            #print("A: ", a)
        res.reduce()
        return res.words[0]
    

    def __truediv__(self,other):
        k = self.bitLen()
        n = other.bitLen()
        res = GFelement([0,0,0],self.p,self.m)
        if k > n:
            h1 = GFelement(self.words,self.p,self.m)
            while k >= n:
                tmp = other.lshift(k - n)
                h1 = h1 + tmp
                res.words[(k-n)//64] ^= (1 << (k-n)%64)
                k = h1.bitLen()
        return res
    def isnull(self):
        if set(self.words) == {0}:
            return True 
        return False

    def inv(self):
        b = GFelement(self.words,self.p,self.m)
        a = GFelement(self.p.words,self.p,self.m)
        q = GFelement([0,0,0],self.p,self.m)
        
        x0 = GFelement([1,0,0],self.p,self.m)
        y0 = GFelement([0,0,0],self.p,self.m)
        x1 = GFelement([0,0,0],self.p,self.m)
        y1 = GFelement([1,0,0],self.p,self.m)
        while not b.isnull():
            q = a / b 
            tmp = b
            b = a + (b * q)
            a = tmp 

            tmp = x0 
            x0 = x1 
            x1 = tmp + q * x1
            tmp = y0 
            y0 = y1 
            y1 = tmp + q * y1
        return y0



    def getBase(self) -> int:
        res = 0
        for elem in self.words[::-1]:
            res = (res * 2**BASE) + elem
        return res
    def __repr__(self):
        return hex(self.getBase())
    
    def __str__(self):
        return hex(self.getBase())




        
        
