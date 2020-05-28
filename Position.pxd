# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:44:28 2020

@author: Sid
"""

from Utils cimport COLOR, PIECE, COLOR_STR, PIECE_STR, ULL, USI

cdef class Position:
    cdef ULL[:,:] board
    cdef int[:] pieceBoard
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
    # def printPosition(self):
    #     tempBoard = [6]*64
    #     for bits in iterBits(self.us):
    #         tempBoard[bits] = printPieces[self.color][self.pieceBoard[bits]]

    #     for bits in iterBits(self.them):
    #         tempBoard[bits] = printPieces[self.opColor][self.pieceBoard[bits]]

    #     tempBoard = [x if x != EMPTY else printPieces[self.color][EMPTY] for x in tempBoard]

    #     prettyBoard = []
    #     prettyBoard.append(tempBoard[56:64])
    #     prettyBoard.append(tempBoard[48:56])
    #     prettyBoard.append(tempBoard[40:48])
    #     prettyBoard.append(tempBoard[32:40])
    #     prettyBoard.append(tempBoard[24:32])
    #     prettyBoard.append(tempBoard[16:24])
    #     prettyBoard.append(tempBoard[8:16])
    #     prettyBoard.append(tempBoard[0:8])


    #     for row in prettyBoard:
    #         print(' '.join(row))
    #     print("\n")