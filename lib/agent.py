#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
#This contains our agent's memory and meat and houses the gp tree.

import util, random
from node import node
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
            
        self.mdepth = int(cfg[AGENT][DEPTH])
        self.meth = cfg[INIT][METHOD]
        
        self.fit = 0
        #Our children update our depth as they're added
        self.depth = 0
        
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

        #Nodes by depth
        self.nbd = [ [] for i in range(self.mdepth) ]
        
        #Root node
        self.root = None
        
        if type == "evolve":
            #We do grow, randomly if "half and half"
            if ( self.meth == HALFANDHALF and util.flip( ) ) or self.meth == GROW:
                self.populate( GROW )
            else: #Otherwise we do full initialization
                self.populate( FULL )
        elif type == "lastwin":
            #Drop a simple tree here that always chooses last winner
            #Our memory is a stack where [0] is the latest
            self.root = node( self, None, None, False )
            self.root.operator = self.root.winner
            self.root.children.append( node( self, self.root, ["O", 0], False ) )
            self.root.children.append( node( self, self.root, ["P", 0], False ) )
        
    def __str__( self ):
        ret = ""
        
        for nl in self.nbd:
            for n in nl:
                if n.isLeaf:
                    ret += ''.join([n.operator[0], str(n.operator[1]), "   "])
                else:
                    ret += ''.join([n.operator.__name__, "   "])
            ret += "\n"
        return ret
    
    # Pass a parent and we'll randomly add a terminal/node or intelligently end the tree
    def randomNodule( self, parent, meth=None ):
        #True? We're going to be a terminal
        if ( meth == GROW and util.flip( ) ) or self.mdepth <= 1 or ( parent != None and parent.depth == self.mdepth-2 ):
            return node( self, parent, self.randomTerm( ), True )
        else:
            return node( self, parent, None, False )
        
    def randomTerm( self ):
        term = []
        if util.flip( ):
            term.append("O")
        else:
            term.append("P")
        
        #-1 here since this will reference our list blindly
        term.append(random.randint(0,self.mem-1))
        return term
    
    # Pass the node whose children we're populating and, depending on that node's depth, we'll populate kids for it
    #   recursively
    def populate( self, method, nod=None ):
        if nod != None and nod.isLeaf:
            raise TypeError("Populate called on leaf")
        elif nod == None and self.root != None:
            raise TypeError("Root exists but no node passed")
        
        #Special case for root
        if self.root == None:
            self.root = self.randomNodule( None )
            if self.root.isLeaf:
                return
            nod = self.root
        
        nod.children.append( self.randomNodule( nod, method ) )
        nod.children.append( self.randomNodule( nod, method ) )
        
        for n in nod.children:
            if not n.isLeaf:
                self.populate( method, n )
    
    # Run our GP and return our choice. We do our own memory except for the payoff / tmoves, which is done by
    #   upres.
    def run( self ):
        res = -2
        if self.root.isLeaf:
            res=self.root.lookup( )
        else:
            res=self.root.operator( )
            
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
        return self.preorder( self.root )

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
    
        