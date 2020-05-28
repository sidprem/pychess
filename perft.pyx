# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:46:30 2020

@author: Sid
"""

from __future__ import print_function
from Position cimport Position
from Movegen cimport generateLegalMoves, getOrig, getDes, createMove
from Bitboard cimport initAttacks, prettyPrintBitBoard
from Utils cimport USI, ALGEBRAIC

cdef int perft(int depth,Position pos,int root):
    cdef int nodes = 0
    cdef int count = 0
    cdef USI m = 0
    if depth == root:
        print("depth is " + str(depth))

    if depth == 0:
        return 1
    for m in generateLegalMoves(pos):
        if depth == 1:
            nodes += 1
        else:
            pos.applyMove(m)
            count = perft(depth - 1,pos,root)
            nodes += count
            pos.undoMove()
            # if depth == root:
            #     print(ALGEBRAIC[getOrig(m)]+ALGEBRAIC[getDes(m)] + " " + str(count))           
    return nodes


def goPerft():
    initAttacks()
    cdef Position pos = Position()
    pos.posFromFEN('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    n = 5
    root = 5
    return perft(n,pos,root)
    