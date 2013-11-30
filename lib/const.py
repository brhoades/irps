#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
# Contains our base constants used for everything.

#main config sections
AGENT = "agent"
MAIN = "main"
GENERATION = "gen"
INIT = "init"
PARSEL = "parentselection"
MUTATE = "mutation"
SURVSEL = "survivalselection"
TERMINATE = "terminate"
LOG = "log"

#agent
DEPTH = "d"
MEM = "k"
PAYOFF = "payoff"
PARSIMONY_PRESSURE_COEFF = "ppcoeff"
CSV_FILE = "csv"
COEV_FIT_SAMPLE_PERCENT = "coevfsp"

#main
SEED = "seed"
SEQRUNS = "l"
RUNS = "runs"
OPP = "opp"

#gen
MU = "mu"
LAMBDA = "lamb"

#init
METHOD = "method"

#survival and parent selection
TYPE = "type"
TOURNAMENT_K = "k"
OVERSEL_PERCENT = "c"
STRATEGY = "strat"

#mutate
MUTATION_RATE = "chance"

#Termination parameters
FITEVALS="fitevals"
NO_CHANGE_FITNESS="j"

#arguments / operators
FITNESS_PROPORTIONAL = "0"
OVER_SELECTION = "1"
TRUNCATION = "0"
K_TOURNAMENT = "2"

#Strategy types
COMMA = "0"
PLUS = "1"

#Termination shit
NUM_OF_FITEVALS = "0"
NO_CHANGE_IN_FITNESS = "1"

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

OPS = [moves.ROCK, moves.SCISSORS, moves.PAPER]


#Our victor lookup, using p1 as first key and p2 as second.
#Rock is 0, so first tuple is rock as p1, then first res of first tuple is rockvrock
#1 means p1 wins or tie, 2 p2
VICTOR_LOOKUP_TABLE = ((1,2,1,),     #rockvrock, rockvpaper, rockvscissors
                       (1,1,2,),     #papervrock, papervpaper, papervscissors
                       (2,1,1,),)    #scissorsvrock, scissorsvpaper, scissorsvscissors
class victor_results:
    P1 = 1
    P2 = 2

#Source Type
class srctype:
    OPPONENT=0
    PLAYER=1
