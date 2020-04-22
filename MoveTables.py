# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:49:59 2020

@author: lblas
"""

from Bitboard import BB_SQUARES

# Using LERF Board notation for bitboards

#   a  b  c  d  e  f  g  h    
#   -----------------------
# 8|56 57 58 59 60 61 62 63
# 7|48 49 50 51 52 53 54 55
# 6|40 41 42 43 44 45 46 47
# 5|32 33 34 35 36 37 38 39
# 4|24 25 26 27 28 29 30 31
# 3|16 17 18 19 20 21 22 23
# 2|8  9  10 11 12 13 14 15
# 1|0  1  2  3  4  5  6  7

map = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
		-1,  0,  1,  2,  3,  4,  5,  6,  7, -1, 
		-1,  8,  9, 10, 11, 12, 13, 14, 15, -1,
		-1, 16, 17, 18, 19, 20, 21, 22, 23, -1, 
		-1, 24, 25, 26, 27, 28, 29, 30, 31, -1, 
		-1, 32, 33, 34, 35, 36, 37, 38, 39, -1, 
		-1, 40, 41, 42, 43, 44, 45, 46, 47, -1, 
		-1, 48, 49, 50, 51, 52, 53, 54, 55, -1, 
		-1, 56, 57, 58, 59, 60, 61, 62, 63, -1, 
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

moveArray = [[0]*64 for i in range(4)]

nonSlideAttacks = [
    [9,11], #white pawn attacks
    [-9,-11], #black pawn atatcks
    [-21,-19,-12,-8,8,12,19,21], #knight moves
    [-11,-10,-9,-1,1,9,10,11] #king moves
    ]

for piece in range(len(nonSlideAttacks)):
    print(piece)
    for index in range(120):
        mcord = map[index]
        if(mcord == -1):
            continue
        b = 0
        coord = 0
        for dir in nonSlideAttacks[piece]:
            coord = map[index + dir]
            if(coord == -1):
                continue
            b |= BB_SQUARES[coord]
        moveArray[piece][mcord] = b

