import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider, fixed, VBox, interactive_output, HTML, Button, HBox, Label


# Initialize the global counter
param_change_counter = 0  
initial_run = True

def plot_hydrograph(Imax, Ce, Sumax, beta, Pmax, Tlag, Kf, Ks, model, forcing):
    Sin = np.array([0,  100,  0,  5  ])
    Par = np.array([Imax, Ce, Sumax, beta, Pmax, Tlag, Kf, Ks])
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

    # Create a display widget to show the counter
    #counter_display = HTML(value=f"<b>Parameter Changes: {param_change_counter}</b>")
    # Create a label to show recalculation status
    # recalculating_label = Label(value="")
    recalculating_label = HTML(value="")
    
    # Update recalculating status
    
    # Calculate average parameter values
    Imax = (params['Imax']['min'] + params['Imax']['max']) / 2
    Ce = (params['Ce']['min'] + params['Ce']['max']) / 2
    Sumax = (params['Sumax']['min'] + params['Sumax']['max']) / 2 
    beta = (params['beta']['min'] + params['beta']['max']) / 2
    Pmax = (params['Pmax']['min'] + params['Pmax']['max']) / 2
    Tlag = (params['Tlag']['min'] + params['Tlag']['max']) / 2
    Kf = (params['Kf']['min'] + params['Kf']['max']) / 2
    Ks = (params['Ks']['min'] + params['Ks']['max']) / 2

    # Create sliders with the specified min and max values
    sliders = {
        'Imax': FloatSlider(min=params['Imax']['min'], max=params['Imax']['max'], step=0.1, value=Imax),
        'Ce': FloatSlider(min=params['Ce']['min'], max=params['Ce']['max'], step=0.01, value=Ce),
        'Sumax': FloatSlider(min=params['Sumax']['min'], max=params['Sumax']['max'], step=1, value=Sumax),
        'beta': FloatSlider(min=params['beta']['min'], max=params['beta']['max'], step=0.1, value=beta),
        'Pmax': FloatSlider(min=params['Pmax']['min'], max=params['Pmax']['max'], step=0.001, value=Pmax),
        'Tlag': IntSlider(min=params['Tlag']['min'], max=params['Tlag']['max'], step=1, value=Tlag),
        'Kf': FloatSlider(min=params['Kf']['min'], max=params['Kf']['max'], step=0.01, value=Kf),
        'Ks': FloatSlider(min=params['Ks']['min'], max=params['Ks']['max'], step=0.0001, value=Ks, readout_format='.3f')
    }

    # Combine sliders with their labels, and align them to the left
    slider_widgets = [HBox([Label(value=name, layout={'width': '150px'}), slider], layout={'align_items': 'flex-start'}) 
                      for name, slider in sliders.items()]

    def update_counter(change):
        global param_change_counter, initial_run
        if not initial_run:
            param_change_counter += 1
            #counter_display.value = f"<b>Parameter Changes: {param_change_counter}</b>"
            
        recalculating_label.value = "<b>Loading....</b>"

        out.clear_output(wait=True)
        with out:
            plot_hydrograph(
                Imax=sliders['Imax'].value, 
                Ce=sliders['Ce'].value, 
                Sumax=sliders['Sumax'].value, 
                beta=sliders['beta'].value, 
                Pmax=sliders['Pmax'].value, 
                Tlag=sliders['Tlag'].value, 
                Kf=sliders['Kf'].value, 
                Ks=sliders['Ks'].value,
                model=model, 
                forcing=forcing
            )
    
        # Update recalculation status after completion
        recalculating_label.value = "<b>Recalculation Complete</b>"
    
    
    # Attach the change handler to each slider
    for slider in sliders.values():
        slider.observe(update_counter, names='value')

    
    # Create the interactive plot
    ui = VBox([recalculating_label] + slider_widgets) #+ list(sliders.values()))
    out = interactive_output(lambda **kwargs: None, {})  # Empty output placeholder

    display(ui, out)

    # Plot the first time without incrementing the counter
    if initial_run:
        out.clear_output(wait=True)
        initial_run = False
        with out:
            plot_hydrograph(
                Imax=sliders['Imax'].value, 
                Ce=sliders['Ce'].value, 
                Sumax=sliders['Sumax'].value, 
                beta=sliders['beta'].value, 
                Pmax=sliders['Pmax'].value, 
                Tlag=sliders['Tlag'].value, 
                Kf=sliders['Kf'].value, 
                Ks=sliders['Ks'].value,
                model=model, 
                forcing=forcing
            )
        

# import numpy as np
# import matplotlib.pyplot as plt
# from ipywidgets import FloatSlider, IntSlider, fixed, VBox, interactive_output, HTML, Button, HBox, Label, Layout

# # Initialize the global counter
# param_change_counter = 0  

