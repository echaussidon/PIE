# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:41:43 2019
"""
import numpy as np
import constantes as c



def vitesses(theta, z_ref):                                 # calcule les vitesses à partir de theta, z_ref: False si tropopause, true si couche en dessous
    Theta = np.fft.fft2(theta)                              # transformation de Fourier en 2D
    ThetaU = np.copy(Theta)                                 # copie pour calcul de u
    ThetaV = np.copy(Theta)                                 # copie pour calcul de v
    for i in range(c.Nx):
        for j in range(c.Ny):
            if z_ref:                                       # si sur z_ref:
                factor_z = np.exp(-c.Nt * c.K[i][j] * np.abs(c.z_ref) / c.f) # facteur en z n'est plus égale à 1 (éq 4)
            else:
                factor_z = 1
            if c.K[i][j] != 0:
                ThetaV[i][j] = ThetaV[i][j] * 1j * c.k[i] * c.A / c.K[i][j] * factor_z   # multiplication avec k[i] pour dérivée de x
                ThetaU[i][j] = -ThetaU[i][j] * 1j * c.l[j] * c.A / c.K[i][j] * factor_z    # multiplication avec l[j] pour dérivée de y
            else:
                ThetaV[i][j] = 0
                ThetaU[i][j] = 0
    u = np.real(np.fft.ifft2(ThetaU))                        # partie réelle de l'inverse de Fourier
    v = np.real(np.fft.ifft2(ThetaV))                       # ~ y
    return(u,v)