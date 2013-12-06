#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
#This contains our agent's memory and meat and houses the gp tree.

import util, random
from node import node
from tree import *
from const import *
from collections import deque

class agent:
    def __init__( self, gen, **args ):        
        #Our parent generation
        self.gen = gen
        
        #A temporary pointer to our opponent's memory
        self.tmoves = None
        
        #Store our individual payoffs for each sequence, ordered
        self.payoffs = []
        
        self.mem = int(self.gen.agent[MEM])
        if self.mem < 4:
            self.mem = 4
        
        #Store our moves on each sequence, ordered
        # Create some random noise for the first sequence
        self.mymoves = deque( [random.randint(moves.MINMOVE, moves.MAXMOVE) for i in range(self.mem)], self.mem )
                
        if not "copy" in args and not "read" in args:
            self.tree = tree( self, int(self.gen.agent[DEPTH]), self.gen.method )
        elif "copy" in args:
            self.tree = tree( self, int(self.gen.agent[DEPTH]), None )
            self.tree.copy( args["copy"].tree )
        elif "read" in args:
            self.tree = tree( self, 0, None )
        
        self.fit = 0
        
    # Run our GP and return our choice. We do not touch our memory so it's easier to pass mymoves to them payoff / tmoves, which is done by
    #   upres.
    def run( self, tmoves ):
        res = -2
        self.tmoves = tmoves
        
        if self.tree.root.isLeaf:
            res=self.tree.root.lookup( )
        else:
            res=self.tree.root.operator( )
        
        #Put this back for later
        self.tmoves = None
        
        return res
    
    # Update our payload
    def upres( self, res, opp ):
        self.payoffs.append(self.gen.pofftable[opp][res])
        
        #Update our memory
        #Our memory is a LIFO where [0] is the latest and [k-1] is the oldest, k turns ago
        self.mymoves.appendleft(res)
    
    # Our fitness, just an average of our payloads
    #   However we need to run our competition a few times
    #   All payoffs are cleared at the beginning of a generation (in plus)
    #   We will use payoffs given from other rounds to save time.
    def fitness( self ):
        numtogo = self.gen.coefnum - len( self.payoffs )
        if numtogo > 0:
            opponents = random.sample(self.gen.inds, numtogo)
            beforepayoff = self.mem * 2
            
            for opp in opponents:
                for i in range(self.gen.seqs):                
                    ores = opp.run( self.mymoves )
                    myres = self.run( opp.mymoves )
                    if i > beforepayoff:
                        self.upres( myres, ores )
                        opp.upres( ores, myres )
                self.gen.fitevals += 1

        sum = 0
        for i in self.payoffs:
            sum += i
        self.fit = sum/len(self.payoffs)

        self.penalize( )
        
    # Penalizes our fitness based on tree size
    def penalize( self ):
        coeff = float(self.gen.agent[PARSIMONY_PRESSURE_COEFF])
        
        if self.tree.depth > self.tree.maxdepth:
            self.fit += (self.tree.maxdepth - self.tree.depth) * coeff
            if self.fit < 0:
                self.fit = 0
        
    # Return our structure in preorder
    def serialize( self ):
        return self.preorder( self.tree.root )

    # Outputs our nodes in preorder
    def preorder( self, cur ):
        ret = ""
        
        if cur.isLeaf:
            p1 = "O"
            if cur.operator[0] != srctype.OPPONENT:
                p1 = "P"
            ret += ''.join([p1, str(cur.operator[1]), " "])
        else:
            ret += ''.join([cur.operator.__name__, " "])
        
        if len(cur.children) > 0:
            ret += self.preorder(cur.children[0])
            ret += self.preorder(cur.children[1])
        
        return ret
    
    # Mutate oursevles if we have a chance
    def mutate( self ):
        if not util.roll( self.gen.mutaterate ):
            return
        
        point = random.sample(self.tree.nodes, 1)[0]
        
        newtree = tree( self, int(self.tree.maxdepth), "grow" )
        
        swapsubtree( self.tree, point, newtree, newtree.root )

        point.parent = None
        
        point.delete( )
        
        #Fitness is calculated in recombine
        
    def delete( self ):
        self.gen = None
        self.tree.delete( )
        self.tree = None