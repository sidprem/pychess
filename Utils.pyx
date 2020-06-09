# -*- coding: utf-8 -*-
"""
Created on Sat May 16 11:14:03 2020

@author: Sid
"""
import array

PIECE_STR = "PNKBRQ"

COLOR_STR = 'wb'

ALGEBRAIC = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
             "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
             "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
             "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
             "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
             "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",    
             "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
             "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]

ALGPIECE = 'NKBRQ'

MAX_MOVES = 256

MIN_VALUE = -32767

MAX_VALUE = 32767

PIECE_EVAL = array.array('i',[100,300,2000,330,500,900,0])
