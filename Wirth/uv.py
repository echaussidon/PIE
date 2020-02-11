# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:41:43 2019
"""
import numpy as np
import constantes as c
import time_m

#@time_m.time_measurement
def vitesses(theta, z_ref):                                   # calcule les vitesses à partir de theta
    ThetaU = np.fft.fft2(theta)                               # transformation de Fourier en 2D, utilisée pour le calcul de u
    ThetaV = np.copy(ThetaU)                                  # copie de theta, utilisée pour le calcul de v

    factor_z = np.exp(-c.Nt * c.K * np.abs(c.z_ref) / c.f)
    ThetaV = np.where(c.K != 0, ThetaV*1j*c.k*c.A/c.K, np.zeros((c.Nx,c.Ny))) #le runetime qui peut s'afficher n'est pas très important (car l'endroit ou l'erreur est déclarée, on ne conserve pas la valeur)
    ThetaU = np.where(c.K != 0, -ThetaU*1j*c.l*c.A/c.K, np.zeros((c.Nx,c.Ny)))

    if(z_ref):
        ThetaV = ThetaV*factor_z
        ThetaU = ThetaU*factor_z

    u = np.real(np.fft.ifft2(ThetaU))                         # partie réelle de l'inverse de Fourier
    v = np.real(np.fft.ifft2(ThetaV))                         # ~ y
    return u, v
