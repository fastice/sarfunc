# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 15:37:55 2018

@author: ian
"""
import utilities as u

def read3Floats(line):
    try :
        poly=[float(x) for x in line.split() ]
        if len(poly) != 3 :
            raise NameError()  
        return poly
        
    except Exception :
        u.myerror('Problem reading offset poly file {0:s}'.format(fileName))  
    
def readOffPoly(fileName) :
    ''' read an offset poly file produced by simoffsets'''
    fp=open(fileName)
    count=0
    for line in fp :
        if '#' not in line :
            if count == 0 :
                rangePoly=read3Floats(line)
                count+=1
            else :
                azPoly=read3Floats(line)
                return rangePoly,azPoly
                
    u.myerror('Problem reading offset poly file {0:s}'.format(fileName))
            
    