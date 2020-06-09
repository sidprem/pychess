# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:50:55 2020

@author: Sid
"""
from __future__ import print_function

from Position cimport Position
from Utils cimport MIN_VALUE, MAX_VALUE, USI, MOVE_FLAG
from Movegen cimport generateLegalMoves, getOrig, getDes, getFlag
from Bitboard cimport initAttacks

cdef int alphaBeta(int alpha, int beta, int depth, Position pos):
    cdef int score = MIN_VALUE
    cdef USI move

    if depth == 0:
        return pos.evaluate() #quiescent(alpha,beta,pos)

    for move in generateLegalMoves(pos):
        pos.applyMove(move)
        score = -alphaBeta(-beta,-alpha,depth-1,pos)
        pos.undoMove()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

cdef int quiescent(int alpha, int beta, Position pos):
    cdef int stand_pat = pos.evaluate()
    cdef int score
    cdef USI move

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in generateLegalMoves(pos):
        pos.applyMove(move)
        score = -quiescent(-beta,-alpha,pos)
        pos.undoMove()

        if score >= beta:
            return beta
        if score < alpha:
            alpha = score

    return alpha

cdef USI search(Position pos, int depth):
    cdef USI move, bestMove
    cdef int bestScore, alpha, beta, score

    bestScore = MIN_VALUE
    alpha = MIN_VALUE
    beta = MAX_VALUE

    for move in generateLegalMoves(pos):
        pos.applyMove(move)
        score = -alphaBeta(alpha,beta,depth-1,pos)
        pos.undoMove()

        if score > bestScore:
            bestScore = score
            bestMove = move

    print(getOrig(bestMove),getDes(bestMove))
    return bestMove

def test():
    initAttacks()
    cdef Position pos = Position()
    pos.posFromFEN('r3k2r/p1ppqpb1/bn1Ppnp1/4N3/1p2P2p/2N2Q2/1PPBBPPP/R3K2R w KQkq - 0 1')

    return search(pos,3)
