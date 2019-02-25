# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 11:59:29 2018

@author: ian
"""
import utilities as u
import sarfunc as s
import os

def writeStrackKeyValue(fpStrack,keyword,value,comment=None) :
    if comment == None :
        print(keyword+'  (-) = '+value ,file=fpStrack)
    else :
        print(keyword ,file=fpStrack) 
        
def writeStrackImages(slcFiles1,slcFiles2,slcScale,orbit2,frame,fpStrack,myPath='') :
    #
    path2=os.path.join(myPath,'../{0:d}_{1:0}'.format(orbit2,frame))
    path1=os.path.join(myPath,'')
    #
    writeStrackKeyValue(fpStrack,';\n; inputs\n;','',comment=True)
    writeStrackKeyValue(fpStrack,'image1','{0:s}'.format(os.path.join(path1,slcFiles1['slc'+slcScale]))  )
    writeStrackKeyValue(fpStrack,'image2','{0:s}'.format(os.path.join(path2,slcFiles2['slc'+slcScale])))    
    writeStrackKeyValue(fpStrack,'image1par','{0:s}'.format(os.path.join(path1,slcFiles1['par'+slcScale]))  )
    writeStrackKeyValue(fpStrack,'image2par','{0:s}'.format(os.path.join(path2,slcFiles2['par'+slcScale]) ))
    
def writeImageBlock(sensorInfo,orbit1,frame,scaleDelta,fpStrack,myPath='') :
    # write the parameters for the region to process
    writeStrackKeyValue(fpStrack,';\n; params\n;','',comment=True)
    writeStrackKeyValue(fpStrack,'rStart','{0:d}'.format(sensorInfo['rStart'])) 
    writeStrackKeyValue(fpStrack,'aStart','{0:d}'.format(sensorInfo['aStart'])) 
    writeStrackKeyValue(fpStrack,'deltaR','{0:d}'.format(scaleDelta*sensorInfo['deltaR'])) 
    writeStrackKeyValue(fpStrack,'deltaA','{0:d}'.format(scaleDelta*sensorInfo['deltaA']))
    #
    writeStrackKeyValue(fpStrack,';','',comment=True) 
    nR,nA=s.sizeOffsets(sensorInfo,scaleDelta,orbit1,frame,myPath=myPath)
    writeStrackKeyValue(fpStrack,'nR','{0:d}'.format(nR)) 
    writeStrackKeyValue(fpStrack,'nA','{0:d}'.format(nA)) 
    writeStrackKeyValue(fpStrack,';','',comment=True) 
    
def openStrackInput(sensorInfo,orbit1,orbit2,frame,scaleFactor,register=False,filenameModifier='') :
    ''' open strackinput file and comput scaleDelta (scale for sim registration offsets),
    and slcScale (for naming looked down slcs)'''
    # defaults
    nameStr='strackin.' 
    slcScale=''
    scaleDelta=1    
    if register :
        if scaleFactor < 1 or scaleFactor > 4 :
            u.myerror('setupStrackInput: invalid scaleFactor {0:d}',scaleFactor)
        #
        outputFile='{0:d}_{2:d}.{1:d}_{2:d}.register.offsets'.format(orbit1,orbit2,frame)    
        nameStr='strackRegister.{0:d}.'.format(scaleFactor)
        # if > 1, add factor to name
        if scaleFactor > 1 :
            slcScale='{0:d}'.format(scaleFactor)
            outputFile+='.'+slcScale
        scaleDelta=sensorInfo['scaleDelta']
    else :
       outputFile='{0:d}_{2:d}.{1:d}_{2:d}.offsets{3:s}'.format(orbit1,orbit2,frame,filenameModifier)
    # open file
    strackFile=nameStr+'{0:d}_{1:d}_{2:d}{3:s}'.format(orbit1,orbit2,frame,filenameModifier)
    fpStrack=open(strackFile,'w') 
    return fpStrack,scaleDelta,slcScale, strackFile,outputFile   
    
def writeInterferogramFile(sensorInfo,slcFiles1,orbit1,orbit2,frame,slcScale,register,fastTrack,fpStrack,myPath='') :
    ''' write the interferogram file if requested by the modes '''
    # always write the geodat (might be used by others)
    writeStrackKeyValue(fpStrack,'intgeodat',os.path.join(myPath,slcFiles1['geo'+slcScale]))
    # interferogram not used for fast tracking or no complex mathching
   
    # set up regist file name stuff
    if register  :
        baseParamsSuffix='.reg'
    else :
        baseParamsSuffix=''
    # note this writes baseparams even for no complex because it causes strack to read the geodat
    writeStrackKeyValue(fpStrack,'baseparams',
                        'P{0:d}_{2:d}.P{1:d}_{2:d}.params{3:s}'.format(orbit1,orbit2,frame,baseParamsSuffix))
    if fastTrack or sensorInfo['noComplexRegMatch'] or sensorInfo['noComplexMatch'] :
        return
    #  
    if sensorInfo['useInt'] and not register :
        ifgFile=os.path.join(myPath,s.ifgFilename(orbit1,orbit2,frame,sensorInfo,reflat=True))
        if not os.path.exists(ifgFile) :
            u.myerror('Use inteferogram for tracking requested, but {0:s} does not exist'.format(ifgFile))
        # output intfile
        writeStrackKeyValue(fpStrack,'intfile',ifgFile)
        
def writeInitialOffsets(orbit1,orbit2,frame,fpStrack,myPath='') :
    initOffsetFile=os.path.join(myPath,'{0:d}_{2:d}.{1:d}_{2:d}.off'.format(orbit1,orbit2,frame))
    writeStrackKeyValue(fpStrack,'initialoffsetfile',initOffsetFile) 
    
def writeMatchParams(sensorInfo,scaleFactor,fpStrack,fastTrack=False,fastParams=None,register=False) :
    if fastTrack :
        if fastParams == None :
            u.myerror('setupStrackInput, writeMatchParams : fastTrack True but fastParams = None ')
        wra,waa=fastParams['wra'],fastParams['waa']
        navgr,navga=fastParams['navgr'],fastParams['navga']
        #edgePad=fastParams['edgePad']
    else :
        # setup window size key
        if register :
            wModifier='Hi' # register offsets window on full res
            if scaleFactor > 1 :
                wModifier='Low' # register offsets window on low res
        else :
            wModifier='Offsets' # regiser offsets for main speckle tracing
        wra,waa=sensorInfo['wra'+wModifier],sensorInfo['waa'+wModifier]
        navgr,navga=1,1
    #
    # now write everything
    writeStrackKeyValue(fpStrack,'wr','{0:d}'.format(sensorInfo['wr'])) 
    writeStrackKeyValue(fpStrack,'wa','{0:d}'.format(sensorInfo['wa'])) 
    writeStrackKeyValue(fpStrack,'wra','{0:d}'.format(wra)) 
    writeStrackKeyValue(fpStrack,'waa','{0:d}'.format(waa))
    writeStrackKeyValue(fpStrack,';','',comment=True) 
    if fastTrack :
        writeStrackKeyValue(fpStrack,'EdgeR','{0:d}'.format(fastParams['edgePadR']))
        writeStrackKeyValue(fpStrack,'EdgeA','{0:d}'.format(fastParams['edgePadA']))
    else :
        writeStrackKeyValue(fpStrack,'scalefactor','{0:d}'.format(scaleFactor))
    writeStrackKeyValue(fpStrack,';','',comment=True) 
    writeStrackKeyValue(fpStrack,'navgr','{0:d}'.format(navgr)) 
    writeStrackKeyValue(fpStrack,'navga','{0:d}'.format(navga)) 
    
def writeOutputFiles(outputFile,fpStrack):
    writeStrackKeyValue(fpStrack,';\n; Output file\n;','',comment=True)
    writeStrackKeyValue(fpStrack,'outputFile',outputFile)
    
def writeMaskFile(maskFile,fpStrack,myPath='') :        
    if maskFile == None :
        return
    # have file, so write
    writeStrackKeyValue(fpStrack,'offsetmaskfile','{0:s}'.format(os.path.join(myPath,maskFile))) 
    maskDat=os.path.join(myPath,'.'.join(maskFile.split('.')[0:-1])+'.dat')
    writeStrackKeyValue(fpStrack,'offsetmaskdat','{0:s}'.format(maskDat)) \
    
def writeInitShifts(initShifts,fpStrack,myPath='') :        
    if initShifts == None :
        return   
    writeStrackKeyValue(fpStrack,'initshift','{0:s}'.format(os.path.join(myPath,initShifts))) 
        
def setupStrackInput(slcFiles1,slcFiles2,sensorInfo,orbit1,orbit2,frame,scaleFactor,initShifts,maskFile,
                     register=False,myLogger=None,myPath='',fastTrack=False,fastParams=None,filenameModifier='',
                     maskPath='',initShiftsPath='') :
    ''' Set up input file for speckle tracker 
    Note myPath applies to almost everything and is generally going to be .. for fast tracking. 
    maskPath and initShiftsPath are seperate because they reside in . for fast tracking. The seperate paths 
    will likely never be used but are included just in case.'''
    # open logger
    if myLogger != None :
        myLogger.logEntry('setupStrackInput')
    # open input file, determine output file, and scaleDelta and slcScale
    fpStrack,scaleDelta,slcScale,strackFile,outputFile=openStrackInput(sensorInfo,orbit1,orbit2,frame,scaleFactor,
                                                            register=register,filenameModifier=filenameModifier)
    #
    writeStrackImages(slcFiles1,slcFiles2,slcScale,orbit2,frame,fpStrack,myPath=myPath)
    # Decide whether to write interferogram to file
    writeInterferogramFile(sensorInfo,slcFiles1,orbit1,orbit2,frame,slcScale,register,fastTrack,fpStrack,myPath=myPath)
    # write cw offset poly nomial (may remove at some pointmo)
    writeInitialOffsets(orbit1,orbit2,frame,fpStrack,myPath=myPath)
    # rStart,aStart,deltaR,deltaA
    writeImageBlock(sensorInfo,orbit1,frame,scaleDelta,fpStrack,myPath=myPath) 
    #
    writeMatchParams(sensorInfo,scaleFactor,fpStrack,fastTrack=fastTrack,fastParams=fastParams,register=register) 
    #
    writeOutputFiles(outputFile,fpStrack)
    # initial shift file
    writeMaskFile(maskFile,fpStrack,myPath=maskPath)
    #
    writeInitShifts(initShifts,fpStrack,myPath=initShiftsPath)
    
    fpStrack.close()
    if myLogger != None :
        myLogger.logReturn('setupStrackInput')
    return strackFile,outputFile