# def plot_hydrograph(Imax, Ce, Sumax, beta, Pmax, Tlag, Kf, Ks, model, forcing):
#     Sin = np.array([0,  100,  0,  5  ])
#     Par = np.array([Imax, Ce, Sumax, beta, Pmax, Tlag, Kf, Ks])
#     Qm = model(Par, forcing, Sin, hydrograph='FALSE')

#     # Calculate NSE
#     Qo = forcing['Q'].values
#     ind = np.where(Qo >= 0)
#     QoAv = np.mean(Qo[ind])
#     ErrUp = np.sum((Qo[ind] - Qm[ind]) ** 2)
#     ErrDo = np.sum((Qo[ind] - QoAv) ** 2)
#     Obj = 1 - (ErrUp / ErrDo)

#     # Plot hydrograph
#     plt.figure(figsize=(10, 5))
#     plt.plot(forcing.index, forcing['Q'], label='Observed Q')
#     plt.plot(forcing.index, Qm, label='Simulated Q')

#     plt.xlabel('Date')
#     plt.ylabel('Flow')
#     plt.title(f'Hydrograph - NSE = {Obj:.2f}')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# def interactive_plot(model, forcing, params):
#     global param_change_counter

#     # Create a display widget to show the counter
#     counter_display = HTML(value=f"<b>Attempts: {param_change_counter}</b>")
    

#     # Create the "Recalculate" button
#     play_button = Button(description="Recalculate")
    
#     # Create sliders with the specified min and max values
#     sliders = {
#         'Imax': FloatSlider(min=params['Imax']['min'], max=params['Imax']['max'], step=0.1, value=(params['Imax']['min'] + params['Imax']['max']) / 2),
#         'Ce': FloatSlider(min=params['Ce']['min'], max=params['Ce']['max'], step=0.01, value=(params['Ce']['min'] + params['Ce']['max']) / 2),
#         'Sumax': FloatSlider(min=params['Sumax']['min'], max=params['Sumax']['max'], step=1, value=(params['Sumax']['min'] + params['Sumax']['max']) / 2),
#         'beta': FloatSlider(min=params['beta']['min'], max=params['beta']['max'], step=0.1, value=(params['beta']['min'] + params['beta']['max']) / 2),
#         'Pmax': FloatSlider(min=params['Pmax']['min'], max=params['Pmax']['max'], step=0.001, value=(params['Pmax']['min'] + params['Pmax']['max']) / 2),
#         'Tlag': IntSlider(min=params['Tlag']['min'], max=params['Tlag']['max'], step=1, value=(params['Tlag']['min'] + params['Tlag']['max']) / 2),
#         'Kf': FloatSlider(min=params['Kf']['min'], max=params['Kf']['max'], step=0.01, value=(params['Kf']['min'] + params['Kf']['max']) / 2),
#         'Ks': FloatSlider(min=params['Ks']['min'], max=params['Ks']['max'], step=0.0001, value=(params['Ks']['min'] + params['Ks']['max']) / 2, readout_format='.3f')
#     }

#     # Combine sliders with their labels, and align them to the left
#     slider_widgets = [HBox([Label(value=name, layout=Layout(width='200px')), slider], layout={'align_items': 'flex-start'}) 
#                       for name, slider in sliders.items()]

#     # Function to be called when the "Recalculate" button is clicked
#     def on_button_click(b=None):
#         global param_change_counter
#         param_change_counter += 1
#         counter_display.value = f"<b>Attempts: {param_change_counter}</b>"
        
#         play_button.description = "Loading..."
        
#         out.clear_output(wait=True)
#         with out:
#             plot_hydrograph(
#                 Imax=sliders['Imax'].value, 
#                 Ce=sliders['Ce'].value, 
#                 Sumax=sliders['Sumax'].value, 
#                 beta=sliders['beta'].value, 
#                 Pmax=sliders['Pmax'].value, 
#                 Tlag=sliders['Tlag'].value, 
#                 Kf=sliders['Kf'].value, 
#                 Ks=sliders['Ks'].value,
#                 model=model, 
#                 forcing=forcing
#             )
        
#         # Update button text and recalculation status
#         play_button.description = "Recalculate"



#     # Attach the button click handler
#     play_button.on_click(on_button_click)

#     # Layout with sliders, recalculation status, and the recalculate button
#     ui = VBox([counter_display] + slider_widgets + [play_button])
#     out = interactive_output(lambda **kwargs: None, {})  # Empty output placeholder

#     display(ui, out)

#     # Plot the first time without incrementing the counter
#     out.clear_output(wait=True)
#     with out:
#         plot_hydrograph(
#             Imax=sliders['Imax'].value, 
#             Ce=sliders['Ce'].value, 
#             Sumax=sliders['Sumax'].value, 
#             beta=sliders['beta'].value, 
#             Pmax=sliders['Pmax'].value, 
#             Tlag=sliders['Tlag'].value, 
#             Kf=sliders['Kf'].value, 
#             Ks=sliders['Ks'].value,
#             model=model, 
#             forcing=forcing
#         )

# # Example usage in your notebook
# # interactive_plot(model, forcing, params)
