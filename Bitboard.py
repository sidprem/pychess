# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:31:57 2020

@author: Sid
"""

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


#universal bitboards
BB_EMPTY = 0x0
BB_ALL_SQUARES = 0xFFFFFFFFFFFFFFFF

#square bitboards
BB_SQUARES = [
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8
] = [1 << i for i in range(64)]

#File bitboards
BB_A_FILE = 0x0101010101010101
BB_B_FILE = BB_A_FILE << 1
BB_C_FILE = BB_A_FILE << 2
BB_D_FILE = BB_A_FILE << 3
BB_E_FILE = BB_A_FILE << 4
BB_F_FILE = BB_A_FILE << 5
BB_G_FILE = BB_A_FILE << 6
BB_H_FILE = BB_A_FILE << 7

#rank bitboards
BB_RANK_1 = 0xFF
BB_RANK_2 = BB_RANK_1 << (8*1)
BB_RANK_3 = BB_RANK_1 << (8*2)
BB_RANK_4 = BB_RANK_1 << (8*3)
BB_RANK_5 = BB_RANK_1 << (8*4)
BB_RANK_6 = BB_RANK_1 << (8*5)
BB_RANK_7 = BB_RANK_1 << (8*6)
BB_RANK_8 = BB_RANK_1 << (8*7)

#File bitboards
BB_NOT_A_FILE = ~BB_A_FILE & BB_ALL_SQUARES
BB_NOT_C_FILE = ~BB_C_FILE & BB_ALL_SQUARES
BB_NOT_D_FILE = ~BB_D_FILE & BB_ALL_SQUARES
BB_NOT_E_FILE = ~BB_E_FILE & BB_ALL_SQUARES
BB_NOT_F_FILE = ~BB_F_FILE & BB_ALL_SQUARES
BB_NOT_G_FILE = ~BB_G_FILE & BB_ALL_SQUARES
BB_NOT_H_FILE = ~BB_H_FILE & BB_ALL_SQUARES

#rank bitboards
BB_NOT_RANK_1 = ~BB_RANK_1 & BB_ALL_SQUARES
BB_NOT_RANK_2 = ~BB_RANK_2 & BB_ALL_SQUARES
BB_NOT_RANK_3 = ~BB_RANK_3 & BB_ALL_SQUARES
BB_NOT_RANK_4 = ~BB_RANK_4 & BB_ALL_SQUARES
BB_NOT_RANK_5 = ~BB_RANK_5 & BB_ALL_SQUARES
BB_NOT_RANK_6 = ~BB_RANK_6 & BB_ALL_SQUARES
BB_NOT_RANK_7 = ~BB_RANK_7 & BB_ALL_SQUARES
BB_NOT_RANK_8 = ~BB_RANK_8 & BB_ALL_SQUARES

BB_BYCOLOR = []
BB_BYPIECE = []

    
def initBitBoard():
    #piece bitboards
    BB_WPAWNS = BB_RANK_2
    BB_BPAWNS = BB_RANK_7
    BB_ROOKS = BB_A1 | BB_H1 | BB_A8 | BB_H8
    BB_KNIGHTS = BB_B1 | BB_G1 | BB_B8 | BB_G8
    BB_BISHOPS = BB_C1 | BB_F1 | BB_C8 | BB_F8
    BB_QUEENS = BB_D1 | BB_D8
    BB_KINGS = BB_E1 | BB_E8

    #color bitboards
    BB_WHITE_PIECES = BB_RANK_1 | BB_RANK_2
    BB_BLACK_PIECES = BB_RANK_7 | BB_RANK_8

    global BB_BYCOLOR
    BB_BYCOLOR = [BB_WHITE_PIECES,BB_BLACK_PIECES]
    
    global BB_BYPIECE
    BB_BYPIECE = [BB_WPAWNS,BB_BPAWNS,BB_KNIGHTS,BB_KINGS,BB_BISHOPS,BB_ROOKS,BB_QUEENS]

def getBitBoardByColor(color):
    return BB_BYCOLOR[color]

def getBitBoardByPiece(pieceType):
    return BB_BYPIECE[pieceType]

def getBitBoardByPieceandColor(color, pieceType):
    return getBitBoardByColor(color) & getBitBoardByPiece(pieceType)

def shiftBitBoard(bb, direction):
    return (bb << direction) if (direction >= 0) else (bb >> abs(direction))

def prettyPrintBitBoard(bb: int) -> str:
    bb_formatted = format(bb,'#066b')
    board = []
    board.append(bb_formatted[2:10][::-1])
    board.append(bb_formatted[10:18][::-1])
    board.append(bb_formatted[18:26][::-1])
    board.append(bb_formatted[26:34][::-1])
    board.append(bb_formatted[34:42][::-1])
    board.append(bb_formatted[42:50][::-1])
    board.append(bb_formatted[50:58][::-1])
    board.append(bb_formatted[58:66][::-1])
    for row in board:
        print(' '.join(row))
    print("\n")

def initRandomBitBoard():
    #piece bitboards
    BB_PAWNS = BB_H8
    BB_ROOKS = BB_EMPTY
    BB_KNIGHTS = BB_EMPTY
    BB_BISHOPS = BB_EMPTY
    BB_QUEENS = BB_EMPTY
    BB_KINGS = BB_EMPTY

    #color bitboards
    BB_WHITE_PIECES = BB_EMPTY
    BB_BLACK_PIECES = BB_H8
    
    #Occupied and not occupied squares
    BB_OCCUPIED = BB_WHITE_PIECES | BB_BLACK_PIECES
    BB_NOT_OCCUPIED = ~BB_OCCUPIED & BB_ALL_SQUARES

    global BB_BYPIECE 
    BB_BYPIECE = [BB_NOT_OCCUPIED, BB_PAWNS, BB_KNIGHTS, BB_BISHOPS, BB_ROOKS, BB_QUEENS, BB_KINGS, BB_OCCUPIED]

    global BB_BYCOLOR
    BB_BYCOLOR = [BB_WHITE_PIECES, BB_BLACK_PIECES]   




