import numpy       as np
import matplotlib.pyplot as plt
from HBVMod import HBVMod

forcing=np.genfromtxt('Forcing.txt',  dtype=float, autostrip=True)

Sin= np.array([0,  100,  0,  5  ])

forcing= forcing[:,3:6]

A=np.genfromtxt('MC2.txt',  dtype=float, autostrip=True, delimiter=',')


#find the optimum
#find the optimal parameter set


plt.figure(1)
Obj=HBVMod(OptPar,forcing,Sin, hydrograph='TRUE')

plt.figure(2)
plt.subplot(421)
plt.plot(A[:,0],A[:,8],'.')
plt.xlabel(...)
plt.ylabel(...)

plt.subplot(422)
plt.plot(A[:,1],A[:,8],'.')


plt.subplot(423)
#
#

plt.subplot(424)
#
#

plt.subplot(425)
#
#

plt.subplot(426)


plt.subplot(427)

plt.subplot(428)

plt.show()

