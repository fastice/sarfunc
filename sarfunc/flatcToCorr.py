import numpy as np
import utilities as u
import os

def flatcToCorr(cfile,nlr,nla) :
    # open geodat
    basepath=os.path.dirname(cfile)
    geodatFile='{0:s}/geodat{1:d}x{2:d}.in'.format(basepath,nlr,nla)
    myGeodat=u.geodatrxa(file=geodatFile)
    # read data
    cpx=u.readImage(cfile,myGeodat.nr*2,myGeodat.na,'>i2')
    cpx=cpx.astype(np.float32)
    # line index
    ir=np.arange(0,myGeodat.nr)*2
    c=np.zeros((myGeodat.na,myGeodat.nr))
    myScale=1/16000.
    for i in range(0,myGeodat.na)  :
        c[i,:]=np.sqrt(np.power(cpx[i,ir],2) + np.power(cpx[i,ir+1],2))*myScale
    #
    u.writeImage(cfile+'.cor',c,'>f4')
    



