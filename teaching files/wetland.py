import numpy       as np
from Weigfun import Weigfun

def wetland(  timestep, Par, forcing, Fluxes, States, Ss, landscape_per ):
	#HBVpareto Calculates values of 3 objective functions for HBV model

	Imax=Par[0]
	Ce=Par[1]
	Sumax=Par[2]
	beta=Par[3]
	Cmax=Par[4]
	Kf=Par[5]

	Qo=forcing[:,0]
	Prec=forcing[:,1]
	Etp=forcing[:,2]


	tmax=len(Prec)
	Si=States[:,0]
	Su=States[:,1]
	Sf=States[:,2]

	Eidt=Fluxes[:,0]
	Eadt=Fluxes[:,1]
	Qfdt=Fluxes[:,2]

	dt=1
	t=timestep


	Pdt=Prec[t]*dt
	Epdt=Etp[t]*dt
    
	# Interception Reservoir
    ...

	# Unsaturated Reservoir
    ...

	# Transpiration
    ...

	#Capillary rise
	Qrdt=(1-Su[t]/Sumax)*...
    
    #check if the groundwater has enough water (note: you need to use the landscape percentage!!!)
	Qrdt=min(Qrdt, ...

    # su cannot be more than sumax
	if( (Su[t] + Qrdt) > Sumax):
		Qrdt = Sumax - Su[t]

	Su[t] = Su[t] + ...
	Ss[t]=Ss[t]- ... # * landscape_per

	if t<tmax-1:
		Su[t+1]=Su[t]


	# Fast Reservoir
    ...


	#save output
	States[:,0]=Si
	States[:,1]=Su
	States[:,2]=Sf

	Fluxes[:,0]=Eidt
	Fluxes[:,1]=Eadt
	Fluxes[:,2]=Qfdt


	return(Fluxes, States, Ss)


