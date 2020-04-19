# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:26:34 2020

@author: Sid
"""

# state
#     - en passant (ep square)
#     - castle available (queen & king side) (1 or 0, 1 or 0)
#     - 50 move rule (# of moves)
#     - 3 repeated position (# of repeats)
    
#who's move is it?

class Position:
    def __init__(self,bb):
        self.bb = bb
        self.state = 0b0000000011000000
        
    def getBB():
        return self.bb
    
    def getState():
        return self.state
    
    def setBB(bitBB):
        self.bb = bitBB
    
    def setState(st):
        self.state = st
        
    def getEpSquare():
        return (state << )