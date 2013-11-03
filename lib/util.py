#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2a
#Our miscellaneous functions that don't depend on any specific classes.

import random, datetime, time, configparser, fileinput, argparse, re, sys, math, subprocess, shutil, os, copy
from const import *

# Returns the winner of the two in a RPS contest
def victor( m1, m2 ):
    #Need to do this due to some type issues with reading the CSV
    m1 = int(m1)
    m2 = int(m2)
    
    if m1 == m2:
        return m1
    
    if m1 == moves.ROCK and m2 == moves.PAPER:
        return m2
    if m1 == moves.ROCK and m2 == moves.SCISSORS:
        return m1
    
    if m1 == moves.PAPER and m2 == moves.ROCK:
        return m1
    if m1 == moves.PAPER and m2 == moves.SCISSORS:
        return m2
    
    if m1 == moves.SCISSORS and m2 == moves.PAPER:
        return m1
    if m1 == moves.SCISSORS and m2 == moves.ROCK:
        return m2
     
    raise TypeError( "Somehow I missed a combination.", tauriTran( m1 ), tauriTran( m2 ) )

#Load our CSV into memory, parse it into our format, and then return a list
#This CSV takes ages to parse, made it a "static" variable for huge time savings
def loadCSV( fn ):
    if not hasattr( loadCSV, "logar" ):        
        fh = open( fn, 'r' )
        ln = 0
        for line in fh:
            if ln == 0:
                loadCSV.logar = []
                #Make us a k*2 dimensional array w/ a single element at the end
                # for b-treeish lookups.
                nlist( loadCSV.logar, int(line)*2, 3, True )
                ln += 1
                continue
            if line == '\n':
                continue
            
            rl = line.split(',')
            for c in range(0,len(rl)):
                rl[c] = int( tauriTran( rl[c] ) )
            
            #At the values from rl[0] to rl[last-1] set rl[last]
            recurlook( loadCSV.logar, rl[:-1], rl[len(rl)-1] )

    return loadCSV.logar
        
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
    

#Decide what the csv tells us to do
def csvop( csvdata, tmov, mmove ):
    ##################interlace tmov and mmov so it looks like Tauritz's thing
    hist = [ -5 for i in range(0,len(mmove)*2) ]
    
    hi = 0 
    #P1, O1, P2, O2, ...Pn, On, Outcome
    #my moves, player, go before the opponent's
    for i in range(0,len(mmove)*2, 2):
        hist[i] = mmove[hi]
        hi += 1
    
    hi = 0
    for i in range(1,len(tmov)*2, 2):
        hist[i] = tmov[hi]
        hi += 1
        
    if len(hist) != len(tmov)*2:
        raise TypeError("Math problem in history calculation!")
    
    #splice this to only have the data that's relevant in st
    hist[(len(csvdata[0])-1):]
    
    #Look for our string in csvdata
    return recurlook(csvdata, hist)

#Recursively pops values off lv and looks at that spot in l.
#  If set != None, it sets that index to set.
def recurlook( l, lv, st=None ):
    if len(lv) > 1:
        return recurlook(l[lv.pop()], lv, st)
    elif st != None:
        l[lv.pop()] = st
        return st
    
    return l[lv.pop()]
    
#Create a n-dimensional list that's x wide
#  endel adds a value onto the end automatically
def nlist( l, n, x=3, endel=False ):
    n -= 1
    if n >= 0:
        for i in range(0,x):
            l.append([])
            nlist( l[i], n, x )
    elif endel:
        l.append(-1)
        
    return l
    
######################################
# RNG-related functions
######################################

# Generates a seed for the rng.
def seed( ):
    dt = datetime.datetime.now( )
    return time.mktime(dt.timetuple())+float("0.%s"%dt.microsecond)

# "Roll" a 100 sided die and compares it to chance%.
def roll( chance ):
    if( random.uniform(0, 100) <= chance*100 ):
        return True
        
    return False
# "Flip" a coin uniformly. Since Python's random is uniform this works.
def flip( ):
    prob = random.uniform(0, 1)
    return prob >= 0.5 #in [a,b], b is often not included due to floating point rounding, so >=

# Returns a chance between 1 - 1M
def chance( ):
    return random.randint( 1, 1000000 )

######################################
# Config-parsing functions / logging functions
######################################
# Reads in a config from a file handle and returns a dictionary.
def readConfig( fn ):
    config = configparser.ConfigParser()
    config.read(fn)
    return config._sections

# Called before readConfig to parse command line options or return the default.
def gcfg( ):
    parser = argparse.ArgumentParser(description='CS348 FS2013 Assignment 2')
    parser.add_argument('-c', type=str,
                        help='Specifies a configuration file (default: cfg/default.cfg)',
    default="cfg/default.cfg")
    
    args = parser.parse_args()
    return args.c

