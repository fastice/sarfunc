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
        self.nocull=None
        self.pound2=False
        self.header=[]
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
       
    def readCullFile(self,cullFile) :
        ''' read a cull file '''
        # open file
        fp=open(cullFile,'r')
        myParams=eval(fp.readline())
        print(myParams["tieFile"])
        print(self.tieFile)
        cullPoints=[]
        for line in fp :
            cullPoints.append(int(line))
        if len(cullPoints) != myParams["nBad"] :
            u.myerror(f'reading culled points expected {myParams["nBad"]} but only found {len(cullPoints) }')
        #
        fp.close()
        return np.array(cullPoints)
        
        
    def applyCullFile(self,cullFile )  :
        ''' read a tiepoint cull file and update nocull'''
        #
        self.header.append(cullFile)
        toCull=self.readCullFile(cullFile)
        if len(toCull) > 0 :
            self.nocull[toCull]=False
        
    def readTies(self,tieFile=None) :
        ''' read ties, set projection based on hemisphere, convert to x,y (m)'''
        self.setTieFile(tieFile)
        self.checkTieFile()
        #
        fpIn=open(self.tieFile,'r')
        latv,lonv,zv,vxv,vyv,vzv=[],[],[],[],[],[]
        for line in fpIn :
            if '#' in line and '2' in line :
                self.pound2=True
            if '&' not in line and ';' not in line and '#' not in line :
                lat,lon,z,vx,vy,vz =[float(x) for x in line.split()[0:6]]
                latv.append(lat)
                lonv.append(lon)
                zv.append(z)
                vxv.append(vx)
                vyv.append(vy)
                vzv.append(vz)
        self.lat=np.append(self.lat,np.array(latv))
        self.lon=np.append(self.lon,np.array(lonv))
        self.z=np.append(self.z,np.array(zv))
        self.vx=np.append(self.vx,np.array(vxv))
        self.vy=np.append(self.vy,np.array(vyv))
        self.vz=np.append(self.vz,np.array(vzv) )   
        self.vh=np.sqrt(self.vx**2 + self.vy**2)       
        fpIn.close()
        # set epsg
        self.setEPSG()
        #
        self.nocull=np.ones(self.vx.shape,dtype=bool)
        # do coordinate conversion
        self.x,self.y=self.lltoxym(self.lat,self.lon)
        
        
    def writeTies(self,tieFileOut) :
        ''' write ties '''
        #
        fpOut=open(tieFileOut,'w')
        # in case type file that needs this.
        for line in self.header :
            print(f'; {line}',file=fpOut)
        if self.pound2 : 
            print('# 2',file=fpOut)
        for lat,lon,z,vx,vy,vz,nocull in zip(self.lat,self.lon,self.z,self.vx,self.vy,self.vz,self.nocull) :
            if nocull :
                print(f'{lat:10.5f} {lon:10.5f} {z:8.1f} {vx:8.1f} {vy:8.1f} {vz:8.1f}',file=fpOut )
        print('&',file=fpOut)
        fpOut.close()
        # set epsg
           
        
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
   
        
    
    
 
    