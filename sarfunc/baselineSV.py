# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 12:50:29 2019

@author: ian
"""
import utilities as u
import os
import numpy as np
import math
class baselineSV :

    """ baseline object - computes baseline along track from state vectors - largely used to test algorithms before coding in C"""

    def __init__(self,file1=None,file2=None,echo=False) :
        """ initialize a geodatrxa object, where :
        file\t is optional file name, can be input later with readFile(file=file) 
        echo\t set to true to echo results as they are read in, otherwise no output """
        #
        # set everything to empty values
        self.file1=file1
        self.file2=file2
        self.geo1=None
        self.geo2=None
        #
        if self.file1 != None :
           self.file1,self.geo1=self.loadgeodat(file1)
        if self.file2 !=None :
            self.file2,self.geo2=self.loadgeodat(file2)
           
    def loadgeodat(self,myFile) :
        ''' read geodat file, return file and geo object'''
        if os.path.exists(myFile) :
            return myFile,u.geodatrxa(file=myFile)
        else :
            u.myerror('baseline.loadgeodat: error reading file - {0:s}'.format(myFile))
            
    def haveGeo(self) :
        if self.geo1 != None and self.geo2 != None :
            return True
        return False
        
    def readgeodats(self,file1,file2) :
        ''' specify and load geodats - will overwrite any orginal '''
        self.file1,self.geo1=self.loadgeodat(file1)
        self.file2,self.geo2=self.loadgeodat(file2)
    
    def unitTCN(self,myTime,geo) :
        ''' compute downward point radial unit vector '''
        r=-np.array(geo.interpPos(myTime))
        v=np.array(geo.interpVel(myTime))
        # downward normal
        N=r/np.linalg.norm(r)
        # cross with v, in the same plane, but not orthogonal
        Nxv=np.cross(N,v)
        # cross track unit
        C=Nxv/np.linalg.norm(Nxv)
        # along rack unit
        T=np.cross(C,N)
        # done
        return T,C,N
        
    def BTCNfromState(self,myTime1) :
        ''' Derive the baseline as the vector that minimizes the projection 
        of the position difference onto the T vector of the master image '''
        sPos1=np.array(self.geo1.interpPos(myTime1))
        # assume well registered and account for t shift
        myTime2=myTime1 -self.geo1.t0 + self.geo2.t0
        T,C,N=self.unitTCN(myTime1,self.geo1)
        for i in range(0,10) :
            # position at candidte time
            sPos2=np.array(self.geo2.interpPos(myTime2))
            vs2=np.array(self.geo2.interpVel(myTime2))
            # basleine vector
            b=sPos2- sPos1
            # Compute dt
            C1=np.dot(vs2,T) 
            dt=np.dot(b,T)/C1
            #print('theta ',np.dot(T,b/np.linalg.norm(b)),C1,dt,np.linalg.norm(b))
            #
            myTime2 -= dt
            if np.abs(dt) < 1e-11 :
                break 
        bTCN=np.array([np.dot(b,T),np.dot(b,C),np.dot(b,N)])
        return bTCN,b
        
    def dBTCNfromState(self,myTime1,deltaT=1) :
        bTCN1,b1=self.BTCNfromState(myTime1-deltaT*0.5)
        bTCN2,b2=self.BTCNfromState(myTime1+deltaT*0.5)
        dTCN=(bTCN2-bTCN1)/deltaT
        return dTCN
        
    def BnBpfromState(self,myTime1,thetaC=None) :
        ''' use nominal center theta to compute Bn, Bp '''
        #thetaCrad=self.geo1.thetaCActualrad()
        if thetaC == None  :
            thetaCrad=self.geo1.thetaCrad()
        else :
            thetaCrad=thetaC
            print(thetaCrad*180./np.pi)   
        b,bxyz=self.BTCNfromState(myTime1)
        bp=b[2]*math.cos(thetaCrad) + b[1] *math.sin(thetaCrad)
        bn=b[1]*math.cos(thetaCrad) - b[2] *math.sin(thetaCrad)
        #print(bp,bn)
        return bn,bp
    
    def myTest(self,myTime) :
        T,C,N=self.unitTCN(myTime,self.geo1)
        print(T)
        print(C)
        print(N)
        
        