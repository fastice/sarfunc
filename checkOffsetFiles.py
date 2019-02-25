# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 12:19:05 2018

@author: ian
"""
import utilities as u
import os

def checkOffsetFiles(offsetFile,myLog=None) :
    ''' checks that offsets both exist and are the correct size'''
    if myLog  != None :
        myLog.logEntry('checkOffsetFiles')
    #
    if not os.path.exists(offsetFile+'.dat') :
        u.myerror('Missing offsets dat file {0:s}'.format(offsetFile+'.dat'))
    try :
        r0,a0,nr,na,dr,da=readOffsetDat(offsetFile) 
    except :
        u.myerror('Error reading offsets dat file {0:s}'.format(offsetFile+'.dat'))
    #
    mySize=nr*na*4
    suffixes=['.dr','.da']
    for suffix in suffixes :
        # check exists
        if not os.path.exists(offsetFile+suffix) :
            u.myerror('Missing offset file {0:s}'.format(offsetFile+suffix))
        # check size
        else :
            statinfo=os.stat(offsetFile+suffix)
            fileSize=statinfo.st_size
            if fileSize != mySize :
                u.myerror('Offset file {0:s} should have {1:d} bytes but only has {2:d} bytes'.format(offsetFile+suffix,mySize,fileSize),myLogger=myLog)
    
    if myLog  != None :
       myLog.logReturn('checkOffsetFiles')