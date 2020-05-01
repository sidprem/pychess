# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:29:43 2020

@author: Sid
"""

from Bitboard import shiftBitBoard, BB_SQUARES, \
    BB_A_FILE, BB_B_FILE, BB_C_FILE, BB_D_FILE, BB_E_FILE, BB_F_FILE, BB_G_FILE, \
    BB_H_FILE, BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, \
    BB_RANK_7, BB_RANK_8, BB_EMPTY, BB_ALL_SQUARES, BB_NOT_A_FILE, BB_NOT_B_FILE, \
    BB_NOT_H_FILE, BB_NOT_G_FILE, BB_SQUARES, prettyPrintBitBoard, iterBits
    
from Utils import WHITE, BLACK, N, S, E, W, NW, SW, NE, SE, PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, EMPTY, \
    moveFlag, NORMAL, ENPASSANT, KING_CASTLE, QUEEN_CASTLE

from MoveTables import moveArray, RBITS, BBITS, BISHOP_MAGICS, ROOK_MAGICS, BISHOP_ATTACKS, \
    BISHOP_ATTACK_MASK, BISHOP_ATTACKS, ROOK_ATTACKS
    
from Position import Position

#0-5 from
#6-11 to
#12-16 Normal, enpassant, king castle, queen castle, knight promo, bishop promo, rook promo, queen promo 

#create move
def createMove(orig,des,flag):
    return orig | (des << 6) | (flag << 12)

def getOrig(move):
    return move & 0x3F

def getDes(move):
    return (move >> 6) & 0x3F

def getFlag(move):
    return (move >> 12) & 0x7

#generate psuedo moves
def generatePseudoLegalMoves(bb,color):
    pawnMoves = generatePawnMoves(bb,color)
    

#pseudo legal pawn moves pawn moves
def generatePawnMoves(pos):
    
    #get pawns
    us = pos.color
    them = ~pos.color & 1
    
    direction = N if us == WHITE else S
    
    enPassDir = BB_RANK_5 if us == WHITE else BB_RANK_4
    
    enemies = pos.them
    friends = pos.us
    
    usPawns = pos.board[us][PAWN]
    
    emptySquares = ~(enemies | friends) & BB_ALL_SQUARES
    
    pawnsToPromote = (usPawns & BB_RANK_7) if us == WHITE else (usPawns & BB_RANK_2)
    
    pawnsNotMoved = (usPawns & BB_RANK_2) if us == WHITE else (usPawns & BB_RANK_7)

    pawnsNotPromote = usPawns & (~pawnsToPromote & BB_ALL_SQUARES)
    
    pawnNormalMoves = shiftBitBoard(pawnsNotPromote,direction) & emptySquares
    
    
    for bits in iterBits(pawnNormalMoves):
        yield createMove(bits - direction, bits, NORMAL)
    
    pawnNotMovedShift = shiftBitBoard(pawnsNotMoved,direction) & emptySquares
    pawnDoubleMoves = shiftBitBoard(pawnNotMovedShift,direction) & emptySquares
    
    for bits in iterBits(pawnDoubleMoves):
        yield createMove(bits - 2*direction, bits, NORMAL)
    
    #quiet pawn promotions bb
    pawnPromotions = shiftBitBoard(pawnsToPromote,direction) & emptySquares
    
    for bits in iterBits(pawnPromotions):
        for p in moveFlag[3:]:
            yield createMove(bits - direction, bits, p)
    
    #capture pawn moves
    pawnCapturesNE = shiftBitBoard(pawnsNotPromote,direction + E) & enemies
    for bits in iterBits(pawnCapturesNE):
        yield createMove(bits - (direction + E), bits, NORMAL)
        
    pawnCapturesNW = shiftBitBoard(pawnsNotPromote,direction + W) & enemies
    for bits in iterBits(pawnCapturesNW):
        yield createMove(bits - (direction + W), bits, NORMAL)
        
    #capture pawn promotions
    pawnCapturePromoNE = shiftBitBoard(pawnsToPromote,direction + E) & enemies
    for bits in iterBits(pawnCapturePromoNE):
        for p in moveFlag[3:]:
            yield createMove(bits - (direction + E), bits, p)
            
    pawnCapturePromoNW = shiftBitBoard(pawnsToPromote,direction + W) & enemies
    for bits in iterBits(pawnCapturePromoNW):
        for p in moveFlag[3:]:
            yield createMove(bits - (direction + W), bits, p)
    
    if(pos.enpassant != -1):
        ep_bb = BB_SQUARES[pos.enpassant]
        ep_viable_NE = shiftBitBoard(usPawns & enPassDir,direction + E) & ep_bb
        ep_viable_NW = shiftBitBoard(usPawns & enPassDir,direction + W) & ep_bb
        if ep_viable_NE:
            yield createMove(pos.enpassant - (direction + E),pos.enpassant,ENPASSANT)
        elif ep_viable_NW:
            yield createMove(pos.enpassant - (direction + W),pos.enpassant,ENPASSANT)
            
# def generateKingMoves(bb: int, color: Color):
#     moves = []

# def generateKnightMoves(bb: int, color: Color):
#     moves = []
    
#     # get color
#     us = color
#     them = ~color & 1
    
#     us_kights = getBitBoardByPieceandColor(us, PieceType.KIGHT.value)
#     them_knight = getBitBoardByPieceandColor(them, PieceType.KNIGHT.value)

#     #direction bitboards
#     nne = shiftBitBoard(bb, 2*Direction.N.value + Direction.E.value) & BB_NOT_A_FILE
#     nee = shiftBitBoard(bb, Direction.N.value + 2*Direction.E.value) & (BB_NOT_A_FILE & BB_NOT_B_FILE)
#     nnw = shiftBitBoard(bb, 2*Direction.N.value + Direction.W.value) & (BB_NOT_A_FILE & BB_NOT_B_FILE)
#     nww = shiftBitBoard(bb, Direction.N.value + 2*Direction.W.value) & BB_NOT_A_FILE
#     sse = shiftBitBoard(bb, 2*Direction.S.value + Direction.E.value) & BB_NOT_H_FILE
#     see = shiftBitBoard(bb, Direction.S.value + 2*Direction.E.value) & (BB_NOT_H_FILE & BB_NOT_G_FILE)
#     ssw = shiftBitBoard(bb, 2*Direction.S.value + Direction.W.value) & (BB_NOT_H_FILE & BB_NOT_G_FILE)
#     sww = shiftBitBoard(bb, Direction.S.value + 2*Direction.W.value) & BB_NOT_H_FILE
    
    
    
def test():
    pos = Position()
    pos.posFromFEN("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    
    for i in generatePawnMoves(pos):
        orig = getOrig(i)
        des = getDes(i)
        print(orig)
        print(des)
        print("\n")
        prettyPrintBitBoard(BB_SQUARES[orig] | BB_SQUARES[des])
    
    
