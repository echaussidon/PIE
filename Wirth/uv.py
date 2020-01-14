# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:41:43 2019
"""
import numpy as np
import constantes as c



def vitesses(theta, z_ref):                                        # calcule les vitesses à partir de theta
    Theta = np.fft.fft2(theta)                              # transformation de Fourier en 2D, utilisée pour le calcul de u
    ThetaU = np.copy(Theta)
    ThetaV = np.copy(Theta)                                 # copie de theta, utilisée pour le calcul de v
    for i in range(c.Nx):
        for j in range(c.Ny):
            if z_ref:
                factor_z = np.exp(-c.Nt * c.K[i][j] * np.abs(c.z_ref) / c.f)
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
    
def calcW(theta, u, v, u_z_ref, v_z_ref):
    Theta = np.fft.fft2(theta)
    ThetaX = np.copy(Theta)
    ThetaY = np.copy(Theta)
    for i in range(c.Nx):
        for j in range(c.Ny):
#            factor_z = (1 - np.exp(-c.Nt * K[i][j] * np.abs(c.z_ref) / c.f)) * np.exp(-c.Nt * K[i][j] * np.abs(c.z_ref) / c.f) * c.A / c.Nt
            factor_z = c.A / c.Nt * np.exp(-c.Nt * c.K[i][j] * np.abs(c.z_ref) / c.f)
            ThetaX[i][j] = ThetaX[i][j] * 1j * c.k[i] * factor_z
            ThetaY[i][j] = ThetaY[i][j] * 1j * c.l[j] * factor_z
    thetax = np.real(np.fft.ifft2(ThetaX))
    thetay = np.real(np.fft.ifft2(ThetaY))
#    w = u * thetax + v * thetay
    w = (u - u_z_ref) * thetax + (v - v_z_ref) * thetay
    return w