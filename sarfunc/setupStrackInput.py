# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 11:59:29 2018

@author: ian
"""
import utilities as u
import sarfunc as s
import os


def writeStrackKeyValue(fpStrack, keyword, value, comment=None):
    if comment is None:
        print(f'{keyword} (-) = {value}', file=fpStrack)
    else:
        print(keyword, file=fpStrack)


def writeStrackImages(slcFiles1, slcFiles2, slcScale, orbit2, frame, fpStrack,
                      myPath=''):
    #
    path2 = os.path.join(myPath, f'../{orbit2:d}_{frame:0}')
    path1 = os.path.join(myPath, '')
    #
    writeStrackKeyValue(fpStrack, ';\n; inputs\n;', '', comment=True)
    writeStrackKeyValue(fpStrack, 'image1',
                        f"{os.path.join(path1, slcFiles1['slc'+slcScale])}")
    writeStrackKeyValue(fpStrack, 'image2',
                        f"{os.path.join(path2, slcFiles2['slc'+slcScale])}")
    writeStrackKeyValue(fpStrack, 'image1par',
                        f"{os.path.join(path1,slcFiles1['par'+slcScale])}")
    writeStrackKeyValue(fpStrack, 'image2par',
                        f"{os.path.join(path2,slcFiles2['par'+slcScale])}")


def writeImageBlock(sensorInfo, orbit1, frame, scaleDelta, fpStrack,
                    myPath=''):
    # write the parameters for the region to process
    writeStrackKeyValue(fpStrack, ';\n; params\n;', '', comment=True)
    writeStrackKeyValue(fpStrack, 'rStart', f"{sensorInfo['rStart']}")
    writeStrackKeyValue(fpStrack, 'aStart', f"{sensorInfo['aStart']}")
    writeStrackKeyValue(fpStrack, 'deltaR',
                        f"{scaleDelta*sensorInfo['deltaR']}")
    writeStrackKeyValue(fpStrack, 'deltaA',
                        f"{scaleDelta*sensorInfo['deltaA']}")
    #
    writeStrackKeyValue(fpStrack, ';', '', comment=True)
    nR, nA = s.sizeOffsets(sensorInfo, scaleDelta, orbit1, frame,
                           myPath=myPath)
    writeStrackKeyValue(fpStrack, 'nR', f"{nR:d}")
    writeStrackKeyValue(fpStrack, 'nA', f"{nA:d}")
    writeStrackKeyValue(fpStrack, ';', '', comment=True)


def openStrackInput(sensorInfo, orbit1, orbit2, frame, scaleFactor,
                    register=False, filenameModifier=''):
    ''' open strackinput file and comput scaleDelta (scale for sim
    registration offsets), and slcScale (for naming looked down slcs)'''
    # defaults
    nameStr = 'strackin.'
    slcScale = ''
    scaleDelta = 1
    if register:
        if scaleFactor < 1 or scaleFactor > 4:
            u.myerror(f'setupStrackInput: invalid scaleFactor {scaleFactor}')
        #
        outputFile = f'{orbit1}_{frame}.{orbit2}_{frame}.register.offsets'
        nameStr = f'strackRegister.{scaleFactor}.'
        # if > 1, add factor to name
        if scaleFactor > 1:
            slcScale = f"{scaleFactor}"
            outputFile += f'.{slcScale}'
        scaleDelta = sensorInfo['scaleDelta']
    else:
        outputFile = \
            f'{orbit1}_{frame}.{orbit2}_{frame}.offsets{filenameModifier}'
    # open file
    strackFile = f'{nameStr}{orbit1}_{orbit2}_{frame}{filenameModifier}'
    fpStrack = open(strackFile, 'w')
    return fpStrack, scaleDelta, slcScale, strackFile, outputFile


def writeInterferogramFile(sensorInfo, slcFiles1, orbit1, orbit2, frame,
                           slcScale, register, fastTrack, fpStrack, myPath=''):
    ''' write the interferogram file if requested by the modes '''
    # always write the geodat (might be used by others)
    writeStrackKeyValue(fpStrack, 'intgeodat',
                        os.path.join(myPath, slcFiles1[f'geo{slcScale}']))
    # interferogram not used for fast tracking or no complex mathching

    # set up regist file name stuff
    if register:
        baseParamsSuffix = '.reg'
    else:
        baseParamsSuffix = ''
    # note this writes baseparams even for no complex because it causes
    # strack to read the geodat
    basePar = f'P{orbit1}_{frame}.P{orbit2}_{frame}.params{baseParamsSuffix}'
    writeStrackKeyValue(fpStrack, 'baseparams', basePar)
    if fastTrack or sensorInfo['noComplexRegMatch'] or \
            sensorInfo['noComplexMatch']:
        return
    #
    if sensorInfo['useInt'] and not register:
        ifgFile = os.path.join(myPath,
                               s.ifgFilename(orbit1, orbit2, frame, sensorInfo,
                                             reflat=True))
        if not os.path.exists(ifgFile):
            u.myerror(f'Use inteferogram for tracking requested, but {ifgFile}'
                      ' does not exist')
        # output intfile
        writeStrackKeyValue(fpStrack, 'intfile', ifgFile)


def writeInitialOffsets(orbit1, orbit2, frame, fpStrack, myPath=''):
    initOffsetFile = os.path.join(myPath,
                                  f'{orbit1}_{frame}.{orbit2}_{frame}.off')
    writeStrackKeyValue(fpStrack, 'initialoffsetfile', initOffsetFile)


def writeMatchParams(sensorInfo, scaleFactor, fpStrack,
                     fastTrack=False, fastParams=None, register=False):
    if fastTrack:
        if fastParams is None:
            u.myerror('setupStrackInput, writeMatchParams: fastTrack True but '
                      'fastParams = None ')
        wra, waa = fastParams['wra'], fastParams['waa']
        navgr, navga = fastParams['navgr'], fastParams['navga']
        # edgePad=fastParams['edgePad']
    else:
        # setup window size key
        if register:
            wModifier = 'Hi'  # register offsets window on full res
            if scaleFactor > 1:
                wModifier = 'Low'  # register offsets window on low res
        else:
            wModifier = 'Offsets'  # regiser offsets for main speckle tracing
        wra, waa = sensorInfo[f'wra{wModifier}'], sensorInfo[f'waa{wModifier}']
        navgr, navga = 1, 1
    #
    # now write everything
    writeStrackKeyValue(fpStrack, 'wr', f"{sensorInfo['wr']}")
    writeStrackKeyValue(fpStrack, 'wa', f"{sensorInfo['wa']}")
    writeStrackKeyValue(fpStrack, 'wra', f"{wra}")
    writeStrackKeyValue(fpStrack, 'waa', f"{waa}")
    writeStrackKeyValue(fpStrack, ';', '', comment=True)
    if fastTrack:
        writeStrackKeyValue(fpStrack, 'EdgeR', f"{fastParams['edgePadR']}")
        writeStrackKeyValue(fpStrack, 'EdgeA', f"{fastParams['edgePadA']}")
    else:
        writeStrackKeyValue(fpStrack, 'scalefactor', f"{scaleFactor}")
    writeStrackKeyValue(fpStrack, ';', '', comment=True)
    writeStrackKeyValue(fpStrack, 'navgr', f"{navgr}")
    writeStrackKeyValue(fpStrack, 'navga', f"{navga}")


def writeOutputFiles(outputFile, fpStrack):
    writeStrackKeyValue(fpStrack, ';\n; Output file\n;', '', comment=True)
    writeStrackKeyValue(fpStrack, 'outputFile', outputFile)


def writeMaskFile(maskFile, fpStrack, myPath='', maskVrt=None):
    if maskFile is None:
        return
    # have file, so write
    writeStrackKeyValue(fpStrack, 'offsetmaskfile',
                        os.path.join(myPath, maskFile))
    if maskVrt is not None:
        writeStrackKeyValue(fpStrack, 'offsetmaskvrt',
                            os.path.join(myPath, maskVrt))
    else:
        maskDat = os.path.join(myPath,
                               '.'.join(maskFile.split('.')[0:-1])+'.dat')
        writeStrackKeyValue(fpStrack, 'offsetmaskdat', maskDat)


def writeInitShifts(initShifts, fpStrack, myPath=''):
    if initShifts is None:
        return
    writeStrackKeyValue(fpStrack, 'initshift', os.path.join(myPath,
                                                            initShifts))


def setupStrackInput(slcFiles1, slcFiles2, sensorInfo, orbit1, orbit2, frame,
                     scaleFactor, initShifts, maskFile, register=False,
                     myLogger=None, myPath='', fastTrack=False,
                     fastParams=None, filenameModifier='',
                     maskPath='', initShiftsPath='', setupOnly=False,
                     maskVrt=None):
    '''
    Set up input file for speckle tracker
    Note myPath applies to almost everything and is generally going to
    be .. for fast tracking. maskPath and initShiftsPath are seperate because
    they reside in . for fast tracking. The seperate paths
    will likely never be used but are included just in case.
    '''
    # open logger
    if myLogger is not None:
        myLogger.logEntry('setupStrackInput')
    # open input file, determine output file, and scaleDelta and slcScale
    fpStrack, scaleDelta, slcScale, strackFile, outputFile = \
        openStrackInput(sensorInfo, orbit1, orbit2, frame, scaleFactor,
                        register=register, filenameModifier=filenameModifier)
    # this is to make cull only work if some files have been erased.
    #
    writeStrackImages(slcFiles1, slcFiles2, slcScale, orbit2, frame,
                      fpStrack, myPath=myPath)
    # Decide whether to write interferogram to file
    writeInterferogramFile(sensorInfo, slcFiles1, orbit1, orbit2, frame,
                           slcScale, register, fastTrack, fpStrack,
                           myPath=myPath)
    # write cw offset poly nomial (may remove at some pointmo)
    writeInitialOffsets(orbit1, orbit2, frame, fpStrack, myPath=myPath)
    # rStart,aStart,deltaR,deltaA
    writeImageBlock(sensorInfo, orbit1, frame, scaleDelta, fpStrack,
                    myPath=myPath)
    #
    writeMatchParams(sensorInfo, scaleFactor, fpStrack, fastTrack=fastTrack,
                     fastParams=fastParams, register=register)
    #
    writeOutputFiles(outputFile, fpStrack)
    # initial shift file
    writeMaskFile(maskFile, fpStrack, myPath=maskPath, maskVrt=maskVrt)
    #
    writeInitShifts(initShifts, fpStrack, myPath=initShiftsPath)

    fpStrack.close()
    #u.myerror("STOP")
    if myLogger is not None:
        myLogger.logReturn('setupStrackInput')
    return strackFile, outputFile
