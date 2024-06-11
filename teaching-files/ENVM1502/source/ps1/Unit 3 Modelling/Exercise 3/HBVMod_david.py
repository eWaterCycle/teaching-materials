import numpy       as np
import math
import matplotlib.pyplot as plt
from Weigfun import Weigfun

def HBVMod(Par, df, Sin, hydrograph=False,ax=None, printing = False, Obj_type="NSE"):
    """
    Function to run a simple HBV model to model stream flow
    
    Parameters
    ----------
    Par: array_like
        array/list containing 8 parameters: Imax,  Ce,  Sumax, beta,  Pmax,  Tlag,   Kf,   Ks (floats)
    df: pandas.core.frame.DataFrame
        DataFrame containing 'P', 'Q', 'EP' columns as forcing for the model.
    Sin: array_like
        array/list containing 4 storage terms Si,  Su, Sf, Ss (floats)
    
    Keywords
    ----------
    hydrograph: Bool
        whether to plot a hydrograph
    printing: Bool
        whether to print the water balance values 
    Obj_type: String
        which type of objective function:
        =============   ===============================
        String          description
        =============   ===============================
        NSE             Nash and Sutcliffe coefficient
        NSE_log         Nash and Sutcliffe, but logarithmic
        NSE_sqrt        Nash and Sutcliffe, but square-root

    Returns
    ----------
    Obj, df: float, pandas.core.frame.DataFrame
        return of the objective function and corresponding dataframe

    """
    #HBVpareto Calculates values of 3 objective functions for HBV model
    
    # define parameters 
    I_max  = Par[0]   # maximum interception
    Ce     = Par[1]   # Ea = Su / (sumax * Ce) * Ep
    Su_max = Par[2]   # ''
    beta   = Par[3]   # Cr = (su/sumax)**beta
    P_max  = Par[4]   # Qus = Pmax * (Su/Sumax)
    T_lag  = Par[5]   # used in triangular transfer function
    Kf     = Par[6]   # Qf=kf*sf
    Ks     = Par[7]   # Qs=Ks*Ss

    # precipitation is given by the first column, Q0 by the second and  
    Prec   = df.P.values
    Qo     = df.Q.values
    Etp    = df.EP.values

    # get the final time setp
    t_max=len(Prec)
    
    # allocate Si, Su, Sf, Ss, Eidt, Eadt, Qtotdt
    Si        = np.zeros(t_max) # Interception storage
    Su        = np.zeros(t_max) # Unsaturated Rootzone Storage
    Sf        = np.zeros(t_max) # Fastflow storage
    Ss        = np.zeros(t_max) # Groundwater storage
    Ei_dt     = np.zeros(t_max) # interception evaporation
    Ea_dt     = np.zeros(t_max) # actual evaportation
    Qs_dt_lst = np.zeros(t_max)
    Qf_dt_lst = np.zeros(t_max)
    Q_tot_dt  = np.zeros(t_max) # total flow
    
    # initialize the storage coefficients Si, Su, Sf, Ss
    Si[0] = Sin[0]
    Su[0] = Sin[1]
    Sf[0] = Sin[2]
    Ss[0] = Sin[3]

    # time step of one day
    dt = 1

    # Model 1 SOF1
    for i in range(0, t_max):
        P_dt  = Prec[i] * dt
        Ep_dt = Etp[i]  * dt
        
        # Interception Reservoir
        if P_dt > 0:
            # if there is rain, no evap
            Si[i]    = Si[i] + P_dt               # increase the storage
            Pe_dt    = max((Si[i] - I_max) / dt, 0)
            Si[i]    = Si[i] - Pe_dt 
            Ei_dt[i] = 0                          # if rainfall, evaporation = 0 as too moist 
        else:
            # Evaporation only when there is no rainfall
            Pe_dt    = 0                      # nothing flows in so must be 0
            Ei_dt[i] = min(Ep_dt, Si[i] / dt) # evaporation limited by storage
            Si[i]    = Si[i] - Ei_dt[i] 
        
        # if not the end, initialise the next storage
        if i < t_max - 1:
            Si[i+1] = Si[i]
        
        
        # split flow into Unsaturated Reservoir and Fast flow
        if Pe_dt > 0:
            cr     = (Su[i] / Su_max)**beta
            Qiu_dt = (1 - cr ) * Pe_dt      # flux from Ir to Ur
            Su[i]  = Su[i] + Qiu_dt
            Quf_dt = cr  * Pe_dt            # flux from Su to Sf
        else:
            Quf_dt=0
        
        # Transpiration
        Ep_dt    = max(0, Ep_dt - Ei_dt[i])        # Transpiration 
        Ea_dt[i] = Ep_dt  * (Su[i] / (Su_max * Ce))
        Ea_dt[i] = min(Su[i], Ea_dt[i])            # limited by water in soil 
        Su[i]    = Su[i] - Ea_dt[i]
        
        # Percolation
        Qus_dt = P_max * (Su[i] / Su_max) * dt # Flux from Su to Ss
        Su[i]  = Su[i] - Qus_dt
        
        # make the final steps to update next step
        if i < t_max - 1:
            Su[i+1]=Su[i]
        
        # Fast Reservoir
        Sf[i] = Sf[i] + Quf_dt
        Qf_dt = dt * Kf * Sf[i]
        Sf[i] = Sf[i] - Qf_dt
        if i < t_max -  1:
            Sf[i+1] = Sf[i]
        
        # Slow Reservoir
        Ss[i] = Ss[i] + Qus_dt
        Qs_dt = Ss[i] * Ks * dt
        Ss[i] = Ss[i] - Qs_dt
        if i < t_max-1:
            Ss[i+1] = Ss[i]
        
        Q_tot_dt[i] = Qs_dt + Qf_dt
        Qs_dt_lst[i] = Qs_dt
        Qf_dt_lst[i] = Qf_dt
    
    # Check Water Balance
    Sf  = Si[-1] + Ss[-1] + Sf[-1] + Su[-1] # final storage
    Sin = sum(Sin)                          # initial storage
    WB  = sum(Prec) - sum(Ei_dt)- sum(Ea_dt) - sum(Q_tot_dt) + Sin - Sf
    
    
    if printing:
        print(f'P :\t{sum(Prec):.2f} \nEi:\t {sum(Ei_dt):.2f} \nEa:\t{sum(Ea_dt):.2f}'
              f'\nQ :\t{sum(Q_tot_dt):.2f} \nWB:\t{WB:.2g}')

    # Offset Q
    Weigths = Weigfun(T_lag)
    
    Qm = np.convolve(Q_tot_dt, Weigths)
    Qm = Qm[0:t_max]
    
    Qs_dt_lst = np.convolve(Qs_dt_lst, Weigths)
    Qs_dt_lst = Qs_dt_lst[0:t_max]
    
    Qf_dt_lst = np.convolve(Qf_dt_lst, Weigths)
    Qf_dt_lst = Qf_dt_lst[0:t_max]
    
    df["Qm"] = Qm
    df["Q_slow"] = Qs_dt_lst
    df["Q_fast"] = Qf_dt_lst
    
    #### Calculate objective function

    # filter any unrealistic values
    ind   = np.where(Qo>=0)
    if Obj_type == "NSE":
        Qo    = Qo[ind]
    
    # in case other obj, use these
    elif Obj_type == "NSE_log":
        Qo = np.log(Qo[ind])
        Qm = np.log(Qm)

    elif Obj_type == "NSE_sqrt":
        Qo    = np.sqrt(Qo[ind])
        Qm  = np.sqrt(Qm)
    
    # compute final statistic
    QoAv  = np.mean(Qo)
    ErrUp = np.sum((Qm - Qo)**2)
    ErrDo = np.sum((Qo - QoAv)**2)
    Obj   = 1 - (ErrUp / ErrDo)
    
    # in case none, return -999
    if Obj_type not in ["NSE", "NSE_log", "NSE_sqrt"]:
        Obj = -999
    


    if hydrograph:
    ## Plot
    # hour=1:tmax\
        if ax is None:
            fig, ax = plt.subplots(1)
        df.Q.plot(ax=ax)
        df.Qm.plot(ax=ax)
#         df.Q_slow.plot(ax=ax)
#         df.Q_fast.plot(ax=ax)
        ax.legend(["Stream flow","Modeled stream flow"])
        ax.set_title("Comparison of model with reality")
        # plt.close(fig)
        

    return Obj, df