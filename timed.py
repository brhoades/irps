#!/usr/bin/env python
#Author: Billy J Rhoades <bjrq48@mst.edu>
#Class: CS348 Assignment 2c
#Test Unit Functions
#  This program is called to compare speeds quickly.

import os, unittest, io, cProfile, timeit, time, datetime, sys, pstats
import main

pr = cProfile.Profile()
pr.enable()
main.main( )
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
