# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:11:55 2020

@author: Sid
"""

from Utils cimport USI, ULL
from Position cimport Position
from cpython cimport array
import array

#0-5 from
#6-11 to
#12-16 Normal, enpassant, king castle, queen castle, knight promo, bishop promo, rook promo, queen promo

#create move
cdef inline USI createMove(USI orig,USI des,USI flag):
    return (orig | (des << 6) | (flag << 12))

cdef inline USI getOrig(USI move):
    return move & <USI>0x3F

cdef inline USI getDes(USI move):
    return (move >> 6) & <USI>0x3F

cdef inline USI getFlag(USI move):
    return (move >> 12) & <USI>0x7

cdef USI[:] generateLegalMoves(Position pos)

cdef array.array generatePawnMoves(Position pos)