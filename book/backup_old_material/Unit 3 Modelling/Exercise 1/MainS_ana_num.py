import numpy       as np
import matplotlib.pyplot as plt
from Snum import Snum


#define variables and empty vectors
S0 = 75                    #mm
t0 = 0                     #days
k = 0.01                   #day^-1
tmax = 200                 #days
dt = 1                    #days
Sn = np.zeros(tmax/dt)      #mm

## analytical solution
#for the analytical solution you don't need a for loop
t=np.arange(0,tmax,dt)
Sa=S0*np.exp(-k*t-t0)


## numerical solution
Sn[0] = S0                           #start your loop with the second value of the numerical solution
# start for loop: the values are starting value:timestep:final value
for i in range(1,tmax/dt):
	Sn[i] = Snum(Sn[i-1],k,dt)     #use the function 'Snum' to calculate the numerical solution for timestep t


## plot both solutions in the same plot
t=range(0,tmax,dt)
plt.plot(t,Sa, 'r')
plt.plot(t,Sn, 'b--')
plt.title( 'Analytical and numerical solution for storage reservoir, k=' + str(k)+ ', dt=' + str(dt))
plt.legend(['analytical','numerical'], loc=5)

plt.show()
