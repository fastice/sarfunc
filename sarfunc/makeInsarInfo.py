# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:18:40 2018

@author: ian
"""

def makeInsarInfo(orbit1,orbit2,path1,path2,frame,sensorInfo,slcFiles1,slcFiles2) :
    ''' create a dictonary with all of the interferogram generation relevant files '''
    insarInfo={}
    insarInfo['off']='{0:d}_{2:d}.{1:d}_{2:d}.off'.format(orbit1,orbit2,frame)
    insarInfo['ifg']='{0:d}_{2:d}.{1:d}_{2:d}.{3:d}x{4:d}.int'.format(orbit1,orbit2,frame,sensorInfo['intLooksR'],sensorInfo['intLooksA'])
    insarInfo['regOff']='register.offsets'
    insarInfo['pwr1']='{0:d}_{2:d}.{1:d}_{2:d}.pwr1'.format(orbit1,orbit2,frame)
    insarInfo['pwr2']='{0:d}_{2:d}.{1:d}_{2:d}.pwr2'.format(orbit1,orbit2,frame)
    insarInfo['intLooksR']=sensorInfo['intLooksR']
    insarInfo['intLooksA']=sensorInfo['intLooksA']
    insarInfo['slc1']=slcFiles1['slc']
    insarInfo['slc2']=slcFiles2['slc']
    insarInfo['isppar1']=slcFiles1['isppar']
    insarInfo['isppar2']=slcFiles2['isppar']
    insarInfo['insarGeo']= 'geodat{0:d}x{1:d}.in'.format(insarInfo['intLooksR'],insarInfo['intLooksA']) 
    
    insarInfo['newBase']='{0:d}_{2:d}.{1:d}_{2:d}.base'.format(orbit1,orbit2,frame)
    insarInfo['oldBase']='P{0:d}_{2:d}.P{1:d}_{2:d}.base'.format(orbit1,orbit2,frame)
    insarInfo['params']='P{0:d}_{2:d}.P{1:d}_{2:d}.params'.format(orbit1,orbit2,frame)
    #
    return insarInfo