# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 12:10:03 2018

@author: ian
"""
import os

def processCWLine(line,myType) :
    pieces=line.split()
    return(myType(pieces[1]))
    
def slcParams(orbit,frame,myPath='') :
    parfile=os.path.join(myPath,'p{0:d}_{1:d}.slc.par.cw'.format(orbit,frame))
    fpPar=open(parfile,'r')
    for line in fpPar :
        if 'azimuth_pixels' in line :
            azLines=processCWLine(line,int)
        elif 'range_pixels' in line :
            rgLines=processCWLine(line,int)
    fpPar.close()
    return rgLines,azLines
    
def sizeOffsets(sensorInfo,scaleDelta,orbit1,frame,myPath='') :
    sR,sA=slcParams(orbit1,frame,myPath=myPath)
    nR=int( ( (sR-2*sensorInfo['rStart'])/(scaleDelta*sensorInfo['deltaR']))/6)*6
    nA=int( ( (sA-2*sensorInfo['aStart'])/(scaleDelta*sensorInfo['deltaA']))/6)*6
    return nR,nA