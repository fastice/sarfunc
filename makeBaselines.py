# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 10:06:52 2018

@author: ian
"""
import utilities as u


ISPpath='/home/ian/gammaISP/GAMMA_SOFTWARE-20160611/ISP/bin/'

def makeBaselines(insarInfo,logger=None) :
    ''' make baseline file by running cw code'''
    # setup args
    myArgs=[insarInfo['isppar1'],insarInfo['isppar2'],insarInfo['newBase']]
    if logger != None :
        logger.logEntry('makeBaselines')
    # call command
    u.callMyProg(ISPpath+'base_orbit',myArgs=myArgs,screen=True,logger=logger)
    #
    if logger != None :
        logger.logReturn('makeBaselines')