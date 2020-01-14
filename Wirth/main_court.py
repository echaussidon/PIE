# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019
"""
import constantes as c
import plots
import alphas
import save_data
import avancement as av

import tqdm as tqdm

# plot initial
plots.plots(0)
savefile, savetheta, savetime = save_data.initialisation(filename=c.savefilename)

# avancement en temps
for itplot in tqdm.tqdm(range(c.Nitplot)):                                 # itérations avec plot
    for itnoplot in range(c.Nitnoplot):                         # itérations sans plot
        it = itplot*c.Nitnoplot + itnoplot + 1                  # numéro d'itération
        temps = it*c.dt/60./60.                                 # temps en heures

        alphas.calc_alpha()                                     # calcul des alphas
        alphas.calc_alpha_z_ref()

        av.calc_thetatp1()                                      # avancement en temps
        av.calc_DT_histtp1()
    # plots
    plots.plots(temps)
    save_data.save_step(savetheta, savetime, temps, itplot)

save_data.close_file(savefile)
