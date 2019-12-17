# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:41:43 2019
"""
import numpy as np
import constantes as c

k = np.zeros((1,c.Nx))                                        # nombres d'onde en x
l = np.zeros((1,c.Ny))                                        # ~ y
K = np.zeros((c.Nx,c.Ny))                                     # magnitude de k et l (sqrt(k^2+l^2))

if np.mod(c.Nx,2) == 0:                                       # remplir k, ça diffère si N est pair ou impair
    # k = [0, 1, ... N/2 - 1, -N/2, -N/2 + 1, ... -1]
    k = np.concatenate((np.arange(0,c.Nx/2), np.arange(-c.Nx/2,0)))*2*np.pi/c.Lx
else:
    # k = [0, 1, ... (N-1)/2 - 1, (N-1)/2, -(N-1)/2, -(N-1)/2 + 1, ... -1]
    k = np.concatenate((np.arange(0,(c.Nx-1)/2+1), np.arange(-(c.Nx-1)/2,0)))*2*np.pi/c.Lx

if np.mod(c.Ny,2) == 0:                                       # ~ y
    l = np.concatenate((np.arange(0,c.Ny/2), np.arange(-c.Ny/2,0)))*2*np.pi/c.Ly
else:
    l = np.concatenate((np.arange(0,(c.Ny-1)/2+1), np.arange(-(c.Ny-1)/2,0)))*2*np.pi/c.Ly

for i in range(c.Nx):
    for j in range(c.Ny):
        K[i][j] = np.sqrt(k[i]**2 + l[j]**2)

def vitesses(theta):                                        # calcule les vitesses à partir de theta
    Theta = np.fft.fft2(theta)                              # transformation de Fourier en 2D, utilisée pour le calcul de u
    ThetaV = np.copy(Theta)                                 # copie de theta, utilisée pour le calcul de v
    for i in range(c.Nx):
        for j in range(c.Ny):
            if K[i][j] != 0:
                ThetaV[i][j] = ThetaV[i][j] * 1j * k[i] * c.A / K[i][j]    # multiplication avec k[i] pour dérivée de x
                Theta[i][j] = -Theta[i][j] * 1j * l[j] * c.A / K[i][j]     # multiplication avec l[j] pour dérivée de y
            else:
                ThetaV[i][j] = 0
                Theta[i][j] = 0
    u = np.real(np.fft.ifft2(Theta))                        # partie réelle de l'inverse de Fourier
    v = np.real(np.fft.ifft2(ThetaV))                       # ~ y
#    print('min u: ' + str(np.min(u)))
#    print('max u: ' + str(np.max(u)))
#    print('min v: ' + str(np.min(v)))
#    print('max v: ' + str(np.max(v)))
    return(u,v)