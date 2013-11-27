#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
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
        
        #Array of all nodes
        self.nodes = []
        
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
            self.root = node( self, None, leaf=False )
            self.root.operator = self.root.winner
            self.root.children.append( node( self, self.root, op=["O", 0], leaf=False ) )
            self.root.children.append( node( self, self.root, ["P", 0], leaf=False ) )
        
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
    
    def copy( self, other ):
        self.root = node( self, None, leaf=other.root.isLeaf, op=other.root.operator, copy=True )
                
        if not self.root.isLeaf:
            self.copynode( self.root, other.root.children[0] )
            self.copynode( self.root, other.root.children[1] )
            
    def copynode( self, parent, nod ):
        thisnode = node( self, parent, leaf=nod.isLeaf, op=nod.operator, copy=True )
        parent.children.append( thisnode )
        
        if not thisnode.isLeaf:
            self.copynode( thisnode, nod.children[0] )
            self.copynode( thisnode, nod.children[1] )
            
    # Pass a parent and we'll randomly add a terminal/node or intelligently end the tree
    def randomNodule( self, parent, meth=None ):
        #True? We're going to be a terminal
        if ( meth == GROW and util.flip( ) ) or self.maxdepth <= 1 or ( parent != None and parent.depth == self.maxdepth-2 ):
            return node( self, parent, op=self.randomTerm( ), leaf=True )
        else:
            return node( self, parent, leaf=False )
    
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
                
    #Update depth on the tree recursively and accurately
    def updateDepth( self, nod=None ):
        set = False
        if nod == None:
            nod = self.root
            set = True
        
        if not nod.isLeaf:
            d1 = self.updateDepth( nod.children[0] )
            d2 = self.updateDepth( nod.children[1] )
            
            if d1 >= d2 and not set:
                return d1
            elif d1 > d2:
                self.depth = d1
                return
            
            if d2 > d1 and not set:
                return d2
            elif d2 > d1:
                self.depth = d2
                return
        else:
            return nod.depth
                
    #Derefs everything
    def delete( self ):
        self.root.delete( )
        
        self.nodes = [1]
        
        self.root = None
        self.agent = None
    
#Swaps two subtrees between two trees
# 1) Dereferences two subtress from their tree.
# 2) Points them to a new tree with its new children.
# 3) Recursively updates depth.
def swapsubtree( mytree, mysubtree, theirtree, theirsubtree ):
    #root check, swap roots if applicable
    if mysubtree.parent == None:
        mytree.root = theirsubtree
    if theirsubtree.parent == None:
        theirtree.root = mysubtree
    
    #Exchange parents
    mypar = theirsubtree.parent
    theirsubtree.parent = mysubtree.parent
    mysubtree.parent = mypar
    
    #Set our new parents to their new children
    if theirsubtree.parent != None:
        theirsubtree.parent.children[theirsubtree.parent.children.index(mysubtree)] \
            = theirsubtree
    if mysubtree.parent != None:
        mysubtree.parent.children[mysubtree.parent.children.index(theirsubtree)] \
            = mysubtree
    
    updateSTree( mysubtree, theirtree )
    updateSTree( theirsubtree, mytree )
    
    mytree.updateDepth( )
    theirtree.updateDepth( )

#Recursively UPDATES a Sub TREE's references/depth
def updateSTree( nod, ntree ):
    otree = nod.tree
    nod.tree = ntree
    
    if nod.parent == None:
        nod.depth = 0
    else:
        nod.depth = nod.parent.depth + 1
    
    #Update both tree's nods
    nod.tree.nodes.append( nod )
    otree.nodes.remove( nod )
    
    for n in nod.children:
        updateSTree( n, ntree )