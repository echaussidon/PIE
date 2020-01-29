# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:41:43 2019
"""
import numpy as np
import constantes as c
import time_m

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



k_mat = np.tile(k,(c.Ny,1)).transpose()                       #matrice [k,k,...,k]
l_mat = np.tile(l,(c.Nx,1))
K = np.sqrt(k_mat**2+l_mat**2)

#@time_m.time_measurement
def vitesses(theta, z_ref):                                   # calcule les vitesses à partir de theta
    ThetaU = np.fft.fft2(theta)                               # transformation de Fourier en 2D, utilisée pour le calcul de u
    ThetaV = np.copy(ThetaU)                                  # copie de theta, utilisée pour le calcul de v

    factor_z = np.exp(-c.Nt * K * np.abs(c.z_ref) / c.f)
    ThetaV=np.where(K != 0, ThetaV*1j*k_mat*c.A/K, np.zeros((c.Nx,c.Ny)))
    ThetaU=np.where(K != 0, -ThetaU*1j*l_mat*c.A/K, np.zeros((c.Nx,c.Ny)))

    if(z_ref):
        ThetaV = ThetaV*factor_z
        ThetaU = ThetaU*factor_z

    u = np.real(np.fft.ifft2(ThetaU))                         # partie réelle de l'inverse de Fourier
    v = np.real(np.fft.ifft2(ThetaV))                         # ~ y
    return u, v
