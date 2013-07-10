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
	data   = hdu[1].data
	cols   = hdu[1].columns
#	cols.info()


	### CREATES DICTIONARY THAT CONTAINS THE NAMES OF THE COLUMNS ON THE FITS FILE
	NAMES_DICTIONARY = {}
	##     EXTRACTING COLUMNS' NAMES
	COLUMNS_NAMES     = filename[1].columns.names

	for ii in range(0, len( COLUMNS_NAMES ) ):
		''' The key is the name of the column, while the value is the index of that column in the 'COLUMNS_NAMES' array '''
		NAMES_DICTIONARY[COLUMNS_NAMES[ii] ] = ii


	

