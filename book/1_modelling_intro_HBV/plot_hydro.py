import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import FloatSlider, IntSlider, VBox, HTML, HBox, Label, Output

# Initialize the global counter
param_change_counter = 0  
initial_run = True

def plot_hydrograph(I_max, Ce, Su_max, beta, P_max, T_lag, Kf, Ks, model, forcing):
    Sin = np.array([0, 100, 0, 5])
    Par = np.array([I_max, Ce, Su_max, beta, P_max, T_lag, Kf, Ks])
    Qm = model(Par, forcing, Sin, hydrograph='FALSE')

    # Calculate NSE
    Qo = forcing['Q'].values
    ind = np.where(Qo >= 0)
    QoAv = np.mean(Qo[ind])
    ErrUp = np.sum((Qo[ind] - Qm[ind]) ** 2)
    ErrDo = np.sum((Qo[ind] - QoAv) ** 2)
    Obj = 1 - (ErrUp / ErrDo)

    # Plot hydrograph
    plt.figure(figsize=(10, 5))
    plt.plot(forcing.index, forcing['Q'], label='Observed Q')
    plt.plot(forcing.index, Qm, label='Simulated Q')
    plt.xlabel('Date')
    plt.ylabel('Flow')
    plt.title(f'Hydrograph - NSE = {Obj:.2f}')
    plt.legend()
    plt.grid(True)
    plt.show()


def interactive_plot(model, forcing, params):
    global param_change_counter, initial_run

    recalculating_label = HTML(value="")

    # Calculate initial parameter values
    I_max = (params['I_max']['min'] + params['I_max']['max']) / 2
    Ce = (params['Ce']['min'] + params['Ce']['max']) / 2
    Su_max = (params['Su_max']['min'] + params['Su_max']['max']) / 2 
    beta = (params['beta']['min'] + params['beta']['max']) / 2
    P_max = (params['P_max']['min'] + params['P_max']['max']) / 2
    T_lag = (params['T_lag']['min'] + params['T_lag']['max']) / 2
    Kf = (params['Kf']['min'] + params['Kf']['max']) / 2
    Ks = (params['Ks']['min'] + params['Ks']['max']) / 2

    # Create sliders
    sliders = {
        'I_max': FloatSlider(min=params['I_max']['min'], max=params['I_max']['max'], step=0.1, value=I_max),
        'Ce': FloatSlider(min=params['Ce']['min'], max=params['Ce']['max'], step=0.01, value=Ce),
        'Su_max': FloatSlider(min=params['Su_max']['min'], max=params['Su_max']['max'], step=1, value=Su_max),
        'beta': FloatSlider(min=params['beta']['min'], max=params['beta']['max'], step=0.1, value=beta),
        'P_max': FloatSlider(min=params['P_max']['min'], max=params['P_max']['max'], step=0.001, value=P_max),
        'T_lag': IntSlider(min=params['T_lag']['min'], max=params['T_lag']['max'], step=1, value=T_lag),
        'Kf': FloatSlider(min=params['Kf']['min'], max=params['Kf']['max'], step=0.01, value=Kf),
        'Ks': FloatSlider(min=params['Ks']['min'], max=params['Ks']['max'], step=0.0001, value=Ks, readout_format='.3f')
    }

    # Combine sliders with labels
    slider_widgets = [
        HBox([Label(value=name, layout={'width': '150px'}), slider], layout={'align_items': 'flex-start'})
        for name, slider in sliders.items()
    ]

    # Create Output widget
    out = Output()

    # Function called when sliders change
    def update_counter(change):
        global param_change_counter, initial_run
        if not initial_run:
            param_change_counter += 1

        recalculating_label.value = "<b>Loading...</b>"

        out.clear_output(wait=True)
        with out:
            plot_hydrograph(
                I_max=sliders['I_max'].value, 
                Ce=sliders['Ce'].value, 
                Su_max=sliders['Su_max'].value, 
                beta=sliders['beta'].value, 
                P_max=sliders['P_max'].value, 
                T_lag=sliders['T_lag'].value, 
                Kf=sliders['Kf'].value, 
                Ks=sliders['Ks'].value,
                model=model, 
                forcing=forcing
            )
        recalculating_label.value = "<b>Recalculation Complete</b>"

    # Attach observer to all sliders
    for slider in sliders.values():
        slider.observe(update_counter, names='value')

    # Display UI
    ui = VBox([recalculating_label] + slider_widgets)
    display(ui, out)

    # Initial plot
    if initial_run:
        out.clear_output(wait=True)
        initial_run = False
        with out:
            plot_hydrograph(
                I_max=sliders['I_max'].value, 
                Ce=sliders['Ce'].value, 
                Su_max=sliders['Su_max'].value, 
                beta=sliders['beta'].value, 
                P_max=sliders['P_max'].value, 
                T_lag=sliders['T_lag'].value, 
                Kf=sliders['Kf'].value, 
                Ks=sliders['Ks'].value,
                model=model, 
                forcing=forcing
            )
