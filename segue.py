#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Josh Walawender on 2013-07-10.
Copyright (c) 2013 . All rights reserved.
"""

import sys
import os
import getopt
from astropy.io import fits
import numpy as np


def get_columns(filename, *args):
	"""Gets column data from a SEGUE file"""
	
	## Check File Size
	try:
		filesize_bytes = os.stat(filename).st_size
	except OSError:
		raise OSError("File probably doesn't exist.  Did you put in the correct path?")

	## Open the fits file
	## If file is large, use memmap
	try:
		if filesize_bytes < 2**30:
			hdu = fits.open(filename, memmap=False)
		else:
			hdu = fits.open(filename, memmap=True)
	except IOError:
		raise IOError("Probably not a fits file.  Try again with the correct file.")

	## Extract Data in to Structured Array
	header = hdu[0].header
	data = hdu[1].data
	cols = hdu[1].columns
	cols.info()
	

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
	data = get_columns(filename)



if __name__ == "__main__":
	sys.exit(main())
