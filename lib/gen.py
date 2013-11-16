#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2b
# This houses our generations of iRPS genetic programs.

from agent import agent
from const import *
from util import *

import random, tree

class gen:
    def __init__( self, cfg ):
        #Our individuals
        self.inds = []
        
        self.cfg = cfg
        
        self.mu = int(cfg[GENERATION][MU])
        self.lamb = int(cfg[GENERATION][LAMBDA])
        
        self.survtype = cfg[SURVSEL][TYPE]
        self.survk = cfg[SURVSEL][TOURNAMENT_K]
        
        self.method = cfg[INIT][METHOD]
        
        self.partype = cfg[PARSEL][TYPE]
        
        self.agent = cfg[AGENT]
        self.main = cfg[MAIN]
        
        #Our internal counter for fitness evaluations
        self.fitevals = 0
        
        ################### Process stupid table ###################
        tpv = cfg[AGENT][PAYOFF].split(',')
        #Pay OFF TABLE
        self.pofftable = [[] for i in range(moves.MINMOVE,moves.MAXMOVE+1)]
        for i in range(0,len(tpv)):
            tpv[i] = float(tpv[i])
        #opponentplayer => res value
        #rr,rp,rs,pr,pp,ps,sr,sp,ss
        self.pofftable[moves.ROCK].append(tpv[0])
        self.pofftable[moves.ROCK].append(tpv[1])
        self.pofftable[moves.ROCK].append(tpv[2])

        self.pofftable[moves.PAPER].append(tpv[3])
        self.pofftable[moves.PAPER].append(tpv[4])
        self.pofftable[moves.PAPER].append(tpv[5])
        
        self.pofftable[moves.SCISSORS].append(tpv[6])
        self.pofftable[moves.SCISSORS].append(tpv[7])
        self.pofftable[moves.SCISSORS].append(tpv[8])
        ###################DONE WITH STUPID TABLE###################
        
        #number of sequences for a fitness evaluation
        self.seqs = int(cfg[MAIN][SEQRUNS])
        if self.seqs < 3*int(cfg[AGENT][MEM]):
            self.seqs = 3*int(cfg[AGENT][MEM])
        
    # Set up our inital population
    def initialize( self ):
        self.inds = []

        delprn( "Creating Trees\t\t", 2 )
        #Set up random trees
        for i in range(0,self.mu):
            delprn( ''.join([str(perStr( i/self.mu )), "%"]), 3 )
            self.inds.append(agent( self ) )
        
        delprn( "Calc. Inital Fitness\t", 2 )
        #Do our initial run
        for i in range(0,len(self.inds)):
            delprn( ''.join([str(perStr( i/len(self.inds) )), "%"]), 3 )
            self.inds[i].fitness( )

    # Select our parents for kids
    def parentSelection( self ):
        pairs = []
        delprn( "Choosing Parents\t\t", 2 )
        
        if self.partype == FITNESS_PROPORTIONAL:
            for i in range(0,self.lamb):
                pairs.append( probSel( self.inds, 0, 2 ) )
                delprn( ''.join([str(perStr( i/self.lamb )), "%"]), 3 )
        elif self.partype == OVER_SELECTION:
            sortedinds = sorted(self.inds, key=lambda ind: ind.fit)
            #always choose top 320 individuals according to book
            top = sortedinds[:320]
            bot = sortedinds[320:]
            
            for i in range(0,self.lamb):
                pair = []
                for j in range(0,2):
                    if roll(.8):
                        pair.append(random.sample(top,1)[0])
                    else:
                        pair.append(random.sample(bot,1)[0])
                pairs.append(pair)
                delprn( ''.join([str(perStr( i/self.lamb )), "%"]), 3 )
        return pairs
            
    # Breed and mix
    def recombination( self ):
        parents = self.parentSelection( )
        kids = []
        delprn( "Makin' Babbies\t\t", 2 )
        for i in range(0,len(parents)):
            delprn( ''.join([str(perStr( i/self.lamb )), "%"]), 3 )
            pair = parents[i]
            p1 = pair[0]
            p2 = pair[1]
            #We're just doing cross over for now, so hardcode this in:
            
            #Create two kids, one from each parent
            kid1 = agent( self, copy=p1 )
            kid2 = agent( self, copy=p2 )
            
            #And sample for a random crossover point from both kids
            kid1pt = random.sample(kid1.tree.nodes, 1)[0]
            kid2pt = random.sample(kid2.tree.nodes, 1)[0]
            
            #Now swap subtrees
            tree.swapsubtree( kid1.tree, kid1pt, kid2.tree, kid2pt )
            
            #Determine fitness
            kid1.fitness( )
            kid2.fitness( )
            
            kids.append(kid1)
            kids.append(kid2)
            
        #Just implementing plus for now
        for ind in kids:
            self.inds.append( ind ) 
            


    def average( self ):
        avg = 0
        
        for ind in self.inds:
            avg += ind.fit
        
        if len(self.inds) == 0:
            return 0
        
        avg /= len(self.inds)
        
        return avg
        
    def best( self ):
        best = 0
        
        for ind in self.inds:
            if ind.fit > best:
                best = ind.fit
        
        return best