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


help_message = '''
The help message goes here.
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def get_columns(filename, *args):
	## Check File Size
	try:
		filesize_bytes = os.stat(filename).st_size
	except OSError:
		raise OSError("File probably doesn't exist.  Did you put in the correct path?")

	## Open the fits file
	try:
		if filesize_bytes < 2**30:
			hdu = fits.open(filename, memmap=False)
		else:
			hdu = fits.open(filename, memmap=True)
	except IOError:
		raise IOError("Probably not a fits file.  Try again with the correct file.")


def main(argv=None):
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

	## Main Program Stats Here
	data = get_columns(filename)



if __name__ == "__main__":
	sys.exit(main())
