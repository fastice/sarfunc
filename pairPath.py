# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:25:11 2018

@author: ian
"""
import os

def pairPath(orbit1,orbit2,frame1,frame2,myPath1=None,myPath2=None) :
    ''' This just creates the paths for a pair of images. This simple
    routine is so that information is applied in one place in case future renaming
    scheme is used.; In this case orbit1,and frame 1 are not used, but they might in the future'''
    path1,path2='.','../{0:d}_{1:d}'.format(orbit2,frame2)
    if myPath1 != None :
        path1=os.path.join(myPath1,path1)
    if myPath2 != None :
        path2=os.path.join(myPath2,path2)    
    return path1,path2