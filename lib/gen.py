#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
# This houses our generations of iRPS genetic programs.

from agent import agent
from const import *
from util import *

from math import floor

import random, tree

class gen:
    def __init__( self, cfg, num=-1 ):
        #Our individuals
        self.inds = []
        
        self.cfg = cfg

        self.num = num+1
        
        self.mu = int(cfg[GENERATION][MU])
        self.lamb = int(cfg[GENERATION][LAMBDA])
        
        self.strat = cfg[SURVSEL][STRATEGY]
        
        self.survtype = cfg[SURVSEL][TYPE]
        self.survk = int(cfg[SURVSEL][TOURNAMENT_K])
        
        self.method = cfg[INIT][METHOD]
        
        self.partype = cfg[PARSEL][TYPE]
        
        self.mutaterate = float(cfg[MUTATE][MUTATION_RATE])
        
        self.overselnum = float(self.cfg[PARSEL][OVERSEL_PERCENT])*self.mu*-1
        
        self.agent = cfg[AGENT]
        self.main = cfg[MAIN]
        
        #Determine the constant amount to remove each survival selection
        if self.strat == PLUS:
            if self.mu < self.lamb:
                self.survivalamount = 0 #population explodes forever
            else:
                self.survivalamount = self.lamb #typical case
        elif self.strat == COMMA:
            if self.mu <= self.lamb: 
                self.survivalamount = self.lamb - self.mu #typical case
            elif self.mu > self.lamb:
                self.survivalamount = 0 #population dies
        
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
            delprn( str(perStr( i/self.mu )), 3 )
            self.inds.append(agent( self ) )
        
        delprn( "Calc. Inital Fitness\t", 2 )
        #Do our initial run
        for i in range(0,len(self.inds)):
            delprn( str(perStr( i/len(self.inds) )), 3 )
            self.inds[i].fitness( )

    # Select our parents for kids
    #  Only need half as many parents since each pair has two kids!
    def parentSelection( self ):
        pairs = []
        delprn( "Choosing Parents\t\t", 2 )
        
        if self.partype == FITNESS_PROPORTIONAL:
            for i in range(0,floor(self.lamb/2)):
                pairs.append( probSel( self.inds, 2, 0 ) )
                delprn( str(perStr( i/floor(self.lamb/2) )), 3 )
        elif self.partype == OVER_SELECTION:
            sortedinds = sorted(self.inds, key=lambda ind: ind.fit)
            #Choose top c% individuals
            top = sortedinds[self.overselnum:]
            bot = sortedinds[:self.overselnum]
            
            for i in range(0,floor(self.lamb/2)):
                pair = []
                for j in range(0,2):
                    if roll(.8):
                        pair.append(random.sample(top,1)[0])
                    else:
                        pair.append(random.sample(bot,1)[0])
                pairs.append(pair)
                delprn( str(perStr( i/floor(self.lamb/2) )), 3 )
        return pairs
            
    # Breed and mix
    def recombination( self ):
        parents = self.parentSelection( )
        kids = []
        delprn( "Creating Children\t", 2 )
        for i in range(0,len(parents)):
            delprn( str(perStr( i/self.lamb )), 3 )
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
            
            #Mutate them
            kid1.mutate( )
            kid2.mutate( )
            
            #Determine fitness
            kid1.fitness( )
            kid2.fitness( )
            
            kids.append(kid1)
            kids.append(kid2)
            
        #Just implementing plus for now
        for ind in kids:
            self.inds.append( ind ) 
    
    # Survival selection routine.
    def survivalselection( self ):
        delprn( "Survival\t\t", 2 )
            
        if self.survtype == TRUNCATION:
            #NOTE: Sorts from worst to greatest
            sortedinds = sorted(self.inds, key=lambda ind: ind.fit)
            
            #Since we're bringing pop back down to self.mu, do the last mu elements
            #Does both comma and lambda 
            self.inds = sortedinds[self.survivalamount:]
            for ind in sortedinds:
                if ind not in self.inds:
                    ind.delete( )
                
        elif self.survtype == K_TOURNAMENT:
            for i in range(0,self.survivalamount):
                dead = self.tournament( False, self.survk, i, self.lamb )
                self.inds.remove( dead )
                dead.delete( )

    # Creates a random tournament and returns a one indivudal
    #   Disqualified peeps in ineg.
    def tournament( self, pos=True, size=5, curnum=1, totnum=1, ineg=[] ):
        parents = random.sample(self.inds, size)
        once = True
        while once or len(parents) < size:
            parents.extend( random.sample(self.inds, size-len(parents)) )
            for sqr in ineg:
                if sqr in parents:
                    parents.remove( sqr )
            once = False
            
        while len(parents) > 1:
            random.shuffle( parents )
            plist = parents[:]
            delprn(''.join([perStr(((size-len(parents))/size*(1/totnum))+(curnum/totnum))]), 3)
            
            while len(plist) > 1:
                p1 = plist.pop( )
                p2 = plist.pop( )

                if p1.fit > p2.fit:
                    if pos:
                        parents.remove( p2 )
                    else:
                        parents.remove( p1 )
                else:
                    if pos:
                        parents.remove( p1 )
                    else:
                        parents.remove( p2 )
        return parents.pop( )

    def average( self ):
        avg = 0
        
        for ind in self.inds:
            avg += ind.fit
        
        if len(self.inds) == 0:
            return 0
        
        avg /= len(self.inds)
        
        return avg
        
    def best( self ):
        if len(self.inds) > 0:
            sortedinds = sorted(self.inds, key=lambda ind: ind.fit, reverse=True)
            
            best = sortedinds[0]
            i = 1
            next = sortedinds[i]
            while best.fit == next.fit and i < len(sortedinds):
                if next.tree.depth < best.tree.depth:
                    best = next
                i += 1
                next = sortedinds[i]
            
            return best
        return None
    
    def delete( self, save=None ):
        while len(self.inds) > 0:
            next = self.inds.pop( )
            if next == save:
                continue
            next.delete( )