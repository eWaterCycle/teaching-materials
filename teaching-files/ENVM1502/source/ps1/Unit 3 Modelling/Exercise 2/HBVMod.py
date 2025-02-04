import numpy       as np
import matplotlib.pyplot as plt
from Weigfun import Weigfun

def HBVMod(Par,forcing,Sin, hydrograph):
    #HBVpareto Calculates values of 3 objective functions for HBV model

    Imax = Par[0]
    Ce = Par[1]
    Sumax = Par[2]
    beta = Par[3]
    Pmax = Par[4]
    Tlag = Par[5]
    Kf = Par[6]
    Ks = Par[7]
    

    Prec = forcing['P'].values
    Qo = forcing['Q'].values
    Etp = forcing['PE'].values


    tmax = len(Prec)
    
    # allocate Si, Su, Sf, Ss, Eidt, Eadt, Qtotdt
    
    Si = np.zeros(tmax)
    Su = np.zeros(tmax)
    Sf = np.zeros(tmax)
    Ss = np.zeros(tmax)
    Eidt = np.zeros(tmax)
    Eadt =  np.zeros(tmax)
    Qtotdt = np.zeros(tmax)
    Qs = np.zeros(tmax)
    Qf = np.zeros(tmax)
    
    # initialize Si, Su, Sf, Ss
    Si[0] = Sin[0]
    Su[0] = Sin[1]
    Sf[0] = Sin[2]
    Ss[0] = Sin[3]

    dt = 1

    #
    # Model 1 SOF1
    for i in range(0, tmax):
        Pdt = Prec[i] * dt
        Epdt = Etp[i] * dt
        
        # Interception Reservoir
        if Pdt > 0:
            Si[i] = Si[i] + Pdt
            Pedt = 
            Si[i] = 
            Eidt[i] = 
        else:
        # Evaporation only when there is no rainfall
            Pedt = 
            Eidt[i] = 
            Si[i] = 
        
        if i < tmax-1:
            Si[i+1] = Si[i]
        
        
        # Split Pe into Unsaturated Reservoir and Preferential reservoir
        if Pedt > 0:
            Cr = 
            Qiudt = 
            Su[i] = 
            Qufdt = 
        else:
            Qufdt = 
        
        # Transpiration
        Epdt = 
        Eadt[i] =
        Eadt[i] = 
        Su[i] =
        
        # Percolation
        Qusdt = 
        Su[i] = 
        
        if i < tmax - 1:
            Su[i+1] = Su[i]
        
        # Fast Reservoir
        Sf[i] = 
        Qfdt =
        Sf[i] =
        if i < tmax-1:
            Sf[i+1] = Sf[i]
        
        # Slow Reservoir
        Ss[i] =
        Qsdt = 
        Ss[i] = 
        if i < tmax-1:
            Ss[i+1] = Ss[i]
        
        Qtotdt[i] = 
        Qs[i] = 
        Qf[i] = 


    # Check Water Balance
    Sf = Si[-1] + Ss[-1] + Sf[-1] + Su[-1] #final storage
    Sin = sum(Sin) #initial storage
    WB = sum(Prec) - sum(Eidt) - sum(Eadt) - sum(Qtotdt) - Sf + Sin
    print(WB)
    # Offset Q

    Weigths = Weigfun(Tlag)
    
    Qm = np.convolve(Qtotdt, Weigths)
    Qm = Qm[0:tmax]
    forcing['Qm'] = Qm
    
    if hydrograph == 'TRUE':
    ## Plot
    # hour=1:tmax\
        fig, ax = plt.subplots(figsize=(12,8))
        forcing['Q'].plot(label='Obserbed', ax=ax)
        forcing['Qm'].plot(label='Model',  ax=ax)
        ax.legend()
        

    return(Qm)

    
    # leg['Qobs','Qmod']