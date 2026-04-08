import numpy as np
from Weigfun import Weigfun

def hillslope(timestep, Par, forcing, Fluxes, States):
	# HBVpareto Calculates values of 3 objective functions for HBV model

	Imax = Par[0]
	Ce = Par[1]
	Sumax = Par[2]
	beta = Par[3]
	D = Par[4]
	Kf = Par[5]
	Qo = forcing['Qo']
	Prec = forcing['Prec']
	Etp = forcing['Etp']


	tmax = len(Prec)
	Si = States[:,0]
	Su = States[:,1]
	Sf = States[:,2]

	Eidt = Fluxes[:,0]
	Eadt = Fluxes[:,1]
	Qfdt = Fluxes[:,2]
	Qusdt = Fluxes[:,3]

	dt = 1
	t = timestep


	Pdt = Prec[t] * dt
	Epdt = Etp[t] * dt
	# Interception Reservoir
	...



	# Unsaturated Reservoir
    ...

	# Transpiration
    ...

	# Preferential Percolation
	Qusdt = D * ...

	# Fast Reservoir
	Sf[t] = Sf[t] + (1-D) * ...
	Qfdt[t] = ...
	Sf[t] = ...    
...

	# Save output
	States[:,0] = Si
	States[:,1] = Su
	States[:,2] = Sf

	Fluxes[:,0] = Eidt
	Fluxes[:,1] = Eadt
	Fluxes[:,2] = Qfdt
	Fluxes[:,3] = Qusdt

	return(Fluxes, States)

	

