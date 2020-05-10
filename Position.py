# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:26:34 2020

@author: Sid
"""

from Bitboard import setBits, clearBits

from Utils import PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, WHITE, BLACK, pieceStr, colorStr, W_OO, W_OOO, \
    B_OO, B_OOO, algebraic

from MoveTables import attackersTo, blockers

class Position:
    def __init__(self):
        self.board = ([0]*6,[0]*6) #bitboard of each color for each piece
        self.pieceBoard = [6]*64 #board of pieceType for each cord
        self.enpassant = -1 #en passant target square cord
        self.king = 0 #king square cord
        self.castles = 0 #castle indicator W_OO | W_OOO | B_OO | B_OOO
        #TODO: self.movehistory = []
        #TODO: self.repetition = 0
        self.color = 0 #color of mover
        self.opColor = 0 #color of Op
        self.us = 0 #mover pieces
        self.them = 0 #opponent pieces
        self.blocker = 0 #blockers on the board
        self.pinned = 0 #pieces absolutely pinned
        self.checkers = 0 #bitboard of all pieces attacking the mover king
        
    def posFromFEN(self,fen):
        state = fen.split()
        
        pieces = state[0]
        mover = state[1]
        castles = state[2]
        ep = state[3]
        #TODO: full_move = state[4]
        #TODO: half_move = state[5]
        
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
        
        #TODO: Half Move & Full Move counter
    
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
        self.pieceBoard[cord] = -1
        
    def isInCheck(self):
        return 1 if self.checkers else 0 