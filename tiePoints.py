# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 12:35:53 2019

@author: ian
"""
import utilities as u
import os
import numpy as np
import pyproj

class tiePoints :

    """ offsets object - use for offset information """

    def __init__(self,tieFile=None ) :
        """ \n\nRead a tiefile and manipulate tie points """
        #
        # set everything to zero as default
        #
        self.tieFile=None
        self.lat,self.lon=np.array([]),np.array([])
        self.x,self.y=np.array([]),np.array([])
        self.z=np.array([])
        self.vx,self.vy,self.vz=np.array([]),np.array([]),np.array([])
        #
        self.setTieFile(tieFile)
        self.epsg=None
        self.llproj=pyproj.Proj("+init=EPSG:4326")
        self.xyproj=None
        
        if tieFile != None :
            self.readTies(tieFile=tieFile)
        
    def setTieFile(self,tieFile) :
        self.tieFile = tieFile            

    def checkTieFile(self) :
        if self.tieFile == None :
            u.myerror("No tiefile specified")
        if not os.path.exists(self.tieFile) :
            u.myerror("tieFile : {0:s} does not exist".format(self.tieFile))
            
    def setEPSG(self) :
        if len(self.lat) <= 0 : 
            u.myerror("Cannot set epsg without valid latlon")
        if(self.lat[0] > 0) :
            self.epsg=3413
            self.xyproj=pyproj.Proj("+init=EPSG:3413")
        else :
            self.epsg=3031   
            self.xyproj=pyproj.Proj("+init=EPSG:3031")
           
            
    def lltoxym(self,lat,lon):
        # convert lat/lon to xy
        if self.xyproj != None :
            x,y=pyproj.transform(self.llproj,self.xyproj,lon,lat)
            return x,y
        else :
            u.myerror("lltoxy : proj not defined")
        
        
    def readTies(self,tieFile=None) :
        ''' read ties, set projection based on hemisphere, convert to x,y (m)'''
        self.setTieFile(tieFile)
        self.checkTieFile()
        #
        fpIn=open(self.tieFile,'r')
        for line in fpIn :
            if '&' not in line and ';' not in line :
                lat,lon,z,vx,vy,vz =[float(x) for x in line.split()[0:6]]
                self.lat=np.append(self.lat,lat)
                self.lon=np.append(self.lon,lon)
                self.z=np.append(self.z,z)
                self.vx=np.append(self.vx,vx)
                self.vy=np.append(self.vy,vy)
                self.vz=np.append(self.vz,vz)
        self.vh=np.sqrt(self.vx**2 + self.vy**2)       
        fpIn.close()
        # set epsg
        self.setEPSG()
        # do coordinate conversion
        self.x,self.y=self.lltoxym(self.lat,self.lon)
        
    def zeroTies(self) :
        return np.abs(self.vh) < 0.00001
    def NzeroTies(self) :
        return sum(self.zeroTies())   
    
    def allTies(self) :
        return np.abs(self.vh) >= 0
        
    def NallTies(self) :
        return sum(self.allTies()) 
    
    def NvRangeTies(self,minv,maxv) :
        return sum(self.vRangeTies(minv,maxv))
        
    def NvAllTies(self,minv,maxv) :
        return sum(self.allTies(minv,maxv)) 
        
    def vRangeTies(self,minv,maxv) :
        return np.logical_and(self.vh >= minv,self.vh <= maxv )
        
    def llzero(self) :
        iZero=self.zeroTies()
        return self.lat(iZero),self.lat(iZero)
    
    def xykm(self,x,y):
        return x/1000.,y/1000.
        
    def xyzerom(self) :
        iZero=self.zeroTies()
        return self.x[iZero],self.y[iZero]
        
    def xyallm(self) :
        return self.x,self.y
   
    def xyallkm(self) :
        return self.xykm(self.x,self.y)
        
    def xyzerokm(self) :
        x,y=self.xyzerom()
        return self.xykm(x,y)
        
    def xyvRangem(self,minv,maxv) :
        iRange=self.vRangeTies(minv,maxv)
        return self.x[iRange],self.y[iRange]
        
    def xyvRangekm(self,minv,maxv) :
        x,y=self.xyvRangem(minv,maxv)
        return self.xykm(x,y)
        
    def _stats(func) :
        def mstd(*args) :
            x,y=func(*args)
            vx,vy,vr=args[1].interpGeo(x,y)
            iGood=np.isfinite(vx)
            return np.average(vx[iGood]),np.average(vy[iGood]),np.std(vx[iGood]),np.std(vy[iGood]),sum(iGood)
        return mstd
    
    @_stats
    def zeroStats(self,vel) :
        return self.xyzerokm()
        
    @_stats
    def allStats(self,vel) :
        return self.xyallkm()    
    @_stats
    def vRangeStats(self,vel,minv,maxv) :
        return self.xyvRangekm(minv,maxv)
    
    def _tieVels(func) :
        def tieV(*args) :
            x,y=func(*args)
            vx,vy,vr=args[1].interpGeo(x,y)
            iGood=np.isfinite(vx)
            return vx,vy,vr,iGood
        return tieV
    
    @_tieVels
    def zeroVData(self,vel) :
        return self.xyzerokm()
        
    @_tieVels
    def allVdata(self,vel) :
        return self.xyallkm()    
    @_tieVels
    def vRangeData(self,vel,minv,maxv) :
        return self.xyvRangekm(minv,maxv) 
   
        
    
    
 
    