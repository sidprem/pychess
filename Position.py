# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:26:34 2020

@author: Sid
"""

from Bitboard import setBits, clearBits, iterBits, prettyPrintBitBoard, pop_lsb

from Utils import EMPTY, PAWN, KNIGHT, KING, BISHOP, ROOK, QUEEN, WHITE, BLACK, pieceStr, colorStr, W_OO, W_OOO, \
    B_OO, B_OOO, algebraic, moveFlag, NORMAL, ENPASSANT, KING_CASTLE, QUEEN_CASTLE, KNIGHT_PROMO, BISHOP_PROMO, \
    ROOK_PROMO,QUEEN_PROMO, N, S, PRINT_PIECES

from MoveTables import attackersTo, blockers

from Movegen import getOrig, getDes, getFlag

class Position:
    def __init__(self):
        self.board = [[0]*6,[0]*6] #bitboard of each color for each piece
        self.pieceBoard = [EMPTY]*64 #board of pieceType for each cord
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
                    if (piece == KING) & (self.color == color):
                        self.king = cord
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
        self.ply = int(half_move)

    def setPiece(self,piece,color,cord):
        if piece != EMPTY:
            self.board[color][piece] = setBits(self.board[color][piece],cord)
            if self.color == color:
               self.us = setBits(self.us,cord)
            else:
               self.them = setBits(self.them,cord)     
        self.pieceBoard[cord] = piece
        
    def clearPiece(self,piece,color,cord):
        if piece != EMPTY:
            self.board[color][piece] = clearBits(self.board[color][piece],cord)
            if self.color == color:
               self.us = clearBits(self.us,cord)
            else:
               self.them = clearBits(self.them,cord)
        self.pieceBoard[cord] = EMPTY

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

        self.history["color"].append(self.color)
        self.history["captured"].append(tPiece)
        self.history["blocker"].append(self.blocker)
        self.history["us"].append(self.us)
        self.history["them"].append(self.them)
        self.history["castles"].append(self.castles)
        self.history["enpassant"].append(self.enpassant)
        self.history["checkers"].append(self.checkers)
        self.history["pinned"].append(self.pinned)
        
        if flag == ENPASSANT:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des - direction)
            self.setPiece(mPiece,self.color,des)
            self.enpassant = -1
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
            self.enpassant = -1
        elif flag == QUEEN_CASTLE:
            rookInitial = 0 if self.color == WHITE else 56
            rookPiece = self.pieceBoard[rookInitial]
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(rookPiece,self.color,rookInitial)
            self.setPiece(mPiece,self.color,des)
            self.setPiece(rookPiece,self.color,des+1)
            if self.color == WHITE:
                self.castles = self.castles ^ W_OOO ^ W_OO
            else:
                self.castles = self.castles ^ B_OOO ^ B_OO
            self.enpassant = -1
        elif flag == KNIGHT_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(KNIGHT,self.color,des)
            self.enpassant = -1
        elif flag == BISHOP_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(BISHOP,self.color,des)
            self.enpassant = -1
        elif flag == ROOK_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(ROOK,self.color,des)
            self.enpassant = -1
        elif flag == QUEEN_PROMO:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(QUEEN,self.color,des)
            self.enpassant = -1
        elif mPiece == PAWN:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(mPiece,self.color,des)
            if(des - orig == 16):
                self.enpassant = des - direction
            else:
                self.enpassant = -1
        else:
            self.clearPiece(mPiece,self.color,orig)
            self.clearPiece(tPiece,self.opColor,des)
            self.setPiece(mPiece,self.color,des)
            if (mPiece == KING) | (mPiece == ROOK):
                if self.color == WHITE:
                    self.castles = self.castles ^ W_OOO ^ W_OO
                else:
                    self.castles = self.castles ^ B_OOO ^ B_OO 
            self.enpassant = -1
        
        self.color = self.opColor
        self.opColor = ~self.color & 1
        
        self.blocker = self.us | self.them
        self.us = self.them
        self.king = pop_lsb(self.board[self.color][KING])
        self.them = self.blocker ^ self.us
        self.checkers = attackersTo(self.board[self.opColor],self.blocker,self.king,self.opColor)
        self.pinned = blockers(self.board[self.opColor],self.blocker,self.king)
                
        self.ply += 1

    def undoMove(self):
        
        move = self.history["moves"].pop()
        if(move == 0):
            return
        orig = getOrig(move)
        des = getDes(move)
        flag = getFlag(move)

        mPiece = self.pieceBoard[des]
        tPiece = self.history["captured"].pop()
        direction = N if self.color == WHITE else S
        
        self.color = self.history["color"].pop()
        self.opColor = ~self.color & 1
        
        self.enpassant = self.history["enpassant"].pop()
        self.blocker =  self.history["blocker"].pop()
        self.us = self.history["us"].pop()
        self.them = self.history["them"].pop()
        self.checkers = self.history["checkers"].pop()
        self.pinned = self.history["pinned"].pop()
        self.castles = self.history["castles"].pop()
        
        if flag == ENPASSANT:
            self.clearPiece(mPiece,self.color,des)
            self.setPiece(tPiece,self.opColor,des + direction)
            self.setPiece(mPiece,self.color,orig)
        elif flag == KING_CASTLE:
            rookInitial = 7 if self.color == WHITE else 63
            self.clearPiece(mPiece,self.color,des)
            self.clearPiece(ROOK,self.color,des-1)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(ROOK,self.color,rookInitial)
        elif flag == QUEEN_CASTLE:
            rookInitial = 0 if self.color == WHITE else 56
            self.clearPiece(mPiece,self.color,des)
            self.clearPiece(ROOK,self.color,des+1)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(ROOK,self.color,rookInitial)
        elif flag == KNIGHT_PROMO:
            self.clearPiece(KNIGHT,self.color,des)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(tPiece,self.color,des)
        elif flag == BISHOP_PROMO:
            self.clearPiece(BISHOP,self.color,des)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(tPiece,self.color,des)
        elif flag == ROOK_PROMO:
            self.clearPiece(ROOK,self.color,des)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(tPiece,self.color,des)
        elif flag == QUEEN_PROMO:
            self.clearPiece(QUEEN,self.color,des)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(tPiece,self.color,des)
        else:
            self.clearPiece(mPiece,self.color,des)
            self.setPiece(mPiece,self.color,orig)
            self.setPiece(tPiece,self.color,des)
            
        self.king = pop_lsb(self.board[self.color][KING])
        self.ply -= 1

    def printPosition(self):
        tempBoard = [6]*64
        print(self.ply)
        for bits in iterBits(self.us):
            tempBoard[bits] = PRINT_PIECES[self.color][self.pieceBoard[bits]]
        
        for bits in iterBits(self.them):
            tempBoard[bits] = PRINT_PIECES[self.opColor][self.pieceBoard[bits]]
        
        tempBoard = [x if x != EMPTY else PRINT_PIECES[self.color][EMPTY] for x in tempBoard]
        
        prettyBoard = []
        prettyBoard.append(tempBoard[56:64])
        prettyBoard.append(tempBoard[48:56])
        prettyBoard.append(tempBoard[40:48])
        prettyBoard.append(tempBoard[32:40])
        prettyBoard.append(tempBoard[24:32])
        prettyBoard.append(tempBoard[16:24])
        prettyBoard.append(tempBoard[8:16])
        prettyBoard.append(tempBoard[0:8])

        
        for row in prettyBoard:
            print(' '.join(row))
        print("\n")