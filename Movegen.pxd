# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:11:55 2020

@author: Sid
"""

from Utils cimport USI, ULL
from Position cimport Position

#0-5 from
#6-11 to
#12-15 Normal, enpassant, king castle, queen castle, knight promo, bishop promo, rook promo, queen promo, Captures

#create move
cdef inline USI createMove(USI orig,USI des,USI flag):
    return (orig | (des << 6) | (flag << 12))

cdef inline USI getOrig(USI move):
    return move & <USI>0x3F

cdef inline USI getDes(USI move):
    return (move >> 6) & <USI>0x3F

cdef inline USI getFlag(USI move):
    return (move >> 12)

cdef USI[:] generateLegalMoves(Position pos)