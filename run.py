#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
# Our functions responsible for getting this whole mess running

#fire up our custom libraries
import os, sys, random, time
sys.path.append( os.path.abspath("lib") )

from gen import gen
from agent import agent
from const import *
from util import *

def run( cfg, i, lg, olog ):
    #read some cfg stuff in and convert it. Also init various caches.
    
    cfg[TERMINATE][NO_CHANGE_FITNESS] = int(cfg[TERMINATE][NO_CHANGE_FITNESS])
    cfg[TERMINATE][FITEVALS] = int(cfg[TERMINATE][FITEVALS])
        
    generation = gen( cfg )
        
    prnBase( cfg, i, generation )
        
    generation.initialize( )
        
    prnBase( cfg, i, generation )
        
    while noTerminate( cfg, generation ):
        lg.entry(generation)
        
        #Recomb + Mutation
        generation.recombination( )
        prnBase( cfg, i, generation )
        
        #Survival
        generation.survivalselection( )
        #prnBase( cfg, i, generation )
        

    lg.entry(generation)
    
    #delicately extract the best from the generation
    best = generation.best( )
    generation.delete( best )
    best.gen = None
        
    return best

def noTerminate( cfg, generation ):
    if cfg[TERMINATE][TYPE] == NUM_OF_FITEVALS:
        if generation.fitevals >= cfg[TERMINATE][FITEVALS]:
            return False
        else:
            return True
    elif cfg[TERMINATE][TYPE] == NO_CHANGE_IN_FITNESS:
        if not hasattr( noTerminate, "lastavg" ):
            noTerminate.lastavg = 0
            noTerminate.lastChange = 0
        if generation.average( ) > noTerminate.lastavg:
            noTerminate.lastavg = generation.average( )
            noTerminate.lastChange = 0
        else:
            noTerminate.lastChange += 1
        if noTerminate.lastChange >= cfg[TERMINATE][NO_CHANGE_FITNESS]:
            return False
        else:
            return True
        