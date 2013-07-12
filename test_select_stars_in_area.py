import sys
import os
import getopt
from astropy.io import fits
import numpy as np
import segue
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.io import ascii
from astropy import coordinates as coord
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
	
	## Read list of clusters
	clusterfile = "../ClassMaterial/data/sdss_clusters.txt"
	clusterdata = ascii.read(clusterfile, delimiter=",", data_start=0, names=["Name", "Width"])

	for cluster in clusterdata:
		coordinates = coord.GalacticCoordinates.from_name(cluster["Name"])
		l = (coordinates.l.degrees+180.)*u.deg ## l returned by GalacticCoordinates.from_name are -180 to 180, so add 180 to get a 0-360 value
		b = coordinates.b.degrees*u.deg
		dl = 5.0*u.deg
		db = 5.0*u.deg
		data = segue.select_stars_in_area(filename, l, b, dl, db, "FEH_ADOP", "RV_ADOP", "DIST_ADOP", "L", "B")
		print cluster["Name"], l, b, len(data)
	
	
if __name__ == "__main__":
	sys.exit(main())
	