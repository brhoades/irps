#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
#Our miscellaneous functions that don't depend on any specific classes.

import random, datetime, time, configparser, fileinput, argparse, re, sys, math, subprocess, shutil, os, copy
from const import *
from collections import deque

# Warns the user via the command line interface
def warn( text ):
    print( "WARNING:", text )

# Returns the winner of the two in a RPS contest.
#   Turned into a tuple table to save time.
def victor( p1, p2 ):
    res = VICTOR_LOOKUP_TABLE[p1][p2]
    
    if res == victor_results.P1:
        return p1
    return p2

#Load our CSV into memory, parse it into our format, and then return a list
#This CSV takes ages to parse, made it a "static" variable for huge time savings
def loadCSV( fn ):
    if not hasattr( loadCSV, "logar" ):        
        fh = open( fn, 'r' )
        ln = 0
        for line in fh:
            if ln == 0:
                loadCSV.logar = []
                loadCSV.k = int(line)
                #Make us a k*2 dimensional array w/ a single element at the end
                # for b-treeish lookups.
                nlist( loadCSV.logar, int(line)*2, 3, True )
                ln += 1
                continue
            if line == '\n':
                continue
            
            readlst = line.split(',')
            for c in range(0,len(readlst)):
                readlst[c] = int( tauriTran( readlst[c] ) )
            
            #At the values from rl[0] to rl[last-1] set rl[last]
            recurlook( loadCSV.logar, readlst[:-1], readlst[len(readlst)-1] )
        
        loadCSV.data = loadCSV.logar
        
#Does a TRANslation from TAURItz's format
def tauriTran( char ):
    #We're making this static to save time when parsing this massive file
    if not hasattr( tauriTran, "table" ):
        tauriTran.table = [ i for i in range(0,3) ]
        tauriTran.table[moves.PAPER] = "P"
        tauriTran.table[moves.SCISSORS] = "S"
        tauriTran.table[moves.ROCK] = "R"
    
    #We translate both ways, so try...
    try:
        float(char)
    except ValueError:
        return tauriTran.table.index(char.rstrip('\n'))
    else:
        return tauriTran.table[int(char)]
    
#Decide what the CSV tells us to do.
#  This uses a massive n-dimensonal array called csvdata
#  in which we recursively use an array of indicies (mymove / tmove merged)
#  to find the last value, which tells us what the provided AI does.
def CSVAI( tmoves, mymoves ):
    csvdata = loadCSV.data
    
    #Interlace tmoves and mmoves so it looks like Tauritz's thing
    interlacedHist = [ -5 for i in range(0,len(mymoves)*2) ]
    
    histi = 0 
    #P1, O1, P2, O2, ...Pn, On, Outcome
    #my moves, player, go before the opponent's
    for i in range(0,len(mymoves)*2, 2):
        interlacedHist[i] = mymoves[histi]
        histi += 1
    
    histi = 0 
    for i in range(1,len(tmoves)*2, 2):
        interlacedHist[i] = tmoves[histi]
        histi += 1
        
    if len(interlacedHist) != len(tmoves)*2:
        raise TypeError("Math problem in history calculation!")
    
    #Splice this to only have the data that's relevant in our AI's 
    #  data file.
    #FIXME: This is awful
    if len(interlacedHist) > loadCSV.k*2:
        return recurlook( csvdata, interlacedHist[-(loadCSV.k*2):] )

    #Look for our string in csvdata
    return recurlook(csvdata, interlacedHist)

#Recursively pops values off indicies, an array of indicies,
#  for our n-dimensional list, array, and either:
#    * Sets the spot at the last index, in indicies, to set, and 
#        returns that value
#    * Returns the value at that index if set is not defined
def recurlook( array, indicies, set=None ):
    if len(indicies) > 1:
        return recurlook(array[indicies.pop()], indicies, set)
    elif set != None:
        array[indicies.pop()] = set
        return set
    
    #Otherwise we return the value there, since set isn't set
    return array[indicies.pop()]
    
#Create a n-dimensional list that's w wide at each level, must be uniform
#  If trailingnull is set, a -1 will be appended to the last level of the 
#  list.
def nlist( list, n, w=3, trailingNull=False ):
    n -= 1
    
    if n >= 0:
        for i in range(0,w):
            list.append([])
            nlist( list[i], n, w )
    elif trailingNull:
        list.append(-1)
        
    return list
    
#Fitness related

