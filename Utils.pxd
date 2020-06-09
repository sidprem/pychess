# -*- coding: utf-8 -*-
"""
Created on Sat May 16 11:24:33 2020

@author: Sid
"""

ctypedef unsigned long long ULL
ctypedef unsigned short USI

ctypedef enum DIRECTION:
    N = 8,
    S = -8,
    E = 1,
    W = -1,
    NW = 7,
    NE = 9,
    SW = -9,
    SE = -7
    
ctypedef enum COLOR:
    WHITE,
    BLACK
    
ctypedef enum PIECE:
    PAWN,
    KNIGHT,
    KING,
    BISHOP,
    ROOK,
    QUEEN,
    EMPTY

ctypedef enum CASTLE:
    W_OO = 1,
    W_OOO = 2,
    B_OO = 4,
    B_OOO = 8
    
ctypedef enum MOVE_FLAG:
    NORMAL,
    ENPASSANT,
    KING_CASTLE,
    QUEEN_CASTLE,
    KNIGHT_PROMO,
    BISHOP_PROMO,
    ROOK_PROMO,
    QUEEN_PROMO,
    CAPTURES

cpdef str PIECE_STR

cpdef str COLOR_STR

cdef int MAX_MOVES

cdef int MIN_VALUE

cdef int MAX_VALUE

cpdef ALGEBRAIC

cpdef ALGPIECE

cdef int[:] PIECE_EVAL