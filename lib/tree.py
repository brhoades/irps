#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
#This is the functional part of our gp tree's logic

import util, random
from node import node
from const import *

class tree:
    def __init__( self, agent, maxdepth, method, type="evolve" ):
        self.agent = agent
        
        self.meth = method
        
        #The max depth our tree should have
        #FIXME: This should be generation-level
        self.maxdepth = maxdepth
        
        #Nodes by depth
        self.nbd = [ [] for i in range(self.maxdepth) ]
        
        #Root node
        self.root = None
        
        #Our children update our depth as they're added
        self.depth = 0
        
        if type == "evolve":
            #We do grow, randomly if "half and half"
            if ( self.meth == HALFANDHALF and util.flip( ) ) or self.meth == GROW:
                self.populate( GROW )
            else: #Otherwise we do full initialization
                self.populate( FULL )
        elif type == "lastwin":
            #Drop a simple tree here that always chooses last winner
            #Our memory is a queue where [0] is the latest
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
        if ( meth == GROW and util.flip( ) ) or self.maxdepth <= 1 or ( parent != None and parent.depth == self.maxdepth-2 ):
            return node( self, parent, self.randomTerm( ), True )
        else:
            return node( self, parent, None, False )
    
    # Randomly return a terminal
    def randomTerm( self ):
        term = []
        if util.flip( ):
            term.append("O")
        else:
            term.append("P")
        
        #-1 here since this will reference our list blindly
        term.append(random.randint(0,self.agent.mem-1))
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