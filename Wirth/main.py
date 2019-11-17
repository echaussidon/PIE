# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:45:56 2019

@author: Jan
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy import interpolate

###################
# initialisations #
###################

dt = 1                                                      # pas de temps
Tend = 0                                                    # temps final (but: 48h)
Nit = Tend/dt                                               # nombre d'itérations

Nx = 100                                                    # nombre de points en x
Ny = 50                                                     # ~ y
x0 = 0.                                                     # premier point en x
x1 = 2. * np.pi                                             # dernier point en x
y0 = 0.                                                     # ~ y
y1 = 2. * np.pi                                             # ~ y
dx = (x1-x0) / (Nx-1)                                       # pas en x
dy = (y1-y0) / (Ny-1)                                       # pas en y
x = np.arange(x0,x1+dx,dx)                                  # coordonnées x du maillage : [x0, x0+dx, ... x1]
y = np.arange(y0,y1+dy,dy)                                  # ~ y

theta = np.zeros((Nx,Ny))                                   # les inconnues à instant t
for i in range(Nx):
    for j in range(Ny):
        theta[i][j] = np.sin(x[i])
thetatp1 = np.copy(theta)                                   # les inconnues à instant t+dt (à calculer dans la boucle)
alphax = np.zeros((Nx,Ny))                                  # déplacements en x des particules de instant t à t+dt
alphay = np.zeros((Nx,Ny))                                  # ~ y

k = []                                                      # nombres d'onde en x
l = []                                                      # ~ y

if np.mod(Nx,2) == 0: # ça diffère si N est pair ou impair
    # k = [0, 1, ... N/2 - 1, -N/2, -N/2 + 1, ... -1]
    k.append(np.arange(0,Nx/2))
    k.append(np.arange(-Nx/2+1,0))
else:
    # k = [0, 1, ... (N-1)/2 - 1, (N-1)/2, -(N-1)/2, -(N-1)/2 + 1, ... -1]
    k.append(np.arange(0,(Nx-1)/2+1))
    k.append(np.arange(-(Nx-1)/2,0))

if np.mod(Ny,2) == 0:
    l.append(np.arange(0,Ny/2))
    l.append(np.arange(-Ny/2+1,0))
else:
    l.append(np.arange(0,(Ny-1)/2+1))
    l.append(np.arange(-(Ny-1)/2,0))

# constantes physiques
g = 9.81
Ns = 0
Nt = 0
theta_ref = 0
A = g * (Ns - Nt) / (theta_ref * Ns * Nt)                   # constante défini arbitrairement

###################################################
# code qui calcule les vitesses à partir de theta #
###################################################
def vitesses():
    u = []
    v = []
    return(u,v)

###############################
# initialisation des vitesses #
###############################
u,v = vitesses(theta)                                       # vitesses u et v à instant t
utm1,vtm1 = u,v                                             # vitesses u et v à instant t-dt (au début égale aux celles de t ?)
uloc = 0                                                    # vitesse u locale à instant t (utilisée dans la boucle)
vloc = 0                                                    # ~ v
uloctm1 = 0                                                 # vitesse u locale à instant t+dt
vloctm1 = 0                                                 # ~ v

#####################################
# initialisation des interpolations #
#####################################
fu = interpolate.interp2d(x, y, u, kind='linear')           # lineaire de u (nécessaire pour évaluer à X - alpha/2, hors maillage)
fv = interpolate.interp2d(x, y, v, kind='linear')           # ~ v
futm1 = fu                                                  # lineaire de utm1 (au début égale aux celle de t ?)
fvtm1 = fv                                                  # ~ v
ftheta = interpolate.interp2d(x, y, theta, kind='cubic')    # cubique de theta

#######################
# avancement en temps #
#######################
for it in range(Nit):                                       # itération en temps : avancement de t à t+dt
    ### calcul des alphas ###
    for a in range(2):                                      # 2 itérations pour calcul de alphas
        u,v = vitesses(theta)                               # calcul des vitesses à instant t
        fu = np.interp2d(u)                                 # interpolation lineaire de u
        fv = np.interp2d(v)                                 # ~ v
        
        for i in range(Nx):                                 # itération pour chaque point du maillage
            for j in range(Ny):
                uloc = fu( x[i] - alphax/2, y[i] - alphay/2 )           # évaluation de u à X - alpha/2
                vloc = fu( x[i] - alphax/2, y[i] - alphay/2 )           # ~ v
                uloctm1 = futm1( x[i] - alphax/2, y[i] - alphay/2 )     # évaluation de utm1 à X - alpha/2      
                vloctm1 = futm1( x[i] - alphax/2, y[i] - alphay/2 )     # ~ v
                alphax[i][j] = dt * (1.5 * uloc - 0.5 * uloctm1)        # nouvelle estimation de alphax
                alphay[i][j] = dt * (1.5 * vloc - 0.5 * vloctm1)        # ~ y
    
    ### calcul de theta à instant t+dt ###
    for i in range(Nx):                                     # itération pour chaque point du maillage
        for j in range(Ny):
            thetatp1[i][j] = ftheta( (x[i] - alphax[i][j]), (y[j] - alphay[i][j]) ) # évaluation à Xo = Xn - alpha
    
    ### mis à jour des valeurs à t moins 1 ###
    utm1 = u
    vtm1 = v
    theta = np.copy(thetatp1)
    futm1 = fu
    fvtm1 = fv
    ftheta = np.interp2d(theta)
        
#########
# plots #
#########
x,y = np.meshgrid(y,x)

fig = plt.figure()
plt.pcolor(x,y,theta)
plt.title('theta')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()