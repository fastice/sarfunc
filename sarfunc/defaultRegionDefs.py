# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 09:50:21 2018

@author: ian
"""

import utilities as u
import yaml
#
# Define as a class to allow future addtion of methods
#


class defaultRegionDefs:
    '''
    Encapsulates a lot of information for regions (e.g., Greenland and
    Antarctica).Things like the DEM path can be updated here.
    '''

    def __init__(self, region, regionFile=None, regionDef=None):
        # define regions
        # /Volumes/insar6/gmap/allGLVel/250smooth/Greenland250smooth
        # changed from final greenland velocity Greenland250-V1a to Unmasked
        # version Track-Interp250/mosaicOffsetsFullInterp 6/25/2019
        self.regionsDef = {
            'greenland':
                {'epsg': 3413,
                 'wktFile': None,
                 'dem': '/Volumes/insar7/ian/gimp/gimp2/270m/dem.gimp2.270m',
                 'velMap': '/Volumes/insar6/gmap/allGLVel/release/Track-'
                 'Interp250/mosaicOffsetsFullInterp',
                 'fastmask': '/Users/ian/greenlandmask/output2009/'
                 'greenlandmask2009fast',
                 'mask': '/Users/ian/greenlandmask/Tops/greenlandmaskTops',
                 'sigmaShape':
                     '/Users/ian/greenlandmask/sigmaScale/sigmaScale-3413.shp',
                 'name': region,
                 'icemask': '/Volumes/insar7/ian/gimp/mask/GimpIceMask_90m'
                 },
            'antarctica':
                {'epsg': 3031,
                 'wktFile': None,
                 'dem': '/Volumes/insarb/ian/fromJonathan/newAntarctic/dem1',
                 'velMap':
                     '/Volumes/insar6/gmap/irvineAntarctica/Antarctica1km',
                 'fastmask': '/Users/ian/AntarcticMasks/AntFastMask',
                 'mask': '/Users/ian/AntarcticMasks/TrackLSMask',
                 'shelfMask': None,
                 'sigmaShape': None,
                 'name': region,
                 'icemask': None},
            'amundsen':
                {'epsg': 3031,
                 'wktFile': None,
                 'dem': '/Volumes/insarb/ian/fromJonathan/newAntarctic/dem1',
                 'velMap':
                     '/Volumes/insar6/gmap/irvineAntarctica/Antarctica1km',
                 'fastmask': None,
                 'mask': '/Users/ian/AntarcticMasks/TrackLSMask',
                 'shelfMask': None,
                 'sigmaShape': None,
                 'name': region,
                 'icemask': None},
            'taku':
                {'epsg': None,
                 'wktFile': '/Volumes/insar11/ian/Taku/wkt/taku.wkt',
                 'dem': '/Volumes/insar11/ian/Taku/dems/copernicus/270m/'
                 'dem.wgs84.270m',
                 'velMap': '/Volumes/insar11/ian/Taku/Sentinel1/baseMap/'
                     'track-all/mosaicOffsets',
                 'fastmask': '/Volumes/insar11/ian/Taku/masks/FastMask',
                 'mask': '/Volumes/insar11/ian/Taku/masks/takumaskTops',
                 'shelfMask': None,
                 'sigmaShape': None,
                 'name': region,
                 'icemask': None
                 },
            'columbia':
                {'epsg': 3413,
                 'wktFile': None,
                 'dem': '/Volumes/insar7/ian/TSXAK/Columbia/dems/'
                     'copernicus/270m/dem.wgs84.270m',
                 'velMap': '/Volumes/insar1/ian/SentinelColumbia/'
                     'velocityBasemap/ColumbiaAvgVel',
                 'fastmask': '/Volumes/insar7/ian/TSXAK/Columbia/masks/'
                     'columbiamask2011fast',
                 'mask': '/Volumes/insar7/ian/TSXAK/Columbia/masks/'
                     'ColumbiaMaskTops',
                 'shelfMask': None,
                 'sigmaShape': None,
                 'name': region,
                 'icemask': None
                 }
            }
        if regionDef is not None:
            self.region = regionDef
            return
        # print(region, regionFile)
        if regionFile is not None:
            try:
                with open(regionFile) as fp:
                    result = yaml.load(fp, Loader=yaml.FullLoader)
                    self.region = result
                    return
            except Exception:
                u.myerror(
                    f'defaultRegionDefs: {regionFile} could not be parsed')
        if region is None:
            return
        try:
            self.region = self.regionsDef[region.lower()]
        except Exception:
            u.myerror(
                f'defaultRegionDefs: {region} is an undefined region code')

    def dem(self, tiff=False):
        if tiff:
            return f'{self.region["dem"]}.tif'
        return self.region['dem']

    def velMap(self):
        return self.region['velMap']

    def epsg(self):
        return self.region['epsg']

    def wktFile(self):
        return self.region['wktFile']

    def srsInfo(self):
        return {'wktFile': self.region['wktFile'], 'epsg': self.region['epsg']}

    def name(self):
        return self.region['name']

    def setEPSG(self, epsg):
        self.region['epgs'] = epsg

    def mask(self):
        return self.region['mask']

    def shelfMask(self):
        return self.region['shelfMask']

    def fastmask(self):
        return self.region['fastmask']

    def icemask(self):
        return self.region['icemask']

    def sigmaShape(self):
        return self.region['sigmaShape']

    def setRegionField(self, key, value):
        self.region[key] = value
