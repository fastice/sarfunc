# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 09:50:21 2018

@author: ian
"""
''' This program sets up default region definitions for all of the processing. Things like the DEM path can be updated here.'''
import utilities as u
#
# Define as a class to allow future addtion of methods
#
class defaultRegionDefs :
    def __init__(self,region) :
        # define regions    /Volumes/insar6/gmap/allGLVel/250smooth/Greenland250smooth
        regionsDef={'greenland' : {'epsg' : 3413 , 'dem' : '/Volumes/insar7/ian/fromInsar3/gimp/version3/270m/gimpversion3.0.270m' ,
                                   'velMap' : '/Volumes/insar6/gmap/allGLVel/release/AllGreenlandMosaic250-V1a/Greenland250-V1' ,
                                   'fastmask' : '/Users/ian/greenlandmask/greenlandmask2009fast', 
                                   'mask' : '/Users/ian/greenlandmask/Tops/greenlandmaskTops'},
                    # standard Antarctica
                    'antarctica' : {'epsg' : 3031 , 'dem' : '/Volumes/insarb/ian/fromJonathan/newAntarctic/dem1' ,
                                    'velMap' : '/Volumes/insar6/gmap/irvineAntarctica/Antarctica1km' ,
                                   'fastmask' : None, 
                                   'mask' : '/Users/ian/AntarcticMasks/TrackLSMask'}}
        try :
            self.region = regionsDef[region.lower()]
        except :
            u.myerror('defaultRegionDefs : {0:s} is an undefined region code'.format(region))
            
    def dem(self) :
        return self.region['dem']
    
    def velMap(self) :
        return self.region['velMap']
    
    def epsg(self) :
        return self.region['epsg']
        
    def setEPSG(self,epsg) :
        self.region['epgs']=epsg
        
    def mask(self) :
        return self.region['mask']  
        
    def fastmask(self) :
        return self.region['fastmask']
        
    def setRegionField(self,key,value) :
        self.region[key]=value
    
                               