# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 13:07:03 2018

@author: ian
"""
import utilities as u
import os
import stat


def offFileNames(offsetFile, scaleFactor, register=False, fastCull=False):
    ''' make offsets file names for generating cull files (makeCullFile)'''
    # main offsets types
    offTypes = ['dr', 'da']
    offFiles = []
    interpString = ['.interp', ''][fastCull]
    for offType in offTypes:
        offFiles.append(f'{offsetFile}.cull{interpString}.{offType}')
    # add extra stuff for full offsets (uncertainties)
    if register:
        sF = ''
        if scaleFactor > 1:
            sF = f'.{scaleFactor:d}'
        datFiles = []
        for off in offTypes:
            datFiles.append(f'register.offsets{sF}.{off}.dat')
            datFiles.append(f'{offsetFile}.cull.interp.{off}.dat')
    elif fastCull:
        offTypes += ['sa', 'sr']
        datFiles = [x+'.dat' for x in offFiles]
        datFiles += [x.replace('speckle', 'smooth') for x in datFiles]
        offFiles += [x.replace('.d', '.s') for x in offFiles]
        offFiles = [x.replace('.speckle', '.merge') for x in offFiles]
    else:  # main offsets
        offTypes += ['sa', 'sr']
        # ***
        offFiles += ['azimuth.offsets.slow.sa', 'range.offsets.slow.sr']
        datFiles = ['azimuth.offsets.slow.sa.dat', 'range.offsets.slow.sr.dat',
                    'azimuth.offsets.dat', 'range.offsets.dat']
    # print(offFiles)
    # print(datFiles)
    return offTypes, offFiles, datFiles


def cullSetupStuff(register, fastCull, scaleFactor, sensorInfo, offsetFile,
                   smoothFile=None, mergeFile=None):
    if register and not fastCull:
        cullFile = 'runCullReg{0:d}'.format(scaleFactor)
        cullParams = sensorInfo['regCull']
        interpParams = sensorInfo['regInterp']
        # add scale factor in register.offsets unless 1, then skip
        scaleString = ''
        if scaleFactor > 1:
            scaleString = '.{0:d}'.format(scaleFactor)
        cleanScript = [f'regOffsetsMerge.py {offsetFile}.cull.interp '
                       f' {sensorInfo["offsetsRegBase"]} '
                       f'register.offsets{scaleString}']
    elif fastCull and not register:
        cullFile = 'runFastCull'
        cullParams = sensorInfo['fastCull']
        interpParams = sensorInfo['normalInterp']
        cleanScript = ['pushd ..', 'cleanoff', 'popd']
    #
    # normal offset culling
    else:
        cullFile = 'runcull'
        cullParams = sensorInfo['normalCull']
        interpParams = sensorInfo['normalInterp']
        cleanScript = ['cleanoff']
    return cullFile, cullParams, interpParams, cleanScript


def cullCommand(offsetFile, cullParams, register, sensorInfo, fpCull):
    # cull command
    print('cullst ', file=fpCull, end='')
    # add sime for offsets with regular culling if requested
    if not register and sensorInfo['useSimWithCull']:
        print(f' -useSim {sensorInfo["offsetsBase"]} ', file=fpCull, end='')
    # loop through keys - used sorted to maintain consistent order
    for key in sorted(cullParams.keys()):
        # Hack to double corrThresh for smooth case
        if key == 'corrThresh' and 'smooth' in offsetFile:
            scale = 2
        else:
            scale = 1
        print(' -{0:s} {1:s} '.format(key, str(cullParams[key] * scale)),
              file=fpCull, end='')
    print(offsetFile, offsetFile+'.cull', file=fpCull)


# interp commands
def interpCommands(offsetFile, offTypes, offFiles, interpParams, fpCull,
                   fastCull=False, register=False):
    ''' write interp commands for culled data to file'''
    for offType, offFile in zip(offTypes, offFiles):
        print('#', file=fpCull)
        print(f'intfloat {interpParams["flags"]} -nr $NR -na $NA ',
              file=fpCull, end='')
        print(f'-ratThresh {interpParams["ratThresh"]} '
              f'-thresh {interpParams["thresh"]} ', file=fpCull, end='')
        # for regular tracking use islandCull
        if not register and not fastCull:
            print(f'-islandThresh {interpParams["islandThresh"]}  ',
                  file=fpCull, end='')
        print('\\', file=fpCull)
        # kluge for old naming conv.that doesnot include interp in sa,sr names
        nameStr = ''
        # only do interp on da/dr not sa/sr
        if offType in ['da', 'dr'] or fastCull:
            nameStr = '.cull'
        print(f'{offsetFile}{nameStr}.{offType} > {offFile}', file=fpCull)


def makeCullFile(sensorInfo, offsetFile, orbit1, orbit2, frame, scaleFactor,
                 register=False, myLog=None, fastCull=False, noDatFiles=True):
    ''' make a script to runcull and interpolate the results for
    registration offsets'''
    if myLog is not None:
        myLog.logEntry('makeCullFile')
    #
    # set upfor culling mode
    cullFile, cullParams, interpParams, cleanScript = \
        cullSetupStuff(register, fastCull, scaleFactor, sensorInfo, offsetFile,
                       smoothFile=offsetFile.replace('.speckle', '.smooth'),
                       mergeFile=offsetFile.replace('.speckle', '.merge'))
    # interpolated output file names
    offTypes, offFiles, datFiles = \
        offFileNames(offsetFile, scaleFactor, register=register,
                     fastCull=fastCull)
    #
    fpCull = open(cullFile, 'w')
    # gget offset size data
    tOff = u.offsets(fileRoot=offsetFile+'.da', datFile=offsetFile+'.dat')
    tOff.readOffsetsDat()
    nr, na = tOff.nr, tOff.na
    #
    # image size info
    print('#\nset NR={0:d}\nset NA={1:d}\n#'.format(nr, na), file=fpCull)
    #
    cullCommand(offsetFile, cullParams, register, sensorInfo, fpCull)
    # add second call
    if fastCull:
        cullCommand(offsetFile.replace('.speckle', '.smooth'), cullParams,
                    register, sensorInfo, fpCull)
    else:
        interpCommands(offsetFile, offTypes, offFiles, interpParams, fpCull,
                       register=register)
    #
    # copy dat files
    print('#', file=fpCull)
    if not noDatFiles: 
        for datFile in datFiles:
            print(f'cp {offsetFile}.dat {datFile}', file=fpCull)
    # fast cull interp
    if fastCull:
        # do the merge
        fileSmooth = offsetFile.replace('.speckle', '.smooth')
        fileMerge = offsetFile.replace('.speckle', '.merge')
        print(f'#\nmergefast.py {offsetFile}.cull {fileSmooth}.cull '
              f'{fileMerge} {sensorInfo["sensor"]}\n#', file=fpCull)
        # do the interpolation: 6/26/2019 added mergeRoot to force correct file
        print(f'processfast.py -mergeRoot={fileMerge} ', file=fpCull, end='')
        for myKey in sensorInfo['processFastParams'].keys():
            print(f'-{myKey}={sensorInfo["processFastParams"][myKey]} ',
                  file=fpCull, end='')
        print('\n#', file=fpCull)
    #
    # clean script
    print('#', file=fpCull)
    for line in cleanScript:
        print(line, file=fpCull)
    print('#', file=fpCull)
    fpCull.close()
    os.chmod(cullFile, os.stat(cullFile).st_mode | stat.S_IEXEC)
    #
    if myLog is not None:
        myLog.logReturn('makeCullFile')
    return cullFile
