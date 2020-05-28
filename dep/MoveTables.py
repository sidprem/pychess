6# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 23:49:59 2020

@author: lblas
"""

from Bitboard_old import BB_ALL_SQUARES, BB_SQUARES, pop_count, pop_lsb, iterBits, prettyPrintBitBoard

import numpy as np

from Utils_old import PAWN,KNIGHT,KING,BISHOP,ROOK,QUEEN,WHITE,BLACK

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

RBITS = [
  12, 11, 11, 11, 11, 11, 11, 12,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  11, 10, 10, 10, 10, 10, 10, 11,
  12, 11, 11, 11, 11, 11, 11, 12
]

BBITS = [
  6, 5, 5, 5, 5, 5, 5, 6,
  5, 5, 5, 5, 5, 5, 5, 5,
  5, 5, 7, 7, 7, 7, 5, 5,
  5, 5, 7, 9, 9, 7, 5, 5,
  5, 5, 7, 9, 9, 7, 5, 5,
  5, 5, 7, 7, 7, 7, 5, 5,
  5, 5, 5, 5, 5, 5, 5, 5,
  6, 5, 5, 5, 5, 5, 5, 6
]

BISHOP_MAGICS = [
 	0x0002020202020200, 0x0002020202020000, 0x0004010202000000, 0x0004040080000000,
 	0x0001104000000000, 0x0000821040000000, 0x0000410410400000, 0x0000104104104000,
 	0x0000040404040400, 0x0000020202020200, 0x0000040102020000, 0x0000040400800000,
 	0x0000011040000000, 0x0000008210400000, 0x0000004104104000, 0x0000002082082000,
 	0x0004000808080800, 0x0002000404040400, 0x0001000202020200, 0x0000800802004000,
 	0x0000800400A00000, 0x0000200100884000, 0x0000400082082000, 0x0000200041041000,
 	0x0002080010101000, 0x0001040008080800, 0x0000208004010400, 0x0000404004010200,
 	0x0000840000802000, 0x0000404002011000, 0x0000808001041000, 0x0000404000820800,
 	0x0001041000202000, 0x0000820800101000, 0x0000104400080800, 0x0000020080080080,
 	0x0000404040040100, 0x0000808100020100, 0x0001010100020800, 0x0000808080010400,
 	0x0000820820004000, 0x0000410410002000, 0x0000082088001000, 0x0000002011000800,
 	0x0000080100400400, 0x0001010101000200, 0x0002020202000400, 0x0001010101000200,
 	0x0000410410400000, 0x0000208208200000, 0x0000002084100000, 0x0000000020880000,
 	0x0000001002020000, 0x0000040408020000, 0x0004040404040000, 0x0002020202020000,
 	0x0000104104104000, 0x0000002082082000, 0x0000000020841000, 0x0000000000208800,
 	0x0000000010020200, 0x0000000404080200, 0x0000040404040400, 0x0002020202020200
]

ROOK_MAGICS = [
 	0x0080001020400080, 0x0040001000200040, 0x0080081000200080, 0x0080040800100080,
 	0x0080020400080080, 0x0080010200040080, 0x0080008001000200, 0x0080002040800100,
 	0x0000800020400080, 0x0000400020005000, 0x0000801000200080, 0x0000800800100080,
 	0x0000800400080080, 0x0000800200040080, 0x0000800100020080, 0x0000800040800100,
 	0x0000208000400080, 0x0000404000201000, 0x0000808010002000, 0x0000808008001000,
 	0x0000808004000800, 0x0000808002000400, 0x0000010100020004, 0x0000020000408104,
 	0x0000208080004000, 0x0000200040005000, 0x0000100080200080, 0x0000080080100080,
 	0x0000040080080080, 0x0000020080040080, 0x0000010080800200, 0x0000800080004100,
 	0x0000204000800080, 0x0000200040401000, 0x0000100080802000, 0x0000080080801000,
 	0x0000040080800800, 0x0000020080800400, 0x0000020001010004, 0x0000800040800100,
 	0x0000204000808000, 0x0000200040008080, 0x0000100020008080, 0x0000080010008080,
 	0x0000040008008080, 0x0000020004008080, 0x0000010002008080, 0x0000004081020004,
 	0x0000204000800080, 0x0000200040008080, 0x0000100020008080, 0x0000080010008080,
 	0x0000040008008080, 0x0000020004008080, 0x0000800100020080, 0x0000800041000080,
 	0x00FFFCDDFCED714A, 0x007FFCDDFCED714A, 0x003FFFCDFFD88096, 0x0000040810002101,
 	0x0001000204080011, 0x0001000204000801, 0x0001000082000401, 0x0001FFFAABFAD1A2
]

BISHOP_ATTACK_MASK = [0]*64
ROOK_ATTACK_MASK = [0]*64

BISHOP_ATTACKS = np.zeros((512,64),dtype=np.uint64)
ROOK_ATTACKS = np.zeros((4096,64),dtype=np.uint64)

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
    [9,11],
    [-21,-19,-12,-8,8,12,19,21], #knight moves
    [-11,-10,-9,-1,1,9,10,11], #king moves
    [-9,-11]
    ]

lineBB = [[0]*64 for i in range(64)] 

def batt(sq,block):
    result = 0
    rk = int(sq/8)
    f1 = int(sq%8)
    
    r = rk+1
    f = f1+1

    while (r<=7) & (f<=7):
        result |= (1 << (f+r*8))
        if block & (1 << (f+r*8)):
            break            
        r = r + 1
        f = f + 1
    
    r = rk+1
    f = f1-1
    while (r <=7) & (f >= 0):
        result |= (1 << (f+r*8))
        if block & (1 << (f+r*8)):
            break 
        r = r + 1
        f = f - 1  
 
    r = rk-1
    f = f1+1
    while (r >=0) & (f <= 7):
        result |= (1 << (f+r*8))
        if block & (1 << (f+r*8)):
            break 
        r = r - 1
        f = f + 1  

    r = rk-1
    f = f1-1
    
    while (r >=0) & (f >= 0):
        result |= (1 << (f+r*8))
        if block & (1 << (f+r*8)):
            break 
        r = r - 1
        f = f - 1
    
    return result

def ratt(sq,block):
    result = 0
    
    rk = int(sq/8)
    f1 = int(sq%8)
    for r in range(rk+1,8):
        result |= (1 << (f1 + r*8))
        if block & (1 << (f1+r*8)):
            break 
    for r in range(rk-1,-1,-1):
        result |= (1 << (f1 + r*8))
        if block & (1 << (f1+r*8)):
            break 
    for f in range(f1+1,8):
        result |= (1 << (f + rk*8))
        if block & (1 << (f+rk*8)):
            break 
    for f in range(f1-1,-1,-1):
        result |= (1 << (f + rk*8))
        if block & (1 << (f+rk*8)):
            break 
    return result    

def getSlidingAttack(blocker,square,pieceType):
    
    if pieceType == BISHOP:
        mask = BISHOP_ATTACK_MASK[square]
        bits = BBITS[square]
        magic = BISHOP_MAGICS[square]
        
        index =  (((mask & blocker) * magic) & BB_ALL_SQUARES) >> (64 - bits)
        
        return int(BISHOP_ATTACKS[index,square])
    
    elif pieceType == ROOK:
        mask = ROOK_ATTACK_MASK[square]
        bits = RBITS[square]
        magic = ROOK_MAGICS[square]
        
        index =  (((mask & blocker) * magic) & BB_ALL_SQUARES) >> (64 - bits)
        
        return int(ROOK_ATTACKS[index,square])
    
def index_to_uint64(index,bits,mask):
    result = 0
    for i in range(index):
        j = pop_lsb(mask)
        mask &= (mask - 1)
        if index & (1 << i):
            result |= (1 << j)
    return result

def attacksFrom(pieceType,square,color=WHITE,blocker=-1):
    
    if pieceType == PAWN:
       return moveArray[3][square] if color == WHITE else moveArray[0][square]
    elif (pieceType == KNIGHT) | (pieceType == KING):
        return moveArray[pieceType][square]
    
    if blocker != -1:
        if pieceType == QUEEN:
            return getSlidingAttack(blocker,square,ROOK) | getSlidingAttack(blocker,square,BISHOP)
        else:
            return getSlidingAttack(blocker,square,pieceType)
    
    return 0

def attackersTo(pboard,blocker,square,color):
    
    pawnAttacksTo = attacksFrom(PAWN,square,color=color) & pboard[PAWN]
    knightAttacksTo = attacksFrom(KNIGHT,square) & pboard[KNIGHT]
    bishopAttacksTo = attacksFrom(BISHOP,square,blocker=blocker) & (pboard[BISHOP] | pboard[QUEEN])
    rookAttacksTo = attacksFrom(ROOK,square,blocker=blocker) & (pboard[ROOK] | pboard[QUEEN])
    kingAttacksTo = attacksFrom(KING,square) & pboard[KING]

    return  pawnAttacksTo | knightAttacksTo | bishopAttacksTo | rookAttacksTo | kingAttacksTo

def betweenBB(sq1,sq2):
    a = lineBB[sq1][sq2]
    b = (0xFFFFFFFFFFFFFFFF << sq1) & 0xFFFFFFFFFFFFFFFF
    c = (0xFFFFFFFFFFFFFFFF << sq2) & 0xFFFFFFFFFFFFFFFF
    d = a & (b ^ c)
    
    return d & (d-1)

def blockers(pboard,pieces,square):
    
    bishopAttacksTo = attacksFrom(BISHOP,square,blocker=0) & (pboard[BISHOP] | pboard[QUEEN])
    rookAttacksTo = attacksFrom(ROOK,square,blocker=0) & (pboard[ROOK] | pboard[QUEEN])
    attackers = (bishopAttacksTo | rookAttacksTo)
    
    occ = pieces ^ attackers
    blocker = 0
    for bits in iterBits(attackers):
        b = betweenBB(bits,square)
        inAttack = b & occ
        if pop_count(inAttack) == 1:
            blocker |= inAttack
    
    return blocker

def inRay(sq1,sq2,sq3):
    return lineBB[sq1][sq2] & BB_SQUARES[sq3]
            
#BISHOP ATTACK MASKS
for sq in range(64):
    result = 0
    rk = int(sq/8)
    f1 = int(sq%8)
    
    r = rk+1
    f = f1+1

    while (r<=6) & (f<=6):
        result |= (1 << (f+r*8))
        r = r + 1
        f = f + 1
    
    r = rk+1
    f = f1-1
    while (r <=6) & (f >= 1):
        result |= (1 << (f+r*8))
        r = r + 1
        f = f - 1  
 
    r = rk-1
    f = f1+1
    while (r >=1) & (f <= 6):
        result |= (1 << (f+r*8))
        r = r - 1
        f = f + 1  

    r = rk-1
    f = f1-1
    
    while (r >=1) & (f >= 1):
        result |= (1 << (f+r*8))
        r = r - 1
        f = f - 1       
        
    BISHOP_ATTACK_MASK[sq] = result 
        
    b = [0]*512
    a = [0]*512
    
    n = pop_count(result)
    
    for i in range(1<<n):
          b[i] = index_to_uint64(i,n,result)
          a[i] = batt(sq,b[i])
          
          j = ((b[i]*BISHOP_MAGICS[sq]) & 0xFFFFFFFFFFFFFFFF) >> (64 - BBITS[sq])
          
          BISHOP_ATTACKS[j,sq] = a[i]

#ROOK ATTACK MASKS
for sq in range(64):
    result = 0
    
    rk = int(sq/8)
    f1 = int(sq%8)
    for r in range(rk+1,7):
        result |= (1 << (f1 + r*8))
        
    for r in range(rk-1,0,-1):
        result |= (1 << (f1 + r*8))
        
    for f in range(f1+1,7):
        result |= (1 << (f + rk*8))
        
    for f in range(f1-1,0,-1):
        result |= (1 << (f + rk*8))
        
    ROOK_ATTACK_MASK[sq] = result 
    
    b = [0]*4096
    a = [0]*4096
    
    n = pop_count(result)
    
    for i in range(1<<n):
          b[i] = index_to_uint64(i,n,result)
          a[i] = ratt(sq,b[i])
          
          j = ((b[i]*ROOK_MAGICS[sq]) & 0xFFFFFFFFFFFFFFFF) >> (64 - RBITS[sq])
          
          ROOK_ATTACKS[j,sq] = a[i]
    
   
for piece in range(0,len(nonSlideAttacks)):
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
        
#line BB 
for s1 in range(64):
    for pieces in [BISHOP,ROOK]:
        for s2 in range(64):
            if attacksFrom(pieces,s1,blocker=0) & BB_SQUARES[s2]:
                lineBB[s1][s2] = (attacksFrom(pieces,s1,blocker=0) & attacksFrom(pieces,s2,blocker=0)) | BB_SQUARES[s1] | BB_SQUARES[s2]

    
        