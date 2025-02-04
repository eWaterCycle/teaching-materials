import numpy       as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from HBVMod import HBVMod


forcing=np.genfromtxt('wark_data/forcingWark.txt',  dtype=float, autostrip=True)

                  #      Imax Ce Sumax beta Pmax    Kf  
Par = np.array([6.15, 0.68, 89.15, 1.85, 0.09, 1.10, 0.1, 0.008])




Qm = HBVMod(Par, forcing[:,3:6])
Qo = forcing[:,3]


plt.plot(range(0,len(Qo)),Qo)
plt.plot(range(0,len(Qm)),Qm)
plt.show()
