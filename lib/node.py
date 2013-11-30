#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
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
        
        #Set these for copy recognition
        self.winner.__dict__["type"] = "winner"
        self.other.__dict__["type"] = "other"
        self.loser.__dict__["type"] = "loser"
        
        #List of operator references
        self.ops = (self.winner, self.loser, self.other,)
        
        #Our operation. If we're a leaf this is a list with P/O on the first spot, and a number following. 
        #  If this is a node it's a function ref
        if not "op" in args and not args["leaf"]:
            self.operator = self.randomOp( )
        elif not args["leaf"] and "copy" in args:
            self.operator = self.copyOp( args["op"] )
        else:
            self.operator = args["op"]
        
        #Our two children
        self.children = []
        
        #How deep we are
        self.depth = 0
        if self.parent != None:
            self.depth = self.parent.depth + 1
        elif self.tree.root == None or self == self.tree.root:
            self.depth = 0
        else:
            raise ReferenceError("Dangling node with no parent")
        
        self.tree.nodes.append( self )
    
    # Gives us a random operator reference
    def randomOp( self ):
        return self.ops[random.randint(0,2)]
    
    # Winner returns the winner constant between our children
    def winner( self ):
        cres1, cres2 = self.getCRes( )
        
        return util.victor(cres1, cres2)
    
    # Loser returns the losing constant between our children
    def loser( self ):
        cres1, cres2 = self.getCRes( )

        #return the LOSER, so the one that's not the victor
        if util.victor(cres1, cres2) == cres1:
            return cres2
        
        return cres1
        
    # Other returns the OTHER option between the two children. If there's more
    #   than one other, it returns a random one of the two.
    def other( self ):
        cres1, cres2 = self.getCRes( )
        
        ops = OPS[:]
        if cres1 in ops:
            ops.remove(cres1)
    
        if cres2 in ops:
            ops.remove(cres2)
    
        if len(ops) == 1:
            return ops[0]
        
        return ops[random.randint(0,1)]
        
    # Gets the resulting rock, paper, or scissors results from all children        
    def getCRes( self ):
        cres1 = None
        cres2 = None
        
        #If child is a leaf, just perform a simple lookup for the outcome. Otherwise call its function.
        if self.children[0].isLeaf:
            cres1 = self.children[0].lookup( )
        else:
            cres1 = self.children[0].operator( )
            
        if self.children[1].isLeaf:
            cres2 = self.children[1].lookup( )
        else:
            cres2 = self.children[1].operator( )
                        
        return cres1, cres2
      
    # "Looks up" in our memory what our operator looks for, when we are a leaf
    def lookup( self ):
        type, index = self.operator
        
        #Types could be "P" or could be "O". If it's "P" we look at our previous moves. If it's "O" we look
        #  at theirs.
        if type == srctype.OPPONENT:
            return self.tree.agent.tmoves[index]
        
        return self.tree.agent.mymoves[index]

    #Copies an operator over to our own operator using an internal register
    def copyOp( self, other ):
        if other.type == "winner":
            return self.winner
        if other.type == "loser":
            return self.loser
        if other.type == "other":
            return self.other
    
    #Derefs everything below including this node
    def delete( self ):
        self.parent = None
        
        if not self.isLeaf:
            self.children[0].delete( )
            self.children[1].delete( )

        self.tree = None
        
        self.op = None
        
        self.children = [1]