# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:25:57 2019
"""
import numpy as np
from scipy import interpolate
import constantes as c
import variables as var

def calc_thetatp1():
    ftheta = interpolate.interp2d(c.y, c.x, var.theta, kind='cubic')    # interpolation cubique de theta
    vftheta=np.vectorize(ftheta)
    
    X=np.tile(c.x,(c.Ny,1)).transpose()
    Y=np.tile(c.y, (c.Nx, 1))                      
    
    Xeval = np.remainder(X-var.alphax, c.Lx)        #np.remainder: reste de la division euclidienne -> correspond aux cond. lim. périodiques.
    Yeval = np.remainder(Y-var.alphay, c.Ly)        #Xeval et Yeval sont les coordonnées d'évaluation de theta
    
    var.thetatp1 = vftheta(Yeval,Xeval)
    
    var.theta = np.copy(var.thetatp1)                                   # mis à jour de theta
    
def calc_DT_histtp1():
    fDT_hist = interpolate.interp2d(c.y, c.x, var.DT_hist, kind='cubic')    # interpolation cubique de theta
    vfDT_hist=np.vectorize(fDT_hist)
    
    X=np.tile(c.x,(c.Ny,1)).transpose()
    Y=np.tile(c.y, (c.Nx, 1))
    
    Xeval = np.remainder(X-var.alphax_z_ref, c.Lx)
    Yeval = np.remainder(Y-var.alphay_z_ref, c.Ly)
    
    var.DT_histtp1 = vfDT_hist(Yeval,Xeval)
    
    
    var.DT_hist = np.copy(var.DT_histtp1)                                   # mis à jour de theta