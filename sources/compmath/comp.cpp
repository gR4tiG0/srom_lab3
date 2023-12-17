#include <cstdint>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include <math.h>


extern "C" {
    void prArr(uint64_t* num, int size) {
        for (int i = 0; i<size;i++){
            printf("%lu ",num[i]);
        }
        printf("\n");
    }
    void add (uint64_t* res, uint64_t* a, uint64_t* b, int size)
    {
      // prArr(a, size);
      // prArr(b, size);
      for (int i = 0; i < size; i++) 
      {
        res[i] = a[i] ^ b[i];
      }
      // printf("res converted\n");
      // prArr(res, size);
    }
    void mulStep(uint64_t* res, uint64_t a, uint64_t b)
    { 
      for (int i = 0; i < 64; ++i) 
      {
        if (a & (1ULL << i)) {
          for (int j = 0; j < 64; ++j) {
            if (b & (1ULL << j)) {
              if (i+j >= 64) {
                res[1] ^= 1ULL << (i+j - 64);
              }
              else {
                res[0] ^= 1LL << (i+j);
              }
            }
          }
        }
      }
    }
    void lshiftB(uint64_t* number, int size) {
        for (int i = size - 1; i > 0; i--){
            number[i] = (number[i] << 1) | (number[i-1] >> ((8*64)-1));
        }
        number[0] <<= 1;
    }
    void lshift(uint64_t* res, uint64_t* number, int size, int p)
    {
      int words = p / 64;
      for (int i = 0; i < size+words+1;i++) {
        if (i > size) {
          res[i] = 0;
        } else {
          res[i] = number[i];
        }
      }
      // prArr(res,size+words+1);
      if (words) 
      {
        // printf("we are in words if\n");
        for (int i = 0; i < size+words+1; i++) 
        {
          if (i < words) {
            res[i] = 0;
          } else {
            // printf("wearehere\n");
            res[i] = number[i-words];
          }
          // printf("%lu\n",res[i]);
        }
      }
      // prArr(res,size+words+1);
      p = p % 64;
      // printf("p=%i\n",p);
      if (p) {
        for (int i = 0; i < p; i++) 
        {
        // printf("i = %i\n",i);
        // printf("we are on 1b shift cycle\n");
        // prArr(res,size+words+1);
          lshiftB(res, size+words+1);
        // prArr(res,size+words+1);
        }
      }
    }
    uint64_t bitLen(uint64_t* number, int size)
    {
      if (size == 1 && number[size-1] == 0) {
        return 0;
      }
      int c = 0;
      while (number[size-c-1] == 0) {
        c ++;
      }
      uint64_t msb = number[size-c-1];
      size_t bitsize = 0;
      while (msb > 0) {
        msb >>= 1;
        bitsize++;
      }
      return (size - 1 - c)*64 + bitsize;
    }
    void reduce(uint64_t* res, uint64_t* a, uint64_t* p, int aSize, int pSize)
    { 
      int k = bitLen(a, aSize);
      int n = bitLen(p, pSize);
      if (k < n) {
        for (int i = 0; i < aSize; i++)
        {
          if (i < pSize) {
            res[i] = a[i];
          } else {
            res[i] = 0;
          }
        }
      } else {
        uint64_t* h1 = new uint64_t[aSize]();
        uint64_t* h2 = new uint64_t[aSize]();
        for (int i = 0; i < aSize; i++) 
        {
          if (i < pSize) {
            h1[i] = p[i];
          } else {
            h1[i] = 0;
          }
          res[i] = a[i];
          h2[i] = 0;
        }

      // printf("a,p,res,h1,h2 at start\n");
      // prArr(a,aSize);
      // prArr(p,pSize);
      // prArr(res,aSize);
      // prArr(h1,aSize);
      // prArr(h2, aSize);

      while (k >= n) {
        lshift(h2,h1,pSize,k-n);
        // printf("h1,h2,after shift\n");
        // prArr(h1,aSize);
        // prArr(h2,aSize);
        add(res,res,h2,aSize);
        // printf("res after addition\n");
        // prArr(res, aSize);
        k = bitLen(res,aSize);
        // printf("end of cycle k = %i, n = %i\n",k,n);
      }
      // delete[] h1;
      // delete[] h2;
      }
    }
    void mul(uint64_t* res, uint64_t* a, uint64_t* b, int size)
    {
      for (int i = 0; i < size*2; i++) 
      {
        res[i] = 0;
      }
      uint64_t* tmp = new uint64_t[2]();
      for (int i = 0; i < size; i++)
      {
        for (int j = 0; j < size; j++)
        {
          tmp[0] = 0;
          tmp[1] = 0;
          mulStep(tmp, a[i], b[j]);
          res[i+j] ^= tmp[0];
          res[i+j+1] ^= tmp[1];
        }
      }
      delete[] tmp;
    }
    void sqr(uint64_t* res, uint64_t* a, int size) 
    {
      // printf("we are here\n");
      for (int i = 0; i < 2*size; i++) {
        res[i] = 0;
      }
      int k = bitLen(a, size);
      // printf("c++ a:");
      // prArr(a,size);
      for (int i = 0; i < k; i++) {
        // printf("a[i] = %lu, shift check = %lu\n",a[i/64], ((uint64_t)1 << (i%64)));
        if (a[i/64] & ((uint64_t)1 << (i%64))) {
          // printf("i=%i 2i/64 %i : ",i,(2*i)/64);
          res[(2*i)/64] ^= ((uint64_t)1 << (2*i)%64);
          // printf("res in cycle: ");
          // prArr(res,size*2);
        }
      }
      // prArr(res,size*2);
    }

}
