# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019
"""
import constantes as c
import plots
import alphas
import save_data
import avancement
import w
import tqdm as tqdm

# plots initials
plots.plots(0)
savefile, savetheta, savetime = save_data.initialisation(filename=c.savefilename)

# avancement en temps
for itplot in tqdm.tqdm(range(c.Nitplot)):                      # itérations avec plot
    for itnoplot in range(c.Nitnoplot):                         # itérations sans plot
        it = itplot*c.Nitnoplot + itnoplot + 1                  # numéro d'itération
        temps = it*c.dt/60./60.                                 # temps en heures

        if c.print_time_measurement :
            print("\nit = {} / {}, t = {} h".format(it, c.Nitplot*c.Nitnoplot, temps))

        alphas.calc_alpha()                                     # calcul des alphas
        alphas.calc_alpha_z_ref()                               # calcul des alphas

        avancement.calc_thetatp1()

        w.calcW()                                               # calcul des vitesses verticales

        avancement.calc_DT()                                    # calcul image vapeur d'eau

    # plots
    plots.plots(temps)
    save_data.save_step(savetheta, savetime, temps, itplot)

save_data.close_file(savefile)