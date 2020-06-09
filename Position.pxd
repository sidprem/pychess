# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:44:28 2020

@author: Sid
"""

from Utils cimport COLOR, PIECE, COLOR_STR, PIECE_STR, ULL, USI

cdef class Position:
    cdef ULL[:,:] board
    cdef int[:] pieceBoard
    cdef int[:,:] pieceCount
    cdef int enpassant
    cdef int king
    cdef unsigned int castles
    cdef COLOR color
    cdef COLOR opColor
    cdef ULL us
    cdef ULL them
    cdef ULL blocker
    cdef ULL pinned
    cdef ULL checkers
    cdef ULL zHash
    cdef int ply
    cdef str notation
    cdef dict history
    
    cpdef void posFromFEN(self,str fen)
    
    cdef void setPiece(self,PIECE piece,COLOR color,int cord)    

    cdef void clearPiece(self,PIECE piece,COLOR color,int cord)
    
    cdef ULL getUs(self)
    
    cdef ULL getThem(self)
    
    cdef bint isInCheck(self)

    cdef void applyMove(self,USI move)
    
    cdef void undoMove(self)
    
    cpdef moveToSAN(self,move)
    
    cdef int evaluate(self)
    
    cdef int see(self,move)
