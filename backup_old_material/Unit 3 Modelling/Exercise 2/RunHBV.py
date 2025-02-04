import numpy       as np
import matplotlib as mpl
import pandas     as pd
from HBVMod import HBVMod
from datetime import date

def run():
    
    data = pd.read_csv('Forcing.txt', skipinitialspace=True, delimiter='\t', names=['year', 'month', 'day', 'P', 'Q', 'PE'])
    forcing = pd.DataFrame()
    forcing['P'] = data['P']
    forcing['PE'] = data['PE']
    forcing['Q'] = data['Q']
    forcing.index = data.apply(lambda x: date(int(x.year), int(x.month), int(x.day)), axis=1)
    forcing.index = pd.to_datetime(forcing.index, format='%Y-%m-%d')



              #      Imax Ce Sumax beta Pmax   Tlag   Kf  Ks
    Par = np.array([2,   .5,  100,   2,  .01,    5,   .05,  .001])

                  #Si, Su,   Sf, Ss
    Sin = np.array([0,  100,  0,  5  ])


    Qm = HBVMod(Par, forcing , Sin, hydrograph='TRUE')


