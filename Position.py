# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:26:34 2020

@author: Sid
"""

from Bitboard import setBits, clearBits

from Utils import PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, WHITE, BLACK, pieceStr, colorStr, W_OO, W_OOO, \
    B_OO, B_OOO, algebraic, moveFlag, NORMAL, ENPASSANT, KING_CASTLE, QUEEN_CASTLE, KNIGHT_PROMO, BISHOP_PROMO, \
    ROOK_PROMO,QUEEN_PROMO, N, S

from MoveTables import attackersTo, blockers

from Movegen import getOrig, getDes, getFlag

class Position:
    def __init__(self):
        self.board = [[0]*6,[0]*6] #bitboard of each color for each piece
        self.pieceBoard = [6]*64 #board of pieceType for each cord
        self.enpassant = -1 #en passant target square cord
        self.king = 0 #king square cord
        self.castles = 0 #castle indicator W_OO | W_OOO | B_OO | B_OOO
        #TODO: self.repetition = 0
        self.color = 0 #color of mover
        self.opColor = 0 #color of Op
        self.us = 0 #mover pieces
        self.them = 0 #opponent pieces
        self.blocker = 0 #blockers on the board
        self.pinned = 0 #pieces absolutely pinned
        self.checkers = 0 #bitboard of all pieces attacking the mover king
        self.ply = 0

        self.history = {
            "enpassant" : [],
            "castles" : [],
            "moves" : [],
            "captured" : [],
            "color" : [],
            "checkers" : [],
            "us" : [],
            "them" : [],
            "blocker" : [],
            "pinned" : []
            }

    def posFromFEN(self,fen):
        state = fen.split()

        pieces = state[0]
        mover = state[1]
        castles = state[2]
        ep = state[3]
        half_move = state[5]

        self.color = colorStr[mover]
        self.opColor = ~self.color & 1

        for r,rank in enumerate(pieces.split("/")):
            cord = (7-r)*8
            for char in rank:
                if char.isdigit():
                    cord+=int(char)
                else:
                    piece = pieceStr[char]
                    color = WHITE if char.isupper() else BLACK
                    self.setPiece(piece,color,cord)
                    cord+=1

        self.blocker = self.us | self.them
        
        for char in castles:
            if char == "K":
                self.castles = self.castles | W_OO
            elif char == "Q":
                self.castles = self.castles | W_OOO
            elif char == "k":
                self.castles = self.castles | B_OO
            elif char == "q":
                self.castles = self.castles | B_OOO

        if ep != "-":
            self.enpassant = algebraic.index(ep)
        else:
            self.enpassant = -1
            
        self.checkers = attackersTo(self.board[self.opColor],self.blocker,self.king,self.opColor)
        self.pinned = blockers(self.board[self.opColor],self.blocker,self.king)
        
        self.history["blocker"].append(self.blocker)
        self.history["castles"].append(self.castles)
        self.history["color"].append(self.color)
        self.history["enpassant"].append(self.enpassant)
        self.history["checkers"].append(self.checkers)
        self.history["pinned"].append(self.pinned)
        self.ply = half_move

    def setPiece(self,piece,color,cord):
        self.board[color][piece] = setBits(self.board[color][piece],cord)
        self.pieceBoard[cord] = piece
        if self.color == color:
           self.us = setBits(self.us,cord)
           if(piece == KING):
               self.king = cord
        else:
           self.them = setBits(self.them,cord)

    def clearPiece(self,piece,color,cord):
        self.board[color][piece] = clearBits(self.board[color][piece],cord)
        if self.color == color:
           self.us = clearBits(self.us,cord)
        else:
           self.them = clearBits(self.them,cord)
        self.pieceBoard[cord] = -1

    def isInCheck(self):
        return 1 if self.checkers else 0

    def applyMove(self,move):

        self.history["moves"].append(move)
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)

        mPiece = self.pieceBoard[orig]
        tPiece = self.pieceBoard[des]
        direction = N if self.color == WHITE else S

        #enpassant
        if flag == ENPASSANT:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des - direction)
            self.setPiece(mPiece,self.color,des)
            self.history["captured"].append(tPiece)
        elif flag == KING_CASTLE:
            rookInitial = 7 if self.color == WHITE else 63
            rookPiece = self.pieceBoard[rookInitial]
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(rookPiece,self.color,rookInitial)
            self.setPiece(mPiece,self.color,des)
            self.setPiece(rookPiece,self.color,des-1)
            if self.color == WHITE:
                self.castles = self.castles ^ W_OO ^ W_OOO
            else:
                self.castles = self.castles ^ B_OO ^ B_OOO    
        elif flag == QUEEN_CASTLE:
            rookInitial = 0 if self.color == WHITE else 56
            rookPiece = self.pieceBoard[rookInitial]
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(rookPiece,self.color,rookInitial)
            self.setPiece(mPiece,self.color,des)
            self.setPiece(rookPiece,self.color,des+ 1)
            if self.color == WHITE:
                self.castles = self.castles ^ W_OOO ^ W_OO
            else:
                self.castles = self.castles ^ B_OOO ^ B_OO
        elif flag == KNIGHT_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.setPiece(KNIGHT,self.color,des)
        elif flag == BISHOP_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.setPiece(BISHOP,self.color,des)
        elif flag == ROOK_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.setPiece(ROOK,self.color,des)
        elif flag == QUEEN_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.setPiece(QUEEN,self.color,des)
        elif mPiece == PAWN:
            self.clearPiece(mPiece,self.color,orig)
            self.setPiece(mPiece,self.color,des)
            if(des - orig == 16):
                self.enpassant = des - direction
        else:
            self.clearPiece(mPiece,self.color,orig)
            self.setPiece(mPiece,self.color,des)
            if (mPiece == KING) | (mPiece == ROOK):
                if self.color == WHITE:
                    self.castles = self.castles ^ W_OOO ^ W_OO
                else:
                    self.castles = self.castles ^ B_OOO ^ B_OO 
                    
        self.history["color"].append(self.color)
        self.color = self.opColor
        self.opColor = ~self.color & 1
        
        self.enpassant = -1
        self.blocker = self.us | self.them
        self.us = self.them
        self.them = self.blocker ^ self.us
        self.checkers = attackersTo(self.board[self.opColor],self.blocker,self.king,self.opColor)
        self.pinned = blockers(self.board[self.opColor],self.blocker,self.king)
        
        self.history["captured"].append(tPiece)
        self.history["blocker"].append(self.blocker)
        self.history["castles"].append(self.castles)
        self.history["enpassant"].append(self.enpassant)
        self.history["checkers"].append(self.checkers)
        self.history["pinned"].append(self.pinned)
        
        self.ply += 1