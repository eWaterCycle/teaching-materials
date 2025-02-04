import numpy       as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from FLEXtopo import FLEXtopo


forcing=np.genfromtxt('wark_data/forcingWark.txt',  dtype=float, autostrip=True)

                  #      Imax Ce Sumax beta Pmax    Kf  
ParPlateau   = np.array([3.2, 0.50, 17.40, 0.95, 1.76, 0.91])   
                  #      Imax Ce Sumax beta D     Kf  
ParHillslope = np.array([3.25, 0.50, 321.99, 0.99, 0.4,0.97])
                  #      Imax Ce Sumax beta Cmax     Kf  
ParWetland   = np.array([9.94, 0.50, 53.25, 0.70, 0.65, 0.45])
              # Ks Tlag
ParCatchment = np.array([0.0281, 2.21])

#landscape percentages
landscape_per= np.array([plateau_per, hillslope_per, wetland_per])


Qm = FLEXtopo(ParPlateau, ParHillslope, ParWetland, ParCatchment, forcing[:,3:6], landscape_per)
Qo = forcing[:,3]

plt.plot(range(0,len(Qo)),Qo)
plt.plot(range(0,len(Qm)),Qm)
plt.show()
