# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:43:24 2020

@author: Sid
"""

from __future__ import print_function
from Utils cimport COLOR, PIECE, CASTLE, COLOR_STR, PIECE_STR, ALGEBRAIC, ULL, USI, DIRECTION, MOVE_FLAG, ALGPIECE, PIECE_EVAL
from Bitboard cimport setBits, clearBits, blockers, attackersTo, prettyPrintBitBoard, attacksFrom, betweenBB, pop_lsb, lsb, getFile, getRank, BB_SQUARES, BB_RANK_8, BB_RANK_1
from Movegen cimport getOrig, getDes, getFlag, createMove
from TranspositionTable cimport zobristHash
import numpy as np


cdef class Position:

    def __cinit__(self):
        self.board = np.zeros((2,6),dtype=np.uint64) #bitboard of each color for each piece
        self.pieceBoard = np.full(64,6,dtype=int) #board of pieceType for each cord
        self.pieceCount = np.zeros((2,6),dtype=int)
        self.enpassant = -1 #en passant target square cord
        self.king = 0 #king square cord
        self.castles = 0 #castle indicator W_OO | W_OOO | B_OO | B_OOO
        #TODO: self.repetition = 0
        self.color = COLOR.WHITE #color of mover
        self.opColor = COLOR.BLACK #color of Op
        self.us = 0 #mover pieces
        self.them = 0 #opponent pieces
        self.blocker = 0 #blockers on the board
        self.pinned = 0 #pieces absolutely pinned
        self.checkers = 0 #bitboard of all pieces attacking the mover kings
        self.zHash = 0 #zobrist hash for the position
        self.ply = 0  #half-move counter
      #  self.notation = ''
        self.history = { #history dictionary for undos
            "enpassant" : [],
            "castles" : [],
            "moves" : [],
            "captured" : [],
            "color" : [],
            "checkers" : [],
            "pinned" : [],
            "hash" : []
            }

    #creates a position class given a standard FEN str
    cpdef void posFromFEN(self,str fen):

        state = fen.split()
        pieces = state[0]
        mover = state[1]
        castles = state[2]
        ep = state[3]
        half_move = state[5]

        str_color = COLOR_STR.index(mover)
        self.color = <COLOR>str_color
        self.opColor = <COLOR>(~<int>self.color & 1)

        for r,rank in enumerate(pieces.split("/")):
            cord = (7-r)*8
            for ch in rank:
                if ch.isdigit():
                    cord+=int(ch)
                else:
                    piece = PIECE_STR.index(ch.upper())
                    color = COLOR.WHITE if ch.isupper() else COLOR.BLACK
                    self.setPiece(<PIECE>piece,<COLOR>color,cord)
                    if (piece == <int>PIECE.KING) & (self.color == color):
                        self.king = cord
                    cord+=1

        self.us = self.getUs()
        self.them = self.getThem()
        self.blocker = self.us | self.them

        for ch in castles:
            if ch == "K":
                self.castles = self.castles | CASTLE.W_OO
            elif ch == "Q":
                self.castles = self.castles | CASTLE.W_OOO
            elif ch == "k":
                self.castles = self.castles | CASTLE.B_OO
            elif ch == "q":
                self.castles = self.castles | CASTLE.B_OOO

        if ep != "-":
            self.enpassant = ALGEBRAIC.index(ep)
        else:
            self.enpassant = -1

        self.checkers = attackersTo(self.board,self.blocker,self.king) & self.them
        self.pinned = blockers(self.board[<int>self.opColor],self.blocker,self.king)
        self.ply = int(half_move)

    #sets pieces to the position board
    cdef void setPiece(self,PIECE piece,COLOR color,int cord):
        if piece != PIECE.EMPTY:
            self.board[<int>color,<int>piece] = setBits(self.board[<int>color,<int>piece],cord)
            self.pieceCount[<int>color,<int>piece] += 1
            self.zHash ^= zobristHash[<int>color,<int>piece,cord]
        self.pieceBoard[cord] = <int>piece

    #clears pieces from the position board
    cdef void clearPiece(self,PIECE piece,COLOR color,int cord):
        if piece != PIECE.EMPTY:
            self.board[<int>color,<int>piece] = clearBits(self.board[<int>color,<int>piece],cord)
            self.pieceCount[<int>color,<int>piece] -= 1
            self.zHash ^= zobristHash[<int>color,<int>piece,cord]
        self.pieceBoard[cord] = <int>PIECE.EMPTY

    #retrieves mover pieces
    cdef ULL getUs(self):
        cdef int i = 0
        cdef ULL result = 0
        for i from 0 <= i < len(self.board[<int>self.color]):
            result |= self.board[<int>self.color,i]
        return result

    #retrieves opposite color mover pieces
    cdef ULL getThem(self):
        cdef int i = 0
        cdef ULL result = 0
        for i from 0 <= i < len(self.board[<int>self.opColor]):
            result |= self.board[<int>self.opColor,i]
        return result

    #returns True if mover king is in check
    cdef bint isInCheck(self):
        return 1 if self.checkers else 0

    #applies a given move to the position and updates all boards, states, and adds states to history dict
    cdef void applyMove(self,USI move):
        cdef USI orig, des, flag, rookInitial
        cdef PIECE mPiece, tPiece, rookPiece
        cdef DIRECTION direction

        self.history["moves"].append(move)
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)

        mPiece = <PIECE>self.pieceBoard[orig]
        tPiece = <PIECE>self.pieceBoard[des]

        direction = DIRECTION.N if self.color == COLOR.WHITE else DIRECTION.S

        self.history["color"].append(self.color)
        self.history["captured"].append(tPiece)
        self.history["castles"].append(self.castles)
        self.history["enpassant"].append(self.enpassant)
        self.history["checkers"].append(self.checkers)
        self.history["pinned"].append(self.pinned)

        if flag == MOVE_FLAG.ENPASSANT:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(PIECE.PAWN,self.opColor,des - <int>direction)
            self.setPiece(mPiece,self.color,des)
            self.enpassant = -1
        elif flag == MOVE_FLAG.KING_CASTLE:
            rookInitial = 7 if self.color == COLOR.WHITE else 63
            rookPiece = <PIECE>self.pieceBoard[<int>rookInitial]
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(rookPiece,self.color,rookInitial)
            self.setPiece(mPiece,self.color,des)
            self.setPiece(rookPiece,self.color,des-1)
            if self.color == COLOR.WHITE:
                self.castles = self.castles & ~CASTLE.W_OO & ~CASTLE.W_OOO
            else:
                self.castles = self.castles & ~CASTLE.B_OO & ~CASTLE.B_OOO
            self.enpassant = -1
        elif flag == MOVE_FLAG.QUEEN_CASTLE:
            rookInitial = 0 if self.color == COLOR.WHITE else 56
            rookPiece = <PIECE>self.pieceBoard[<int>rookInitial]
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(rookPiece,self.color,rookInitial)
            self.setPiece(mPiece,self.color,des)
            self.setPiece(rookPiece,self.color,des+1)
            if self.color == COLOR.WHITE:
                self.castles = self.castles & ~CASTLE.W_OOO & ~CASTLE.W_OO
            else:
                self.castles = self.castles & ~CASTLE.B_OOO & ~CASTLE.B_OO
            self.enpassant = -1
        elif flag == MOVE_FLAG.KNIGHT_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(PIECE.KNIGHT,self.color,des)
            self.enpassant = -1
        elif flag == MOVE_FLAG.BISHOP_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(PIECE.BISHOP,self.color,des)
            self.enpassant = -1
        elif flag == MOVE_FLAG.ROOK_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(PIECE.ROOK,self.color,des)
            self.enpassant = -1
        elif flag == MOVE_FLAG.QUEEN_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(PIECE.QUEEN,self.color,des)
            self.enpassant = -1
        elif mPiece == PIECE.PAWN:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(mPiece,self.color,des)
            if((des - orig) == 16) | ((des - orig) == -16):
                self.enpassant = des - <int>direction
            else:
                self.enpassant = -1
        else:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(mPiece,self.color,des)
            self.enpassant = -1

        if mPiece == PIECE.ROOK:
            if self.color == COLOR.WHITE:
                if orig == 0:
                    self.castles = self.castles & ~CASTLE.W_OOO
                elif orig == 7:
                    self.castles = self.castles & ~CASTLE.W_OO
            else:
                if orig == 56:
                    self.castles = self.castles & ~CASTLE.B_OOO
                elif orig == 63:
                    self.castles = self.castles & ~CASTLE.B_OO

        if mPiece == PIECE.KING:
            if (flag == MOVE_FLAG.NORMAL) | (flag == MOVE_FLAG.CAPTURES):
                if self.color == COLOR.WHITE:
                    self.castles = self.castles & ~CASTLE.W_OOO & ~CASTLE.W_OO
                else:
                    self.castles = self.castles & ~CASTLE.B_OOO & ~CASTLE.B_OO

        if self.color == COLOR.WHITE:
            if (tPiece == PIECE.ROOK) & (des == 56):
                self.castles = self.castles & ~CASTLE.B_OOO
            elif (tPiece == PIECE.ROOK) & (des == 63):
                self.castles = self.castles & ~CASTLE.B_OO
        else:
            if (tPiece == PIECE.ROOK) & (des == 0):
                self.castles = self.castles & ~CASTLE.W_OOO
            elif (tPiece == PIECE.ROOK) & (des == 7):
                self.castles = self.castles & ~CASTLE.W_OO

        self.color = self.opColor
        self.opColor = <COLOR>(~<int>self.color & 1)

        self.us = self.getUs()
        self.them = self.getThem()
        self.blocker = self.us | self.them
        self.king = lsb(self.board[<int>self.color,<int>PIECE.KING])
        self.checkers = attackersTo(self.board,self.blocker,self.king) & self.them
        # if self.isInCheck():
        #     self.notation = self.notation + "+"
        self.pinned = blockers(self.board[<int>self.opColor],self.blocker,self.king)
        self.ply += 1

    #undo the previous move, restores board to previous board, state, and histories
    cdef void undoMove(self):
        cdef USI move, orig, des, flag
        cdef PIECE mPiece, tPiece, rookPiece
        cdef DIRECTION direction

        move = self.history["moves"].pop()

        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)

        mPiece = <PIECE>self.pieceBoard[des]
        tPiece = self.history["captured"].pop()
        self.color = self.history["color"].pop()
        self.opColor = <COLOR>(~<int>self.color & 1)

        direction = DIRECTION.N if self.color == COLOR.WHITE else DIRECTION.S

        if flag == MOVE_FLAG.ENPASSANT:
            self.clearPiece(mPiece,self.color,des)
            self.setPiece(PIECE.PAWN,self.opColor,des - <int>direction)
            self.setPiece(mPiece,self.color,orig)
        elif flag == MOVE_FLAG.KING_CASTLE:
            rookInitial = 7 if self.color == COLOR.WHITE else 63
            self.clearPiece(mPiece,self.color,des)
            self.clearPiece(PIECE.ROOK,self.color,des-1)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(PIECE.ROOK,self.color,rookInitial)
        elif flag == MOVE_FLAG.QUEEN_CASTLE:
            rookInitial = 0 if self.color == COLOR.WHITE else 56
            self.clearPiece(mPiece,self.color,des)
            self.clearPiece(PIECE.ROOK,self.color,des+1)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(PIECE.ROOK,self.color,rookInitial)
        elif flag == MOVE_FLAG.KNIGHT_PROMO:
            self.clearPiece(PIECE.KNIGHT,self.color,des)
            self.setPiece(PIECE.PAWN,self.color,orig)
            self.setPiece(tPiece,self.opColor,des)
        elif flag == MOVE_FLAG.BISHOP_PROMO:
            self.clearPiece(PIECE.BISHOP,self.color,des)
            self.setPiece(PIECE.PAWN,self.color,orig)
            self.setPiece(tPiece,self.opColor,des)
        elif flag == MOVE_FLAG.ROOK_PROMO:
            self.clearPiece(PIECE.ROOK,self.color,des)
            self.setPiece(PIECE.PAWN,self.color,orig)
            self.setPiece(tPiece,self.opColor,des)
        elif flag == MOVE_FLAG.QUEEN_PROMO:
            self.clearPiece(PIECE.QUEEN,self.color,des)
            self.setPiece(PIECE.PAWN,self.color,orig)
            self.setPiece(tPiece,self.opColor,des)
        else:
            self.clearPiece(mPiece,self.color,des)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(tPiece,self.opColor,des)

        self.enpassant = self.history["enpassant"].pop()
        self.checkers = self.history["checkers"].pop()
        self.pinned = self.history["pinned"].pop()
        self.castles = self.history["castles"].pop()

        self.us = self.getUs()
        self.them = self.getThem()
        self.blocker = self.us | self.them
        self.king = lsb(self.board[<int>self.color,<int>PIECE.KING])
        self.ply -= 1

    #prints the SAN given a move (cannot calculate "+" and "#" until move is applied)
    cpdef moveToSAN(self,move):
        cdef USI orig, des, flag
        cdef int mPiece, tPiece, sameFile, sameRank
        cdef ULL sameSquare
        cdef str notation = ""
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)
        mPiece = self.pieceBoard[orig]
        tPiece = self.pieceBoard[des]
        if mPiece != 0:
            notation = notation + ALGPIECE[mPiece-1]

        sameSquare = attackersTo(self.board,self.blocker,orig) & self.board[<int>self.color,mPiece]

        sameFile = 0
        sameRank = 0

        while sameSquare:
            sq = lsb(sameSquare)
            file = getFile(sq)
            rank = getRank(sq)
            if file == getFile(orig):
                sameFile = 1
            if rank == getRank(orig):
                sameRank = 1
            sameSquare = pop_lsb(sameSquare)

        if sameFile & sameRank:
            notation = notation + ALGEBRAIC[orig]
        elif sameFile:
            notation = notation + ALGEBRAIC[orig][1]
        elif sameRank:
            notation = notation + ALGEBRAIC[orig][0]

        if tPiece != <int>PIECE.EMPTY:
            if mPiece == <int>PIECE.PAWN:
                notation = notation + ALGEBRAIC[orig][0]
            notation = notation + "x"

        notation = notation + ALGEBRAIC[des]

        if flag == MOVE_FLAG.KING_CASTLE:
            notation = notation = "O-O"
        elif flag == MOVE_FLAG.QUEEN_CASTLE:
            notation = notation = "O-O-O"
        elif flag == MOVE_FLAG.KNIGHT_PROMO:
            notation = notation + "=" + ALGPIECE[PIECE.KNIGHT]
        elif flag == MOVE_FLAG.BISHOP_PROMO:
            notation = notation + "=" + ALGPIECE[PIECE.BISHOP]
        elif flag == MOVE_FLAG.ROOK_PROMO:
            notation = notation + "=" + ALGPIECE[PIECE.ROOK]
        elif flag == MOVE_FLAG.QUEEN_PROMO:
            notation = notation + "=" + ALGPIECE[PIECE.QUEEN]

        return notation

    #evaluate the position using an evaluation function
    cdef int evaluate(self):
        cdef int mover, pawnEval, knightEval, bishopEval, rookEval, queenEval
        mover = 1 if self.color == COLOR.WHITE else -1

        pawnEval = PIECE_EVAL[<int>PIECE.PAWN] * (self.pieceCount[<int>COLOR.WHITE][<int>PIECE.PAWN] - self.pieceCount[<int>COLOR.BLACK][<int>PIECE.PAWN])
        knightEval = PIECE_EVAL[<int>PIECE.KNIGHT] * (self.pieceCount[<int>COLOR.WHITE][<int>PIECE.KNIGHT] - self.pieceCount[<int>COLOR.BLACK][<int>PIECE.KNIGHT])
        bishopEval = PIECE_EVAL[<int>PIECE.BISHOP] * (self.pieceCount[<int>COLOR.WHITE][<int>PIECE.BISHOP] - self.pieceCount[<int>COLOR.BLACK][<int>PIECE.BISHOP])
        rookEval = PIECE_EVAL[<int>PIECE.ROOK] * (self.pieceCount[<int>COLOR.WHITE][<int>PIECE.ROOK] - self.pieceCount[<int>COLOR.BLACK][<int>PIECE.ROOK])
        queenEval = PIECE_EVAL[<int>PIECE.QUEEN] * (self.pieceCount[<int>COLOR.WHITE][<int>PIECE.QUEEN] - self.pieceCount[<int>COLOR.BLACK][<int>PIECE.QUEEN])

        return ((pawnEval + knightEval + bishopEval + rookEval + queenEval) * mover)

    #Static exchange evaluation algorithm for a move
    cdef int see(self,move):
        cdef USI orig, des, flag
        cdef ULL attackers, stmAttackers, pin, occ, bb
        cdef int see_value, trophy_value, swap, sq, isPromo
        cdef COLOR stm = self.color
        cdef ULL stmPieces = self.us
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)

        swap = 1
        see_value = PIECE_EVAL[self.pieceBoard[des]]
        if flag == MOVE_FLAG.KNIGHT_PROMO:
            trophy_value = PIECE_EVAL[<int>PIECE.KNIGHT]
        elif flag == MOVE_FLAG.BISHOP_PROMO:
            trophy_value = PIECE_EVAL[<int>PIECE.BISHOP]
        elif flag == MOVE_FLAG.ROOK_PROMO:
            trophy_value = PIECE_EVAL[<int>PIECE.ROOK]
        elif flag == MOVE_FLAG.QUEEN_PROMO:
            trophy_value = PIECE_EVAL[<int>PIECE.QUEEN]
        else:
            trophy_value = PIECE_EVAL[self.pieceBoard[orig]]

        occ = clearBits(self.blocker, orig) & ~BB_SQUARES[des]
        stmPieces = stmPieces & occ
        attackers = attackersTo(self.board,occ,des) & ~BB_SQUARES[orig]

        while True:
            stm = <COLOR>(~<int>stm & 1)
            stmPieces = (self.them & occ) if swap == 1 else (self.us & occ)
            stmAttackers = attackers & stmPieces
            swap = -1*swap
            
            if stmAttackers == 0:
                break

            pin = blockers(self.board[~<int>stm & 1],occ,lsb(self.board[<int>stm][<int>PIECE.KING]))

            stmAttackers &= ~pin

            if stmAttackers == 0:
                break

            bb = stmAttackers & self.board[<int>stm][<int>PIECE.PAWN]
            if bb:
                see_value = see_value + swap*trophy_value
                sq = lsb(bb)
                isPromo = (BB_SQUARES[des] & BB_RANK_8) if stm == COLOR.WHITE else (BB_SQUARES[des] & BB_RANK_1)
                if isPromo:
                    trophy_value = PIECE_EVAL[<int>PIECE.QUEEN]
                else: 
                    trophy_value = PIECE_EVAL[<int>PIECE.PAWN]
                    
                occ = clearBits(occ,sq)
                
                attackers = clearBits(attackers,sq)
                attackers |= attacksFrom(PIECE.BISHOP, des, COLOR.WHITE, occ) & (self.board[<int>stm][<int>PIECE.BISHOP] | self.board[<int>stm][<int>PIECE.QUEEN])

                continue

            bb = stmAttackers & self.board[<int>stm][<int>PIECE.KNIGHT]
            if bb:
                see_value = see_value + swap*trophy_value
                trophy_value = PIECE_EVAL[<int>PIECE.KNIGHT]
                sq = lsb(bb)
                
                occ = clearBits(occ,sq)
                
                attackers = clearBits(attackers,sq)
                continue

            bb = stmAttackers & self.board[<int>stm][<int>PIECE.BISHOP]
            if bb:
                see_value = see_value + swap*trophy_value
                trophy_value = PIECE_EVAL[<int>PIECE.BISHOP]
                sq = lsb(bb)
                
                occ = clearBits(occ,sq)
                
                attackers = clearBits(attackers,sq)
                attackers |= attacksFrom(PIECE.BISHOP, des, COLOR.WHITE, occ) & (self.board[<int>stm][<int>PIECE.BISHOP] | self.board[<int>stm][<int>PIECE.QUEEN])

                continue

            bb = stmAttackers & self.board[<int>stm][<int>PIECE.ROOK]
            if bb:
                see_value = see_value + swap*trophy_value
                trophy_value = PIECE_EVAL[<int>PIECE.ROOK]
                sq = lsb(bb)
                
                occ = clearBits(occ,sq)
                
                attackers = clearBits(attackers,sq)
                attackers |= (attacksFrom(PIECE.ROOK, des, COLOR.WHITE, occ) & (self.board[<int>stm][<int>PIECE.ROOK] | self.board[<int>stm][<int>PIECE.QUEEN])) | \
                              (attacksFrom(PIECE.BISHOP, des, COLOR.WHITE, occ) & (self.board[<int>stm][<int>PIECE.BISHOP] | self.board[<int>stm][<int>PIECE.QUEEN]))

                continue

            bb = stmAttackers & self.board[<int>stm][<int>PIECE.QUEEN]
            if bb:
                see_value = see_value + swap*trophy_value
                trophy_value = PIECE_EVAL[<int>PIECE.QUEEN]
                sq = lsb(bb)
                
                occ = clearBits(occ,sq)
                
                attackers = clearBits(attackers,sq)
                attackers |= attacksFrom(PIECE.QUEEN, des, COLOR.WHITE, occ) & (self.board[<int>stm][<int>PIECE.ROOK] | self.board[<int>stm][<int>PIECE.QUEEN])

                continue
            
            bb = stmAttackers & self.board[<int>stm][<int>PIECE.KING]
            if bb:
                stmPieces = (self.them & occ) if swap == 1 else (self.us & occ)
                if (attackers & stmPieces):
                    break
                
                see_value = see_value + swap*trophy_value
                sq = lsb(bb)
                
                occ = clearBits(occ,sq)
                
                attackers = clearBits(attackers,sq)

                break
            
        return see_value
