#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a

#fire up our custom libraries
import os, sys, random
sys.path.append( os.path.abspath("lib") )

#load our custom libraries
import util
from run import run
from agent import agent
from const import *


def main():
    cfg = util.readConfig(util.gcfg( ))
    
    cseed = 0
    if cfg[MAIN][SEED] == '':
        cseed = util.seed( )
    else:
        cseed = float(cfg[MAIN][SEED])
    
    random.seed(cseed)
    
    #lg = log( cfg, cseed, gcfg( ) )
    #best = False
    for i in range( int(cfg[MAIN][RUNS]) ):
        print( "Run:", str(i+1) )
        eagt=agent(cfg, type="evolve")        
        print( eagt )
        run(cfg, eagt, i)
    #lg.best(best)
    #lg.wrapUp(best)

if __name__ == '__main__':
    main()
