# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 09:41:50 2018

@author: ian
"""
import utilities as u

def getDict(dicts,key) :
    ''' return dict from a dict of dicts - takes care of errors for a more graceful exit'''
    try :
        return dicts[key]
    except :
        u.myerror('invalid region or sensor key {0:s}'.format(key))