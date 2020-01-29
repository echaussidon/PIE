# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:25:57 2019
"""
import numpy as np
from scipy import interpolate
import constantes as c
import variables as var
import time_m

@time_m.time_measurement
def calc_thetatp1():
    ftheta = interpolate.interp2d(c.y, c.x, var.theta, kind='cubic')        # interpolation cubique de theta
    vftheta=np.vectorize(ftheta)

    X=np.tile(c.x,(c.Ny,1)).transpose()
    Y=np.tile(c.y, (c.Nx, 1))

    Xeval = np.remainder(X-var.alphax, c.Lx)                                #np.remainder: reste de la division euclidienne -> correspond aux cond. lim. périodiques.
    Yeval = np.remainder(Y-var.alphay, c.Ly)                                #Xeval et Yeval sont les coordonnées d'évaluation de theta

    var.thetatp1 = vftheta(Yeval,Xeval)
    var.theta = np.copy(var.thetatp1)                                       # mis à jour de theta

@time_m.time_measurement
def calc_DT_histtp1():
    fDT_hist = interpolate.interp2d(c.y, c.x, var.DT_hist, kind='cubic')    # interpolation cubique de theta
    vfDT_hist=np.vectorize(fDT_hist)

    X=np.tile(c.x,(c.Ny,1)).transpose()
    Y=np.tile(c.y, (c.Nx, 1))

    Xeval = np.remainder(X-var.alphax_z_ref, c.Lx)
    Yeval = np.remainder(Y-var.alphay_z_ref, c.Ly)

    var.DT_histtp1 = vfDT_hist(Yeval,Xeval)
    var.DT_hist = np.copy(var.DT_histtp1)                                   # mis à jour de theta


def calc_DT_disptp1():                                                  # avancement de DT_disp
    fDT_disp = interpolate.interp2d(c.y, c.x, var.DT_disp, kind='cubic')
    for i in range(c.Nx):
        for j in range(c.Ny):
            xeval = c.x[i] - var.alphax_z_ref[i][j]                     # couche en dessous, donc autres vitesses et autres alphas
            yeval = c.y[j] - var.alphay_z_ref[i][j]
            xeval,yeval = cond_lim(xeval, yeval)
            var.DT_disptp1[i][j] = fDT_disp( yeval, xeval ) + var.w[i][j] * c.dt * c.gamma2 # terme source = vitesse verticale
    var.DT_disp = np.copy(var.DT_disptp1)

def calc_DT_cloud():
    var.DT_cloud = np.zeros((c.Nx,c.Ny))
    var.DT_cloud[var.DT_disp / c.gamma2 > c.DelZc] = -5
        
def cond_lim(xeval, yeval):
    if xeval < c.x0:
        xeval = xeval + c.Lx
    elif xeval > c.x1:
        xeval = xeval - c.Lx
    if yeval < c.y0:
        yeval = yeval + c.Ly
    elif yeval > c.y1:
        yeval = yeval - c.Ly
    return xeval,yeval
