import sys
import os
import getopt
import numpy as np
import segue
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

import pdb


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
		sys.exit(1)  ## this should be improved
	
	
	## Main Program Stats Here
	data = segue.get_columns(filename, "RV_ADOP", "L", "B")
	#get rid of any bad values in L and B and cut the radial velocity plot
	
	
	el = np.array(data["L"][(np.isfinite(data["L"])) & (np.isfinite(data["B"])) & (np.isfinite(data["RV_ADOP"]))])
	be = np.array(data["B"][(np.isfinite(data["L"])) & (np.isfinite(data["B"])) & (np.isfinite(data["RV_ADOP"]))])
	radvel = np.array(data["RV_ADOP"][(np.isfinite(data["L"])) & (np.isfinite(data["B"])) & (np.isfinite(data["RV_ADOP"]))])
	
	print len(el), len(be), len(radvel)
	el_radians = np.radians(el - 180)
	be_radians = np.radians(be)
	
	plt.subplot(111, projection="hammer")


	
	plt.scatter(el_radians, be_radians, s=5, c=radvel, marker = 'o', cmap=cm.jet, norm = colors.normalize(vmin=-50, vmax=50, clip=True), alpha=0.4)
	plt.colorbar()
	
	plt.savefig('all_sky_rotation.png')
	plt.show()

	
if __name__ == "__main__":
	sys.exit(main())
