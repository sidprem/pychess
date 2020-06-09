# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:21:58 2020

@author: Sid
"""

from __future__ import print_function

from cpython cimport array
import array
import numpy as np
from Utils cimport PIECE, COLOR, ULL

from Position cimport Position

#Universal bitboard
BB_EMPTY = 0x0
BB_ALL_SQUARES = 0xFFFFFFFFFFFFFFFF

#Square bitboards
cdef array.array a = array.array('Q', [1 << i for i in range(64)])
BB_SQUARES = a

#File bitboards
BB_A_FILE = 0x0101010101010101
BB_B_FILE = BB_A_FILE << 1
BB_C_FILE = BB_A_FILE << 2
BB_D_FILE = BB_A_FILE << 3
BB_E_FILE = BB_A_FILE << 4
BB_F_FILE = BB_A_FILE << 5
BB_G_FILE = BB_A_FILE << 6
BB_H_FILE = BB_A_FILE << 7

#Rank bitboards
BB_RANK_1 = 0xFF
BB_RANK_2 = BB_RANK_1 << (8*1)
BB_RANK_3 = BB_RANK_1 << (8*2)
BB_RANK_4 = BB_RANK_1 << (8*3)
BB_RANK_5 = BB_RANK_1 << (8*4)
BB_RANK_6 = BB_RANK_1 << (8*5)
BB_RANK_7 = BB_RANK_1 << (8*6)
BB_RANK_8 = BB_RANK_1 << (8*7)

#Not rank and file bitboards
BB_NOT_A_FILE = ~BB_A_FILE & BB_ALL_SQUARES
BB_NOT_B_FILE = ~BB_B_FILE & BB_ALL_SQUARES
BB_NOT_C_FILE = ~BB_C_FILE & BB_ALL_SQUARES
BB_NOT_D_FILE = ~BB_D_FILE & BB_ALL_SQUARES
BB_NOT_E_FILE = ~BB_E_FILE & BB_ALL_SQUARES
BB_NOT_F_FILE = ~BB_F_FILE & BB_ALL_SQUARES
BB_NOT_G_FILE = ~BB_G_FILE & BB_ALL_SQUARES
BB_NOT_H_FILE = ~BB_H_FILE & BB_ALL_SQUARES

BB_NOT_RANK_1 = ~BB_RANK_1 & BB_ALL_SQUARES
BB_NOT_RANK_2 = ~BB_RANK_2 & BB_ALL_SQUARES
BB_NOT_RANK_3 = ~BB_RANK_3 & BB_ALL_SQUARES
BB_NOT_RANK_4 = ~BB_RANK_4 & BB_ALL_SQUARES
BB_NOT_RANK_5 = ~BB_RANK_5 & BB_ALL_SQUARES
BB_NOT_RANK_6 = ~BB_RANK_6 & BB_ALL_SQUARES
BB_NOT_RANK_7 = ~BB_RANK_7 & BB_ALL_SQUARES
BB_NOT_RANK_8 = ~BB_RANK_8 & BB_ALL_SQUARES

cdef array.array b = array.array('i', [0, 47, 1, 56, 48, 27, 2, 60,
                                       57, 49, 41, 37, 28, 16,  3, 61,
                                       54, 58, 35, 52, 50, 42, 21, 44,
                                       38, 32, 29, 23, 17, 11,  4, 62,
                                       46, 55, 26, 59, 40, 36, 15, 53,
                                       34, 51, 20, 43, 31, 22, 10, 45,
                                       25, 39, 14, 33, 19, 30,  9, 24,
                                       13, 18,  8, 12,  7,  6,  5, 63])

#Look up table for lsb debruijn
index64 = b

cdef array.array c = array.array('i',[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
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
                                      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

#Padded board map to pre-initializes non-sliding attacks
cdef int[:] BOARD_MAP = c

#Non-sliding attack directional arrays
d = np.array([[0,0,0,0,0,0,9,11], [-21,-19,-12,-8,8,12,19,21], [-11,-10,-9,-1,1,9,10,11], [0,0,0,0,0,0,-9,-11]], dtype=int)
cdef int[:,:] NON_SLIDING_ATTACK = d

#Non-sliding piece arrays for attack pre-initialization (Pawn attacks, knight & king moves)
MOVE_ARRAY = np.zeros((4,64),dtype=np.uint64)

cdef array.array e = array.array('i',[6, 5, 5, 5, 5, 5, 5, 6,
                                      5, 5, 5, 5, 5, 5, 5, 5,
                                      5, 5, 7, 7, 7, 7, 5, 5,
                                      5, 5, 7, 9, 9, 7, 5, 5,
                                      5, 5, 7, 9, 9, 7, 5, 5,
                                      5, 5, 7, 7, 7, 7, 5, 5,
                                      5, 5, 5, 5, 5, 5, 5, 5,
                                      6, 5, 5, 5, 5, 5, 5, 6
                                      ])
#Bits to shift by for magic index look-up used in bishop attacks
BBITS = e

cdef array.array f = array.array('i',[12, 11, 11, 11, 11, 11, 11, 12,
                                      11, 10, 10, 10, 10, 10, 10, 11,
                                      11, 10, 10, 10, 10, 10, 10, 11,
                                      11, 10, 10, 10, 10, 10, 10, 11,
                                      11, 10, 10, 10, 10, 10, 10, 11,
                                      11, 10, 10, 10, 10, 10, 10, 11,
                                      11, 10, 10, 10, 10, 10, 10, 11,
                                      12, 11, 11, 11, 11, 11, 11, 12
                                      ])
#Bits to shift by for magic index look-up used in rook attacks
RBITS = f

cdef array.array g = array.array('Q',[0x0002020202020200, 0x0002020202020000, 0x0004010202000000, 0x0004040080000000,
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
                                     ])
#Bishop magic numbers per square (0-63)
BISHOP_MAGICS = g

cdef array.array h = array.array('Q',[0x0080001020400080, 0x0040001000200040, 0x0080081000200080, 0x0080040800100080,
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
                                      ])
#Rook magic numbers per square (0-63)
ROOK_MAGICS = h

#Bishop and rook attack masks
BISHOP_ATTACK_MASK = np.zeros(64,dtype=np.uint64)
ROOK_ATTACK_MASK = np.zeros(64,dtype=np.uint64)

#Rook and bishop magic attacks
BISHOP_ATTACKS = np.zeros((512,64),dtype=np.uint64)
ROOK_ATTACKS = np.zeros((4096,64),dtype=np.uint64)

LINE_BB = np.zeros((64,64),dtype=np.uint64)

#Pretty prints a bitboard. Used for debugging
cpdef str prettyPrintBitBoard(b):
    cdef str s = '+---+---+---+---+---+---+---+---+\n'
    cdef int i, j, sq
    for i in range(7,-1,-1):
        for j in range(8):
            sq = getSquare(j,i)
            if b & BB_SQUARES[sq]:
                s += '| X '
            else:
                s += '|   '
        s += '|\n+---+---+---+---+---+---+---+---+\n';

    return print(s)

#Bishop attack function to be used to pre-initialize bishop attacks
cdef ULL batt(int sq, ULL block):
    cdef ULL result = 0
    cdef int rk = sq/8
    cdef int f1 = sq%8

    cdef r = rk+1
    cdef f = f1+1

    while (r<=7) & (f<=7):
        result |= (<ULL>1 << (f+r*8))
        if block & (<ULL>1 << (f+r*8)):
            break
        r = r + 1
        f = f + 1

    r = rk+1
    f = f1-1
    while (r <=7) & (f >= 0):
        result |= (<ULL>1 << (f+r*8))
        if block & (<ULL>1 << (f+r*8)):
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
        result |= (<ULL>1 << (f+r*8))
        if block & (<ULL>1 << (f+r*8)):
            break
        r = r - 1
        f = f - 1

    return result

#Rook attack function to be used to pre-initialize rook attacks
cdef ULL ratt(int sq, ULL block):
    cdef ULL result = 0
    cdef int rk, f1, r, f
    
    rk = sq/8
    f1 = sq%8

    for r from (rk+1) <= r < 8:
        result |= (<ULL>1 << (f1 + r*8))
        if block & (<ULL>1 << (f1+r*8)):
            break
    for r from (rk-1) >= r > -1:
        result |= (<ULL>1 << (f1 + r*8))
        if block & (<ULL>1 << (f1+r*8)):
            break
    for f from (f1+1) <= f < 8:
        result |= (<ULL>1 << (f + rk*8))
        if block & (<ULL>1 << (f+rk*8)):
            break
    for f from (f1-1) >= f > -1:
        result |= (<ULL>1 << (f + rk*8))
        if block & (<ULL>1 << (f+rk*8)):
            break
    
    return result

#Calculates bishop attack mask given a square
cdef ULL bmask(int sq):
    cdef ULL result = 0
    cdef int rk, f1, r, f

    rk = sq/8
    f1 = sq%8

    r = rk+1
    f = f1+1
    while (r<=6) & (f<=6):
        result = result | (<ULL>1 << (f+r*8))
        r = r + 1
        f = f + 1

    r = rk+1
    f = f1-1
    while (r <=6) & (f >= 1):
        result |= (<ULL>1 << (f+r*8))
        r = r + 1
        f = f - 1

    r = rk-1
    f = f1+1
    while (r >=1) & (f <= 6):
        result |= (<ULL>1 << (f+r*8))
        r = r - 1
        f = f + 1

    r = rk-1
    f = f1-1
    while (r >=1) & (f >= 1):
        result |= (<ULL>1 << (f+r*8))
        r = r - 1
        f = f - 1

    return result

#Calculates rook attack mask given a square
cdef ULL rmask(int sq):
    cdef ULL result = 0
    cdef int rk, f1, r, f

    rk = sq/8
    f1 = sq%8

    for r from (rk+1) <= r < 7:
        result |= (<ULL>1 << (f1 + r*8))

    for r from (rk-1) >= r > 0:
        result |= (<ULL>1 << (f1 + r*8))

    for f from (f1+1) <= f < 7:
        result |= (<ULL>1 << (f + rk*8))

    for f from (f1-1) >= f > 0:
        result |= (<ULL>1 << (f + rk*8))

    return result

#Function to creates blocker for given mask and bits
cdef ULL index_to_uint64(int index,int bits,ULL mask):
    cdef ULL result = 0
    cdef int i, j
    for i from 0 <= i < bits:
        j = lsb(mask)
        mask = pop_lsb(mask)
        if index & (1 << i):
            result |= (<ULL>1 << j)
    return result

#Initialize piece attacks non-sliding
cdef void initNonSlidingAttacks():
    cdef int piece, index, mcord, coord, direction
    cdef ULL b
    for piece from 0 <= piece < len(NON_SLIDING_ATTACK):
        for index from 0 <= index < len(BOARD_MAP):
            mcord = BOARD_MAP[index]
            b = 0
            if mcord == -1:
                continue
            for direction in NON_SLIDING_ATTACK[piece,:]:
                if direction != 0:
                    coord = BOARD_MAP[index + direction]
                    if coord == -1:
                        continue
                    b |= BB_SQUARES[coord]
            MOVE_ARRAY[piece,mcord] = b

#Initialize piece attacks sliding
cdef void initSlidingAttacks():
    cdef ULL result, magic
    cdef int sq, n, i, j
    cdef ULL[:] a = np.zeros(4096,dtype=np.uint64)
    cdef ULL[:] b = np.zeros(4096,dtype=np.uint64)
    cdef PIECE piece
    for piece in [PIECE.BISHOP,PIECE.ROOK]:
        for sq from 0 <= sq < 64:
            result = bmask(sq) if piece == PIECE.BISHOP else rmask(sq)

            if piece == PIECE.BISHOP:
                BISHOP_ATTACK_MASK[sq] = result
            else:
                ROOK_ATTACK_MASK[sq] = result

            n = pop_count(result)
            for i from 0 <= i < (1<<n):
                b[i] = index_to_uint64(i,n,result)
                a[i] = batt(sq,b[i]) if piece == PIECE.BISHOP else ratt(sq,b[i])
                magic = BISHOP_MAGICS[sq] if piece == PIECE.BISHOP else ROOK_MAGICS[sq]
                bits = BBITS[sq] if piece == PIECE.BISHOP else RBITS[sq]
                j = <int>((b[i]*magic) >> (64 - bits))
                
                if piece == PIECE.BISHOP:
                    BISHOP_ATTACKS[j,sq] = a[i]
                else:
                    ROOK_ATTACKS[j,sq] = a[i]

        a = np.zeros(4096,dtype=np.uint64)
        b = np.zeros(4096,dtype=np.uint64)
        
#Function to wrap non-sliding and sliding attack generation
cpdef void initAttacks():
    initNonSlidingAttacks()
    initSlidingAttacks()
    initLineBB()

cdef ULL getSlidingAttack(ULL blocker, int square, PIECE pieceType):
    cdef ULL mask, magic, a, b
    cdef int bits, index
    if pieceType == PIECE.BISHOP:
        mask = BISHOP_ATTACK_MASK[square]
        bits = BBITS[square]
        magic = BISHOP_MAGICS[square]

        index = ((mask & blocker) * magic) >> (64 - bits)

        return BISHOP_ATTACKS[index,square]

    elif pieceType == PIECE.ROOK:
        mask = ROOK_ATTACK_MASK[square]
        bits = RBITS[square]
        magic = ROOK_MAGICS[square]
        index = <int>(((mask & blocker) * magic) >> (64 - bits))

        return ROOK_ATTACKS[index,square]
    
#Calculate the attackers to a square given blockers in a position
cdef ULL attackersTo(ULL[:,:] pboard,ULL blocker,int square):
    cdef ULL pawnAttacksTo, knightAttacksTo, bishopAttacksTo, rookAttacksTo, kingAttacksTo
    
    pawnAttacksTo = (attacksFrom(PIECE.PAWN,square,COLOR.WHITE,0) & pboard[<int>COLOR.WHITE][<int>PIECE.PAWN]) | \
                    (attacksFrom(PIECE.PAWN,square,COLOR.BLACK,0) & pboard[<int>COLOR.BLACK][<int>PIECE.PAWN]) 
    knightAttacksTo = (attacksFrom(PIECE.KNIGHT,square,COLOR.WHITE,0) & pboard[<int>COLOR.WHITE][<int>PIECE.KNIGHT]) | \
                      (attacksFrom(PIECE.KNIGHT,square,COLOR.BLACK,0) & pboard[<int>COLOR.BLACK][<int>PIECE.KNIGHT])
    bishopAttacksTo = (attacksFrom(PIECE.BISHOP,square,COLOR.WHITE,blocker) & (pboard[<int>COLOR.WHITE][<int>PIECE.BISHOP] | pboard[<int>COLOR.WHITE][<int>PIECE.QUEEN])) | \
                      (attacksFrom(PIECE.BISHOP,square,COLOR.BLACK,blocker) & (pboard[<int>COLOR.BLACK][<int>PIECE.BISHOP] | pboard[<int>COLOR.BLACK][<int>PIECE.QUEEN]))
    rookAttacksTo = (attacksFrom(PIECE.ROOK,square,COLOR.WHITE,blocker) & (pboard[<int>COLOR.WHITE][<int>PIECE.ROOK] | pboard[<int>COLOR.WHITE][<int>PIECE.QUEEN])) | \
                    (attacksFrom(PIECE.ROOK,square,COLOR.BLACK,blocker) & (pboard[<int>COLOR.BLACK][<int>PIECE.ROOK] | pboard[<int>COLOR.BLACK][<int>PIECE.QUEEN]))
    kingAttacksTo = (attacksFrom(PIECE.KING,square,COLOR.WHITE,blocker) & pboard[<int>COLOR.WHITE][<int>PIECE.KING]) | \
                    (attacksFrom(PIECE.KING,square,COLOR.BLACK,blocker) & pboard[<int>COLOR.BLACK][<int>PIECE.KING])
                    
    return  pawnAttacksTo | knightAttacksTo | bishopAttacksTo | rookAttacksTo | kingAttacksTo

#Calculate the attacksFrom a given pieceType on a given square for a given color
cdef ULL attacksFrom(PIECE pieceType, int square, COLOR color, ULL blocker):

    if pieceType == PIECE.PAWN:
        return MOVE_ARRAY[3,square] if color == COLOR.WHITE else MOVE_ARRAY[0,square]
    elif (pieceType == PIECE.KNIGHT) | (pieceType == PIECE.KING):
        return MOVE_ARRAY[<int>pieceType,square]
    if pieceType == PIECE.QUEEN:
        return getSlidingAttack(blocker,square,PIECE.ROOK) | getSlidingAttack(blocker,square,PIECE.BISHOP)
    else:
        return getSlidingAttack(blocker,square,pieceType)

#Finds the blocker pieces from attacks of a given color board to a square (Pinned pieces)
cdef ULL blockers(ULL[:] pboard,ULL pieces,int square):
    cdef ULL bishopAttacksTo, rookAttacksTo, attackers, occ, b, inAttack
    cdef ULL blocker = 0
    bishopAttacksTo = attacksFrom(PIECE.BISHOP,square,COLOR.WHITE,0) & (pboard[<int>PIECE.BISHOP] | pboard[<int>PIECE.QUEEN])
    rookAttacksTo = attacksFrom(PIECE.ROOK,square,COLOR.WHITE,0) & (pboard[<int>PIECE.ROOK] | pboard[<int>PIECE.QUEEN])
    attackers = (bishopAttacksTo | rookAttacksTo)
    occ = pieces ^ attackers
    
    while(attackers):
        b = betweenBB(lsb(attackers),square)
        inAttack = b & occ
        if pop_count(inAttack) == 1:
            blocker |= inAttack
        attackers = pop_lsb(attackers)
    return blocker

#Creates a bitboard of bits set between 2 squares
cdef ULL betweenBB(int sq1,int sq2):
    cdef ULL a, b, c, d = 0
    a = LINE_BB[sq1][sq2]
    b = (<ULL>0xFFFFFFFFFFFFFFFF << sq1)
    c = (<ULL>0xFFFFFFFFFFFFFFFF << sq2)
    d = a & (b ^ c)

    return d & (d-1)

#Calculates whether the squares in teh same line
cdef bint inRay(int sq1,int sq2,int sq3):
    return <bint>(LINE_BB[sq1][sq2] & BB_SQUARES[sq3])

#Calculates a line of squares given 2 squares if they are aligned. Used in betweenBB to later find squares between 2 sq
cdef void initLineBB():
    cdef int s1, s2
    for s1 from 0 <= s1 < 64:
        for pieces in [PIECE.BISHOP,PIECE.ROOK]:
            for s2 from 0 <= s2 < 64:
                if attacksFrom(pieces,s1,COLOR.WHITE,0) & BB_SQUARES[s2]:
                    LINE_BB[s1][s2] = (attacksFrom(pieces,s1,COLOR.WHITE,0) & attacksFrom(pieces,s2,COLOR.WHITE,0)) | BB_SQUARES[s1] | BB_SQUARES[s2]