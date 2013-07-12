import sys
import os
import getopt
import astropy
from astropy import table
from astropy.io import fits
import numpy as np
import math
import astropy.units as u
import astropy.constants as consts
import urllib2
import json
from scipy import interpolate
import segue

class Spectrum(object):
	
	def Spectrum_def(self, spectrum_array):
		mjd, plate, fiber = spectrum_array
		self.url   = "http://api.sdss3.org/spectrum?plate={0}&mjd={1}&fiber={2}&format=json".format(plate, mjd, fiber)
		
		response   = urllib2.urlopen(self.url)
		spectrum   = json.load(response)
		return spectrum

## Abbreviation
S = Spectrum()

## Obtaining data from file
data_spec = segue.get_columns(filename, 'MJD', 'PLATE', 'FIBER')

## Initializing the array for the spectra
Spectra_array = []

### Extracts 10 Spectra
for i in range(0, 10):
    Spectra_array.append( S.Spectrum_def( data_spec[ i ] ) )

### Turning list into an array
Spectra_array = np.array( Spectra_array )

### INTERPOLATION
cubic_func_array = [[] for x in xrange( Spectra_array.size ) ]

### Computes interpolation for the first wavelength
cubic_func_array_0 = interp1d(Spectra_array[0]['wavelengths'], Spectra_array[0]['flux'], kind='linear', bounds_error=False)

### Plotting first spectrum
plot( Spectra_array[0]['wavelengths'], Spectra_array[0]['flux'], 'r--', label='Interpolation_Linear_{0}'.format(0), markersize = 15)

sum_spectra_flux = Spectra_array[0]['flux']


## Calculating interpolation values for each spectrum.
cmap = cm.Accent
for i in range(1, len( Spectra_array) ):
	cubic_func_array[i] = cubic_func_array_0( Spectra_array[i]['wavelengths'] )
	sum_spectra_flux += cubic_func_array[i]
	### Still needed to change colors
	plot( Spectra_array[i]['wavelengths'], cubic_func_array[i], color=cmap(i ), label='Interpolation_Linear_{0}'.format(i), markersize = 15)



### Graph extras
xlabel('Wavelength',fontsize=14)
ylabel('Flux', fontsize=14)
xlim(4000, 5000)
legend()

### Wavelengths are located in: ''Spectra_array[i]['wavelengths']
### Fluxes are located in     : ''Spectra_array[i]['flux']
### Spectro class located in  : ''Spectra_array[i]['spectro_class']

### Plotting the spectra ###
#plot( Spectra_array[0]['wavelengths'], Spectra_array[0]['flux'], marker=None, drawstyle='steps')
#title(Spectra_array[0]['spectro_class'], fontsize=15)
#xlabel('Wavelength',fontsize=14)
#ylabel('Flux', fontsize=14)
#xlim(4000, 5000)