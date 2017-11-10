#!/usr/bin/env python
"""This is my doc string.

Keyword arguments:
A -- apple
"""
# Copyright 2015 Austin Fox
# Program is distributed under the terms of the
# GNU General Public License see ./License for more information.

# Python 3 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
# #######################

import sys
import numpy as np
import argparse
from matplotlib import pyplot as plt
from scipy.integrate import quad


s= np.radians(4)
m=0
a=0.5
A = 1
#A = 1/((1-a)/(s*np.sqrt(np.pi/np.log(2)))+a/(s*np.pi))

def f(x):

    return ((((1-a)*A)/(s*np.sqrt(np.pi/np.log(2)))*
             np.exp(-(x-m)**2*np.log(2)/s**2))+
            a*A/np.pi*(s/((x-m)**2+s**2)))


def f2(x):

    return ((((1-a)*A)/(s*np.sqrt(np.pi/np.log(2)))*
             np.exp(-(x-m)**2*np.log(2)/s**2))+
            a*A/np.pi*(s/((x-m)**2+s**2)))*np.cos(x)**2
def f3(x):

    return 1/np.radians(45)*np.cos(x)**2

def test():
    """doc string
    """
    global s
    x = np.linspace(-10,10)
    print(A)
    print(((1-a)*A)/(s*np.sqrt(np.pi/np.log(2))))
    print(a*A/np.pi)
    ans, err = quad(f2, 0, np.radians(45))
    print('fwhm=4', ans*2, err)
    s=np.radians(8)
    ans, err = quad(f2, 0, np.radians(45))
    print('fwhm=8', ans*2, err)
    ans, err = quad(f3, 0, np.radians(45))
    print("poly", ans, err)
    #plt.plot(x, f(x))
    #plt.show()

if __name__ == '__main__':
    test()
