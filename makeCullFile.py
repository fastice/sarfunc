# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 13:07:03 2018

@author: ian
"""
import utilities as u
import os
import stat


def offFileNames(offsetFile,scaleFactor,register=False,fastCull=False) :
    ''' make offsets file names for generating cull files (makeCullFile)'''
    # main offsets types
    offTypes=['dr','da']
    offFiles=[]
    interpString=['.interp',''][fastCull]
    for offType in offTypes :
        offFiles.append('{0:s}.cull{1:s}.{2:s}'.format(offsetFile,interpString,offType))
    # add extra stuff for full offsets (uncertainties)
    if register :
        sF=''
        if scaleFactor > 1 :
            sF='.{0:d}'.format(scaleFactor)
        datFiles=[]
        for off in offTypes :
            datFiles.append('register.offsets{0:s}.{1:s}.dat'.format(sF,off))
            datFiles.append('{0:s}.cull.interp.{1:s}.dat'.format(offsetFile,off))  
    elif fastCull :
        offTypes +=['sa','sr']
        datFiles=[x+'.dat' for x in offFiles]
        datFiles+=[x.replace('speckle','smooth') for x in datFiles]
        offFiles+=[x.replace('.d','.s') for x in offFiles]
        offFiles=[x.replace('.speckle','.merge') for x in offFiles]
    # main offsets
    else :
        offTypes +=['sa','sr']
        offFiles+=['azimuth.offsets.sa','range.offsets.sr']
        datFiles=['azimuth.offsets.dat','range.offsets.dat']
    print(offFiles)
    print(datFiles)
    return offTypes,offFiles,datFiles
    
def cullSetupStuff(register,fastCull,scaleFactor,sensorInfo,offsetFile,smoothFile=None,mergeFile=None) :
    if register and not fastCull :
        cullFile='runCullReg{0:d}'.format(scaleFactor)
        cullParams=sensorInfo['regCull']
        interpParams=sensorInfo['regInterp']
        # add scale factor in register.offsets unless 1, then skip
        scaleString=''
        if scaleFactor > 1 :
            scaleString='.{0:d}'.format(scaleFactor)
        cleanScript=['regOffsetsMerge.py {0:s}.cull.interp {1:s} register.offsets{2:s}'.format(
               offsetFile,sensorInfo['offsetsRegBase'],scaleString)  ] 
    elif fastCull and not register :
        cullFile='runFastCull'
        cullParams=sensorInfo['fastCull']
        interpParams=sensorInfo['normalInterp']
        cleanScript=['pushd ..','cleanoff','popd']
    #
    # normal offset culling
    else : 
        cullFile='runcull'
        cullParams=sensorInfo['normalCull']
        interpParams=sensorInfo['normalInterp']
        cleanScript=['cleanoff']
        
    return cullFile,cullParams,interpParams,cleanScript
    
def cullCommand(offsetFile,cullParams,register,sensorInfo,fpCull) :
    # cull command
    print('cullst ',file=fpCull,end='')
    # add sime for offsets with regular culling if requested
    if not register and sensorInfo['useSimWithCull'] :
        print(' -useSim {1:s} '.format(sensorInfo['offsetsBase']),file=fpCull,end='') 
    # loop through keys - used sorted to maintain consistent order
    for key in sorted(cullParams.keys()) :
        print(' -{0:s} {1:s} '.format(key,str(cullParams[key])),file=fpCull,end='')
    print(offsetFile,offsetFile+'.cull',file=fpCull)
    
    
# interp commands
def interpCommands(offsetFile,offTypes,offFiles,interpParams,fpCull,fastCull=False,register=False) :
    ''' write interp commands for culled data to file'''
    for offType,offFile in zip(offTypes,offFiles) :
         print('#',file=fpCull) 
         print('intfloat {0:s} -nr $NR -na $NA '.format(interpParams['flags']),file=fpCull,end='')
         print('-ratThresh {0:d} -thresh {1:d} '.format(interpParams['ratThresh'],interpParams['thresh']),file=fpCull,end='')
         # for regular tracking use islandCull
         if not register and not fastCull :
             print('-islandThresh {0:d}  '.format(interpParams['islandThresh']),file=fpCull,end='')   
         print('\\',file=fpCull)
         # kluge to deal with old nameing convention that does not include interp in sa,sr names
         nameStr=''
         # only do interp on da/dr not sa/sr
         if offType in ['da','dr'] or fastCull:
             nameStr='.cull'
         print('{0:s}{1:s}.{2:s} > {3:s}'.format(offsetFile,nameStr,offType,offFile),file=fpCull)    
    
def makeCullFile(sensorInfo,offsetFile,orbit1,orbit2,frame,scaleFactor,register=False,myLog=None,fastCull=False) :
    ''' make a script to runcull and interpolate the results for registration offsets'''
    if myLog != None :
        myLog.logEntry('makeCullFile')
    #
    # set upfor culling mode
    cullFile,cullParams,interpParams,cleanScript=cullSetupStuff(register,fastCull,scaleFactor,sensorInfo,offsetFile,
                                                                smoothFile=offsetFile.replace('.speckle','.smooth'),
                                                                mergeFile=offsetFile.replace('.speckle','.merge'))
    # interpolated output file names
    offTypes,offFiles,datFiles=offFileNames(offsetFile,scaleFactor,register=register,fastCull=fastCull)
    #
    fpCull=open(cullFile,'w')
    # gget offset size data
    tOff=u.offsets(fileRoot=offsetFile+'.da',datFile=offsetFile+'.dat')
    tOff.readOffsetsDat()
    nr,na=tOff.nr,tOff.na
    #
    # image size info
    print('#\nset NR={0:d}\nset NA={1:d}\n#'.format(nr,na),file=fpCull)
    #
    cullCommand(offsetFile,cullParams,register,sensorInfo,fpCull)
    # add second call
    if fastCull :
        cullCommand(offsetFile.replace('.speckle','.smooth'),cullParams,register,sensorInfo,fpCull)  
    else :
        interpCommands(offsetFile,offTypes,offFiles,interpParams,fpCull,register=register)
    #
    # copy dat files
    print('#',file=fpCull)
    for datFile in datFiles :
         print('cp {0:s}.dat {1:s}'.format(offsetFile,datFile),file=fpCull)
    # fast cull interp
    if fastCull :
        # do the merge
        print('#\nmergefast.py {0:s}.cull {1:s}.cull {2:s} {3:s}\n#'.format(offsetFile,
              offsetFile.replace('.speckle','.smooth'),offsetFile.replace('.speckle','.merge'),sensorInfo['sensor']),file=fpCull)
        # do the interpolation
        print('processfast.py ',file=fpCull,end='')
        for myKey in sensorInfo['processFastParams'].keys() :
            print('-{0:s}={1:d} '.format(myKey,sensorInfo['processFastParams'][myKey]),file=fpCull,end='')
        print('\n#',file=fpCull)
    #
    # clean script
    print('#',file=fpCull) 
    for line in cleanScript :
        print(line,file=fpCull)
    print('#',file=fpCull) 
    fpCull.close()
    os.chmod(cullFile,os.stat(cullFile).st_mode | stat.S_IEXEC)
    #
    if myLog != None :
        myLog.logReturn('makeCullFile')
    return cullFile