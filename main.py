#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
# Our "main" function that dispatches everything.

#fire up our custom libraries
import os, sys, random
sys.path.append( os.path.abspath("lib") )

#load our custom libraries
import util
from log import log
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
    
    util.loadCSV(cfg[AGENT][CSV_FILE])
    
    lg = log( cfg, cseed, util.gcfg( ) )
    util.renderHead( cfg )

    best = None

    for i in range( 0, int(cfg[MAIN][RUNS]) ):
        lg.sep( i )

        nbest = run(cfg, i, lg)

        #Determine if our new potential best is better,
        #  this just uses the average of the two fitness values versus the bad opponents
        if best == None or nbest.fit > best.fit:
            if best != None:
                best.delete( )
            best = nbest

    lg.best(best)
    lg.absBestFinish(cfg, best)
    lg.wrapUp(best)
    
    print("\n")

if __name__ == '__main__':
    main()
