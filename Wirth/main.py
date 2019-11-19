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

# à changer
plot = 1                                                    # 0: pas de plots, 1: plots
dt = 0.5                                                    # pas de temps
Tend = 10                                                   # temps final (but: 48h)
Nx = 100                                                    # nombre de points en x
Ny = 100                                                    # ~ y
x0 = 0.                                                     # premier point en x
x1 = 2. * np.pi                                             # dernier point en x
y0 = 0.                                                     # ~ y
y1 = 2. * np.pi                                             # ~ y

# constantes physiques
g = 9.81
Ns = 0.02
Nt = 0.01
theta_ref = 300
A = g * (Ns - Nt) / (theta_ref * Ns * Nt)                   # constante défini arbitrairement

# à ne pas changer (sauf theta initial)
Nit = Tend/dt                                               # nombre d'itérations
dx = (x1-x0) / (Nx-1)                                       # pas en x
dy = (y1-y0) / (Ny-1)                                       # pas en y
x = np.arange(x0,x1+dx,dx)                                  # coordonnées x du maillage : [x0, x0+dx, ... x1]
y = np.arange(y0,y1+dy,dy)                                  # ~ y
Lx = x1 - x0                                                # longueur du domaine en x
Ly = y1 - y0                                                # ~ y
Y,X = meshgrid(y,x)                                         # pour les plots
theta = np.zeros((Nx,Ny))                                   # les inconnues à instant t
for i in range(Nx):
    for j in range(Ny):
        theta[i][j] = np.sin(x[i]/2)*np.sin(y[j]/2)
thetatp1 = np.copy(theta)                                   # les inconnues à instant t+dt (à calculer dans la boucle)
Theta = np.zeros((Nx,Ny))                                   # stockage pour transformation de Fourier
ThetaV = np.zeros((Nx,Ny))                                  # stockage pour transformation de Fourier
alphax = np.zeros((Nx,Ny))                                  # déplacements en x des particules de instant t à t+dt
alphay = np.zeros((Nx,Ny))                                  # ~ y

k = np.zeros((1,Nx))                                        # nombres d'onde en x
l = np.zeros((1,Ny))                                        # ~ y
K = np.zeros((Nx,Ny))                                       # magnitude de k et l (sqrt(k^2+l^2))

if np.mod(Nx,2) == 0:                                       # remplir k, ça diffère si N est pair ou impair
    # k = [0, 1, ... N/2 - 1, -N/2, -N/2 + 1, ... -1]
    k = np.concatenate((np.arange(0,Nx/2), np.arange(-Nx/2,0)))
else:
    # k = [0, 1, ... (N-1)/2 - 1, (N-1)/2, -(N-1)/2, -(N-1)/2 + 1, ... -1]
    k = np.concatenate((np.arange(0,(Nx-1)/2+1), np.arange(-(Nx-1)/2,0)))

if np.mod(Ny,2) == 0:                                       # ~ y
    l = np.concatenate((np.arange(0,Ny/2), np.arange(-Ny/2,0)))
else:
    l = np.concatenate((np.arange(0,(Ny-1)/2+1), np.arange(-(Ny-1)/2,0)))

for i in range(Nx):
    for j in range(Ny):
        K[i][j] = np.sqrt(k[i]**2 + l[j]**2)
    
###################################################
# code qui calcule les vitesses à partir de theta #
###################################################
def vitesses():
    Theta = np.fft.fft2(theta)                              # transformation de Fourier en 2D, utilisée pour le calcul de u
    ThetaV = np.copy(Theta)                                 # copie de theta, utilisée pour le calcul de v
    for i in range(Nx):
        for j in range(Ny):
            if K[i][j] != 0:
                ThetaV[i][j] = Theta[i][j] * 1j * k[i] * A / K[i][j]    # multiplication avec k[i] pour dérivée de x
                Theta[i][j] = Theta[i][j] * 1j * l[j] * A / K[i][j]     # multiplication avec l[j] pour dérivée de y
    u = np.real(np.fft.ifft2(Theta))                        # partie réelle de l'inverse de Fourier
    v = np.real(np.fft.ifft2(ThetaV))                       # ~ y
    return(u,v)

