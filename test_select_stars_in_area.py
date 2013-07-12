import sys
import os
import getopt
from astropy.io import fits
import numpy as np
import segue
import matplotlib.pyplot as plt
import astropy.units as u
import math

def main(argv=None):
	filename = None
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hi:v", ["help", "input="])
		except getopt.error, msg:
			raise Usage(msg)
	
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-i", "--input"):
				filename = value
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2

	## If no -i input set use the first argument as the fits filename
	if not filename and len(args)>0:
		filename = args[0]
	else:
		print "Bad things happened"
		sys.exit(1)  ## this should be improved
	
	
	## Main Program Starts Here
	l = 237.*u.deg
	b = 37.*u.deg
	dl = 3.*u.deg
	db = 3.*u.deg
	data = segue.select_stars_in_area(filename, l, b, dl, db, "FEH_ADOP", "RV_ADOP", "DIST_ADOP", "L", "B")
	print len(data)
	print data
	
	
if __name__ == "__main__":
	sys.exit(main())
	