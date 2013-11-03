#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a
# Our "main" function that dispatches everything.

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
    
    #It takes so long to parse this CSV, I'm caching it globally
    olog = None
    if cfg[MAIN][OPP] != "0":
        olog = util.loadCSV(cfg[MAIN][OPP])
    
    lg = util.log( cfg, cseed, util.gcfg( ) )
    best = None
    util.renderHead( cfg )
    for i in range( 0, int(cfg[MAIN][RUNS]) ):
        lg.sep( i )
        eagt=run(cfg, i, lg, olog)
        if best == None or eagt.fit > best.fit:
            best = eagt
        lg.spacer( )
    lg.best(best)
    lg.wrapUp(best)
    
    print("\n")

if __name__ == '__main__':
    main()
