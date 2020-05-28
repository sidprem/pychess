# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:29:43 2020

@author: Sid
"""

from Bitboard_old import shiftBitBoard, BB_SQUARES, \
    BB_A_FILE, BB_B_FILE, BB_C_FILE, BB_D_FILE, BB_E_FILE, BB_F_FILE, BB_G_FILE, \
    BB_H_FILE, BB_RANK_1, BB_RANK_2, BB_RANK_3, BB_RANK_4, BB_RANK_5, BB_RANK_6, \
    BB_RANK_7, BB_RANK_8, BB_EMPTY, BB_ALL_SQUARES, BB_NOT_A_FILE, BB_NOT_B_FILE, \
    BB_NOT_H_FILE, BB_NOT_G_FILE, BB_SQUARES, prettyPrintBitBoard, iterBits, pop_lsb, pop_count

from Utils_old import WHITE, BLACK, N, S, E, W, PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, \
    moveFlag, NORMAL, ENPASSANT, KING_CASTLE, QUEEN_CASTLE, W_OO, W_OOO, B_OO, B_OOO

from MoveTables import attacksFrom, attackersTo, betweenBB, inRay

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

#generate evasions
def generateEvasionMoves(pos):

    us = pos.color
    notFriends = ~pos.us & BB_ALL_SQUARES

    #double check
    if pop_count(pos.checkers) > 1:
        #king moves out of check
        usKing = pos.board[us][KING]
        checkerAttacks = 0
        for cord in iterBits(pos.checkers):
            checkerAttacks |= attacksFrom(pos.pieceBoard[cord],cord,blocker=0)

        notCheckAttacks = ~checkerAttacks & BB_ALL_SQUARES

        for bits in iterBits(usKing):
            for m in iterBits(attacksFrom(KING,bits) & notFriends & notCheckAttacks):
                yield createMove(bits,m,0)
    #single check
    else:
        #king move out of check
        usKing = pos.board[us][KING]
        checkerAttacks = 0
        cord = pop_lsb(pos.checkers)
        checkerAttacks = attacksFrom(pos.pieceBoard[cord],cord,blocker=0)

        notCheckAttacks = ~checkerAttacks & BB_ALL_SQUARES

        kingSq = pop_lsb(usKing)
        for m in iterBits(attacksFrom(KING,kingSq) & notFriends & notCheckAttacks):
            yield createMove(kingSq,m,0)

        #capture checker
        checkerAttackers = attackersTo(pos.board[pos.color],pos.blocker,cord,pos.color)

        promoteRank = BB_RANK_7 if us == WHITE else BB_RANK_2
        for bits in iterBits(checkerAttackers):
            if pos.pieceBoard[bits] == PAWN:
                if BB_SQUARES[bits] & promoteRank:
                    for p in moveFlag[4:]:
                        yield createMove(bits,cord,p)
                else:
                    yield createMove(bits,cord,0)
            else:
                yield createMove(bits,cord,0)

        #check if en-passant capture will remove checker
        direction = N if us == WHITE else S
        if (pos.enpassant == cord + direction) & (pos.pieceBoard[cord] == PAWN):
            pawnsAtEp = attackersTo(pos.board[us],pos.blocker,pos.enpassant,us)
            for bits in iterBits(pawnsAtEp):
                yield createMove(bits,pos.enpassant,ENPASSANT)

        #block check
        between = betweenBB(cord,kingSq)
        for bb in pos.board[us][KNIGHT:]:
            for sq in iterBits(bb):
                piece = pos.pieceBoard[sq]
                if piece != KING:
                    attack = attacksFrom(piece,sq,color=us,blocker=pos.blocker)
                    for m in iterBits(attack & between):
                        yield createMove(sq,m,0)

        #pawns set-wise
        usPawns = pos.board[us][PAWN]

        emptySquares = ~(pos.blocker) & BB_ALL_SQUARES

        pawnsToPromote = (usPawns & BB_RANK_7) if us == WHITE else (usPawns & BB_RANK_2)

        pawnsNotMoved = (usPawns & BB_RANK_2) if us == WHITE else (usPawns & BB_RANK_7)

        pawnsNotPromote = usPawns & (~pawnsToPromote & BB_ALL_SQUARES)

        pawnNormalMoves = shiftBitBoard(pawnsNotPromote,direction) & emptySquares & between

        for bits in iterBits(pawnNormalMoves):
            yield createMove(bits - direction, bits, NORMAL)

        pawnNotMovedShift = shiftBitBoard(pawnsNotMoved,direction) & emptySquares
        pawnDoubleMoves = shiftBitBoard(pawnNotMovedShift,direction) & emptySquares & between

        for bits in iterBits(pawnDoubleMoves):
            yield createMove(bits - 2*direction, bits, NORMAL)

        #quiet pawn promotions bb
        pawnPromotions = shiftBitBoard(pawnsToPromote,direction) & emptySquares & between

        for bits in iterBits(pawnPromotions):
            for p in moveFlag[4:]:
                yield createMove(bits - direction, bits, p)

#generate psuedo moves
def generatePseudoLegalMoves(pos):
    yield from generatePawnMoves(pos)
    yield from generateKnightMoves(pos)
    yield from generateKingMoves(pos)
    yield from generateBishopMoves(pos)
    yield from generateRookMoves(pos)
    yield from generateQueenMoves(pos)

#pseudo legal pawn moves pawn moves
def generatePawnMoves(pos):

    #get pawns
    us = pos.color

    direction = N if us == WHITE else S

    enemies = pos.them

    usPawns = pos.board[us][PAWN]

    emptySquares = ~(pos.blocker) & BB_ALL_SQUARES

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
    pawnCapturesNE = shiftBitBoard(pawnsNotPromote & BB_NOT_H_FILE,direction + E) & enemies
    for bits in iterBits(pawnCapturesNE):
        yield createMove(bits - (direction + E), bits, NORMAL)

    pawnCapturesNW = shiftBitBoard(pawnsNotPromote & BB_NOT_A_FILE,direction + W) & enemies
    for bits in iterBits(pawnCapturesNW):
        yield createMove(bits - (direction + W), bits, NORMAL)

    #capture pawn promotions
    pawnCapturePromoNE = shiftBitBoard(pawnsToPromote & BB_NOT_H_FILE,direction + E) & enemies
    for bits in iterBits(pawnCapturePromoNE):
        for p in moveFlag[4:]:
            yield createMove(bits - (direction + E), bits, p)

    pawnCapturePromoNW = shiftBitBoard(pawnsToPromote & BB_NOT_A_FILE,direction + W) & enemies
    for bits in iterBits(pawnCapturePromoNW):
        for p in moveFlag[4:]:
            yield createMove(bits - (direction + W), bits, p)

    if(pos.enpassant != -1):
        pawnsAtEp = attackersTo(pos.board[us],pos.blocker,pos.enpassant,us) & usPawns
        for bits in iterBits(pawnsAtEp):
            yield createMove(bits,pos.enpassant,ENPASSANT)

def generateKingMoves(pos):

    us = pos.color

    usKing = pos.board[us][KING]

    emptySquares = ~(pos.blocker) & BB_ALL_SQUARES

    notFriends = ~pos.us & BB_ALL_SQUARES

    for bits in iterBits(usKing):
        for m in iterBits(attacksFrom(KING,bits) & notFriends):
            yield createMove(bits,m,0)

    if us == WHITE:
        if pos.castles & W_OO:
            wooStepOvers = betweenBB(4,7)
            if (wooStepOvers & emptySquares) == wooStepOvers:
                yield createMove(4,6,KING_CASTLE)
        if pos.castles & W_OOO:
            woooStepOvers = betweenBB(0,4)
            if (woooStepOvers & emptySquares) == woooStepOvers:
                yield createMove(4,2,QUEEN_CASTLE)
    elif us == BLACK:
        if pos.castles & B_OO:
            booStepOvers = betweenBB(60,63)
            if (booStepOvers & emptySquares) == booStepOvers:
                yield createMove(60,62,KING_CASTLE)
        if pos.castles & B_OOO:
            boooStepOvers = betweenBB(56,60)
            if (boooStepOvers & emptySquares) == boooStepOvers:
                yield createMove(60,58,QUEEN_CASTLE)


def generateKnightMoves(pos):

    # get color
    us = pos.color

    usKnights = pos.board[us][KNIGHT]

    notFriends = ~pos.us & BB_ALL_SQUARES

    for bits in iterBits(usKnights):
        for m in iterBits(attacksFrom(KNIGHT,bits) & notFriends):
            yield createMove(bits,m,0)

def generateBishopMoves(pos):

    us = pos.color

    blocker = pos.blocker

    usBishops = pos.board[us][BISHOP]

    notFriends = ~pos.us & BB_ALL_SQUARES

    for sq in iterBits(usBishops):

        attack = attacksFrom(BISHOP,sq,blocker=blocker) & notFriends

        for m in iterBits(attack):
            yield createMove(sq,m,0)

def generateRookMoves(pos):

    us = pos.color

    blocker = pos.blocker

    usRooks = pos.board[us][ROOK]

    notFriends = ~pos.us & BB_ALL_SQUARES

    for sq in iterBits(usRooks):

        attack = attacksFrom(ROOK,sq,blocker=blocker) & notFriends

        for m in iterBits(attack):
            yield createMove(sq,m,0)

def generateQueenMoves(pos):

    us = pos.color

    blocker = pos.blocker

    usQueens = pos.board[us][QUEEN]

    notFriends = ~pos.us & BB_ALL_SQUARES

    for sq in iterBits(usQueens):
        attack = (attacksFrom(BISHOP,sq,blocker=blocker) | attacksFrom(ROOK,sq,blocker=blocker)) & notFriends
        for m in iterBits(attack):
            yield createMove(sq,m,0)

def generateLegalMoves(pos):
    
    moveList = generateEvasionMoves(pos) if pos.isInCheck() else generatePseudoLegalMoves(pos)

    absolutelyPinned = pos.pinned

    for move in moveList:
        
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)
            
        if flag == ENPASSANT:
            newUsPieces = pos.us ^ BB_SQUARES[orig] ^ BB_SQUARES[des]
            direction = N if pos.color == WHITE else S
            newThemPieces = pos.them ^ BB_SQUARES[des - direction]
            newBoard = pos.board
            newBoard[pos.opColor][0] =newBoard[pos.opColor][0] ^ BB_SQUARES[des - direction]
            checkers = attackersTo(newBoard[pos.opColor],newUsPieces | newThemPieces,pos.king,pos.opColor)
            if checkers == 0:
                yield move
        elif flag == KING_CASTLE:
            stepOver = betweenBB(4,7) if  pos.color == WHITE else betweenBB(60,63)
            squareAttacked = 0
            for sq in iterBits(stepOver):
                squareAttacked |= attackersTo(pos.board[pos.opColor],pos.blocker,sq,pos.opColor)
            if squareAttacked == 0:
                yield move
        elif flag == QUEEN_CASTLE:
            stepOver = betweenBB(0,4) if  pos.color == WHITE else betweenBB(56,60)
            squareAttacked = 0
            for sq in iterBits(stepOver):
                squareAttacked |= attackersTo(pos.board[pos.opColor],pos.blocker,sq,pos.opColor)
            if squareAttacked == 0:
                yield move

        if pos.pieceBoard[orig] == KING:
            if flag == NORMAL:
                squareAttacked = attackersTo(pos.board[pos.opColor],pos.blocker,des,pos.opColor)
                if ~(squareAttacked > 0) & 1:
                    yield move
        elif ((~absolutelyPinned & BB_ALL_SQUARES) & BB_SQUARES[orig]) | inRay(orig,des,pos.king):
            if flag == NORMAL:
                yield move

