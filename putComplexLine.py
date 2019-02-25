# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 09:39:25 2018

@author: ian
"""

from sarfunc.complex16 import complex16 

def putComplexLine(fp,cType,buf) :
    ''' write a complex line either as default complex type
    or convert to non-standar c4 or >c4'''
    # handle my custom type
    if 'c4' in cType :    
        buf=complex16(buf,16000.)
        if '>' in cType :
           buf.byteswap(True)
    buf.tofile(fp)
        