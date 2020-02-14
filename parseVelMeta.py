#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:36:02 2019

@author: ian
"""
import utilities as u
import os

def parseVelMeta(metaFile) :
    ''' parse a meta file, return results as a dict '''
    if not os.path.exists(metaFile) :
        u.myerror(f'parseVelMeta : meta file ({metaFile}) does not exist')
    # read all results
    try :
        fp=open(metaFile)
        myDict={}
        for line in fp :
            if '=' in line :
                key,value=[x.strip() for x in line.split('=')]
                myDict[key]=value
    except :
        u.myerror(f'parseVelMeta : error reading meta file ({metaFile}) ')
    return myDict

            