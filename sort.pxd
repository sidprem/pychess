# -*- coding: utf-8 -*-
"""
Created on Sat May 30 20:25:07 2020

@author: Sid
"""

from Utils cimport USI
from Position cimport Position

cdef USI[:] sortMoves(USI[:] moves, Position pos)