# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:54:14 2018

@author: ian
"""

# sensorsDef = {'CSK': {'nlooksR': 3, 'nlooksA': 3 , 'intLooksR': 9,
# 'intLooksA': 9, 'sensorpar': 'CSK.par' , 'ISProutine': 'interf_SLCoffShort',
#              'intGen':}
import utilities as u


class sensorDefinitions:
    def __init__(self, sensor):
        # ---------------------------------------------------
        # Parameters for CSK processing
        # ---------------------------------------------------
        if sensor == 'CSK':
            # max days to try and setup pairs
            maxDays = 33
            # number of looks in range and azimuth
            nlooksR, nlooksA = 3, 3
            # par file for this sensor
            sensorpar = 'CSK.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [3, 1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for simulated reg offsets 1/scaleDelta regular
            scaleDelta = 4
            # range: low (for subsampled slcs) and hi (for full res slcs)
            # amplitude tracking windows
            wraHi, wraLow = 72, 96  # registration only
            # same for azimuth
            waaLow, waaHi = 72, 96  # registration only
            #
            wraOffsets, waaOffsets = 96, 96  # offset tracking
            # complex matching window size
            wr, wa = 48, 48
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 24
            # w = window size, searchMult*maxOffsets = searchwindow range,
            # strackTol no fasttrack if all offs less this % of strack search
            strackwParams = {'wr': 96, 'wa': 96, 'searchMult': 0.6,
                             'navgr': 3, 'navga': 3, 'minFastPts': 20,
                             'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'ignoreOffsets': '', 'boxSize': 5, 'nGood': 9,
                       'maxA': 6, 'maxR': 4, 'sr': 2, 'sa': 2}
            # use sim offfsets for culling (sub at beginning and add at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'ignoreOffsets': '', 'boxSize': 9, 'nGood': 17,
                          'maxA': 6, 'maxR': 6, 'sr': 5, 'sa': 5}
            # fast cull
            fastCull = {'ignoreOffsets': '', 'boxSize': 9, 'nGood': 17,
                        'maxA': 3, 'maxR': 3, 'sr': 5, 'sa': 5}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 80,
                            'ratThresh': 1, 'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 3, 'thresh': 80,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 9, 9
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = True
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoffShort'
            #  args to for interferogram generation -inserted in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = False
            # For main speckle tracking (not reg) use only amplitude match -
            # note if this is true, useInt will be ignored
            noComplexMatch = True  # small complex match is not as good as
            # large hi-res match window
            # apply a hanning window (generally the default)
            applyHanningToComplex = True
            noComplexRegMatch = True
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'grepdate'
        # ---------------------------------------------------
        # Parameters for S1 processing
        # ---------------------------------------------------
        elif sensor == 'S1':
            # max days to try and setup pairs
            maxDays = 36
            # number of looks in range and azimuth
            nlooksR, nlooksA = 10, 2
            # par file for this sensor
            sensorpar = 'Sentinel-IW.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for sim registration offsets 1/scaleDelta regular
            scaleDelta = 4
            # registration offset range: low (for subsampled slcs) and hi
            # (for full res slcs) amplitude tracking windows
            wraLow, wraHi = 72, 96
            # same for azimuth
            waaLow, waaHi = 72, 96
            #
            wraOffsets, waaOffsets = 108, 64  # offset tracking
            # complex matching window size
            wr, wa = 48, 48
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 18
            # w = window size, searchMult*maxOffsets = searchwindow range -
            # navg r is for smooth tracking
            strackwParams = {'wr': 108, 'wa': 64, 'searchMult': 0.5,
                             'navgr': 5, 'navga': 1, 'minFastPts': 20,
                             'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'boxSize': 5, 'nGood': 9, 'maxA': 6, 'maxR': 4,
                       'sr': 2, 'sa': 2}
            # use sim offfsets for culling (sub at beginning and add  at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                          'sr': 9, 'sa': 2}
            # note this changes from prior 13by3 smoothing (both normal & fast)
            fastCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                        'sr': 9, 'sa': 2}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 20,
                            'ratThresh': 1, 'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 5, 'thresh': 20,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 10, 2
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = True
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoffShort'
            #  arguments to for interferogram generation -ins in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = True
            # For main speckle tracking (not reg) use only amplitude match -
            # note if this is true, useInt will be ignored
            noComplexMatch = False
            # apply a hanning window (generally the default)
            applyHanningToComplex = True
            noComplexRegMatch = False
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'greptops'
        # ---------------------------------------------------
        # Parameters for TSX processing
        # ---------------------------------------------------
        elif sensor == 'TSX':
            # max days to try and setup pairs
            maxDays = 33
            # number of looks in range and azimuth
            nlooksR, nlooksA = 3, 3
            # par file for this sensor
            sensorpar = 'TSX.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [3, 1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for simulated registration offsets 1/scaleDelta reg
            scaleDelta = 4
            # range: low (for subsampled slcs) and hi (for full res slcs)
            # amplitude tracking windows
            wraLow, wraHi = 72, 96
            # same for azimuth
            waaLow, waaHi = 72, 96
            #
            wraOffsets, waaOffsets = 96, 96  # offset tracking
            # complex matching window size
            wr, wa = 48, 48
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 24
            # w = window size, searchMult*maxOffsets = searchwindow range
            strackwParams = {'wr': 96, 'wa': 96, 'searchMult': 0.6, 'navgr': 3,
                             'navga': 3,  'minFastPts': 20, 'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'ignoreOffsets': '', 'boxSize': 5, 'nGood': 9,
                       'maxA': 6, 'maxR': 4, 'sr': 2, 'sa': 2}
            # use sim offfsets for culling (sub at beginning and add  at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'ignoreOffsets': '', 'boxSize': 9, 'nGood': 17,
                          'maxA': 3, 'maxR': 3, 'sr': 7, 'sa': 7}
            # fast cull
            fastCull = {'ignoreOffsets': '', 'boxSize': 8, 'nGood': 17,
                        'maxA': 6, 'maxR': 6, 'sr': 7, 'sa': 7}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            #
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 80, 'ratThresh': 1,
                            'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 3, 'thresh': 80,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 9, 9
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = False
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoff'
            #  arguments to for interferogram generation -ins in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = False
            # For main speckle tracking (not reg) use only amplitude match -
            # note if this is true, useInt will be ignored
            noComplexMatch = True  # small complex match is not as good as
            # large hi-res match window
            # apply a hanning window (generally the default)
            applyHanningToComplex = True
            noComplexRegMatch = True
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'grepdate'
        elif sensor == 'TEST':
            # max days to try and setup pairs
            maxDays = 36
            # number of looks in range and azimuth
            nlooksR, nlooksA = 10, 2
            # par file for this sensor
            sensorpar = 'Sentinel-IW.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for simulated registration offsets 1/scaleDelta reg
            scaleDelta = 4
            # registration offset range: low (for subsampled slcs) an
            # hi (for full res slcs) amplitude tracking windows
            wraLow, wraHi = 72, 96
            # same for azimuth
            waaLow, waaHi = 72, 96
            #
            wraOffsets, waaOffsets = 108, 64  # offset tracking
            # complex matching window size
            wr, wa = 48, 48
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 18
            # w = window size, searchMult*maxOffsets = searchwindow range -
            # navg r is for smooth tracking
            strackwParams = {'wr': 108, 'wa': 64, 'searchMult': 0.5,
                             'navgr': 5, 'navga': 1, 'minFastPts': 20,
                             'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'boxSize': 5, 'nGood': 9, 'maxA': 6, 'maxR': 4,
                       'sr': 2, 'sa': 2}
            # use sim offfsets for culling (subt at beginning and add at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                          'sr': 9, 'sa': 2,
                          'singleMT': 2}  # single MT for DEBUG ONLY
            # note this changes from prior 13by3 smoothing (both normal & fast)
            fastCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                        'sr': 9, 'sa': 2}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 40, 'ratThresh': 1,
                            'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 5, 'thresh': 40,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 10, 2
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = True
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoffShort'
            # arguments to for interferogram generation -ins in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = True
            # For main speckle tracking (not reg) use only amplitude match -
            # note if this is true, useInt will be ignored
            noComplexMatch = True
            # apply a hanning window (generally the default)
            applyHanningToComplex = True
            noComplexRegMatch = True
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'greptops'
        elif sensor == 'TEST64x64':
            # max days to try and setup pairs
            maxDays = 36
            # number of looks in range and azimuth
            nlooksR, nlooksA = 10, 2
            # par file for this sensor
            sensorpar = 'Sentinel-IW.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for sim registration offsets 1/scaleDelta regular
            scaleDelta = 4
            # registration offset range: low (for subsampled slcs) and hi
            # (for full res slcs) amplitude tracking windows
            wraLow, wraHi = 72, 96
            # same for azimuth
            waaLow, waaHi = 72, 96
            #
            wraOffsets, waaOffsets = 64, 64  # offset tracking
            # complex matching window size
            wr, wa = 48, 48
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 18
            # w = window size, searchMult*maxOffsets = searchwindow range -
            # navg r is for smooth tracking
            strackwParams = {'wr': 64, 'wa': 64, 'searchMult': 0.5,
                             'navgr': 5, 'navga': 1, 'minFastPts': 20,
                             'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'boxSize': 5, 'nGood': 9, 'maxA': 6, 'maxR': 4,
                       'sr': 2, 'sa': 2}
            # use sim offfsets for culling (sub at beginning and add at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                          'sr': 9, 'sa': 2,
                          'singleMT': 2}  # use single MT for DEBUG ONLY
            # note this changes from prior 13by3 smoothing (both normal & fast)
            fastCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                        'sr': 9, 'sa': 2}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 40, 'ratThresh': 1,
                            'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 5, 'thresh': 40,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 10, 2
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = True
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoffShort'
            # arguments to for interferogram generation -inserted in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = True
            # For main speckle tracking (not reg) use only amplitude match
            # note if this is true, useInt will be ignored
            noComplexMatch = True
            # apply a hanning window (generally the default)
            applyHanningToComplex = True
            #
            noComplexRegMatch = True
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'greptops'
        elif sensor == 'TESTNoHanning':
            # max days to try and setup pairs
            maxDays = 36
            # number of looks in range and azimuth
            nlooksR, nlooksA = 10, 2
            # par file for this sensor
            sensorpar = 'Sentinel-IW.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for sim registration offsets 1/scaleDelta regular
            scaleDelta = 4
            # registration offset range: low (for subsampled slcs) and hi
            # (for full res slcs) amplitude tracking windows
            wraLow, wraHi = 72, 96
            # same for azimuth
            waaLow, waaHi = 72, 96
            #
            wraOffsets, waaOffsets = 108, 64  # offset tracking
            # complex matching window size
            wr, wa = 48, 48
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 18
            # w = window size, searchMult*maxOffsets = searchwindow range -
            # navg r is for smooth tracking
            strackwParams = {'wr': 108, 'wa': 64, 'searchMult': 0.5,
                             'navgr': 5, 'navga': 1, 'minFastPts': 20,
                             'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'boxSize': 5, 'nGood': 9, 'maxA': 6, 'maxR': 4,
                       'sr': 2, 'sa': 2}
            # use sim offfsets for culling (sub at beginning and add  at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                          'sr': 9, 'sa': 2,
                          'singleMT': 1}  # use single MT for DEBUG ONLY
            # note this changes from prior 13by3 smoothing (both normal & fast)
            fastCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                        'sr': 9, 'sa': 2}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 40, 'ratThresh': 1,
                            'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 5, 'thresh': 40,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 10, 2
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = True
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoffShort'
            #  arguments to for interferogram generation -ins in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = True
            # For main speckle tracking (not reg) use only amplitude match -
            # note if this is true, useInt will be ignored
            noComplexMatch = False
            # apply a hanning window (generally the default)
            applyHanningToComplex = False
            #
            noComplexRegMatch = True
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'greptops'
        elif sensor == 'TESTNoHanning24':
            # max days to try and setup pairs
            maxDays = 36
            # number of looks in range and azimuth
            nlooksR, nlooksA = 10, 2
            # par file for this sensor
            sensorpar = 'Sentinel-IW.par'
            # looks for reduced res slcs to use for bootstrapping offsets
            subSLC = [1]
            # basename for simulated offsets
            offsetsBase = 'offsets'
            # basename for simulated offsets for registration offsets
            offsetsRegBase = 'offsets.reg'
            #
            registerBase = 'register.offsets'
            # scalefactor for sim registration offsets 1/scaleDelta regular
            scaleDelta = 4
            # registration offset range: low (for subsampled slcs) and
            # hi (for full res slcs) amplitude tracking windows
            wraLow, wraHi = 72, 96
            # same for azimuth
            waaLow, waaHi = 72, 96
            #
            wraOffsets, waaOffsets = 108, 64  # offset tracking
            # complex matching window size
            wr, wa = 24, 24
            # starting offsets for speckle tracking
            rStart, aStart = 180, 180
            # step size for speckle tracking (e.g, output grid spacing)
            deltaR, deltaA = 24, 18
            # w = window size, searchMult*maxOffsets = searchwindow range -
            # navg r is for smooth tracking
            strackwParams = {'wr': 108, 'wa': 64, 'searchMult': 0.5,
                             'navgr': 5, 'navga': 1, 'minFastPts': 20,
                             'minFastRange': 6}
            # registration offsets cull set params (cullst)
            regCull = {'boxSize': 5, 'nGood': 9, 'maxA': 6, 'maxR': 4,
                       'sr': 2, 'sa': 2}
            # use sim offfsets for culling (sub at beginning and add at end)
            useSimWithCull = False
            # parameters for normal culling
            normalCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                          'sr': 9, 'sa': 2,
                          'singleMT': 1}  # use single MT for DEBUG ONLY
            # note this changes from prior 13by3 smoothing (both normal & fast)
            fastCull = {'boxSize': 9, 'nGood': 17, 'maxA': 3, 'maxR': 3,
                        'sr': 9, 'sa': 2}
            # registration interpolation params
            regInterp = {'flags': '-allowBreaks -padEdges -wdist ',
                         'thresh': 5000, 'ratThresh': 1}
            # interpolation of offsets
            normalInterp = {'flags': ' -wdist ', 'thresh': 40, 'ratThresh': 1,
                            'islandThresh': 20}
            # interpolation paramters for fast offsets
            processFastParams = {'kernelSize': 5, 'thresh': 40,
                                 'islandThresh': 20}
            # interferogram
            intLooksR, intLooksA = 10, 2
            # integer Complex - True if SLC stored as int16 complex
            IntegerComplex = True
            # suffix for isp file
            ispSuffix = '.cw'
            # insar code
            ispprog = 'interf_SLCoffShort'
            #  arguments to for interferogram generation -ins in dict below
            parg01 = 'slc1'
            parg02 = 'slc2'
            parg03 = 'isppar1'
            parg04 = 'isppar2'
            parg05 = 'off'
            parg06 = 'pwr1'
            parg07 = 'pwr2'
            parg08 = 'ifg'
            parg09 = 'regOff'
            parg10 = 'intLooksR'
            parg11 = 'intLooksA'
            # use interferogram in tracking
            useInt = True
            # For main speckle tracking (not reg) use only amplitude match -
            # note if this is true, useInt will be ignored
            noComplexMatch = False
            # True apply a hanning window (generally the default)
            applyHanningToComplex = False
            #
            noComplexRegMatch = True
            # merge weights- must add to one
            regW, fastW = 0.5, 0.5
            # command used to grep info about track
            grepCMD = 'greptops'
        else:
            print(sensor)
            u.myerror(f'parameters for {sensor} sensor not set up yet')
        #
        # if not an interferogram, this is setting up speckle tracking

        self.SAR = {'sensor': sensor, 'maxDays': maxDays, 'nlooksR': nlooksR,
                    'nlooksA': nlooksA, 'sensorpar': sensorpar,
                    'subSLC': subSLC, 'offsetsBase': offsetsBase,
                    'offsetsRegBase': offsetsRegBase,
                    'registerBase': registerBase, 'scaleDelta': scaleDelta,
                    'wraLow': wraLow, 'wraHi': wraHi, 'wr': wr,
                    'waaLow': waaLow, 'waaHi': waaHi,
                    'wraOffsets': wraOffsets, 'waaOffsets': waaOffsets,
                    'wa': wa, 'rStart': rStart, 'aStart': aStart,
                    'deltaR': deltaR, 'deltaA': deltaA,
                    'intLooksR': intLooksR, 'intLooksA': intLooksA,
                    'IntegerComplex': IntegerComplex, 'ispSuffix': ispSuffix,
                    'regCull': regCull, 'regInterp': regInterp,
                    'useSimWithCull': useSimWithCull,
                    'normalCull': normalCull, 'normalInterp': normalInterp,
                    'fastCull': fastCull, 'useInt': useInt,
                    'processFastParams': processFastParams,
                    'noComplexMatch': noComplexMatch,
                    'noComplexRegMatch': noComplexRegMatch,
                    'strackwParams': strackwParams,
                    'regW': regW, 'fastW': fastW, 'grepCMD': grepCMD,
                    'applyHanningToComplex': applyHanningToComplex}
        # program to create interferogram, and corresponding set of args -
        # many of which index runtime dict with insar info
        intGen = {'ispprog': ispprog, 'parg01': parg01, 'parg02': parg02,
                  'parg03': parg03, 'parg04': parg04, 'parg05': parg05,
                  'parg06': parg06, 'parg07': parg07, 'parg08': parg08,
                  'parg09': parg09, 'parg10': parg10, 'parg11': parg11}
        self.inSAR = {'sensor': sensor, 'nlooksR': nlooksR, 'nlooksA': nlooksA,
                      'intLooksR': intLooksR, 'intLooksA': intLooksA,
                      'sensorpar': sensorpar, 'intGen': intGen}

    def geodatName(self):
        return f'geodat{self.SAR["intLooksR"]}x{self.SAR["intLooksA"]}.in'
