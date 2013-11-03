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
    seqs = int(cfg[MAIN][SEQRUNS])
    agnt = agent(cfg, type="evolve")        
    otype = cfg[MAIN][OPP]
    olog = None
    print( "Run:", i )
    if otype != "0":
        olog = loadCSV(otype)
    
    for seqn in range(0,seqs):
        print("Sequence:", seqn)
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
        
    