"""
usage: eigs.py [-h] <filename> [--k=<k>] [--resolution=<r>] [--zup=<u>] [--zlow=<l>]

options:
    -h, --help      show this help message and exit
    <filename>      text file of the edgelist.
    --k=<k>             max. of the number of communities [default: 10]
    --resolution=<r>    resolution parameter [default: 1]
    --zup=<u>           upper bound of variable z [default: 100]
    --zlow=<l>          lower bound of variable z [default: 1]
"""

import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt
import SpectralModularity as mod
from docopt import docopt


def make_sparsematrix():
	dlinks = np.concatenate([links, np.ones((links.shape[0],1))],axis=1)

	if directed == False: #and [links[0,1],links[0,0]] not in links.tolist():
		revlinks =  np.concatenate([np.asmatrix(links[:,1]).T,np.asmatrix(links[:,0]).T],axis=1)
		dlinks = np.append(dlinks,np.concatenate([revlinks,np.ones((links.shape[0],1))],axis=1),axis=0)

	dlinks = np.unique(dlinks, axis=0)
	A = sparse.coo_matrix((dlinks[:,2],(dlinks[:,0],dlinks[:,1])),shape=(Ntot,Ntot)).tocsc()

	return A

def read_graph():
	f = open(dataset, 'r')

	row = f.readline()
	nodeids = []
	while row:
		row = row.strip()
		li = row.split(" ")
		nodeids.append(int(li[0]))
		nodeids.append(int(li[1]))
		row = f.readline()
	nodeids = list(set(nodeids))

	f.seek(0)
	row = f.readline()
	links = np.empty((0,2),int)
	while row:
		row = row.strip()
		li = row.split(" ")
		links = np.append(links,np.array([[nodeids.index(int(li[0])),nodeids.index(int(li[1]))]]), axis=0)
		row = f.readline()

	return nodeids, links


def ScatterPlot():
	fig, ax = plt.subplots(figsize=(6,2))

	y = np.zeros(len(evalues))
	plt.scatter(evalues, y, edgecolors="#ff9900", c="", label="K = "+str(B+1))
	plt.xlabel("Eigenvalue")
	plt.axvline(x=bandedge,ls='--',color='k')

	ax.set_yticklabels([])
	#ax.legend()

	plt.savefig("eigenvalues_modularity_"+dataset+".pdf")
	plt.show()


def Historgram():
	# plot the cumulative histogram
	fig, ax = plt.subplots(figsize=(8, 4))

	n_bins = 50
	n, bins, patches = ax.hist(evalues, n_bins, normed=False, histtype='stepfilled',
                           cumulative=False, facecolor="#ff9900", range=(2.2, 7), label='Data')

	plt.axvline(x=bandedge,ls='--',color='k')

	ax.set_title('Eigenvalue histogram of the modularity matrix')
	ax.set_xlabel('Eigenvalue')
	ax.set_ylabel('Count')

	plt.savefig("eigenvalues_modularity_histogram_"+dataset+".pdf")
	plt.show()

def CumulativeHistorgram():
	# plot the cumulative histogram
	fig, ax = plt.subplots(figsize=(8, 4))

	n_bins = 50
	n, bins, patches = ax.hist(evalues, n_bins, normed=False, histtype='stepfilled',
                           cumulative=-1, label='Data')

	plt.axvline(x=bandedge,ls='--',color='k')

	ax.set_title('Cumulative step histogram')
	ax.set_xlabel('Eigenvalue')
	ax.set_ylabel('Count')

	plt.savefig("eigenvalues_modularity_cumulative-histogram_"+dataset+".pdf")
	plt.show()


if __name__ == "__main__":

	args = docopt(__doc__)
	dataset = args["<filename>"]
	kmax = int(args["--k"])
	resolution = int(args["--resolution"])
	zinit = int(args["--zup"])
	zfin = int(args["--zlow"])

	directed = False
	zinit += 1e-6
	zfin += 1e-6

	nodeids, links = read_graph()
	Ntot = len(nodeids)
	A = make_sparsematrix()

	bandedge = mod.spectralband(A,zinit,zfin)
	evalues, evecs = mod.simultaneous_power_iteration(A,kmax,resolution)

	B = len(evalues[evalues>=bandedge]) # Number of modules - 1
	if B == kmax:
		print("Raise kmax!")
	else:
		print("Estimated number of modules = "+str(B+1))
	
	#print(np.sort(evalues)[::-1])
	#CumulativeHistorgram()
	#Historgram()
	ScatterPlot()
