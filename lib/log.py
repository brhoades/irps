#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
#Logging class and functions

from util import *
from gen import gen
from agent import agent

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
        self.cfgStr( fcfg[GENERATION], "Generation Parameters:" )
        self.cfgStr( fcfg[INIT], "Initialization Parameters:" )
        self.cfgStr( fcfg[PARSEL], "Parent Selection Parameters:" )
        self.cfgStr( fcfg[MUTATE], "Mutation Parameters:" )
        self.cfgStr( fcfg[SURVSEL], "Survival Selection Parameters:" )
        self.cfgStr( fcfg[TERMINATE], "Termination Parameters:" )

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

    def entry( self, gen ):
        self.res.write( ''.join( [ str(gen.fitevals), "\t", str(gen.average( )), "\t", str(gen.best( ).fit), "\n" ] ) )

    # Print our absolute fitness for our bests
    # basically reverse engineering fitness + logging + run
    def spacer( self, best ):
        fits = []
        regfit = best.fit

        self.res.write( "=SPACER=\n" )

    # Print out stuff about our local best's absolute fitness.
    def bestFinish( self, best ):
        self.res.write( "\nAbsolute Fitness\n" )

        regfit = best.fit
        fits = []

        for i in range(0,2):
            tmoves = deque( [random.randint(moves.MINMOVE, moves.MAXMOVE) for i in range(best.mem)], best.mem )
            beforepayoff = best.mem * 2
            best.fit = 0
            best.payoffs = []
            for j in range(0, best.gen.seqs):
                ores = -2
                if i == 0:
                    ores = victor( tmoves[0], best.mymoves[0] )
                else:
                    ores = CSVAI( tmoves, best.mymoves )

                tmoves.appendleft( ores )
                myres = best.run( tmoves )

                if j > beforepayoff:
                    best.upres( myres, ores )

            sum = 0
            for pay in best.payoffs:
                sum += pay
            sum /= len(best.payoffs)

            fits.append( sum )
        best.fit = regfit

        self.res.write( str(fits[0]) + "\n" + str(fits[1]) + "\n" )

    # Print out stuff about our global best's absolute fitness
    def absBestFinish( self, cfg, best ):
        self.res.write( "\n Tree with the Global Best Fitness\n" )

        #Mock container generation
        generation = gen( cfg )

        #Avoiding errors
        best.gen = generation

        self.bestFinish( best )

        self.res.write( "\nRandom GP Performance\n" )

        #Clear old payoffs
        best.payoffs = []

        #Randomly make many individuals to face.
        for i in range(30):
            generation.inds.append( agent( generation ) )

        for opp in generation.inds:
            beforepayoff = best.mem*2
            for j in range(0,generation.seqs):
                tmoves = opp.mymoves
                oppres = opp.run( best.mymoves )
                myres = best.run( opp.mymoves )

                if j > beforepayoff:
                    best.upres( myres, oppres )
                    opp.upres( oppres, myres )

        avg = 0
        for i in best.payoffs:
            avg += i
        avg /= len(best.payoffs)
        self.res.write( "Average 30 GP Performance: " )
        self.res.write( str(avg) )

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

        if best != None:
            dir = re.sub(r'\%bf', str(round(best.fit,3)), dir )
        return dir

    # Create directories and do substutitions on variables (currently only %c)
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