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
    
    otype = cfg[MAIN][OPP]
    fitevals = int(cfg[MAIN][FITEVALS])
        
    #running best stuff
    best = None
    #Running average
    avg = []
    #Fitness counter
    fitcnt = 0
        
    generation = gen( cfg )
        
    prnBase( cfg, i, generation )
        
    generation.initialize( )
        
    prnBase( cfg, i, generation )
        
    while generation.fitevals < fitevals:
        
        #Recomb + Mutation
        generation.recombination( )
        prnBase( cfg, i, generation )
        
        #Survival
        generation.survivalselection( )
        prnBase( cfg, i, generation )
        
        #if best == None or agnt.fit > best.fit:
            #best = agnt
            #lg.entry( fitcnt, agnt)
        
        #tavg = 0
        #for ind in avg:
            #tavg += ind
        #tavg /= len(avg)
        
    return best