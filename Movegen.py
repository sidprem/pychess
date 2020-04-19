# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:29:43 2020

@author: Sid
"""

from Bitboard import shiftBitBoard, getBitBoardByPieceandColor, BB_SQUARES, \
    BB_A_FILE, BB_B_FILE, BB_C_FILE, BB_D_FILE, BB_E_FILE, BB_F_FILE, BB_G_FILE, \
    BB_H_FILE, BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, \
    BB_RANK_7, BB_RANK_8, BB_EMPTY, BB_ALL_SQUARE

from Utils import Color, Direction, PieceType

#generate psuedo moves

def generatePseudoLegalMoves(bb,color):
    
    pawnMoves = generatePawnMoves(bb,color)
    

#pseudo legal pawn moves pawn moves
def generatePawnMoves(bb: int, color: Color):
    
    #init list of moves
    moves = [];
    
    #get pawns
    us = color
    them = ~color & 1
    
    us_pawns = getBitBoardByPieceandColor(us,PieceType.PAWN.value)
    them_pawns = getBitBoardByPieceandColor(them,PieceType.PAWN.value)
    
    #promotion potential pawns
    pawnsToPromote = (us_pawns & BB_RANK_7) if us == Color.WHITE.value else (us_pawns & BB_RANK_2)
    
    #potential double move pawns
    pawnsNotMoved = (us_pawns & BB_RANK_2) if us == Color.WHITE.value else (us_pawns & BB_RANK_7)
    #rest of pawns
    pawnsNotPromote = us_pawns & (~pawnsToPromote & BB_ALL_SQUARE)
    
    #quiet pawn move
    pawnsNormalMoves = shiftBitBoard(pawnsNotPromote,Direction.N.value)
    
    #double pawn moves
    pawnDoubleMoves = shiftBitBoard(pawnsNotMoved,2*Direction.N.value)
        
    #
    
def generateKingMoves(bb: int, color: Color):
    moves = []

def generateKnightMoves(bb: int, color: Color):
    moves = []
    
    # get color
    us = color
    them = ~color & 1
    
    us_kights = getBitBoardByPieceandColor(us, PieceType.KIGHT.value)
    them_knight = getBitBoardByPieceandColor(them, PieceType.KNIGHT.value)

    nne = shiftBitBoard(bb, 2*Direction.N.value + Direction.E.value)
    nee = shiftBitBoard(bb, Direction.N.value + 2*Direction.E.value)
    nnw = shiftBitBoard(bb, 2*Direction.N.value + Direction.W.value)
    nww = shiftBitBoard(bb, Direction.N.value + 2*Direction.W.value)
    sse = shiftBitBoard(bb, 2*Direction.S.value + Direction.E.value)
    see = shiftBitBoard(bb, Direction.S.value + 2*Direction.E.value)
    ssw = shiftBitBoard(bb, 2*Direction.S.value + Direction.W.value)
    sww = shiftBitBoard(bb, Direction.S.value + 2*Direction.W.value)