###############################
# initialisation des vitesses #
###############################
u,v = vitesses(theta)                                       # vitesses u et v à instant t
utm1,vtm1 = np.copy(u), np.copy(v)                          # vitesses u et v à instant t-dt (au début égale aux celles de t ?)
uloc = 0                                                    # vitesse u locale à instant t (utilisée dans la boucle)
vloc = 0                                                    # ~ v
uloctm1 = 0                                                 # vitesse u locale à instant t-dt
vloctm1 = 0                                                 # ~ v

#####################################
# initialisation des interpolations #
#####################################
fu = interpolate.interp2d(y, x, u, kind='linear')           # lineaire de u (nécessaire pour évaluer à X - alpha/2, hors maillage)
fv = interpolate.interp2d(y, x, v, kind='linear')           # ~ v
futm1 = fu                                                  # lineaire de utm1 (au début égale aux celle de t ?)
fvtm1 = fv                                                  # ~ v
ftheta = interpolate.interp2d(y, x, theta, kind='cubic')    # cubique de theta

################
# plot initial #
################
if plot:
    fig = plt.figure()
    plt.pcolor(X,Y,theta)
    plt.title('theta_0')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.show()
    
    fig = plt.figure()
    plt.pcolor(X,Y,u)
    plt.title('u_0')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.show()
    
    fig = plt.figure()
    plt.pcolor(X,Y,v)
    plt.title('v_0')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.show()
    
#######################
# avancement en temps #
#######################
for it in range(Nit):                                                   # itération en temps : avancement de t à t+dt
    ### calcul des alphas ###
    for a in range(2):                                                  # 2 itérations pour calcul de alphas
        u,v = vitesses(theta)                                           # calcul des vitesses à instant t
        fu = interpolate.interp2d(y, x, u, kind='linear')               # interpolation lineaire de u
        fv = interpolate.interp2d(y, x, v, kind='linear')               # ~ v
        
        for i in range(Nx):                                             # itération pour chaque point du maillage
            for j in range(Ny):
                xloc = x[i] - alphax[i][j]/2                            # coordonnée en x pour évaluation de la vitesse
                yloc = y[i] - alphay[i][j]/2                            # ~ y
                uloc = fu( yloc, xloc )                                 # évaluation de u à X - alpha/2
                vloc = fu( yloc, xloc )                                 # ~ v
                uloctm1 = futm1( yloc, xloc )                           # évaluation de utm1 à X - alpha/2      
                vloctm1 = futm1( yloc, xloc )                           # ~ v
                alphax[i][j] = dt * (1.5 * uloc - 0.5 * uloctm1)        # nouvelle estimation de alphax
                alphay[i][j] = dt * (1.5 * vloc - 0.5 * vloctm1)        # ~ y
    
    ### calcul de theta à instant t+dt ###
    for i in range(Nx):                                                 # itération pour chaque point du maillage
        for j in range(Ny):
            xeval = x[i] - alphax[i][j]                                 # coordonnée de x du point d'évaluation de theta
            yeval = y[j] - alphay[i][j]                                 # ~ y
            if xeval < x0:                                              # si ce point est hors du maillage:
                xeval = xeval + Lx                                      # rentrer le de l'autre côté
            elif xeval > x1:                                            # = conditions limites périodiques
                xeval = xeval - Lx
            if yeval < y0:
                yeval = yeval + Ly
            elif yeval > y1:
                yeval = yeval - Ly
            thetatp1[i][j] = ftheta( yeval, xeval ) # évaluation à Xo = Xn - alpha
    
    ### mis à jour des valeurs à t moins 1 ###
    utm1 = np.copy(u)
    vtm1 = np.copy(v)
    theta = np.copy(thetatp1)
    futm1 = fu
    fvtm1 = fv
    ftheta = interpolate.interp2d(y, x, theta, kind='cubic')
    
    ### plots
    if plot:
        fig = plt.figure()
        plt.pcolor(X,Y,theta)
        plt.title('theta_' + str(it+1))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar()
        plt.show()

        fig = plt.figure()
        plt.pcolor(X,Y,u)
        plt.title('u_' + str(it+1))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar()
        plt.show()

        fig = plt.figure()
        plt.pcolor(X,Y,v)
        plt.title('v_' + str(it+1))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar()
        plt.show()
