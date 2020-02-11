# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 16:51:25 2020
"""

import numpy as np
#from scipy import interpolate
from scipy.interpolate import RectBivariateSpline
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
    f = RectBivariateSpline(c.x, c.y, theta_z_reftm1)
    
    # méthode semi-Lagrangienne à l'inverse pour calcul de w
    Xloc=np.remainder(c.X-var.alphax_z_ref, c.Lx)
    Yloc=np.remainder(c.Y-var.alphay_z_ref, c.Ly)
    var.w = c.g / c.Nt**2 / c.theta_ref * (f(Xloc, Yloc, grid = False) - theta_z_ref) / c.dt