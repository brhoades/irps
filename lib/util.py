import random, datetime, time, configparser, fileinput, argparse, re, sys, math, subprocess, shutil, os

######################################
# RNG-related functions
######################################

# Generates a random (!= 0) id for a graph.
def id( ):
    start = seed( )
    start *= 1+random.random( )
    return start

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
                        help='Specifies a configuration file (default: cfgs/default.cfg)',
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
        
        self.res = open( self.rfn, 'w' )
        self.sol = open( self.sfn, 'w' )
        res = self.res
        sol = self.sol
        
        res.write( ''.join(["Result Log\n", "Config File: ", cfgf, "\n"]) )
        if( fcfg[GRAPH][GENERATE] != 'True' ):
            res.write( ''.join(["Puzzle File: ", fcfg[GRAPH][GENERATE], "\n" ]) )
        else:
            res.write( ''.join(["Randomly Generating Graph(s)\n"]) )
            
        res.write( ''.join(['Seed: ', str(gseed), '\n' ]) )
        
        #Fancy git output
        if cfg[GIT_LOG_HEADERS] != '0':
            output = subprocess.check_output("git log -n1 --pretty=\"Git Hash: %H\n  Commit Date: %ad (%ar)\n  Author: %an <%ae>\n  Change Message: %s\"", shell=True)
            output = str( output )
            output = re.sub( r'\\n', '\n', output )
            output = re.sub( r'(b\'|\'$)', '', output )
            self.res.write( output )
        
        #Map generation parameters
        if fcfg[GRAPH][GENERATE] == 'True':
            self.cfgStr( fcfg[GRAPH], "Map generation parameters:", [GRAPH] )
            
        self.cfgStr( fcfg[POP], "Population Parameters:" )        

        
    # Flushes our logs to a file
    def flush( self ):
        self.sol.flush( )
        self.res.flush( )
                
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
        self.res.flush( )
        self.res.write( ''.join( [ "\n", "Run ", str(run+1), "\n" ] ) )
    
    # Our generational best
    def spacer( self ):
        self.res.write( "=SPACER=\n\n" )
        
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
        #dir = re.sub( r'\%cfg', ccfg, dir )
        if best != None:
            dir = re.sub(r'\%bf', str(round(best.fitTable.data[0][0].oldFitness(),3)), dir )
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