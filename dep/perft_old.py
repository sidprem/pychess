# -*- coding: utf-8 -*-
"""
Created on Mon May 11 23:08:53 2020

@author: Sid
"""

from Movegen import generateLegalMoves


def perft(depth,pos,root):
    nodes = 0
    if depth == root:
        print("\n")
        print("depth is " + str(depth))

    if depth == 0:
        return 1
    for m in generateLegalMoves(pos):
        if depth == 1:
            nodes += 1
        else:
            pos.applyMove(m)
            count = perft(depth - 1,pos,root)
            nodes += count
            pos.undoMove()
            if depth == root:
                print(pos.moveToSAN(m)+" "+str(count))
       
    return nodes