# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 09:59:44 2018

@author: ian
"""

import utilities as u
import math


def writeOldBase(insarInfo, b, db):
    ''' write old style base file - not sure if its really used any more'''
    fp = open(insarInfo['oldBase'], 'w')
    print(f'{b[0]:11.8f} {b[1]:11.4f} {b[2]:11.4f}', file=fp)
    print(f'{db[0]:11.8f} {db[1]:11.8f} {db[2]:11.8f}', file=fp)
    print('0.0000 0.0000 0.0000\n0.0000 0.0000 0.000\n0.0000', file=fp)
    fp.close()


def readBase(insarInfo):
    ''' read a new cw baseline file'''
    fp = open(insarInfo['newBase'], 'r')
    b, db = -1, -1
    for line in fp:
        if 'initial_baseline(TCN)' in line:
            b = [float(x) for x in line.split()[1:4]]
        elif 'initial_baseline_rate' in line:
            db = [float(x) for x in line.split()[1:4]]
    fp.close()
    return b, db


def makeBaseParams(insarInfo, nAzLines, suffix='', logger=None):
    ''' make baseline params file used in my processing
    This was written originally for setupInt, but moved to its own routine
    so it can be used by setupStrackReg when a params file is need for
    matching registration offsets
    '''
    #
    if logger is not None:
        logger.logEntry('makeBaseParams')
    # read geodat information
    geodat = u.geodatrxa(file=insarInfo['insarGeo'])
    thetaCrad = geodat.thetaCrad()
    prf = geodat.prf
    b, db = readBase(insarInfo)
    # convert to old format
    writeOldBase(insarInfo, b, db)
    # covert to parallel and normal components- from makeparams
    bp = b[2] * math.cos(thetaCrad) + b[1] * math.sin(thetaCrad)
    bn = b[1] * math.cos(thetaCrad) - b[2] * math.sin(thetaCrad)
    dbp = (db[2] * math.cos(thetaCrad) + db[1] * math.sin(thetaCrad))
    dbn = (db[1] * math.cos(thetaCrad) - db[2] * math.sin(thetaCrad))
    # compute full image length change
    deltabn = dbn*(nAzLines*insarInfo['intLooksA'])/prf
    deltabp = dbp * (nAzLines*insarInfo['intLooksA'])/prf
    # if left looking
    if not geodat.isRightLooking():
        bn *= -1.0
        deltabn *= -1.0
    # write params file
    with open(insarInfo['params']+suffix, 'w') as fp:
        print(
            f'{bn:11.4f} {bp:11.4f} {deltabn:11.4f} {0:7.1f} {deltabp:11.4f}',
            file=fp)
    # write zero params file
    with open('zero.params', 'w') as fp:
        print('0.0 0.0 0.0 0.0 0.0', file=fp)
    if logger is not None:
        logger.logReturn('makeBaseParams')
