# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:59:01 2019
"""
import numpy as np
from scipy import interpolate
import constantes as c
import variables as var
import uv

def calc_alpha():
    for a in range(2):                                                  # 2 itérations pour calcul de alphas
        var.u,var.v = uv.vitesses(var.theta)                            # calcul des vitesses à instant t
        fu = interpolate.interp2d(c.y, c.x, var.u, kind='linear')       # interpolation lineaire de u
        fv = interpolate.interp2d(c.y, c.x, var.v, kind='linear')       # ~ v
        futm1 = interpolate.interp2d(c.y, c.x, var.utm1, kind='linear') # interpolation lineaire de utm1
        fvtm1 = interpolate.interp2d(c.y, c.x, var.vtm1, kind='linear') # ~ v
        for i in range(c.Nx):                                           # itération pour chaque point du maillage
            for j in range(c.Ny):
                xloc = c.x[i] - var.alphax[i][j]/2                      # coordonnée en x pour évaluation de la vitesse
                yloc = c.y[j] - var.alphay[i][j]/2                      # ~ y
                if xloc < c.x0:                                         # si ce point est hors du maillage:
                    xloc = xloc + c.Lx                                  # rentrer le de l'autre côté
                elif xloc > c.x1:                                       # = conditions limites périodiques
                    xloc = xloc - c.Lx
                if yloc < c.y0:
                    yloc = yloc + c.Ly
                elif yloc > c.y1:
                    yloc = yloc - c.Ly
                uloc = fu( yloc, xloc )                                 # évaluation de u à X - alpha/2
                vloc = fv( yloc, xloc )                                 # ~ v
                uloctm1 = futm1( yloc, xloc )                           # évaluation de utm1 à X - alpha/2
                vloctm1 = fvtm1( yloc, xloc )                           # ~ v
                var.alphax[i][j] = c.dt * (1.5 * uloc - 0.5 * uloctm1)  # nouvelle estimation de alphax
                var.alphay[i][j] = c.dt * (1.5 * vloc - 0.5 * vloctm1)  # ~ y
    var.utm1 = np.copy(var.u)                                           # mis à jour de utm1
    var.vtm1 = np.copy(var.v)                                           # ~ y
    return