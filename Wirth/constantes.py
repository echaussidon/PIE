# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:52:44 2019
"""
import numpy as np

# tous les paramètres sont en unités SI

# à changer
init = 2                                        # condition initiale de init_theta
dt = 900                                        # pas de temps (s)
Tend = 48*60*60                                 # temps final (but: 48h) (s)
tplot = 3600                                    # fréquence des plots (un plot chaque tplot) (s)
Nx = 256                                        # nombre de points en x
Ny = 128                                        # ~ y
x0 = 0.                                         # premier point en x (m)
x1 = 2048*1000                                  # dernier point en x (m)
y0 = 0.                                         # ~ y (m)
y1 = 1024*1000                                  # ~ y (m)
folder = "folder"                               # dossier pour sauver les figures
savefig = 0                                     # sauver ou montrer les figures
plot_theta = 1                                  # faire le plot de theta ou non
plot_vitesses = 1                               # ~ vitesses
plot_all = 0                                    # tout sur une figure

# à ne pas changer
Nit = int(Tend/dt)                              # nombre d'itérations
Nitnoplot = int(tplot/dt)                       # nombre d'itérations sans plot
Nitplot = int(Nit/Nitnoplot)                    # nombre d'itérations avec plot
dx = (x1-x0) / (Nx-1)                           # pas en x
dy = (y1-y0) / (Ny-1)                           # pas en y
x = np.arange(x0,x1+dx,dx)                      # coordonnées x du maillage : [x0, x0+dx, ... x1]
y = np.arange(y0,y1+dy,dy)                      # ~ y
Lx = x1 - x0                                    # longueur du domaine en x
Ly = y1 - y0                                    # ~ y
Y,X = np.meshgrid(y,x)                          # pour les plots

# constantes physiques
g = 9.81
Ns = 0.02
Nt = 0.01
theta_ref = 300
A = g * (Ns - Nt) / (theta_ref * Ns * Nt)       # constante défini arbitrairement