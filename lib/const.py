#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a

#main config sections
AGENT = "agent"
MAIN = "main"
INIT = "init"
LOG = "log"

#agent
DEPTH = "d"
MEM = "k"
PAYOFF = "payoff"

#main
SEED = "seed"
SEQRUNS = "l"
RUNS = "runs"
OPP = "opp"
FITEVALS="fitevals"

#init
METHOD = "method"
IPROB = "prob"

GROW = "grow"
FULL = "full"

#log
GIT_LOG_HEADERS = "logh"
RESULT_LOG_FILE = "result"
SOLUTION_LOG_FILE = "solution"

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