#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a

#main config sections
AGENT = "agent"
MAIN = "main"
INIT = "init"

#indicies
DEPTH = "d"
MEM = "k"

#main
SEED = "seed"
SEQRUNS = "l"
RUNS = "runs"

#init
METHOD = "method"
IPROB = "prob"

class moves:
    MINMOVE=0
    ROCK=0
    PAPER=1
    SCISSORS=2
    MAXMOVE=2
    
class payoffs:
    LOSS=-1
    TIE=0
    WIN=1