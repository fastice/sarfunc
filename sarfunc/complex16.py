# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:40:36 2018

@author: ian
"""
import numpy as np

def complex16(x,scale) : 
    ''' convert line buffer to complex16'''
    c=list(x.shape)
    c[0]*=2
    xInt=np.zeros(tuple(c),dtype='int16')
    xInt[0::2]=(scale*x.real).astype('int16')
    xInt[1::2]=(scale*x.imag).astype('int16')
    return xInt
    