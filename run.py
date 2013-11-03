#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a
#Our functions responsible for getting this whole mess running

#fire up our custom libraries
import os, sys, random
sys.path.append( os.path.abspath("lib") )

from agent import agent
from const import *

def run( cfg, i ):
    seqs = int(cfg[MAIN][SEQRUNS])
    agnt = agent(cfg, type="evolve")        
    
    for seqn in range(0,seqs):
        agnt.run( )