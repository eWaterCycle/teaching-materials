import numpy as np

def Weigfun(Tlag): 
    # Function to calculate weights based on Tlag
    nmax = np.ceil(Tlag)
    
    if nmax == 1: 
        Weigths = np.array([1.0])
    else:
        Weigths = np.zeros(int(nmax))
      
        
        th = Tlag / 2
        nh = int(np.floor(th))
        
        for i in range(0, nh): 
            Weigths[i] = (float(i+1) - 0.5) / th
        
        i = nh
        Weigths[i] = ((1 + (float(i+1) - 1) / th) * (th - np.floor(th)) / 2 +
                     (1 + (Tlag - float(i+1)) / th) * (np.floor(th) + 1 - th) / 2)
        
        for i in range(nh+1, int(np.floor(Tlag))):
            Weigths[i] = (Tlag - float(i+1) + 0.5) / th

        if Tlag > np.floor(Tlag):
            Weigths[int(np.floor(Tlag))] = (Tlag - np.floor(Tlag)) ** 2 / (2 * th)

        Weigths = Weigths / sum(Weigths)

    return Weigths
