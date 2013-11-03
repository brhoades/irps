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
        
        self.mem = int(cfg[AGENT][MEM])
        self.mdepth = int(cfg[AGENT][DEPTH])
        self.tprob = float(cfg[INIT][IPROB])
        self.meth = cfg[INIT][METHOD]
        
        for i in range(self.mem):
            self.mymoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )
            self.tmoves.append( random.randint(moves.MINMOVE, moves.MAXMOVE) )

        #Nodes by depth
        self.nbd = [ [] for i in range(self.mdepth) ]
        
        #Root node
        self.root = None
        
        #leaf initialization
        if type == "evolve":
            self.root = self.randomNodule( None )

            if not self.root.isLeaf:
                self.populate( self.root )
                
        elif type == "lastwin":
            #Drop a simple tree here that always chooses last winner
            #FIXME: Is memory a FIFO or FILO?
            self.root = node( self, None, None, False )
            self.root.operator = self.root.winner
            self.root.children.append( node( self, self.root, ["O", 1], False ) )
            self.root.children.append( node( self, self.root, ["P", 1], False ) )
        
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
    def randomNodule( self, parent ):
        #True? We're going to be a terminal
        if ( self.meth == GROW and util.roll(self.tprob) ) or self.mdepth == 0 or ( parent != None and parent.depth == self.mdepth-2 ):
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
    def populate( self, nod ):
        if nod.isLeaf:
            raise TypeError("Populate called on leaf")
        
        nod.children.append( self.randomNodule( nod ) )
        nod.children.append( self.randomNodule( nod ) )
        
        for n in nod.children:
            if not n.isLeaf:
                self.populate( n )
    
    #Run our GP and return our choice. We do our own memory except for the payoff / tmoves, which is done by
    #  upres.
    def run( self ):
        if self.root.isLeaf:
            return self.root.lookup( )
        else:
            return self.root.operator( )
       
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
        if op == None and not leaf:
            self.operator = self.randomOp( )
        else:
            self.operator = op
        
        #our two children
        self.children = []
        
        #How deep we are
        self.depth = 0
        up = self

        while up != self.agent.root and not self.agent.root == None:
            up = up.parent
            self.depth += 1
                    
        self.agent.nbd[self.depth].append(self)
    
    # Gives us a random operator reference
    def randomOp( self ):
        rint = random.randint(0,2)
        if rint == 0:
            return self.winner
        elif rint == 1:
            return self.loser
        elif rint == 2:
            return self.other
    
    # Winner returns the winner constant between our children
    def winner( self ):
        cres = self.getCRes( )
        
        return util.victor(cres[0], cres[1])
    
    # Loser returns the losing constant between our children
    def loser( self ):
        cres = self.getCRes( )

        #return the LOSER, so the one that's not the victor
        if util.victor(cres[0], cres[1]) == cres[0]:
            return cres[1]
        else:
            return cres[0]
        
    # Other returns the OTHER option between the two children. If there's more
    #   than one other, it returns a random one of the two.
    def other( self ):
        cres = self.getCRes( )
        
        ops = [moves.ROCK, moves.SCISSORS, moves.PAPER]
        for c in cres:
            if c in ops:
                ops.remove(c)
        
        if len(ops) == 1:
            return ops[0]
        else:
            return random.sample(ops, 1)[0]
        
    # Gets the resulting rock, paper, or scissors results from all children        
    def getCRes( self ):
        cres = []
        
        for i in range(0,2):
            #If child is a leaf, just perform a simple lookup for the outcome. Otherwise call its function.
            if self.children[i].isLeaf:
                cres.append( self.children[i].lookup( ) )
            else:
                cres.append( self.children[i].operator( ) )
            
        return cres
      
    # "Looks up" in our memory what our operator looks for, when we are a leaf
    def lookup( self ):
        if not self.isLeaf:
            raise TypeError("Lookup called on a node")
        
        type, index = self.operator
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
    
        