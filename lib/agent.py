#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a
#This contains our agent's memory and meat along with our GP tree logic.

import util, random
from const import *

class agent:
    
    def __init__( self, cfg, type ):
        #Store our individual payoffs for each sequence, ordered
        payoffs = []
        
        #Store our moves on each sequence, ordered
        mymoves = []
        
        #Store their moves on each sequence, ordered
        tmoves = []
        
        for i in range(0,int(cfg[AGENT][MEM])):
            mymoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )
        
        #Our depth
        depth = 0
        
        #Root node
        root = None
        
        if type == "evolve":
            while depth < int(cfg[AGENT][DEPTH]):
                #Do grow initialization here
                break
        elif type == "lastwin":
            #Drop a simple tree here that always chooses last win or random
            return
        
    def addNodule( self, parent, type, op=None ):
        return
        
class node:
    
    def __init__( self, root, parent, op ):
        #our parent
        parent = None
        
        #our root
        root = None
        
        #Our two children later
        children = []
        
        #our operation
        operator = None
    
        