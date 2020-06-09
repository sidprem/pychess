# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:11:45 2020

@author: Sid
"""

from Bitboard cimport pop_count, pop_lsb, attacksFrom, attackersTo, lsb, BB_RANK_7, BB_RANK_2, BB_SQUARES, betweenBB, shiftBitBoard, prettyPrintBitBoard, \
                        BB_NOT_H_FILE, BB_NOT_A_FILE, inRay

from Utils cimport PIECE, COLOR, MAX_MOVES, USI, ULL, MOVE_FLAG, DIRECTION, CASTLE

from Position cimport Position

from cpython cimport array
import array
import numpy as np

#generate evasions moves
cpdef array.array generateEvasionMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef int i, cord, kingSq, checkSq, piece, sq
    cdef COLOR us
    cdef DIRECTION direction
    cdef MOVE_FLAG p
    cdef ULL checkerAttacks, notCheckAttacks, checkerAttackers, safeKingMoves, notFriends
    cdef ULL promoteRank, pawnsAtEp, usPawns, pawnsToPromote, pawnsNotMoved, pawnsNotPromote, pawnNormalMoves, pawnNotMovedShift, pawnDoubleMoves
    cdef ULL emptySquares, between, pawnPromotions, checkers, attack
    us = pos.color
    notFriends = ~pos.us
    
    checkers = pos.checkers
    i = 0
    #double check
    if pop_count(pos.checkers) > 1:
        #king moves out of check  
        kingSq = pos.king
        while checkers:
            checkSq = lsb(checkers)
            checkerAttacks |= attacksFrom(<PIECE>pos.pieceBoard[checkSq],checkSq,COLOR.WHITE,pos.blocker & ~BB_SQUARES[kingSq])
            checkers = pop_lsb(checkers)

        notCheckAttacks = ~checkerAttacks
        
        safeKingMoves = attacksFrom(PIECE.KING,kingSq,COLOR.WHITE,0) & notFriends & notCheckAttacks
        while safeKingMoves:
            cord = lsb(safeKingMoves)
            moveList[i] = createMove(kingSq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(kingSq,cord,8)
            i+=1
            safeKingMoves = pop_lsb(safeKingMoves)
    #single check
    else:
        #king move out of check
        kingSq = pos.king
        checkSq = lsb(checkers)
        checkerAttacks = attacksFrom(<PIECE>pos.pieceBoard[checkSq],checkSq,COLOR.WHITE,pos.blocker & ~BB_SQUARES[kingSq])
        notCheckAttacks = ~checkerAttacks
        safeKingMoves = attacksFrom(PIECE.KING,kingSq,COLOR.WHITE,0) & notFriends & notCheckAttacks
        while safeKingMoves:
            cord = lsb(safeKingMoves)
            moveList[i] = createMove(kingSq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(kingSq,cord,8)
            i+=1
            safeKingMoves = pop_lsb(safeKingMoves)
            
        #capture checker
        checkerAttackers = attackersTo(pos.board,pos.blocker,checkSq) & pos.us
        promoteRank = BB_RANK_7 if us == COLOR.WHITE else BB_RANK_2
        while checkerAttackers:
            cord = lsb(checkerAttackers)
            if pos.pieceBoard[cord] == <int>PIECE.PAWN:
                if BB_SQUARES[cord] & promoteRank:
                    for p in [MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO]:
                        moveList[i] = createMove(cord,checkSq,<int>p)
                        i+=1
                else:
                    moveList[i] = createMove(cord,checkSq,8)
                    i+=1
            else:
                if pos.pieceBoard[cord] != <int>PIECE.KING:
                    moveList[i] = createMove(cord,checkSq,8)
                    i+=1
            checkerAttackers = pop_lsb(checkerAttackers)

        #check if en-passant capture will remove checker
        direction = DIRECTION.N if us == <int>COLOR.WHITE else DIRECTION.S
        if (pos.enpassant == checkSq + <int>direction) & (pos.pieceBoard[checkSq] == <int>PIECE.PAWN):
            pawnsAtEp = attackersTo(pos.board,pos.blocker,pos.enpassant) & pos.us
            while pawnsAtEp:
                cord = lsb(pawnsAtEp)
                moveList[i] = createMove(cord,pos.enpassant,MOVE_FLAG.ENPASSANT)
                i+=1
                pawnsAtEp = pop_lsb(pawnsAtEp)
        #block check
        between = betweenBB(checkSq,kingSq)
        for bb in pos.board[<int>us,<int>PIECE.KNIGHT:]:
            while bb:
                sq = lsb(bb)
                piece = pos.pieceBoard[sq]
                if piece != <int>PIECE.KING:
                    attack = attacksFrom(<PIECE>piece,sq,us,pos.blocker) & between & notFriends
                    while (attack):
                        cord = lsb(attack & between & notFriends)
                        moveList[i] = createMove(sq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(sq,cord,8)
                        i+=1
                        attack = pop_lsb(attack)
                bb = pop_lsb(bb)

        #pawns set-wise
        usPawns = pos.board[<int>us,<int>PIECE.PAWN]

        emptySquares = ~pos.blocker

        pawnsToPromote = (usPawns & BB_RANK_7) if us == COLOR.WHITE else (usPawns & BB_RANK_2)

        pawnsNotMoved = (usPawns & BB_RANK_2) if us == COLOR.WHITE else (usPawns & BB_RANK_7)

        pawnsNotPromote = usPawns & ~pawnsToPromote

        pawnNormalMoves = shiftBitBoard(pawnsNotPromote,direction) & emptySquares & between
        while pawnNormalMoves:
            cord = lsb(pawnNormalMoves)
            moveList[i] = createMove(cord - <int>direction, cord, 0)
            i+=1
            pawnNormalMoves = pop_lsb(pawnNormalMoves)

        pawnNotMovedShift = shiftBitBoard(pawnsNotMoved,direction) & emptySquares
        pawnDoubleMoves = shiftBitBoard(pawnNotMovedShift,direction) & emptySquares & between
        
        while pawnDoubleMoves:
            cord = lsb(pawnDoubleMoves)
            moveList[i] = createMove(cord - 2*<int>direction, cord, 0)
            i+=1
            pawnDoubleMoves = pop_lsb(pawnDoubleMoves)       
            
        #quiet pawn promotions bb
        pawnPromotions = shiftBitBoard(pawnsToPromote,direction) & emptySquares & between
        
        while pawnPromotions:
            cord = lsb(pawnPromotions)
            for p in [MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO]:
                moveList[i] = createMove(cord - <int>direction, cord, <int>p)
                i+=1
            pawnPromotions = pop_lsb(pawnPromotions)  

    array.resize(moveList,i)
    return moveList

#generate psuedo moves
cdef array.array generatePseudoLegalMoves(Position pos):
    cdef array.array moveList = generatePawnMoves(pos)
    cdef array.array knightMoves = generateKnightMoves(pos)
    cdef array.array kingMoves = generateKingMoves(pos)
    cdef array.array bishopMoves = generateBishopMoves(pos)
    cdef array.array rookMoves = generateRookMoves(pos)
    cdef array.array queenMoves = generateQueenMoves(pos)
    array.extend(moveList,knightMoves)
    array.extend(moveList,kingMoves)
    array.extend(moveList,bishopMoves)
    array.extend(moveList,rookMoves)
    array.extend(moveList,queenMoves)

    return moveList


#pseudo legal pawn moves
cdef array.array generatePawnMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef int cord, i
    cdef COLOR us
    cdef DIRECTION direction
    cdef ULL enemies, usPawns, emptSquares, pawnsToPromote, pawnsNotMoved, pawnsNormalMoves, pawnsNotMovedShift, pawnsDoubleMoves
    cdef ULL pawnPromotions, pawnCapturesNE, pawnCapturesNW, pawnCapturePromoNE, pawnCapturePromoNW, pawnsAtEP
    i = 0
    #get pawns
    us = pos.color

    direction = DIRECTION.N if us == COLOR.WHITE else DIRECTION.S
    directionAttackW = DIRECTION.NW if us == COLOR.WHITE else DIRECTION.SW
    directionAttackE = DIRECTION.NE if us == COLOR.WHITE else DIRECTION.SE
    
    enemies = pos.them
    usPawns = pos.board[<int>us,<int>PIECE.PAWN]
    emptySquares = ~pos.blocker
    
    pawnsToPromote = (usPawns & BB_RANK_7) if us == COLOR.WHITE else (usPawns & BB_RANK_2)

    pawnsNotMoved = (usPawns & BB_RANK_2) if us == COLOR.WHITE else (usPawns & BB_RANK_7)

    pawnsNotPromote = usPawns & ~pawnsToPromote

    pawnNormalMoves = shiftBitBoard(pawnsNotPromote,direction) & emptySquares
    while pawnNormalMoves:
        cord = lsb(pawnNormalMoves)
        moveList[i] = createMove(cord - <int>direction, cord,0)
        i+=1
        pawnNormalMoves = pop_lsb(pawnNormalMoves)

    pawnDoubleMoves = shiftBitBoard(shiftBitBoard(pawnsNotMoved,direction) & emptySquares,direction) & emptySquares
    while pawnDoubleMoves:
        cord = lsb(pawnDoubleMoves)
        moveList[i] = createMove(cord - 2*<int>direction,cord,0)
        i+=1
        pawnDoubleMoves = pop_lsb(pawnDoubleMoves)

    #quiet pawn promotions bb
    pawnPromotions = shiftBitBoard(pawnsToPromote,direction) & emptySquares
    while pawnPromotions:
        cord = lsb(pawnPromotions)
        for p in [MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO]:
            moveList[i] = createMove(cord - <int>direction, cord, p)
            i+=1
        pawnPromotions = pop_lsb(pawnPromotions)

    #capture pawn moves
    pawnCapturesNE = shiftBitBoard(pawnsNotPromote & BB_NOT_H_FILE,directionAttackE) & enemies
    while pawnCapturesNE:
        cord = lsb(pawnCapturesNE)
        moveList[i] = createMove(cord - <int>directionAttackE,cord,8)
        i+=1
        pawnCapturesNE = pop_lsb(pawnCapturesNE)
        
    pawnCapturesNW = shiftBitBoard(pawnsNotPromote & BB_NOT_A_FILE,directionAttackW) & enemies
    while pawnCapturesNW:
        cord = lsb(pawnCapturesNW)
        moveList[i] = createMove(cord - <int>directionAttackW, cord,8)
        i+=1
        pawnCapturesNW = pop_lsb(pawnCapturesNW)

    #capture pawn promotions
    pawnCapturePromoNE = shiftBitBoard(pawnsToPromote & BB_NOT_H_FILE,directionAttackE) & enemies
    while pawnCapturePromoNE:
        cord = lsb(pawnCapturePromoNE)
        for p in [MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO]:
            moveList[i] = createMove(cord - <int>directionAttackE, cord, p)
            i+=1
        pawnCapturePromoNE = pop_lsb(pawnCapturePromoNE)

    pawnCapturePromoNW = shiftBitBoard(pawnsToPromote & BB_NOT_A_FILE,directionAttackW) & enemies
    while pawnCapturePromoNW:
        cord = lsb(pawnCapturePromoNW)
        for p in [MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO]:
            moveList[i] = createMove(cord - <int>directionAttackW, cord, <int>p)
            i+=1
        pawnCapturePromoNW = pop_lsb(pawnCapturePromoNW)

    if(pos.enpassant != -1):
        pawnsAtEp = attackersTo(pos.board,pos.blocker,pos.enpassant) & usPawns
        while pawnsAtEp:
            cord = lsb(pawnsAtEp)
            moveList[i] = createMove(cord,pos.enpassant,MOVE_FLAG.ENPASSANT)
            i+=1
            pawnsAtEp = pop_lsb(pawnsAtEp)
    
    array.resize(moveList,i)
    return moveList

#pseudo legal king moves
cdef array.array generateKingMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef COLOR us
    cdef ULL emptySquares, notFriends
    cdef int i, cord, kingSq
    i = 0
    us = pos.color
    kingSq = pos.king
    emptySquares = ~pos.blocker

    notFriends = ~pos.us
    
    kingAttacks = attacksFrom(PIECE.KING,kingSq,us,pos.blocker) & notFriends
    while kingAttacks:
        cord = lsb(kingAttacks)
        moveList[i] = createMove(kingSq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(kingSq,cord,8)
        i+=1
        kingAttacks = pop_lsb(kingAttacks)

    if us == COLOR.WHITE:
        if pos.castles & CASTLE.W_OO:
            wooStepOvers = betweenBB(4,7)
            if (wooStepOvers & emptySquares) == wooStepOvers:
                moveList[i] = createMove(4,6,MOVE_FLAG.KING_CASTLE)
                i+=1
        if pos.castles & CASTLE.W_OOO:
            woooStepOvers = betweenBB(0,4)
            if (woooStepOvers & emptySquares) == woooStepOvers:
                moveList[i] = createMove(4,2,MOVE_FLAG.QUEEN_CASTLE)
                i+=1
    elif us == COLOR.BLACK:
        if pos.castles & CASTLE.B_OO:
            booStepOvers = betweenBB(60,63)
            if (booStepOvers & emptySquares) == booStepOvers:
                moveList[i] = createMove(60,62,MOVE_FLAG.KING_CASTLE)
                i+=1
        if pos.castles & CASTLE.B_OOO:
            boooStepOvers = betweenBB(56,60)
            if (boooStepOvers & emptySquares) == boooStepOvers:
                moveList[i] = createMove(60,58,MOVE_FLAG.QUEEN_CASTLE)
                i+=1
                
    array.resize(moveList,i)
    return moveList

#pseudo legal knight moves
cdef array.array generateKnightMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef COLOR us
    cdef int cord, i, sq
    cdef ULL notFriends, usKnights, attacks
    i = 0
    us = pos.color

    usKnights = pos.board[<int>us,<int>PIECE.KNIGHT]

    notFriends = ~pos.us
    
    while usKnights:
        sq = lsb(usKnights)  
        attacks = attacksFrom(PIECE.KNIGHT,sq,us,pos.blocker) & notFriends
        while attacks:
            cord = lsb(attacks)
            moveList[i] = createMove(sq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(sq,cord,8)
            i+=1
            attacks = pop_lsb(attacks)
        usKnights = pop_lsb(usKnights)
        
    array.resize(moveList,i)
    return moveList        
    
#pseudo legal bishop movess
cdef array.array generateBishopMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef COLOR us
    cdef int cord, i, sq
    cdef ULL notFriends, blocker, usBishops, attacks
    i = 0
    us = pos.color

    blocker = pos.blocker

    usBishops = pos.board[<int>us,<int>PIECE.BISHOP]

    notFriends = ~pos.us

    while usBishops:
        sq = lsb(usBishops)  
        attacks = attacksFrom(PIECE.BISHOP,sq,us,blocker) & notFriends
        while attacks:
            cord = lsb(attacks)
            moveList[i] = createMove(sq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(sq,cord,8)
            i+=1
            attacks = pop_lsb(attacks)
        usBishops = pop_lsb(usBishops)

    array.resize(moveList,i)
    return moveList  

cdef array.array generateRookMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef COLOR us
    cdef int cord, i, sq
    cdef ULL notFriends, blocker, usRooks, attacks
    i = 0
    us = pos.color

    blocker = pos.blocker

    usRooks = pos.board[<int>us,<int>PIECE.ROOK]

    notFriends = ~pos.us

    while usRooks:
        sq = lsb(usRooks)  
        attacks = attacksFrom(PIECE.ROOK,sq,us,blocker) & notFriends
        while attacks:
            cord = lsb(attacks)
            moveList[i] = createMove(sq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(sq,cord,8)
            i+=1
            attacks = pop_lsb(attacks)
        usRooks = pop_lsb(usRooks)

    array.resize(moveList,i)
    return moveList  

cdef array.array generateQueenMoves(Position pos):
    cdef array.array moveList = array.array('H',[0]*MAX_MOVES)
    cdef COLOR us
    cdef int cord, i, sq
    cdef ULL notFriends, blocker, usQueens, attacks
    i = 0
    us = pos.color

    blocker = pos.blocker
    usQueens = pos.board[<int>us,<int>PIECE.QUEEN]

    notFriends = ~pos.us

    while usQueens:
        sq = lsb(usQueens)  
        attacks = attacksFrom(PIECE.QUEEN,sq,us,blocker) & notFriends
        while attacks:
            cord = lsb(attacks)
            moveList[i] = createMove(sq,cord,0) if pos.pieceBoard[cord] == <int>PIECE.EMPTY else createMove(sq,cord,8)
            i+=1
            attacks = pop_lsb(attacks)
        usQueens = pop_lsb(usQueens)

    array.resize(moveList,i)
    return moveList  

cdef USI[:] generateLegalMoves(Position pos):
    cdef USI[:] legalMoves
    cdef ULL absolutelyPinned, newUsPieces, newThemPieces, checkers, stepOver, squareAttacked
    cdef USI orig, des, flag
    cdef DIRECTION direction
    cdef ULL[:,:] newBoard = np.zeros((2,6),dtype=np.uint64)
    cdef int i, sq, j, k
    cdef array.array pseudoLegalMoves = generateEvasionMoves(pos) if pos.isInCheck() else generatePseudoLegalMoves(pos)
    cdef array.array lMoves = array.clone(pseudoLegalMoves, len(pseudoLegalMoves), zero=True)
    
    absolutelyPinned = pos.pinned
    i = 0
    for move in pseudoLegalMoves:
        
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)
            
        if flag == MOVE_FLAG.ENPASSANT:
            newUsPieces = pos.us ^ BB_SQUARES[orig] ^ BB_SQUARES[des]
            direction = DIRECTION.N if pos.color == COLOR.WHITE else DIRECTION.S
            newThemPieces = pos.them ^ BB_SQUARES[des - <int>direction]
            for k from 0 <= k < len(pos.board):
                for j from 0 <= j < len(pos.board[k]):
                    newBoard[k,j] = pos.board[k,j]
            newBoard[<int>pos.opColor,0] = newBoard[<int>pos.opColor,0] ^ BB_SQUARES[des - <int>direction]
            checkers = attackersTo(newBoard,newUsPieces | newThemPieces,pos.king) & newThemPieces
            if checkers == <ULL>0:
                lMoves[i] = move
                i+=1
        elif flag == MOVE_FLAG.KING_CASTLE:
            stepOver = betweenBB(4,7) if  pos.color == COLOR.WHITE else betweenBB(60,63)
            squareAttacked = 0
            while stepOver:
                sq = lsb(stepOver)
                squareAttacked |= attackersTo(pos.board,pos.blocker,sq) & pos.them
                stepOver = pop_lsb(stepOver)
            if squareAttacked == 0:
                lMoves[i] = move
                i+=1
        elif flag == MOVE_FLAG.QUEEN_CASTLE:
            stepOver = betweenBB(1,4) if  pos.color == COLOR.WHITE else betweenBB(57,60)
            squareAttacked = 0
            while stepOver:
                sq = lsb(stepOver)
                squareAttacked |= attackersTo(pos.board,pos.blocker,sq) & pos.them
                stepOver = pop_lsb(stepOver)
            if squareAttacked == 0:
                lMoves[i] = move
                i+=1

        if pos.pieceBoard[orig] == <int>PIECE.KING:
            if (flag == MOVE_FLAG.NORMAL) | (flag == MOVE_FLAG.CAPTURES):
                squareAttacked = attackersTo(pos.board,pos.blocker,des) & pos.them
                if (~(squareAttacked > 0)) & 1:
                    lMoves[i] = move
                    i+=1
        elif (~absolutelyPinned & BB_SQUARES[orig]) | inRay(orig,des,pos.king):
            if (flag == MOVE_FLAG.NORMAL) | (flag == MOVE_FLAG.CAPTURES) | (flag in [MOVE_FLAG.KNIGHT_PROMO,MOVE_FLAG.BISHOP_PROMO,MOVE_FLAG.ROOK_PROMO,MOVE_FLAG.QUEEN_PROMO]):
                lMoves[i] = move
                i+=1
    
    array.resize(lMoves,i)
    legalMoves = lMoves

    return legalMoves