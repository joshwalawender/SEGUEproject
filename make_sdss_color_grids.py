import segue
import matplotlib as plt
import numpy as np

def make_sdss_color_grids(filename,l, b, delta_l, delta_b):
	wanted_columns = ["U","G","R","I","Z"]
	photometry = segue.select_stars_in_area(filename,l,b,delta_l,delta_b,wanted_columns)

	good_data = np.isfinite(photometry["U"]) & np.isfinite(photometry["G"]) &
				np.isfinite(photometry["R"]) & np.isfinite(photometry["I"]) &
				np.isfinite(photometry["Z"]) 


	u = photometry["U"][good_data]
	g = photometry["G"][good_data]
	r = photometry["R"][good_data]
	i = photometry["I"][good_data]
	z = photometry["Z"][good_data]


	#Here are the projection plots
	fig,axes = plt.subplots(2,2)
	axes[0,0].plot(u-g,g-r,marker='o',linestyle='')
	axes[0,0].set_xlabel('u-g')
	axes[0,0].set_xlabel('g-r')

	axes[0,1].plot(g-r,r-i,marker='o',linestyle='')
	axes[0,1].set_xlabel('g-r')
	axes[0,1].set_xlabel('r-i')

	axes[1,0].plot(r-i,i-z,marker='o',linestyle='')
	axes[1,0].set_xlabel('r-i')
	axes[1,0].set_xlabel('i-z')

	axes[1,1].plot(u-g,r-i,marker='o',linestyle='')
	axes[1,1].set_xlabel('u-g')
	axes[1,1].set_xlabel('r-i')
	
	plt.savefig('scatter_sdss_photometry.png')


	#Here are the contour plots
	#Step 1: use np.histogram2d to create "density" plots of the points
	H1, xedges1, yedges1 = np.histogram2d((u-g), (g-r))
	H2, xedges2, yedges2 = np.histogram2d((g-r),(r-i))
	H3, xedges3, yedges3 = np.histogram2d((r-i),(i-z))
	H4, xedges4, yedges4 = np.histogram2d((u-g),(r-i))
	
	fig,axes = plt.subplots(2,2)
	extent1 =  [yedges1[0], yedges1[-1], xedges1[0], xedges1[-1]]
	#This draws contours around the density
	cset = axes[0,0].contour(H1,colors=['black','green','blue','red'],
			linewidths=(1.9, 1.6, 1.5, 1.4),extent=extent1)
	#Label the contours!
	axes[0,0].clabel(cset, inline=1, fontsize=10, fmt=’%1.1f’)
	axes[0,0].set_xlabel('u-g')
	axes[0,0].set_xlabel('g-r')

	extent2 =  [yedges2[0], yedges2[-1], xedges2[0], xedges2[-1]]
	cset = axes[0,1].contour(H2,colors=['black','green','blue','red'],
			linewidths=(1.9, 1.6, 1.5, 1.4),extent=extent2)
	axes[0,1].clabel(cset, inline=1, fontsize=10, fmt=’%1.1f’)
	axes[0,1].set_xlabel('g-r')
	axes[0,1].set_xlabel('r-i')

	extent3 =  [yedges3[0], yedges3[-1], xedges3[0], xedges3[-1]]
	cset = axes[1,0].contour(H3,colors=['black','green','blue','red'],
			linewidths=(1.9, 1.6, 1.5, 1.4),extent=extent3)
	axes[1,0].clabel(cset, inline=1, fontsize=10, fmt=’%1.1f’)
	axes[1,0].set_xlabel('r-i')
	axes[1,0].set_xlabel('i-z')

	extent4 =  [yedges4[0], yedges4[-1], xedges4[0], xedges4[-1]]
	cset = axes[1,1].contour(H4,colors=['black','green','blue','red'],
			linewidths=(1.9, 1.6, 1.5, 1.4),extent=extent4)
	axes[1,1].clabel(cset, inline=1, fontsize=10, fmt=’%1.1f’)
	axes[1,1].set_xlabel('u-g')
	axes[1,1].set_xlabel('r-i')

	plt.savefig('contour_sdss_photometry.png')
	