#Find our cumulative fitness. Next compare a random number to all of our generation's fitness.
#We use a sort of inverse fitness function to get the "correct" fitness numbers
def probSel( ogen, num, adj, neg=False, prn=False ):
    gen = []
    cumfit = 0
    for solu in ogen:
        gen.append(solu)
        if not neg:
            cumfit += solu.fit+1
        else:
            cumfit += adj-solu.fit+1
        
    rets = []
    while len(rets) < num:
        if prn:
            delprn(''.join(perStr(len(rets)/num)), 3)
        pnt = random.random( )*cumfit
        
        tfit = 0
        for solu in gen:
            if pnt < tfit:
                gen.remove(solu)
                rets.append(solu)
                if not neg:
                    cumfit -= solu.fit+1
                else:
                    cumfit -= adj-solu.fit+1
                break
            if not neg:
                tfit += solu.fit+1
            else:
                tfit -= adj-solu.fit+1
        else:
            rets.append(solu)
            gen.remove(solu)
            if not neg:
                cumfit -= solu.fit+1
            else:
                cumfit -= adj-solu.fit+1
    return rets
  
######################################
# RNG-related functions
######################################

# Generates a seed for the rng.
def seed( ):
    dt = datetime.datetime.now( )
    return time.mktime(dt.timetuple())+float("0.%s"%dt.microsecond)

# "Roll" a 100 sided die and compares it to chance%.
def roll( chance ):
    if( random.random( ) < chance ):
        return True
        
    return False
# "Flip" a coin uniformly. Since Python's random is uniform this works.
def flip( ):
    prob = random.random( )
    return prob >= 0.5 #in [0,1), so >=

######################################
# Config-parsing functions
######################################
# Reads in a config from a file handle and returns a dictionary.
def readConfig( fn ):
    config = configparser.ConfigParser()
    config.read(fn)
    return config._sections

# Called before readConfig to parse command line options or return the default.
def gcfg( ):
    parser = argparse.ArgumentParser(description='CS348 FS2013 Assignment 2c')
    parser.add_argument('-c', type=str,
                        help='Specifies a configuration file (default: cfg/default.cfg)',
    default="cfg/default.cfg")
    
    args = parser.parse_args()
    return args.c
                
#####
#UI Functions
#####
# Backspaces over previous stuff and padds the end of our line to cover it up
def delprn( new, level=2, overwrite=True ):
    if not hasattr(delprn, "old"):
         delprn.old = []
         for i in range(0,5):
            delprn.old.append("")
    if new == delprn.old[level]:
        return
        
    cnt = 0
    for i in range(level, len(delprn.old)):
        cnt += len(delprn.old[i])
        delprn.old[i] = ""
    print('\r', end='')
    sys.stdout.write("\033[K")
    for i in range(0, level):
        print(delprn.old[i], end='')
    print(new, end='')
    sys.stdout.flush( )
    delprn.old[level] = new
    
# Rounds a number off and gives a string
def perStr( dec, ceil=True, round=True ):
    rnd = 100
    if not round:
        rnd = 1
    if ceil:
        return str(math.ceil(dec*rnd))
    else:
        return str(math.floor(dec*rnd))

# Renders a header depending on options
def renderHead( cfg ):
    print(''.join(["Run #/",cfg[MAIN][RUNS]]), end='')
    if int(cfg[MAIN][RUNS]) < 100:
        print('\t', end='') 
    print(''.join(["Run %", "\t"]), end='')
    
    if cfg[TERMINATE][TYPE] == NUM_OF_FITEVALS:
        print(''.join(["Fit #/", cfg[TERMINATE][FITEVALS], "\t" "Fit %", "\t"]), end='')
    else:
        print('Fit #\t', end='')
    
    print("Avg Fit\tBest Fit\tStatus\t\t\tPercent")
    
def pad(num, pad):
    if pad == '0':
        return str(num)
    inum = str(num)
    return inum.rjust(math.floor(math.log(int(pad), 10)+1), '0')

#Prints our basic string out on the screen
def prnBase( cfg, runn, generation ):
    evals="~"
    avg="~"
    best="~"
    if len(generation.inds) > 0:
        avg = round( generation.average( ), 4 )
        evals = generation.fitevals
        best = round( generation.best( ).fit, 4 )
    out = ""
    out += str(runn+1)
    if int(cfg[MAIN][RUNS]) >= 10:
        out += "\t"
    out += "\t"
    out += perStr( runn/int(cfg[MAIN][RUNS]) )
    out += "\t"
    out += pad(generation.fitevals, cfg[TERMINATE][FITEVALS])
    out += "\t"
    if cfg[TERMINATE][TYPE] == NUM_OF_FITEVALS:
        if math.log(int(cfg[TERMINATE][FITEVALS]), 10) >= 2:
            out += "\t"
        out += perStr( generation.fitevals/int(cfg[TERMINATE][FITEVALS]) )
        out += "\t"
    out += str(avg)
    out += "\t"
    out += str(best)
    out += "\t\t"
    
    delprn(out, 1)
    
