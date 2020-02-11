# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:52:44 2019
"""
import numpy as np

# tous les paramètres sont en unités SI

# à changer
init = 2                                        # condition initiale de init_theta
dt = 600                                        # pas de temps (s)
Tend = 48*60*60                                 # temps final (but: 48h) (s)
tplot = 3600                                    # fréquence des plots (un plot chaque tplot) (s)
Nx = 256                                        # nombre de points en x
Ny = 128                                        # ~ y
x0 = 0.                                         # premier point en x (m)
x1 = 2048*1000                                  # dernier point en x (m)
y0 = 0.                                         # ~ y (m)
y1 = 1024*1000                                  # ~ y (m)
folder = "folder"                               # dossier pour sauver les figures
savefig = True                                  # sauver les figures
showfig = False                                 # afficher les figures
plot_theta = True                               # faire le plot de theta ou non
plot_vitesses = True                            # ~ vitesses
plot_WV = True                                  # ~ image vapeur d'eau
plot_all = False                                # tout sur une figure
savefilename = "simulation_ini_0.nc"            # nom du fichier où son sauvegarder les données en netcdf
print_time_measurement = False                  # affiche le temps d'execution de chaque fonction

# à ne pas changer
Nit = int(Tend/dt)                              # nombre d'itérations
Nitnoplot = int(tplot/dt)                       # nombre d'itérations sans plot
Nitplot = int(Nit/Nitnoplot)                    # nombre d'itérations avec plot
dx = (x1-x0) / (Nx-1)                           # pas en x
dy = (y1-y0) / (Ny-1)                           # pas en y
x = np.arange(x0,x1+dx,dx)                      # coordonnées x du maillage : [x0, x0+dx, ... x1]
y = np.arange(y0,y1+dy,dy)                      # ~ y
X = np.tile(x,(Ny,1)).transpose()               # construction d'une matrice dont les lignes sont toutes égales au vecteur c.x
Y = np.tile(y, (Nx, 1))                         # construction d'une matrice dont les colonnes sont toutes égales au vecteur c.y
Lx = x1 - x0                                    # longueur du domaine en x
Ly = y1 - y0                                    # ~ y
Yplot,Xplot = np.meshgrid(y,x)                  # pour les plots

# nombres d'onde
if np.mod(Nx,2) == 0:                                       # remplir k, ça diffère si N est pair ou impair
    # k = [0, 1, ... N/2 - 1, -N/2, -N/2 + 1, ... -1]
    k = np.concatenate((np.arange(0,Nx/2), np.arange(-Nx/2,0)))*2*np.pi/Lx
else:
    # k = [0, 1, ... (N-1)/2 - 1, (N-1)/2, -(N-1)/2, -(N-1)/2 + 1, ... -1]
    k = np.concatenate((np.arange(0,(Nx-1)/2+1), np.arange(-(Nx-1)/2,0)))*2*np.pi/Lx

if np.mod(Ny,2) == 0:                                       # ~ y
    l = np.concatenate((np.arange(0,Ny/2), np.arange(-Ny/2,0)))*2*np.pi/Ly
else:
    l = np.concatenate((np.arange(0,(Ny-1)/2+1), np.arange(-(Ny-1)/2,0)))*2*np.pi/Ly

k = np.tile(k,(Ny,1)).transpose()                       #matrice [k,k,...,k]
l = np.tile(l,(Nx,1))
K = np.sqrt(k**2+l**2)

# constantes physiques
g = 9.81
Ns = 0.02
Nt = 0.01
theta_ref = 300
f = 1e-4
z_ref = -500                                    # niveau de la couche en dessous (m)
gamma1 = -4e-3
gamma2 = -8.5e-3
DelZc = 500
A = g * (Ns - Nt) / (theta_ref * Ns * Nt)       # constante défini arbitrairement
