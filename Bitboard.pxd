# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:24:58 2020

@author: Sid
"""
from Utils cimport PIECE, COLOR, ULL, DIRECTION

#Universal bitboards
cdef ULL BB_EMPTY
cdef ULL BB_ALL_SQUARES

#Bitboards for each square
cdef ULL[:] BB_SQUARES

#File bitboards
cdef ULL BB_A_FILE
cdef ULL BB_B_FILE
cdef ULL BB_C_FILE
cdef ULL BB_D_FILE
cdef ULL BB_E_FILE
cdef ULL BB_F_FILE
cdef ULL BB_G_FILE
cdef ULL BB_H_FILE

#Rank bitboards
cdef ULL BB_RANK_1
cdef ULL BB_RANK_2
cdef ULL BB_RANK_3
cdef ULL BB_RANK_4
cdef ULL BB_RANK_5
cdef ULL BB_RANK_6
cdef ULL BB_RANK_7
cdef ULL BB_RANK_8

#Not file bitboards
cdef ULL BB_NOT_A_FILE
cdef ULL BB_NOT_B_FILE
cdef ULL BB_NOT_C_FILE
cdef ULL BB_NOT_D_FILE
cdef ULL BB_NOT_E_FILE
cdef ULL BB_NOT_F_FILE
cdef ULL BB_NOT_G_FILE
cdef ULL BB_NOT_H_FILE

#Not rank bitboards
cdef ULL BB_NOT_RANK_1
cdef ULL BB_NOT_RANK_2
cdef ULL BB_NOT_RANK_3
cdef ULL BB_NOT_RANK_4
cdef ULL BB_NOT_RANK_5
cdef ULL BB_NOT_RANK_6
cdef ULL BB_NOT_RANK_7
cdef ULL BB_NOT_RANK_8

#Look up table for lsb debruijn
cdef int[:] index64

#Sliding piece arrays for magic bitboard calculations
cdef int[:] BBITS
cdef int[:] RBITS
cdef ULL[:] BISHOP_MAGICS
cdef ULL[:] ROOK_MAGICS
cdef ULL[:] BISHOP_ATTACK_MASK
cdef ULL[:] ROOK_ATTACK_MASK
cdef ULL[:,:] BISHOP_ATTACKS
cdef ULL[:,:] ROOK_ATTACKS
cdef ULL[:,:] MOVE_ARRAY
cdef ULL[:,:] LINE_BB

cpdef str prettyPrintBitBoard(b)
cpdef void initAttacks()
cdef ULL attackersTo(ULL[:,:] board,ULL blocker,int square)
cdef ULL attacksFrom(PIECE pieceType, int square, COLOR color, ULL blocker)
cdef ULL blockers(ULL[:] pboard,ULL pieces,int square)
cdef ULL betweenBB(int sq1,int sq2)
cdef bint inRay(int sq1,int sq2,int sq3)

#Finds the index of the lsb for a bitboard using debruijn lookup table index64
cdef inline int lsb(ULL bb):
    cdef ULL debruijn64 = 0x03f79d71b4cb0a89
    return index64[<int>(((bb ^ (bb - 1))*debruijn64) >> 58)]

#Finds the population count (count of set bits) in a bitboard
cdef inline int pop_count(ULL bb):
    cdef int count = 0
    if bb == 0:
        return 0
    elif (bb != 0) & ((bb & (bb - 1)) == 0):
        return 1
    else:
        while bb:
            count+=1
            bb &= (bb - 1)
        return count

#Provides a bitboard with the lsb removed
cdef inline ULL pop_lsb(ULL bb):
    return bb & (bb - 1)

#Sets a bit at the index location i
cdef inline ULL setBits(ULL bb, int i):
    return (bb | BB_SQUARES[i])

#Clears a bit at the index location i
cdef inline ULL clearBits(ULL bb, int i):
    return (bb & ~BB_SQUARES[i])

#Gets the square index (0-63) given a rank and a file
cdef inline int getSquare(int file,int rank):
    return (8*rank + file)

#Gets the rank given a square index (0-63)
cdef inline int getRank(int sq):
    return (sq << 3)

#Gets the file given a square index (0-63)
cdef inline int getFile(int sq):
    return (sq & 7)    

cdef inline ULL shiftBitBoard(ULL bb,DIRECTION direction):
    return (bb << <int>direction) if (<int>direction >= 0) else (bb >> abs(<int>direction))