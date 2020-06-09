# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:44:43 2020

@author: Sid
"""


from Utils cimport ULL, USI, PIECE, COLOR

cdef ULL[:,:,:] zobristHash

ctypedef entry TTEntry

cdef struct entry:
    ULL hash
    USI move
    int depth
    int score
    int node
    bint age

cdef class TranspositionTable:
    cdef USI[:,:] killerMoves
    cdef TTEntry[:] entries 
    

