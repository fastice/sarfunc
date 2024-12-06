# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:46:24 2018

@author: ian
"""
import numpy as np

def getBinDataLine(fp,cType,lSize) :
    ''' get a line of type cType, with lSize samples'''
    buf=np.fromfile(fp,dtype=cType,count=lSize)
    return buf    