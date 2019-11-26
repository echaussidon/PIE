# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019
"""
import constantes as c
import plots
import alphas
import avancement as av

# plot initial
plots.plots(c.plot_theta,c.plot_vitesses,0)

# avancement en temps
for itplot in range(c.Nitplot):                                 # itérations avec plot
    for itnoplot in range(c.Nitnoplot):                         # itérations sans plot
        it = itplot*c.Nitnoplot + itnoplot + 1                  # numéro d'itération
        print("it = {}, t = {}".format(it,it*c.dt/60./60.))     # print it et temps
        print("calcul des alphas")
        alphas.calc_alpha()                                     # calcul des alphas
        print("avancement en temps")                                
        av.calc_thetatp1()                                      # avancement en temps
    # plots
    plots.plots(c.plot_theta,c.plot_vitesses,0)