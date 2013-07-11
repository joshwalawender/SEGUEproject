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
	data = segue.get_columns(filename, "FEH_ADOP", "RV_ADOP", "DIST_ADOP", "L", "B")
	
	
	#code for histograms	
	fig, axes = plt.subplots(3,1, sharey = True)

	

	axes[0].hist(data["RV_ADOP"][np.isfinite(data["RV_ADOP"])])
	axes[0].set_xlabel('Radial Velocity')


	axes[1].hist(data["FEH_ADOP"][np.isfinite(data["FEH_ADOP"])])
	axes[1].set_xlabel('[Fe/H]')
	
	axes[2].hist(data["DIST_ADOP"][np.isfinite(data["DIST_ADOP"])])
	axes[2].set_xlabel('Heliocentric Distance') 
	
	fig.savefig("hist1.png")
	
	########
	
	GoodIndicies = np.isfinite(data["DIST_ADOP"])
		
	GalCentricDist = []
	for index in GoodIndicies:
		xyz = segue.convert_to_cartesian(data["L"][index]*u.deg, data["B"][index]*u.deg, data["DIST_ADOP"][index]*u.kpc)
		GCD = math.sqrt(xyz[0].value**2 + xyz[1].value**2 + xyz[2].value**2)
		GalCentricDist.append(GCD)
	# for index in GoodIndicies:
	# 	stuff = segue.convert_to_cartesian(data["L"][index]*u.deg, data["B"][index]*u.deg, data["DIST_ADOP"][index]*u.kpc)
	# 	GCD = math.sqrt(stuff[0].value**2 + stuff[1].value**2 + stuff[2].value**2)
	# 	GalCentricDist.append(GCD)
	
	
	fig2, axes2 = plt.subplots(3,1, sharey = False)
	
	axes2[0].hist(data["RV_ADOP"][np.isfinite(data["RV_ADOP"])])
	axes2[0].set_xlabel('Radial Velocity')

	axes2[1].hist(data["FEH_ADOP"][np.isfinite(data["FEH_ADOP"])])
	axes2[1].set_xlabel('[Fe/H]')
	
	axes2[2].hist(GalCentricDist, bins=25, range=(0.,25.))
	axes2[2].set_xlabel('Galactocentric Distance') 
	axes2[2].set_xlim(0,25)
	
	print len(GalCentricDist)
	
	fig2.savefig("hist2.png")
	
	
if __name__ == "__main__":
	sys.exit(main())
	