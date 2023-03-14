#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 09:11:58 2019

@author: ian
"""


class premet:
    """ \ngeoimage - object for scalar or velocity PS data + geodat data """

    def __init__(self, params, container=None):
        self.params = params
        self.container = container

    def printParams(self, fp=None):
        if self.container is not None:
            print(f'Container={self.container}', file=fp)
        #
        for myKey in self.params.keys():
            print(f'{myKey}={self.params[myKey]}', file=fp)
