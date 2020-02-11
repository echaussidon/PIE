# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:25:57 2019
"""
import numpy as np
from scipy import interpolate
import constantes as c
import variables as var
import time_m
from scipy.interpolate import RectBivariateSpline


@time_m.time_measurement
def calc_thetatp1():
    
    ftheta = RectBivariateSpline(c.x, c.y, var.theta)

    Xeval = np.remainder(c.X-var.alphax, c.Lx)                                # np.remainder: reste de la division euclidienne -> correspond aux cond. lim. périodiques.
    Yeval = np.remainder(c.Y-var.alphay, c.Ly)                                # Xeval et Yeval sont les coordonnées d'évaluation de theta

    var.thetatp1 = ftheta(Xeval,Yeval, grid = False)
    var.thetatm1 = np.copy(var.theta)                                       # mise à jour de theta à t-dt (utilisé pour calcul de w)
    var.theta = np.copy(var.thetatp1)                                       # mise à jour de theta
    
    
@time_m.time_measurement 
def calc_DT():
    fDT_hist = RectBivariateSpline(c.x, c.y, var.DT_hist)
    fDT_disp = RectBivariateSpline(c.x, c.y, var.DT_disp)

    Xeval = np.remainder(c.X-var.alphax_z_ref, c.Lx)
    Yeval = np.remainder(c.Y-var.alphay_z_ref, c.Ly)

    var.DT_hist = fDT_hist(Xeval,Yeval, grid = False)
    var.DT_disp = fDT_disp(Xeval,Yeval, grid = False) + var.w * c.dt * c.gamma2
       
    var.DT_cloud = np.zeros((c.Nx,c.Ny))
    var.DT_cloud[var.DT_disp / c.gamma2 > c.DelZc] = -5