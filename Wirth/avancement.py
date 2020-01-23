# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:25:57 2019
"""
import numpy as np
from scipy import interpolate
import constantes as c
import variables as var

def calc_thetatp1():                                                    # avancement de theta
    ftheta = interpolate.interp2d(c.y, c.x, var.theta, kind='cubic')    # interpolation cubique de theta
    for i in range(c.Nx):                                               # itération pour chaque point du maillage
        for j in range(c.Ny):
            xeval = c.x[i] - var.alphax[i][j]                           # coordonnée de x du point d'évaluation de theta
            yeval = c.y[j] - var.alphay[i][j]                           # ~ y
            xeval,yeval = cond_lim(xeval, yeval)                       # conditions aux limites
            var.thetatp1[i][j] = ftheta( yeval, xeval )                 # évaluation à Xo = Xn - alpha
    var.thetatm1 = np.copy(var.theta)                                   # mise à jour de theta à t-dt
    var.theta = np.copy(var.thetatp1)                                   # mise à jour de theta
    
def calc_DT_histtp1():                                                  # avancement de DT_hist
    fDT_hist = interpolate.interp2d(c.y, c.x, var.DT_hist, kind='cubic')    
    for i in range(c.Nx):                                               
        for j in range(c.Ny):
            xeval = c.x[i] - var.alphax_z_ref[i][j]                     # couche en dessous, donc autres vitesses et autres alphas
            yeval = c.y[j] - var.alphay_z_ref[i][j]                     
            xeval,yeval = cond_lim(xeval, yeval)                        
            var.DT_histtp1[i][j] = fDT_hist( yeval, xeval )             # pas de terme de source
    var.DT_hist = np.copy(var.DT_histtp1)                                   
    
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