#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
#This is the file for our node class, which contains per node logic.

import util, random
from const import *

class node:
    def __init__( self, tree, parent, **args ):
        #our tree
        self.tree = tree

        #our parent
        self.parent = parent
        
        #leaf or node
        self.isLeaf = args["leaf"]
        
        # our operation. If we're a leaf this is a list with P/O on the first spot, and a number following. 
        # If this is a node it's a function ref
        if not "op" in args and not args["leaf"]:
            self.operator = self.randomOp( )
        else:
            self.operator = args["op"]
        
        #Our two children
        self.children = []
        
        #How deep we are
        self.depth = 0
        if self.parent != None:
            self.depth = self.parent.depth + 1
        elif self.tree.root == None:
            self.depth = 0
        else:
            raise ReferenceError("Dangling node with no parent")
        
        self.tree.nodes.append( self )
        
    
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
            lu = self.tree.agent.tmoves
        elif type == "P":
            lu = self.tree.agent.mymoves
        else:
            raise TypeError("Didn't get O or P for lookup in operator.")
    
        if index > len(lu):
            raise TypeError("Somehow ended up with a index above k")

        return lu[index]