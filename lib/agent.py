#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a
#This contains our agent's memory and meat along with our GP tree logic.

import util, random
from const import *

class agent:
    
    def __init__( self, cfg, type ):
        #Store our individual payoffs for each sequence, ordered
        self.payoffs = []
        
        #Store our moves on each sequence, ordered
        self.mymoves = []
        
        #Store their moves on each sequence, ordered
        self.tmoves = []
        
        for i in range(0,int(cfg[AGENT][MEM])):
            self.mymoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )
            self.tmoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )
        
        #Our depth
        self.depth = 0
        
        #Root node
        self.root = None
        
        if type == "evolve":
            while self.depth < int(cfg[AGENT][DEPTH]):
                #Do grow initialization here
                break
        elif type == "lastwin":
            #Drop a simple tree here that always chooses last win or random
            return
        
    def addNodule( self, parent, type, op=None ):
        return
        
class node:
    
    def __init__( self, agent, parent, op, leaf ):
        #our agent
        self.agent = agent

        #our parent
        self.parent = parent
        
        #leaf or node
        self.isLeaf = leaf
        
        # our operation. If we're a leaf this is a list with P/O on the first spot, and a number following. 
        # If this is a node it's a function ref
        self.operator = None
        
        #our two children
        self.children = []
    
    def winner( self ):
        cres = []
        
        for i in range(2):
            #If child is a leaf, just perform a simple lookup for the outcome. Otherwise call its function.
            if self.children[i].isLeaf:
                cres.append( self.lookup( self.children[i].operator ) )
            else:
                cres.append( self.children[i]( ) )
        
        return util.victor(cres[0], cres[1])
        
    def loser( self ):
        cres = []
        
        for i in range(2):
            #If child is a leaf, just perform a simple lookup for the outcome. Otherwise call its function.
            if self.children[i].isLeaf:
                cres.append( self.lookup( self.children[i].operator ) )
            else:
                cres.append( self.children[i]( ) )
        
        #return the LOSER, so the one that's not the victor
        if util.victor(cres[0], cres[1]) == cres[0]:
            return cres[1]
        else:
            return cres[0]
        
    def lookup( self, op ):
        type, index = op
        lu = None
        
        #Types could be P or could be O. If it's P we look at our previous moves. If it's O we look
        #  at theirs.
        if type == "O":
            lu = self.agent.tmoves
        elif type == "P":
            lu = self.agent.mymoves
        else:
            raise TypeError("Didn't get O or P for lookup in operator.")
    
        if index > len(lu):
            raise TypeError("Somehow ended up with a index above k")
        
        return lu[index]
    
        