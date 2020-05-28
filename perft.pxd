# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:47:26 2020

@author: Sid
"""

from Position cimport Position

cdef int perft(int depth,Position pos,int root)