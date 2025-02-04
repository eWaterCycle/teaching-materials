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
            Pedt = np.maximum(0, (Si[i] - Imax) / dt)
            Si[i] = Si[i] - Pedt
            Eidt[i] = 0
        else:
        # Evaporation only when there is no rainfall
            Pedt = np.maximum(0, (Si[i] - Imax) / dt) #is zero, because of no rainfall
            Eidt[i] = np.minimum(Epdt, Si[i] / dt)
            Si[i] = Si[i] - Pedt - Eidt[i]
        
        if i < tmax-1:
            Si[i+1] = Si[i]
        
        
        # Split Pe into Unsaturated Reservoir and Preferential reservoir
        if Pedt > 0:
            Cr = (Su[i] / Sumax) ** beta
            Qiudt = (1 - Cr) * Pedt # flux from Ir to Ur
            Su[i] = Su[i] + Qiudt
            Qufdt = Cr * Pedt #flux from Su to Sf
        else:
            Qufdt = 0
        
        # Transpiration
        Epdt = max(0, Epdt - Eidt[i])
        Eadt[i] = Epdt * (Su[i] / (Sumax * Ce))
        Eadt[i] = min(Su[i] / dt, Eadt[i])
        Su[i] = Su[i] - Eadt[i]
        
        # Percolation
        Qusdt = Pmax * (Su[i] / Sumax) * dt # Flux from Su to Ss
        Su[i] = Su[i] - Qusdt
        
        if i < tmax - 1:
            Su[i+1] = Su[i]
        
        # Fast Reservoir
        Sf[i] = Sf[i] + Qufdt
        Qfdt = dt * Kf * Sf[i]
        Sf[i] = Sf[i] - Qfdt
        if i < tmax-1:
            Sf[i+1] = Sf[i]
        
        # Slow Reservoir
        Ss[i] = Ss[i] + Qusdt
        Qsdt = dt * Ks * Ss[i]
        Ss[i] = Ss[i] - Qsdt
        if i < tmax-1:
            Ss[i+1] = Ss[i]
        
        Qtotdt[i] = Qsdt + Qfdt
        Qs[i] = Qsdt 
        Qf[i] = Qfdt 


    # Check Water Balance
    Sf = Si[-1] + Ss[-1] + Sf[-1] + Su[-1] #final storage
    Sin = sum(Sin) #initial storage
    WB = sum(Prec) - sum(Eidt) - sum(Eadt) - sum(Qtotdt) - Sf + Sin

    # Offset Q

    Weigths = Weigfun(Tlag)
    
    Qm = np.convolve(Qtotdt, Weigths)
    Qm = Qm[0:tmax]
    forcing['Qm'] = Qm
    
    # Calculate objective
    ind = np.where(Qo>=0)
    QoAv = np.mean(Qo[ind])
    ErrUp = np.sum((Qo - Qm) ** 2)
    ErrDo = np.sum((Qo - QoAv) ** 2)
    Obj = 1 - (ErrUp / ErrDo)

    if hydrograph == 'True':
    ## Plot
    # hour=1:tmax\
        plt.plot(range(0,len(Qo)),Qo)
        plt.plot(range(0,len(Qm)),Qm)
        plt.show()
    if hydrograph == 'TRUE':
    ## Plot
    # hour=1:tmax\
        fig, ax = plt.subplots(figsize=(12,8))
        forcing['Q'].plot(label='Observed', ax=ax)
        forcing['Qm'].plot(label='Model',  ax=ax)
        ax.set_xlabel('Time [days]')
        ax.set_ylabel('Runoff Q [$mmd^{-1}$]')

        ax.legend()
        
    return(Obj)


    # leg['Qobs','Qmod']
