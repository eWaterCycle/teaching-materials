import numpy       as np
import matplotlib as mpl
from HBVMod import HBVMod

forcing=np.genfromtxt('Forcing.txt',  dtype=float, autostrip=True)

          #      Imax Ce Sumax beta Pmax   Tlag   Kf  Ks
ParMinn = np.array([0,   0.2,  40,    .5,   .001,   0,     .01,  .0001])
ParMaxn = np.array([8,    1,  800,   4,    .3,     10,    .1,   .01])
Sin= np.array([0,  100,  0,  5  ])

forcing= forcing[:,3:6]


# GLUE
nmax=5000
A=np.zeros((nmax,9))
n_feasible = 0

for n in range(1,nmax): 
	Rnum=... #generate a vector of random number
	Par=... # calculate the random parameter set
	Obj = ... #call the model

	if Obj>.6:
		A[n_feasible,0:8]= Par
		A[n_feasible,8]=Obj
		n_feasible = n_feasible + 1


np.savetxt('MC2.txt',A[0:n_feasible,:], delimiter =',')


#find the optimum
#find the optimal parameter set


Obj=HBVMod(Par,forcing,Sin, hydrograph='TRUE')

