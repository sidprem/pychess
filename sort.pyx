# -*- coding: utf-8 -*-
"""
Created on Sat May 30 20:18:18 2020

@author: Sid
"""

from Utils cimport USI, MOVE_FLAG
from Movegen cimport getOrig, getDes, getFlag
from Position cimport Position
import numpy as np
import array

cdef USI[:] sortMoves(USI[:] moves,Position pos):
    cdef USI[:] sortedMoves = array.array('H',[0]*len(moves))
    cdef int[:,:] moveValue = np.zeros((len(moves),2),dtype=np.int)
    cdef USI flag
    cdef int i, index
    i=0
    for move in moves:
        flag = getFlag(move)
        if flag in [MOVE_FLAG.ENPASSANT,MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO,MOVE_FLAG.CAPTURES]:
            moveValue[i,0] = move
            moveValue[i,1] = pos.see(move)
        else:
            moveValue[i,0] = move
            moveValue[i,1] = -2
            
        i+=1
    
    i=0
    for index in np.argsort(moveValue[:,1]):
        sortedMoves[i] = moves[index]
        i+=1
    
    return sortedMoves
            
            