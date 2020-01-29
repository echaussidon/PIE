# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019
"""
import constantes as c
import plots
import alphas
import avancement

# plot initial
plots.plots(0)

# avancement en temps
for itplot in range(c.Nitplot):                                 # itérations avec plot
    for itnoplot in range(c.Nitnoplot):                         # itérations sans plot
        it = itplot*c.Nitnoplot + itnoplot + 1                  # numéro d'itération
        temps = it*c.dt/60./60.                                 # temps en heures
        print("\nit = {} / {}, t = {} h".format(it, c.Nitplot*c.Nitnoplot, temps))’

        alphas.calc_alpha()                                     # calcul des alphas
        alphas.calc_alpha_z_ref()                               # calcul des alphas

        avancement.calc_thetatp1()                                      # avancement en temps
        avancement.calc_DT_histtp1()                                    # avancement en temps

    # plots
    plots.plots(temps)
