# Welcome to ENVM1502

This is a [teachbook](http://www.ewatercycle.org/teaching-materials/main), the intended way to experience this repo is through this website.
This teachbook makes use of interactive elements. The elements in chapters 1 and 3 will run in the browser using [the online version](http://www.ewatercycle.org/teaching-materials/main). 
The elements in chapter 2 need to executed on a jupyterhub that is running on a machine that support the ewatercycle platform. See [details](https://ewatercycle.readthedocs.io/en/latest/index.html). 
The "jupyterhub" button points to a server that is only accessable to students of ENVM1502 at the Technical University of Delft. If you want to set up your own server for your own class, contact us at question@ewatercycle.org

In the first chapter we will cover how to make a HBV model.
In chapter two we will take you through your own HBV implementation and how to calibrate and use generate CMIP data for HBV.
Chapter three explains to concept of flextopo.

This repository works on an [eWaterCycle machine](https://envm1502.ewatercycle-tud.src.surf-hosted.nl/) but uses a local version of the HBV model. 
This is done so that it does not open a relatively high cost container per model run.
Use the [eWaterCycle machine](https://envm1502.ewatercycle-tud.src.surf-hosted.nl/) to log in using your username/groupname and password.

For questions about the course please email:
 1. Markus Hrachowitz: m.hrachowitz@tudelft.nl
 2. Nick van de Giesen: n.c.vandegiesen@tudelft.nl
 3. Rolf Hut: r.w.hut@tudelft.nl
 
 Techinical questions about this repo and if things do not work:
 - Mark Melotto: m.melotto@tudelft.nl

The course can be found in the folder `book`, this is where you will find the following structure:

## Chapter 1: modelling introduction HBV

### Modelling exercise 1: Linear Reservoir
This is where we get familiar with hydrological bucket modelling.

### Models Exercise 2: Lumped Conceptual Model
Here you make your first HBV model implementation.

## Chapter 2: modelling eWaterCycle

### Exercise 1. Test your own HBV model on eWaterCycle
Having learnt how to make a working HBV model you will now learn to make it BMI compatible and test your own implementation.

### Exercise 2. Generate forcing for any region from ERA5 for HBV model
Using your own shape file you can load in ERA5 data for a HBV model.

### Exercise 3: Run HBV model with ERA5 forcing and GRDC observation
Run your own HBV region model and compare it to observations.

### Exercise 4: Calibrate HBV model with ERA5 forcing and GRDC observation
Calibrate your own HBV region model and compare it to observations.

### Exercise 5: Generate forcing for any region from CMIP6 for HBV model
We will learn to generate CMIP6 forcing for your research question.

## Chapter 3: modelling flextopo
Here we will look into modelling/calibrating different parts of your region (hillslopes, plateaus, wetlands and basins).
