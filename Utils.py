# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:23:00 2020

@author: Sid
"""

direction = [N,S,E,W,NW,SW,NE,SE] = [8,-8,1,-1,7,-9,9,-7]

color = [WHITE, BLACK] = range(2)

pieceType = [PAWN,KNIGHT,KING,BISHOP,ROOK,QUEEN,EMPTY] = range(7)    

pieceStr = {"P": PAWN,
            "N": KNIGHT,
            "B": BISHOP,
            "R": ROOK,
            "Q": QUEEN,
            "K": KING,  
            "p": PAWN,
            "n": KNIGHT,
            "b": BISHOP,
            "r": ROOK,
            "q": QUEEN,
            "k": KING}

colorStr = {"w": WHITE,
            "b": BLACK}

algebraic = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
             "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
             "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
             "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
             "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
             "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",    
             "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
             "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]

moveFlag = [NORMAL,ENPASSANT,KING_CASTLE,QUEEN_CASTLE,KNIGHT_PROMO,BISHOP_PROMO,ROOK_PROMO,QUEEN_PROMO] = range(8)

castle = [W_OO,W_OOO,B_OO,B_OOO] = range(1,5)