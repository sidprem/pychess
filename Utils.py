# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:23:00 2020

@author: Sid
"""

import enum 

class Direction(enum.Enum):
    N = 8
    S = -8
    E = 1
    W = -1
    NW = 7
    SW = -9
    NE = 9
    SE = -7
    

class Color(enum.Enum):
    WHITE = 0
    BLACK = 1
    
    
class PieceType(enum.Enum):
    NO_PIECES = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    ALL_PIECES = 7
    
