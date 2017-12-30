import numpy as np
from scipy import sparse

def spectralband(A,zinit,zfin):

	degrees = sparse.csc_matrix.sum(A,0)
	degrees = np.asarray(degrees).reshape(-1)
	Ntot = len(degrees)
	cm = sum(degrees)/Ntot

	for z in np.linspace(zinit,zfin,1000):
		unique, counts = np.unique(degrees, return_counts=True)
		R1 = 0
		S2 = 0
		for t in range(len(unique)):
			ct = unique[t]
			bt = counts[t]/Ntot
			R1 += bt*ct/(z-ct)
			S2 += bt*(ct**(2))*(z-ct)**(-2)

		hasq = R1/(cm+R1)
		if hasq < 0:
			break
		Diff = S2 - hasq*cm*(1+hasq)*((1-hasq)**(-2))

		if z == zinit and Diff > 0:
			print("Try larger zup!")
			break
		elif z == zfin and Diff < 0:
			print("Try smaller zlow!")
			break
		elif(Diff > 0):
			#print("z = "+str(z))
			#print("residual = "+str(Diff))
			break

	return np.sqrt(hasq)*z


def simultaneous_power_iteration(A,k,alpha):
	# http://mlwiki.org/index.php/Power_Iteration
	shift = 10
	itrmax = 10000
	n, m = A.shape
	Q = np.random.rand(n, k)
	Q, _ = np.linalg.qr(Q)
	Q_prev = Q

	degrees = sparse.csc_matrix.sum(A,0)
	degrees = np.asarray(degrees).reshape(-1)
	totald = sum(degrees)

	for i in range(itrmax):
		resolution = alpha/totald
		Z = A.dot(Q) - resolution*np.outer(degrees,degrees.dot(Q)) + sparse.csc_matrix(shift*np.eye(A.shape[0])).dot(Q)
		Q,R = np.linalg.qr(Z)

		err = ((Q - Q_prev) ** 2).sum()
		Q_prev = Q
		if err < 1e-3:
			break
		if i == itrmax-1:
			print("Power iteration did not converge...!")

	return np.diag(R)-shift, Q
