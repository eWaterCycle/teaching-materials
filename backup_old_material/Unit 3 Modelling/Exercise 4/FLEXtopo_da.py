import numpy       as np
from Weigfun import Weigfun
from plateau import plateau
from hillslope import hillslope
from wetland import wetland

def FLEXtopo(ParPlateau, ParHillslope, ParWetland, ParCatchment, df, landscape_per):

    #parameters and constants
    Tlag = ParCatchment[1]
    Ks   = ParCatchment[0]
    dt   = 1
    tmax = len(df)

    #initialize states
    States_plateau   = np.zeros((tmax,3))
    States_hillslope = np.zeros((tmax,3))
    States_wetland   = np.zeros((tmax,3))
    Ss               = np.zeros((tmax,1))

    #initialize fluxes
    Fluxes_plateau   = np.zeros((tmax,4))
    Fluxes_hillslope = np.zeros((tmax,4))
    Fluxes_wetland   = np.zeros((tmax,3))
    Qsdt             = np.zeros(tmax)
    Qtotdt           = np.zeros(tmax)
    
    plateau_per, hillslope_per, wetland_per= landscape_per[0], landscape_per[1], landscape_per[2]

    #
    #loop over time
    for t in range(0,tmax):
        
        #plateau
        Fluxes_plateau, States_plateau     = plateau(  t, ParPlateau,   df, Fluxes_plateau,   States_plateau)
        
        #hillslope
        Fluxes_hillslope, States_hillslope = hillslope(t, ParHillslope, df, Fluxes_hillslope, States_hillslope)

        #wetland
        Fluxes_wetland, States_wetland, Ss = wetland(  t, ParWetland,   df, Fluxes_wetland,   States_wetland,  Ss, wetland_per)

        # Slow Reservoir
        Ss[t] = Ss[t] + Fluxes_plateau[t,3] * plateau_per + Fluxes_hillslope[t,3] * hillslope_per 
        Qsdt  = dt*Ks*Ss[t] 
        Ss[t] = Ss[t]-min(Qsdt,Ss[t])
        if t < tmax - 1:
            Ss[t+1] = Ss[t]

        Qtotdt[t] = Qsdt + Fluxes_plateau[t,2] * plateau_per + Fluxes_hillslope[t,2] * hillslope_per + Fluxes_plateau[t,2] * wetland_per


    # Offset Q

    Weigths = Weigfun(Tlag)
    
    Qm = np.convolve(Qtotdt,Weigths)
    Qm = Qm[0:tmax]
    
    df["Qm"] = Qm
    
    return df


