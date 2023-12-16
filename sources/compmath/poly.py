#main file for compmath lib, implemetation of operation in polynomial basis
import ctypes
import sys
import os
# get the current directory
curr_dir = os.path.dirname(os.path.realpath(__file__))

# add the current directory to the Python path
sys.path.append(curr_dir)
lib = ctypes.CDLL(curr_dir + '/comp.so')



def prTest(name:str) -> None:
    name = ctypes.c_char_p(name.encode())
    lib.prTest(name)
