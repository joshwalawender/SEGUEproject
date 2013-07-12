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
	fig, axes = plt.subplots(3,1, figsize=(6,8))

	axes[0].tick_params(labelsize=10)

	axes[0].hist(data["RV_ADOP"][np.isfinite(data["RV_ADOP"])], bins=30, label='Radial Velocity')
	axes[0].set_xlabel('Radial Velocity', fontsize=10)
	axes[0].set_ylabel('Number of Stars', fontsize=10)
	axes[0].legend(loc='best', prop={'size':10})
	axes[0].tick_params(labelsize=10)

	axes[1].hist(data["FEH_ADOP"][np.isfinite(data["FEH_ADOP"])], bins=30, label='[Fe/H]')
	axes[1].set_xlabel('[Fe/H]', fontsize=10)
	axes[1].set_ylabel('Number of Stars', fontsize=10)
	axes[1].legend(loc='best', prop={'size':10})
	axes[1].tick_params(labelsize=10)
	
	axes[2].hist(data["DIST_ADOP"][np.isfinite(data["DIST_ADOP"])], bins=30, range=(0,25), label='Heliocentric Distance')
	axes[2].set_xlabel('Heliocentric Distance', fontsize=10) 
	axes[2].set_ylabel('Number of Stars', fontsize=10)
	axes[2].legend(loc='best', prop={'size':10})
	axes[2].tick_params(labelsize=10)
	
	fig.savefig("hist1.png", dpi=100, bbox_inches='tight', pad_inches=0.10)
	
	########
	
	GoodIndicies = np.isfinite(data["DIST_ADOP"])
		
	GalCentricDist = []
	x, y, z = segue.convert_to_cartesian(data["L"][GoodIndicies]*u.deg, data["B"][GoodIndicies]*u.deg, data["DIST_ADOP"][GoodIndicies]*u.kpc)
	GalCentricDist = np.sqrt(x**2 + y**2 + z**2)	
	
	fig2, axes2 = plt.subplots(4,1, figsize=(6,8))
	
	axes2[0].hist(data["RV_ADOP"][np.isfinite(data["RV_ADOP"])], bins=30, label='Radial Velocity')
	axes2[0].set_xlabel('Radial Velocity', fontsize=10)
	axes2[0].set_ylabel('Number of Stars', fontsize=10)
	axes2[0].legend(loc='best', prop={'size':10})
	axes2[0].tick_params(labelsize=10)

	axes2[1].hist(data["FEH_ADOP"][np.isfinite(data["FEH_ADOP"])], bins=30, label='[Fe/H]')
	axes2[1].set_xlabel('[Fe/H]', fontsize=10)
	axes2[1].set_ylabel('Number of Stars', fontsize=10)
	axes2[1].legend(loc='best', prop={'size':10})
	axes2[1].tick_params(labelsize=10)
	
	axes2[2].hist(GalCentricDist, bins=30, range=(0.,15.), label='Galactocentric Distance')
	axes2[2].set_xlabel('Galactocentric Distance', fontsize=10) 
	axes2[2].set_xlim(0,15)
	axes2[2].set_ylabel('Number of Stars', fontsize=10)
	axes2[2].legend(loc='best', prop={'size':10})
	axes2[2].tick_params(labelsize=10)
	
	axes2[3].hist(z, bins=30, range=(0.,15.), label='Height')
	axes2[3].set_xlabel('Height Above Galactic Plane', fontsize=10)
	axes2[3].set_ylabel('Number of Stars', fontsize=10)
	axes2[3].legend(loc='best', prop={'size':10})
	axes2[3].tick_params(labelsize=10)
	
	fig2.savefig("hist2.png", dpi=100, bbox_inches='tight', pad_inches=0.10)
	
	##########
		
	fig3, axes3 = plt.subplots(4,1, figsize=(6,8))
		
	axes3[0].hist(data["RV_ADOP"][(np.isfinite(data["RV_ADOP"])) & (data["FEH_ADOP"] > -1)], color='k', alpha=0.5, label='Radial Velocity (FeH > -1)')
	axes3[0].hist(data["RV_ADOP"][(np.isfinite(data["RV_ADOP"])) & (data["FEH_ADOP"] < -1)], color='r', alpha=0.5, label='Radial Velocity (FeH < -1)')
	axes3[0].set_xlabel('Radial Velocity', fontsize=10)
	axes3[0].legend(loc='best', prop={'size':10})
	axes3[0].tick_params(labelsize=10)

	axes3[1].hist(data["FEH_ADOP"][(np.isfinite(data["FEH_ADOP"])) & (data["FEH_ADOP"] > -1)], color='k', alpha=0.5)
	axes3[1].hist(data["FEH_ADOP"][(np.isfinite(data["FEH_ADOP"])) & (data["FEH_ADOP"] < -1)], color='r', alpha=0.5)
	axes3[1].set_xlabel('[Fe/H]', fontsize=10)
	# axes3[1].legend(loc='best', prop={'size':10})
	axes3[1].tick_params(labelsize=10)
	
	axes3[2].hist(GalCentricDist[(data["FEH_ADOP"][GoodIndicies] > -1)], bins=30, range=(0.,15.), color='k', alpha=0.5, label='Gal. Distance (FeH > -1)')
	axes3[2].hist(GalCentricDist[(data["FEH_ADOP"][GoodIndicies] < -1)], bins=30, range=(0.,15.), color='r', alpha=0.5, label='Gal. Distance (FeH > -1)')
	axes3[2].set_xlabel('Galactocentric Distance', fontsize=10) 
	axes3[2].set_xlim(0,15)
	axes3[2].legend(loc='best', prop={'size':10})
	axes3[2].tick_params(labelsize=10)
	
	axes3[3].hist(z[(data["FEH_ADOP"][GoodIndicies] > -1)], bins=30, range=(0.,15.), color='k', alpha=0.5, label='Height (FeH > -1)')
	axes3[3].hist(z[(data["FEH_ADOP"][GoodIndicies] < -1)], bins=30, range=(0.,15.), color='r', alpha=0.5, label='Height (FeH < -1)')
	axes3[3].set_xlabel('Height Above Galactic Plane', fontsize=10) 
	axes3[3].set_xlim(0,15)
	axes3[3].legend(loc='best', prop={'size':10})
	axes3[3].tick_params(labelsize=10)
	
	fig3.savefig("hist3.png", dpi=100, bbox_inches='tight', pad_inches=0.10)
	
	
	
if __name__ == "__main__":
	sys.exit(main())
	