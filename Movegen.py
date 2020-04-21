# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:29:43 2020

@author: Sid
"""

from Bitboard import shiftBitBoard, getBitBoardByColor, getBitBoardByPieceandColor, BB_SQUARES, \
    BB_A_FILE, BB_B_FILE, BB_C_FILE, BB_D_FILE, BB_E_FILE, BB_F_FILE, BB_G_FILE, \
    BB_H_FILE, BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, \
    BB_RANK_7, BB_RANK_8, BB_EMPTY, BB_ALL_SQUARES, BB_NOT_A_FILE, BB_NOT_B_FILE, \
    BB_NOT_H_FILE, BB_NOT_G_FILE, initBitBoard, prettyPrintBitBoard, initRandomBitBoard
    
from Utils import Color, Direction, PieceType

#generate psuedo moves

def generatePseudoLegalMoves(bb,color):
    
    pawnMoves = generatePawnMoves(bb,color)
    

#pseudo legal pawn moves pawn moves
def generatePawnMoves(bb: int, color: Color):
    
    #init list of moves
    moves = [];
    
    #get pawns
    us = color.value
    them = ~color.value & 1
    
    direction = Direction.N.value if us == Color.WHITE.value else Direction.S.value
    
    enemies = getBitBoardByColor(them)
    
    usPawns = getBitBoardByPieceandColor(us,PieceType.PAWN.value)
    themPawns = getBitBoardByPieceandColor(them,PieceType.PAWN.value)
    
    emptySquares = ~(getBitBoardByColor(us) | getBitBoardByColor(them)) & BB_ALL_SQUARES
    
    pawnsToPromote = (usPawns & BB_RANK_7) if us == Color.WHITE.value else (usPawns & BB_RANK_2)
    
    pawnsNotMoved = (usPawns & BB_RANK_2) if us == Color.WHITE.value else (usPawns & BB_RANK_7)

    pawnsNotPromote = usPawns & (~pawnsToPromote & BB_ALL_SQUARES)
    
    pawnNormalMoves = shiftBitBoard(pawnsNotPromote,direction) & emptySquares
    
    pawnDoubleMoves = shiftBitBoard(pawnsNotMoved,2*direction) & emptySquares
    
    #quiet pawn promotions bb
    pawnPromotions = shiftBitBoard(pawnsToPromote,direction) & emptySquares
    
    #capture pawn moves
    pawnCapturesNE = shiftBitBoard(pawnsNotPromote,direction + Direction.E.value) & enemies
    pawnCapturesNW = shiftBitBoard(pawnsNotPromote,direction + Direction.W.value) & enemies
    
    #capture pawn promotions
    pawnCapturePromoNE = shiftBitBoard(pawnsToPromote,direction + Direction.E.value) & enemies
    pawnCapturePromoNW = shiftBitBoard(pawnsToPromote,direction + Direction.E.value) & enemies
    
    #en passant captures
    #needs move history on any double pawn moves
    
    return moves
    
def generateKingMoves(bb: int, color: Color):
    moves = []

def generateKnightMoves(bb: int, color: Color):
    moves = []
    
    # get color
    us = color
    them = ~color & 1
    
    us_kights = getBitBoardByPieceandColor(us, PieceType.KIGHT.value)
    them_knight = getBitBoardByPieceandColor(them, PieceType.KNIGHT.value)

    #direction bitboards
    nne = shiftBitBoard(bb, 2*Direction.N.value + Direction.E.value) & BB_NOT_A_FILE
    nee = shiftBitBoard(bb, Direction.N.value + 2*Direction.E.value) & (BB_NOT_A_FILE & BB_NOT_B_FILE)
    nnw = shiftBitBoard(bb, 2*Direction.N.value + Direction.W.value) & (BB_NOT_A_FILE & BB_NOT_B_FILE)
    nww = shiftBitBoard(bb, Direction.N.value + 2*Direction.W.value) & BB_NOT_A_FILE
    sse = shiftBitBoard(bb, 2*Direction.S.value + Direction.E.value) & BB_NOT_H_FILE
    see = shiftBitBoard(bb, Direction.S.value + 2*Direction.E.value) & (BB_NOT_H_FILE & BB_NOT_G_FILE)
    ssw = shiftBitBoard(bb, 2*Direction.S.value + Direction.W.value) & (BB_NOT_H_FILE & BB_NOT_G_FILE)
    sww = shiftBitBoard(bb, Direction.S.value + 2*Direction.W.value) & BB_NOT_H_FILE
    
    
    
# def test():
    
#     initRandomBitBoard()
    
#     #get pawns
#     them = Color.WHITE.value
#     us = ~Color.WHITE.value & 1
    
#     direction = Direction.N.value if us == Color.WHITE.value else Direction.S.value
    
#     enemies = getBitBoardByColor(them)
    
#     usPawns = getBitBoardByPieceandColor(us,PieceType.PAWN.value)
#     themPawns = getBitBoardByPieceandColor(them,PieceType.PAWN.value)
    
#     emptySquares = ~(getBitBoardByColor(us) | getBitBoardByColor(them)) & BB_ALL_SQUARES
    
#     pawnsToPromote = (usPawns & BB_RANK_7) if us == Color.WHITE.value else (usPawns & BB_RANK_2)
    
#     pawnsNotMoved = (usPawns & BB_RANK_2) if us == Color.WHITE.value else (usPawns & BB_RANK_7)

#     pawnsNotPromote = usPawns & (~pawnsToPromote & BB_ALL_SQUARES)
    
#     pawnNormalMoves = shiftBitBoard(pawnsNotPromote,direction) & emptySquares
    
#     pawnDoubleMoves = shiftBitBoard(pawnsNotMoved,2*Direction.N.value) & emptySquares
        
#     #quiet pawn promotions bb
#     pawnPromotions = shiftBitBoard(pawnsToPromote,Direction.N.value) & emptySquares
    
#     #capture pawn moves
#     pawnCapturesNE = shiftBitBoard(pawnsNotPromote,Direction.NE.value) & enemies
#     pawnCapturesNW = shiftBitBoard(pawnsNotPromote,Direction.NW.value) & enemies
    
#     #capture pawn promotions
#     pawnCapturePromoNE = shiftBitBoard(pawnsToPromote,Direction.NE.value) & enemies
#     pawnCapturePromoNW = shiftBitBoard(pawnsToPromote,Direction.NW.value) & enemies
    
#     return prettyPrintBitBoard(pawnNormalMoves)