class log:        
    def __init__( self, fcfg, gseed, cfgf):
        cfg = fcfg[LOG]
        self.cfgf = cfgf
        self.rfn = cfg[RESULT_LOG_FILE].rsplit('/')
        self.sfn = cfg[SOLUTION_LOG_FILE].rsplit('/')
        
        self.processDirs( )
                
        self.fullRes = self.rfn
        self.fullSol = self.sfn
        
        print("Writing to:", self.rfn, "and", self.sfn, "you have 3 seconds to cancel.")
        time.sleep(3)
        
        self.res = open( self.rfn, 'w' )
        self.sol = open( self.sfn, 'w' )
        res = self.res
        sol = self.sol
        
        res.write( ''.join(["Result Log\n", "Config File: ", cfgf, "\n"]) )
        res.write( ''.join(['Seed: ', str(gseed), '\n' ]) )
        
        #Fancy git output
        if cfg[GIT_LOG_HEADERS] != '0':
            output = subprocess.check_output("git log -n1 --pretty=\"Git Hash: %H\n  Commit Date: %ad (%ar)\n  Author: %an <%ae>\n  Change Message: %s\"", shell=True)
            output = str( output )
            output = re.sub( r'\\n', '\n', output )
            output = re.sub( r'(b\'|\'$)', '', output )
            self.res.write( output )
            
        self.cfgStr( fcfg[MAIN], "Main Parameters:" )        
        self.cfgStr( fcfg[AGENT], "Agent Parameters:" )      
        self.cfgStr( fcfg[INIT], "Initialization Parameters:" )      
        
    # Flushes our logs to a file
    def flush( self ):
        self.sol.flush( )
        self.res.flush( )
                
    # Outputs our serialized best to a fileinput
    def best( self, best ):
        self.sol.write( best.serialize( ) )
                
    # Prints parameters for a long config sequence, beautifully
    def cfgStr( self, cfg, title, skip=[] ):
        params = ''
        params += title
        for param in cfg:
            if param in skip:
                next
            params += ''.join(["\n  ", param, ": ", cfg[param]])
        params += '\n'
        self.res.write( params )

    # Seperates our result log file with pretty run numbers.
    def sep( self, run ):
        self.res.write( ''.join( [ "\n", "Run ", str(run+1), "\n" ] ) )
        self.res.flush( )
    
    def entry( self, evals, nbest ):
        self.res.write( ''.join( [ str(evals), "\t", str(nbest.fit), "\n" ] ) )
    
    # Our generational best
    def spacer( self ):
        self.res.write( "=SPACER=\n" )
        
    # Do our initial variable sub
    def processDirs( self ):
        for i in range(len(self.rfn)):
            self.rfn[i] = self.variableHand( self.rfn[i] )
        for i in range(len(self.sfn)):
            self.sfn[i] = self.variableHand( self.sfn[i] )
            
        self.createDirectories( self.rfn )
        self.createDirectories( self.sfn )
        
        self.rfn = '/'.join(self.rfn)
        self.sfn = '/'.join(self.sfn)    
        
    # Move any files with new names, organize everything properly
    def wrapUp( self, best ):
        self.res.close( )
        self.sol.close( )
        
        oldrfn = self.rfn
        oldsfn = self.sfn
        
        newrfn = self.variableHand( oldrfn, best )
        newsfn = self.variableHand( oldsfn, best )

        if newrfn != oldrfn:
            shutil.move( os.path.abspath(self.rfn), os.path.abspath(newrfn) )
            
        if newsfn != oldsfn:
            shutil.move( os.path.abspath(self.sfn), os.path.abspath(newsfn) )
            
    # Translate some variables over to something useful
    def variableHand( self, dir, best=None ):
        com = str(subprocess.check_output("git rev-parse --short HEAD", shell=True))
        com = re.sub( r'(b\'|\'$|\?|\\n)', '', com)
        dir = re.sub( r'\%cm', com, dir )
        #ccfg = re.sub( r'\.cfg', '', self.cfgf )
        #ccfg = re.sub( r'cfg\\', '', ccfg )
        #dir = re.sub( r'\%cfg', ccfg, dir )
        if best != None:
            dir = re.sub(r'\%bf', str(round(best.fit,3)), dir )
        return dir
    
    # Create directories and do substutitions on variabes (currently only %c)
    def createDirectories( self, infn ):
        if len(infn) < 2:
            return
        
        fn = infn[0:len(infn)-1]
        for i in range(len(fn)):
            me = ""
            for pd in range(0,i):
                me += me.join([fn[pd], "/"])
            me += fn[i]
            
            d = os.path.abspath(me)
            if not os.path.exists(d):
                os.makedirs(d)   
                
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

# Mutates a square if this returns >= 1  
def mutateSq( mu, sigma ):
    return( math.floor( math.fabs( random.gauss( mu, sigma ) ) ) )

# Renders a header depending on options
def renderHead( cfg ):
    print(''.join(["Run #/",cfg[MAIN][RUNS]]), end='')
    if int(cfg[MAIN][RUNS]) < 100:
        print('\t', end='') 
    print(''.join(["Run %", "\t"]), end='')
    
    print(''.join(["Fit #/", cfg[MAIN][FITEVALS], "\t" "Fit %", "\t"]), end='')
    
    print("Avg Fit\tBest Fit\tStatus" )
    
def pad(num, pad):
    if pad == '0':
        return str(num)
    inum = str(num)
    return inum.rjust(math.floor(math.log(int(pad), 10)+1), '0')

#Prints our basic string out on the screen
def prnBase( cfg, runn, fitevals, avgfit, bestfit, status ):
    evals="~"
    avg="~"
    best="~"
    if runn != -1:
        avg = round( avgfit, 4 )
        evals = fitevals
        best = round( bestfit, 4 )
    out = ""
    out += str(runn+1)
    if int(cfg[MAIN][RUNS]) >= 10:
        out += "\t"
    out += "\t"
    out += perStr( runn/int(cfg[MAIN][RUNS]) )
    out += "\t"
    out += pad(fitevals, cfg[MAIN][FITEVALS])
    out += "\t"
    if math.log(int(cfg[MAIN][FITEVALS]), 10) >= 2:
        out += "\t"
    out += perStr( fitevals/int(cfg[MAIN][FITEVALS]) )
    out += "\t"
    out += str(avg)
    out += "\t"
    out += str(best)
    out += "\t\t"
    out += status
    
    delprn(out, 0)
    
