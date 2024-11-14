import numpy       as np
import matplotlib as mpl
import pandas as pd
from HBVMod import HBVMod

# from datetime import date
# data = pd.read_csv('Forcing.txt', skipinitialspace=True, delimiter='\t', names=['year', 'month', 'day', 'P', 'Q', 'PE'])
# forcing = pd.DataFrame()
# forcing['P'] = data['P']
# forcing['PE'] = data['PE']
# forcing['Q'] = data['Q']
# forcing.index = data.apply(lambda x: date(int(x.year), int(x.month), int(x.day)), axis=1)
# forcing.index = pd.to_datetime(forcing.index, format='%Y-%m-%d')

forcing=np.genfromtxt('Forcing.txt',  dtype=float, autostrip=True)
forcing= forcing[:,3:6]
          #      Imax Ce Sumax beta Pmax   Tlag   Kf  Ks
ParMinn = np.array([0,   0.2,  40,    .5,   .001,   0,     .01,  .0001])
ParMaxn = np.array([8,    1,  800,   4,    .3,     10,    .1,   .01])
Sin = np.array([0,  100,  0,  5  ])




# GLUE
nmax = 5000
A = np.zeros((nmax,9))
n_feasible = 0

for n in range(1,nmax): 
    Rnum = np.random.random(8)  #generate a vector of random number
    
    Par = Rnum * (ParMaxn - ParMinn) + ParMinn # calculate the random parameter set
    Obj = HBVMod(Par, forcing, Sin, hydrograph='FALSE') #call the model

    if Obj>.6:
        A[n_feasible,0:8]= Par
        A[n_feasible,8] = Obj
        n_feasible = n_feasible + 1


np.savetxt('MC2.txt',A[0:n_feasible,:], delimiter =',')


#find the optimum

Opt_obj = A.argmax(axis=0)[8]
print(Opt_obj)

#find the optimal parameter set
OptPar = A[Opt_obj, 0:8]


Obj=HBVMod(OptPar,forcing,Sin, hydrograph='True')

