# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 09:44:37 2018

@author: ian
"""
import os
import utilities as u


def fixTSX(sensorfile,cwfile,ispfile) :
    ''' generats an ISP file for TSX '''
    myArgs=[sensorfile,cwfile,ispfile]
    u.callMyProg('par_MSP',myArgs=myArgs,screen=True)
    
    
def checkSARFiles(path,orbit1,frame,sensorInfo,myLogger=None,resetPar=False) :
    ''' check files and build a dictionary with relevant file names
    path - path for slc
    orbit1 - orbit for slc
    frame - frame for slc
    nlooksR,nlooksA - standard number looks for geodat
    slcLooks - if single slc res use [1], if multiple slc resolutions [3,1] as in CSK  
    return a dict with slcfiles
    'geo','isppar', 'slc', 'cwpar','par','sensorpar','scl3...','geo3'
    '''
    if myLogger != None :
        myLogger.logEntry('checkSARFiles')
    #
    # sensor specifics
    nlooksR,nlooksA=sensorInfo['nlooksR'],sensorInfo['nlooksA']
    slcFiles={'slc' : '{0:d}_{1:d}.slc'.format(orbit1,frame),'par': 'p{0:d}_{1:d}.slc.par'.format(orbit1,frame),
              'cwpar': 'p{0:d}_{1:d}.slc.par.cw'.format(orbit1,frame),'sensorpar' : sensorInfo['sensorpar']}
    #
    # update with low res versions
    lowResSLCs={}
    # if there is 1 case, ignore
    slcLow=[x for x in sensorInfo['subSLC'] if x > 1 ]
    for looks in slcLow :
        for myKey in slcFiles.keys() :
            tmp=myKey+'{0:d}'.format(looks)
            lowResSLCs[ tmp ]=slcFiles[myKey].replace('.slc','.{0:d}x{0:d}.slc'.format(looks))
        lowResSLCs['geo'+'{0:d}'.format(looks)]= 'geodat{0:d}.{1:d}x{2:d}.in'.format(looks,nlooksR,nlooksA)
    
    # other files
    slcFiles['geo']= 'geodat{0:d}x{1:d}.in'.format(nlooksR,nlooksA)
    # fix inconsistent naming convention
    #ispSuffix={'CSK' : '.cw', 'S1' : '', 'TSX' : '.cw'}   
    slcFiles['isppar']= '{0:d}_{1:d}.slc.par{2:s}'.format(orbit1,frame,sensorInfo['ispSuffix'])
   
    if not os.path.exists(path+'/'+slcFiles['isppar']) or resetPar :
        fixTSX(path+'/'+slcFiles['sensorpar'],path+'/'+slcFiles['cwpar'],path+'/'+slcFiles['isppar'])
    # merge lists
    slcFiles={**slcFiles,**lowResSLCs}
    #
    for myKey in slcFiles.keys() :
        slcFile=path+'/'+slcFiles[myKey]
        if not os.path.exists(slcFile) :
            u.myerror('missing {0:s}'.format(slcFile))
    if myLogger != None :
        myLogger.logReturn('checkSARFiles')
    return slcFiles