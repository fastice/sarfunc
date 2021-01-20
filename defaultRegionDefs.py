# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 09:50:21 2018

@author: ian
"""

import utilities as u
#
# Define as a class to allow future addtion of methods
#


class defaultRegionDefs:
    '''
    Encapsulates a lot of information for regions (e.g., Greenland and
    Antarctica).Things like the DEM path can be updated here.
    '''

    def __init__(self, region):
        # define regions
        # /Volumes/insar6/gmap/allGLVel/250smooth/Greenland250smooth
        # changed from final greenland velocity Greenland250-V1a to Unmasked
        # version Track-Interp250/mosaicOffsetsFullInterp 6/25/2019
        regionsDef = \
            {'greenland':
                {'epsg': 3413,
                 'dem': '/Volumes/insar7/ian/gimp/gimp2/270m/dem.gimp2.270m',
                 'velMap': '/Volumes/insar6/gmap/allGLVel/release/Track-'
                 'Interp250/mosaicOffsetsFullInterp',
                 'fastmask': '/Users/ian/greenlandmask/output2009/'
                 'greenlandmask2009fast',
                 'mask': '/Users/ian/greenlandmask/Tops/greenlandmaskTops'
                 },
             'antarctica':
                {'epsg': 3031,
                 'dem': '/Volumes/insarb/ian/fromJonathan/newAntarctic/dem1',
                 'velMap':
                     '/Volumes/insar6/gmap/irvineAntarctica/Antarctica1km',
                 'fastmask': None,
                 'mask': '/Users/ian/AntarcticMasks/TrackLSMask'}}
        try:
            self.region = regionsDef[region.lower()]
        except Exception:
            u.myerror(
                f'defaultRegionDefs: {region} is an undefined region code')

    def dem(self):
        return self.region['dem']

    def velMap(self):
        return self.region['velMap']

    def epsg(self):
        return self.region['epsg']

    def setEPSG(self, epsg):
        self.region['epgs'] = epsg

    def mask(self):
        return self.region['mask']

    def fastmask(self):
        return self.region['fastmask']

    def setRegionField(self, key, value):
        self.region[key] = value
