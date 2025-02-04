import numpy       as np
import matplotlib.pyplot as plt
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
Sin= np.array([0,  100,  0,  5  ])


A=np.genfromtxt('MC2.txt',  dtype=float, autostrip=True, delimiter=',')


#find the optimum
Opt_obj = A.argmax(axis=0)[8]
print(Opt_obj)

#find the optimal parameter set
OptPar = A[Opt_obj, 0:8]


plt.figure(1)
Obj = HBVMod(OptPar,forcing,Sin, hydrograph='TRUE')

fig, ax = plt.subplots(4,2, figsize=(10,10))


ax[0,0].plot(A[:,0],A[:,8],'.')
ax[0,0].set_xlabel('I$_{max}$', fontsize=15)
ax[0,0].set_ylabel('N (-)', fontsize=15)

plt.subplot(422)
ax[0,1].plot(A[:,1],A[:,8],'.')
ax[0,1].set_xlabel('C$_{e}$', fontsize=15)
ax[0,1].set_ylabel('N (-)', fontsize=15)

plt.subplot(423)
ax[1,0].plot(A[:,2],A[:,8],'.')
ax[1,0].set_xlabel('S$_{u,max}$', fontsize=15)
ax[1,0].set_ylabel('N (-)', fontsize=15), 

plt.subplot(424)
ax[1,1].plot(A[:,3],A[:,8],'.')
ax[1,1].set_xlabel('\beta', fontsize=15)
ax[1,1].set_ylabel('N (-)', fontsize=15)

plt.subplot(425)
ax[2,0].plot(A[:,4],A[:,8],'.')
ax[2,0].set_xlabel('P$_{max}$', fontsize=15)
ax[2,0].set_ylabel('N (-)', fontsize=15)

plt.subplot(426)
ax[2,1].plot(A[:,5],A[:,8],'.')
ax[2,1].set_xlabel('T$_{lag}$', fontsize=15)
ax[2,1].set_ylabel('N (-)', fontsize=15)

plt.subplot(427)
ax[3,0].plot(A[:,6],A[:,8],'.')
ax[3,0].set_xlabel('K$_{f}$', fontsize=15)
ax[3,0].set_ylabel('N (-)', fontsize=15)

plt.subplot(428)
ax[3,1].plot(A[:,7],A[:,8],'.')
ax[3,1].set_xlabel('K$_{s}$', fontsize=15)
ax[3,1].set_ylabel('N (-)', fontsize=15)

plt.tight_layout()
plt.show()

