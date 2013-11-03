#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a
#Our functions responsible for getting this whole mess running

#fire up our custom libraries
import os, sys, random
sys.path.append( os.path.abspath("lib") )

from agent import agent
from const import *
from util import *

def run( cfg, i ):
    #read some cfg stuff in and convert it. Also init various caches.
    seqs = int(cfg[MAIN][SEQRUNS])
    otype = cfg[MAIN][OPP]
    fitevals = int(cfg[MAIN][FITEVALS])
    olog = None
    print( "Run:", i )
    if otype != "0":
        olog = loadCSV(otype)
        
    #running best stuff
    best = None
    #Fitness counter
    fitcnt = 0
    
    while fitcnt < fitevals:
        agnt = agent(cfg, type="evolve")        
        
        #Do our sequences
        for seqn in range(0,seqs):
            ores = -2
            #Do whatever the opponent is doing
            if otype == "0":
                ores = victor( agnt.tmoves[0], agnt.mymoves[0] )
            else:
                ores = csvop( olog, agnt.tmoves, agnt.mymoves )
                
            #Do our run
            gpres = agnt.run( )
            
            #print( "GP:", tauriTran(gpres), " ", "Op:", tauriTran(ores), "  vic:", tauriTran(victor(gpres, ores)) )
            
            #Update our internal memory and payload
            agnt.upres( gpres, ores )
        
        #Fitness check
        agnt.fitness( )
        fitcnt += 1
        
        if best == None or agnt.fit > best.fit:
            best = agnt
        
    return best