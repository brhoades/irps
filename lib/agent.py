#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
#This contains our agent's memory and meat and houses the gp tree.

import util, random
from node import node
from tree import tree
from const import *

class agent:
    def __init__( self, cfg, type ):
        #Store our individual payoffs for each sequence, ordered
        self.payoffs = []
        
        #Store our moves on each sequence, ordered
        self.mymoves = []
        
        #Store Their MOVES on each sequence, ordered
        self.tmoves = []
        
        self.mem = int(cfg[AGENT][MEM])
        if self.mem < 4:
            self.mem = 4
            
        self.tree =  tree( self, int(cfg[AGENT][DEPTH]), cfg[INIT][METHOD], type )
        
        self.fit = 0
        
        ################### Process stupid table ###################
        tpv = cfg[AGENT][PAYOFF].split(',')
        #Pay OFF TABLE
        self.pofftable = [[] for i in range(moves.MINMOVE,moves.MAXMOVE+1)]
        for i in range(0,len(tpv)):
            tpv[i] = float(tpv[i])
        #opponentplayer => res value
        #rr,rp,rs,pr,pp,ps,sr,sp,ss
        self.pofftable[moves.ROCK].append(tpv[0])
        self.pofftable[moves.ROCK].append(tpv[1])
        self.pofftable[moves.ROCK].append(tpv[2])

        self.pofftable[moves.PAPER].append(tpv[3])
        self.pofftable[moves.PAPER].append(tpv[4])
        self.pofftable[moves.PAPER].append(tpv[5])
        
        self.pofftable[moves.SCISSORS].append(tpv[6])
        self.pofftable[moves.SCISSORS].append(tpv[7])
        self.pofftable[moves.SCISSORS].append(tpv[8])
        ###################DONE WITH STUPID TABLE###################
        
        
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
        self.payoffs.append(self.pofftable[int(opp)][int(res)])
        
        #Update our memory for them
        del self.tmoves[self.mem-1]
        self.tmoves.insert(0, opp)
        
    # Our fitness, just an average of our payloads
    def fitness( self ):
        sum = 0
        for i in self.payoffs:
            sum += i
        self.fit = sum/len(self.payoffs)
        
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
    
        