# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:51:25 2020
"""

import numpy as np
from scipy import interpolate
import constantes as c
import variables as var
import alphas

def calcW():
    Theta = np.fft.fft2(var.theta) 
    theta_z_ref = np.real(np.fft.ifft2(c.theta_ref * c.A * c.Nt / c.g * Theta * np.exp(-c.Nt * c.K / c.f * np.abs(c.z_ref))))
    Thetatm1 = np.fft.fft2(var.thetatm1) 
    theta_z_reftm1 = np.real(np.fft.ifft2(c.theta_ref * c.A * c.Nt / c.g * Thetatm1 * np.exp(-c.Nt * c.K / c.f * np.abs(c.z_ref))))
    
    # calcul des alphas
    alphas.calc_alpha_z_ref()
    
    f = interpolate.interp2d(c.y, c.x, theta_z_reftm1, kind='cubic')
    
    for i in range(c.Nx):
        for j in range(c.Ny):
            xeval = c.x[i] - var.alphax_z_ref[i][j]                           # coordonnée de x du point d'évaluation de theta
            yeval = c.y[j] - var.alphay_z_ref[i][j]                           # ~ y
            if xeval < c.x0:                                            # si ce point est hors du maillage:
                xeval = xeval + c.Lx                                    # rentrer le de l'autre côté
            elif xeval > c.x1:                                          # = conditions limites périodiques
                xeval = xeval - c.Lx
            if yeval < c.y0:
                yeval = yeval + c.Ly
            elif yeval > c.y1:
                yeval = yeval - c.Ly
            var.w[i][j] = c.g / c.Nt**2 / c.theta_ref * (f(yeval, xeval) - theta_z_ref[i][j]) / c.dt