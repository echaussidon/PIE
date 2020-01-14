# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019
"""
import constantes as c
import plots
import alphas
import avancement as av
import time

# plot initial
plots.plots(0)

# avancement en temps
for itplot in range(c.Nitplot):                                 # itérations avec plot
    for itnoplot in range(c.Nitnoplot):                         # itérations sans plot
        
        print("\n\n\n")
        it = itplot*c.Nitnoplot + itnoplot + 1                  # numéro d'itération
        temps = it*c.dt/60./60.                                 # temps en heures
        print("it = {}, t = {}".format(it,temps))               # print it et temps
        
        
        print("calcul des alphas")
        start_alpha = time.time()
        alphas.calc_alpha() 
        print("temps calcul alphas: " +  str(time.time()-start_alpha))                               # calcul des alphas
        
        
        start_alpha_z_ref = time.time()        
        alphas.calc_alpha_z_ref()
        print("temps calcul alphas_z_ref: " +  str(time.time()-start_alpha_z_ref))                               # calcul des alphas        
        
        print("avancement en temps")                                
        start_calc_thetatp1 = time.time()
        av.calc_thetatp1()                                      # avancement en temps
        print("temps calcul thetatp1: " +  str(time.time()-start_calc_thetatp1))
        start_calc_DT_histtp1 = time.time()        
        av.calc_DT_histtp1()
        print("temps calcul DT_histtp1: " +  str(time.time()-start_calc_DT_histtp1))
    # plots
    plots.plots(temps)
