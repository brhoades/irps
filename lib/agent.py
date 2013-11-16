#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
#This contains our agent's memory and meat and houses the gp tree.

import util, random
from node import node
from tree import tree
from const import *

class agent:
    def __init__( self, gen, cfg, type="evolve" ):
        #Our parent generation
        self.gen = gen
        
        #Store our individual payoffs for each sequence, ordered
        self.payoffs = []
        
        #Store our moves on each sequence, ordered
        self.mymoves = []
        
        #Store Their MOVES on each sequence, ordered
        self.tmoves = []
        
        self.mem = int(cfg[AGENT][MEM])
        if self.mem < 4:
            self.mem = 4
            
        self.tree = tree( self, int(cfg[AGENT][DEPTH]), self.gen.method, type )
        
        self.fit = 0
        
        for i in range(self.mem):
            self.mymoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )
            self.tmoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )
    
    # Run our GP and return our choice. We do our own memory except for the payoff / tmoves, which is done by
    #   upres.
    def run( self ):
        res = -2
        if self.tree.root.isLeaf:
            res=self.tree.root.lookup( )
        else:
            res=self.tree.root.operator( )
            
        #Update our memory
        #Our memory is a LIFO where [0] is the latest and [k-1] is the oldest, k turns ago
        del self.mymoves[self.mem-1]
        self.mymoves.insert(0, res)
        
        return res
    
    # Update our memory for them and our payload
    # UPdates our RESults
    def upres( self, res, opp ):
        self.payoffs.append(self.gen.pofftable[int(opp)][int(res)])
        
        #Update our memory for them
        del self.tmoves[self.mem-1]
        self.tmoves.insert(0, opp)
        
    # Our fitness, just an average of our payloads
    #   However we need to run our competition a few times
    def fitness( self ):
        #FIXME: hacked in
        otype = self.gen.cfg[MAIN][OPP] 
        
        for j in range(0,self.gen.seqs):
            ores = -2
            if otype == "0":
                ores = victor( self.tmoves[0], self.mymoves[0] )
            else:
                ores = util.CSVAI( self.tmoves, self.mymoves )
            
            myres = self.run( )
            
            self.upres( myres, ores )
            
        sum = 0
        for i in self.payoffs:
            sum += i
        self.fit = sum/len(self.payoffs)
        
        self.gen.fitevals += 1
        
    # Return our structure in preorder
    def serialize( self ):
        return self.preorder( self.tree.root )

    #Outputs our nodes in preorder
    def preorder( self, cur ):
        ret = ""
        
        if cur.isLeaf:
            ret += ''.join([cur.operator[0], str(cur.operator[1]), " "])
        else:
            ret += ''.join([cur.operator.__name__, " "])
        
        if len(cur.children) > 0:
            ret += self.preorder(cur.children[0])
            ret += self.preorder(cur.children[1])
        
        return ret
    
        