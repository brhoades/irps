#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
# Contains our base constants used for everything.

#main config sections
AGENT = "agent"
MAIN = "main"
GENERATION = "gen"
INIT = "init"
PARSEL = "parentselection"
MUTATE = "mutation"
SURVSEL = "survivalselection"
LOG = "log"

#agent
DEPTH = "d"
MEM = "k"
PAYOFF = "payoff"
PARSIMONY_PRESSURE_COEFF = "ppcoeff"

#main
SEED = "seed"
SEQRUNS = "l"
RUNS = "runs"
OPP = "opp"
FITEVALS="fitevals"

#gen
MU = "mu"
LAMBDA = "lamb"

#init
METHOD = "method"

#survival and parent selection
TYPE = "type"
TOURNAMENT_K = "k"

#mutate
MUTATION_RATE = "chance"

#arguments / operators
FITNESS_PROPORTIONAL = "0"
OVER_SELECTION = "1"
TRUNCATION = "0"
K_TOURNAMENT = "2"

GROW = "grow"
FULL = "full"
HALFANDHALF = "halfandhalf"

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