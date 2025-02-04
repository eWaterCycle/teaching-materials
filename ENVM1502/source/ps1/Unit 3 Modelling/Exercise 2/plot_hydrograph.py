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

def interactive_plot(model, forcing):
    # Creating interactive widgets
    interact(
        plot_hydrograph,
        Imax=FloatSlider(min=0, max=10, step=0.1, value=2),
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