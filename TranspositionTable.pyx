# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:44:02 2020

@author: Sid
"""


import numpy as np

zobristHash = np.random.randint(np.iinfo(np.uint64).max,size=(2,6,64),dtype=np.uint64)

cdef class TranspositionTable:
    
    def __cinit__(self):
        self.killerMoves = np.zeros((80,3),dtype=np.uint64)