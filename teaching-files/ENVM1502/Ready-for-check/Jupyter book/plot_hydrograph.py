# hydrograph_plot.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider, fixed
from datetime import date

def plot_hydrograph(Imax, Ce, Sumax, beta, Pmax, Tlag, Kf, Ks, model, forcing):
    Sin = np.array([0,  100,  0,  5  ])
    Par = np.array([Imax, Ce, Sumax, beta, Pmax, Tlag, Kf, Ks])
    Qm = model(Par, forcing, Sin, hydrograph='FALSE')

    # Calculate objective
     # Calculate objective

    Qo = forcing['Q'].values
    ind = np.where(Qo>=0)
    QoAv = np.mean(Qo[ind])
    ErrUp = np.sum((Qo[ind] - Qm[ind]) ** 2)
    ErrDo = np.sum((Qo[ind] - QoAv) ** 2)
    Obj = 1 - (ErrUp / ErrDo)

    plt.figure(figsize=(10, 5))
    plt.plot(forcing.index, forcing['Q'], label='Observed Q')
    plt.plot(forcing.index, Qm, label='Simulated Q')

    plt.xlabel('Date')
    plt.ylabel('Flow')
    plt.title(f'Hydrograph - NSE = {Obj:.2f}')
    plt.legend()
    plt.grid(True)
    plt.show()

def interactive_plot(model, forcing, params_min, params_max):

    Imax = (params_max[0] + params_min[0]) / 2
    Ce = (params_max[1] + params_min[1]) / 2
    Sumax = (params_max[2] + params_min[2]) / 2 
    beta = (params_max[3] + params_min[3]) / 2
    Pmax = (params_max[4] + params_min[4]) / 2
    Tlag = (params_max[5] + params_min[5]) / 2
    Kf = (params_max[6] + params_min[6]) / 2
    Ks = (params_max[7] + params_min[7]) / 2

    
    interact(
        plot_hydrograph,
        Imax=FloatSlider(min=params_min[0], max=params_max[0], step=0.1, value=2),
        Ce=FloatSlider(min=0, max=1, step=0.01, value=0.5),
        Sumax=FloatSlider(min=0, max=200, step=1, value=100),
        beta=FloatSlider(min=0, max=5, step=0.1, value=2),
        Pmax=FloatSlider(min=0, max=1, step=0.01, value=0.01),
        Tlag=IntSlider(min=0, max=10, step=0.1, value=5),
        Kf=FloatSlider(min=0, max=1, step=0.01, value=0.05),
        Ks=FloatSlider(min=0, max=0.01, step=0.0001, value=0.001, readout_format='.3f'),
        model=fixed(model),
        forcing=fixed(forcing),
    )

def interactive_plot(model, forcing, params):

    # Bereken de gemiddelde waarden voor de parameters
    Imax = (params['Imax']['min'] + params['Imax']['max']) / 2
    Ce = (params['Ce']['min'] + params['Ce']['max']) / 2
    Sumax = (params['Sumax']['min'] + params['Sumax']['max']) / 2 
    beta = (params['beta']['min'] + params['beta']['max']) / 2
    Pmax = (params['Pmax']['min'] + params['Pmax']['max']) / 2
    Tlag = (params['Tlag']['min'] + params['Tlag']['max']) / 2
    Kf = (params['Kf']['min'] + params['Kf']['max']) / 2
    Ks = (params['Ks']['min'] + params['Ks']['max']) / 2

    # Maak sliders aan met de opgegeven min en max waarden
    interact(
        plot_hydrograph,
        Imax=FloatSlider(min=params['Imax']['min'], max=params['Imax']['max'], step=0.1, value=Imax),
        Ce=FloatSlider(min=params['Ce']['min'], max=params['Ce']['max'], step=0.01, value=Ce),
        Sumax=FloatSlider(min=params['Sumax']['min'], max=params['Sumax']['max'], step=1, value=Sumax),
        beta=FloatSlider(min=params['beta']['min'], max=params['beta']['max'], step=0.1, value=beta),
        Pmax=FloatSlider(min=params['Pmax']['min'], max=params['Pmax']['max'], step=0.001, value=Pmax),
        Tlag=IntSlider(min=params['Tlag']['min'], max=params['Tlag']['max'], step=1, value=Tlag),
        Kf=FloatSlider(min=params['Kf']['min'], max=params['Kf']['max'], step=0.01, value=Kf),
        Ks=FloatSlider(min=params['Ks']['min'], max=params['Ks']['max'], step=0.0001, value=Ks, readout_format='.3f'),
        model=fixed(model),
        forcing=fixed(forcing),
    )
