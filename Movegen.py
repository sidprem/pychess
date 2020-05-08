# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:29:43 2020

@author: Sid
"""

from Bitboard import shiftBitBoard, BB_SQUARES, \
    BB_A_FILE, BB_B_FILE, BB_C_FILE, BB_D_FILE, BB_E_FILE, BB_F_FILE, BB_G_FILE, BB_B1, BB_C1, BB_D1, \
    BB_H_FILE, BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, BB_F1, BB_G1, \
    BB_RANK_7, BB_RANK_8, BB_EMPTY, BB_ALL_SQUARES, BB_NOT_A_FILE, BB_NOT_B_FILE, BB_B8, BB_C8, BB_D8, \
    BB_NOT_H_FILE, BB_NOT_G_FILE, BB_SQUARES, prettyPrintBitBoard, iterBits, BB_F8, BB_G8
    
from Utils import WHITE, BLACK, N, S, E, W, PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, \
    moveFlag, NORMAL, ENPASSANT, KING_CASTLE, QUEEN_CASTLE, W_OO, W_OOO, B_OO, B_OOO

from MoveTables import attacksFrom 

from itertools import chain 

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
def generatePseudoLegalMoves(pos):
    pawnMoves = generatePawnMoves(pos)
    knightMoves = generateKnightMoves(pos)
    kingMoves = generateKingMoves(pos)
    bishopMoves = generateBishopMoves(pos)
    rookMoves = generateRookMoves(pos)
    queenMoves = generateQueenMoves(pos)
    
    return chain(pawnMoves,knightMoves,kingMoves,bishopMoves,rookMoves,queenMoves)

#pseudo legal pawn moves pawn moves
def generatePawnMoves(pos):
    
    #get pawns
    us = pos.color
    
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
        for p in moveFlag[4:]:
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
        for p in moveFlag[4:]:
            yield createMove(bits - (direction + E), bits, p)
            
    pawnCapturePromoNW = shiftBitBoard(pawnsToPromote,direction + W) & enemies
    for bits in iterBits(pawnCapturePromoNW):
        for p in moveFlag[4:]:
            yield createMove(bits - (direction + W), bits, p)
    
    if(pos.enpassant != -1):
        ep_bb = BB_SQUARES[pos.enpassant]
        ep_viable_NE = shiftBitBoard(usPawns & enPassDir,direction + E) & ep_bb
        ep_viable_NW = shiftBitBoard(usPawns & enPassDir,direction + W) & ep_bb
        if ep_viable_NE:
            yield createMove(pos.enpassant - (direction + E),pos.enpassant,ENPASSANT)
        elif ep_viable_NW:
            yield createMove(pos.enpassant - (direction + W),pos.enpassant,ENPASSANT)
            
def generateKingMoves(pos):
    
    us = pos.color
    
    usKing = pos.board[us][KING]
    
    enemies = pos.them
    friends = pos.us
    
    emptySquares = ~(enemies | friends) & BB_ALL_SQUARES
    
    notFriends = ~friends & BB_ALL_SQUARES
    
    for bits in iterBits(usKing):
        for m in iterBits(attacksFrom(KING,bits) & notFriends):
            yield createMove(bits,m,0)
    
    if us == WHITE:
        if pos.castles & W_OO:
            stepOvers = BB_F1 | BB_G1
            if(stepOvers & emptySquares):
                yield createMove(4,6,KING_CASTLE)
        elif pos.castles & W_OOO:
            stepOvers = BB_B1 | BB_C1 | BB_D1
            if(stepOvers & emptySquares):
                yield createMove(4,2,QUEEN_CASTLE)
    elif us == BLACK:
        if pos.castles & B_OO:
            stepOvers = BB_F8 | BB_G8
            if(stepOvers & emptySquares):
                yield createMove(60,62,KING_CASTLE)
        elif pos.castles & B_OOO:
            stepOvers = BB_B8 | BB_C8 | BB_D8
            if(stepOvers & emptySquares):
                yield createMove(60,58,QUEEN_CASTLE)        
    
    
def generateKnightMoves(pos):

    # get color
    us = pos.color
    
    usKnights = pos.board[us][KNIGHT]
    
    friends = pos.us
    
    notFriends = ~friends & BB_ALL_SQUARES
    
    for bits in iterBits(usKnights):
        for m in iterBits(attacksFrom(KNIGHT,bits) & notFriends):
            yield createMove(bits,m,0)

def generateBishopMoves(pos):
    
    us = pos.color
    
    enemies = pos.them
    friends = pos.us
    
    blocker = enemies | friends

    usBishops = pos.board[us][BISHOP]
    
    notFriends = ~friends & BB_ALL_SQUARES
    
    for sq in iterBits(usBishops):

        attack = attacksFrom(BISHOP,sq,blocker=blocker) & notFriends
        
        for m in iterBits(attack):
            yield createMove(sq,m,0)

def generateRookMoves(pos):
    
    us = pos.color
    
    enemies = pos.them
    friends = pos.us
    
    blocker = enemies | friends
    
    usRooks = pos.board[us][ROOK]
    
    notFriends = ~friends & BB_ALL_SQUARES
    
    for sq in iterBits(usRooks):
        
        attack = attacksFrom(ROOK,sq,blocker=blocker) & notFriends
        
        for m in iterBits(attack):
            yield createMove(sq,m,0) 
            
def generateQueenMoves(pos):
    
    us = pos.color
    
    enemies = pos.them
    friends = pos.us
    
    blocker = enemies | friends
    
    usQueens = pos.board[us][QUEEN]
    
    notFriends = ~friends & BB_ALL_SQUARES
    
    for sq in iterBits(usQueens):

        attack = (attacksFrom(BISHOP,sq,blocker=blocker) | attacksFrom(ROOK,sq,blocker=blocker)) & notFriends
        
        for m in iterBits(attack):
            yield createMove(sq,m,0) 
