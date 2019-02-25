# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 12:07:22 2018

@author: ian
"""

def ifgFilename(orbit1,orbit2,frame,sensorInfo,reflat=False) :
    if reflat :
        suffix='.flatc.reflat'
    else :
        suffix=''
    return '{0:d}_{2:d}.{1:d}_{2:d}.{3:d}x{4:d}.int{5:s}'.format(orbit1,orbit2,frame,sensorInfo['intLooksR'],sensorInfo['intLooksA'],suffix)