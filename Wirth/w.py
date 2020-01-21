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
    # calcul de theta sur la couche en dessous (z_ref)
    # fft de theta
    Theta = np.fft.fft2(var.theta)
    # combinaison des équations (4), (5), (6) et (8)
    theta_z_ref = np.real(np.fft.ifft2(c.theta_ref * c.A * c.Nt / c.g * Theta * np.exp(-c.Nt * c.K / c.f * np.abs(c.z_ref))))
    # pareil pour l'étape précédente (en temps)
    Thetatm1 = np.fft.fft2(var.thetatm1) 
    theta_z_reftm1 = np.real(np.fft.ifft2(c.theta_ref * c.A * c.Nt / c.g * Thetatm1 * np.exp(-c.Nt * c.K / c.f * np.abs(c.z_ref))))
    
    # calcul des alphas sur z_ref
    alphas.calc_alpha_z_ref()
    
    # interpolation des thetas précédents pour estimation de la dérivée totale de l'équation (10)
    f = interpolate.interp2d(c.y, c.x, theta_z_reftm1, kind='cubic')
    vf=np.vectorize(f)
    
    # méthode semi-Lagrangienne à l'inverse pour calcul de w
    X=np.tile(c.x,(c.Ny,1)).transpose()
    Y=np.tile(c.y, (c.Nx, 1))
        
    Xloc=np.remainder(X-var.alphax_z_ref, c.Lx)
    Yloc=np.remainder(Y-var.alphay_z_ref, c.Ly)
    var.w = c.g / c.Nt**2 / c.theta_ref * (vf(Yloc, Xloc) - theta_z_ref) / c.dt