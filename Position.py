# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:26:34 2020

@author: Sid
"""

from Bitboard import BB_RANK_1, BB_RANK_2, BB_RANK_7, BB_RANK_8, BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, \
    BB_G1, BB_H1, BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8, setBits, clearBits

from Utils import PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, WHITE, BLACK, pieceStr, colorStr, W_OO, W_OOO, \
    B_OO, B_OOO, algebraic

class Position:
    def __init__(self):
        self.board = ([0]*6,[0]*6)
        self.pieceBoard = [6]*64
        self.enpassant = -1
        self.castles = 0
     #TODO:   self.movehistory = []
     #TODO:   self.repetition = 0
        self.color = 0
        self.us = 0
        self.them = 0
        
    def posFromFEN(self,fen):
        state = fen.split()
        
        pieces = state[0]
        mover = state[1]
        castles = state[2]
        ep = state[3]
        full_move = state[4]
        half_move = state[5]
        
        self.color = colorStr[mover]
        
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
        
        #TODO: Half Move & Full Move counter
    
    def setPiece(self,piece,color,cord):
        self.board[color][piece] = setBits(self.board[color][piece],cord)
        self.pieceBoard[cord] = piece
        if self.color == color:
           self.us = setBits(self.us,cord)
        else:
           self.them = setBits(self.them,cord) 
           
    def clearPiece(self,piece,color,cord):
        self.board[color][piece] = clearBits(self.board[color][piece],cord)
        self.pieceBoard[cord] = -1