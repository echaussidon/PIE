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
    for i in range(c.Nx):                                               # itération pour chaque point du maillage
        for j in range(c.Ny):
            xeval = c.x[i] - var.alphax[i][j]                           # coordonnée de x du point d'évaluation de theta
            yeval = c.y[j] - var.alphay[i][j]                           # ~ y
            if xeval < c.x0:                                            # si ce point est hors du maillage:
                xeval = xeval + c.Lx                                    # rentrer le de l'autre côté
            elif xeval > c.x1:                                          # = conditions limites périodiques
                xeval = xeval - c.Lx
            if yeval < c.y0:
                yeval = yeval + c.Ly
            elif yeval > c.y1:
                yeval = yeval - c.Ly
            var.thetatp1[i][j] = ftheta( yeval, xeval )                 # évaluation à Xo = Xn - alpha
    var.theta = np.copy(var.thetatp1)                                   # mis à jour de theta