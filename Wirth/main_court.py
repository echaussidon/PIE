# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019
"""
import constantes as c
import plots
import alphas
import avancement as av
import w

# plots initials
plots.plots(0)                                   
plots.plotDT(0)

# avancement en temps
for itplot in range(c.Nitplot):                                 # itérations avec plot
    for itnoplot in range(c.Nitnoplot):                         # itérations sans plot
        it = itplot*c.Nitnoplot + itnoplot + 1                  # numéro d'itération
        temps = it*c.dt/60./60.                                 # temps en heures
        print("it = {}, t = {}".format(it,temps))               # print it et temps
        print("calcul des alphas")
        alphas.calc_alpha()                                     # calcul des alphas
        alphas.calc_alpha_z_ref()                               # calcul des alphas sur la couche en dessous
        
        print("avancement en temps")                               
        av.calc_thetatp1()                                      # avancement en temps pour theta
        w.calcW()                                               # calcul des vitesses verticales

        av.calc_DT_histtp1()                                    # calcul de DT_hist
        av.calc_DT_disptp1()                                    # calcul de DT_disp
        av.calc_DT_cloud()
        
    # plots
    plots.plots(temps)
    plots.plotDT(temps)