import sys
import os
import getopt
from astropy.io import fits
import numpy as np
import segue
import matplotlib.pyplot as plt

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
	data = segue.get_columns(filename, "FEH_ADOP", "RV_ADOP", "DIST_ADOP")
	print data["FEH_ADOP"]
	
	
	#code for histograms	
	fig, axes = plt.subplots(3,1, sharey = True)

	isnan_rv = np.isnan(data["RV_ADOP"])
	isnan_feh = np.isnan(data["FEH_ADOP"])
	isnan_d = np.isnan(data["DIST"])
	bad_array = (isnan_rv | isnan_feh | isnan_d)
	

	axes[0].hist(data["RV_ADOP"])
	axes[0].set_xlabel('Radial Velocity')


	axes[1].hist(data["FEH_ADOP"])
	axes[1].set_xlabel('[Fe/H]')
	
	axes[2].hist(data["DIST_ADOP"])
	axes[2].set_xlabel('Heliocentric Distance') 
	
	
if __name__ == "__main__":
	sys.exit(main())
	