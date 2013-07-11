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
import astropy
from astropy import table
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

	## 
	header = hdu[0].header

	### Check if Requested Column Name is actually there
	column_names = hdu[1].columns.names
	requested_cols = args
	data = astropy.table.Table()
	for requested_column in requested_cols:
		try:
			data.add_column(astropy.table.Column(data=hdu[1].data[requested_column], name=requested_column))
		except:
			raise
		## "Clean" data for -999 values, etc.
		if requested_column == "FEH_ADOP" or requested_column == "RV_ADOP" or requested_column == "DIST_ADOP":
			where_bad = np.where((data[requested_column] == -9999.0))
			data[requested_column][where_bad] = np.nan
		
	
	
	return data



def convert_to_cartesian(gal_long, gal_lat, hel_dist):

	import astropy.units as u

	if gal_lat < 0:
		gal_lat = 360 + gal_lat

	if gal_long <0:
		gal_long = 360+gal_long

	if (hasattr(gal_long, 'unit') & hasattr(gal_lat, 'unit') & hasattr(hel_dist, 'unit') ):
		print 'Calculating conversion for:\n\t b {0}\n\t l {1}\n\tDist {2}'.format(gal_long, gal_lat, hel_dist)
	else:
		raise ValueError("At least one input does not have a unit.")

		#convert D to kpc

	hel_dist = hel_dist.to(u.kpc)

		#formulae for conversion
		#x = Dsin(b)cos(l)-8kpc
		#y = Dsin(b)sin(l)
		#z = Dcos(b)


	x = hel_dist * np.sin(gal_long)*np.cos(gal_lat) - 8.*u.kpc
	y = hel_dist * np.sin(gal_long)*np.sin(gal_lat)
	z = hel_dist * np.cos(gal_long)

	return [x,y,z]

