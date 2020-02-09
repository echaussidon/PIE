# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:59:01 2019
"""
import numpy as np
import constantes as c
import variables as var
import uv
import time_m
from scipy.interpolate import RectBivariateSpline


@time_m.time_measurement
def calc_alpha():
    var.u,var.v = uv.vitesses(var.theta, False)                                # calcul des vitesses à instant t
    
    fu = RectBivariateSpline(c.x, c.y, var.u)                       #interpolation de u
    fv = RectBivariateSpline(c.x, c.y, var.v)
    futm1 = RectBivariateSpline(c.x, c.y, var.utm1)
    fvtm1 = RectBivariateSpline(c.x, c.y, var.vtm1)
        
        
    for a in range(2):   
        X=np.tile(c.x,(c.Ny,1)).transpose()             #construction d'une matrice dont les lignes sont toutes égales au vecteur c.x
        Y=np.tile(c.y, (c.Nx, 1))                       #construction d'une matrice dont les colonnes sont toutes égales au vecteur c.y
        Xloc=np.remainder(X-var.alphax/2, c.Lx)         #Condition limite utilisant le reste d'une division euclidienne
        Yloc=np.remainder(Y-var.alphay/2, c.Ly)         # Le point rentre de l'autre côté du maillage
        
        Uloc = fu(Xloc, Yloc, grid = False)
        Vloc = fv(Xloc, Yloc, grid = False)
        Uloctm1 = futm1(Xloc, Yloc, grid = False)
        Vloctm1 = fvtm1(Xloc, Yloc, grid = False)

        var.alphax=c.dt* (1.5 * Uloc - 0.5 * Uloctm1)
        var.alphay=c.dt* (1.5 * Vloc - 0.5 * Vloctm1)

    var.utm1 = np.copy(var.u)                                                 # mis à jour de utm1
    var.vtm1 = np.copy(var.v)                                                 # ~ y

@time_m.time_measurement
def calc_alpha_z_ref():
    for a in range(2):                                                        # 2 itérations pour calcul de alphas
        var.u_z_ref, var.v_z_ref = uv.vitesses(var.theta, True)                # calcul des vitesses à instant t
        
        fu = RectBivariateSpline(c.x, c.y, var.u_z_ref)
        fv = RectBivariateSpline(c.x, c.y, var.v_z_ref)
        futm1 = RectBivariateSpline(c.x, c.y, var.u_z_reftm1)
        fvtm1 = RectBivariateSpline(c.x, c.y, var.v_z_reftm1)
        

        X=np.tile(c.x,(c.Ny,1)).transpose()             #construction d'une matrice dont les lignes sont toutes égales au vecteur c.x
        Y=np.tile(c.y, (c.Nx, 1))                       #construction d'une matrice dont les colonnes sont toutes égales au vecteur c.y

        Xloc=np.remainder(X-var.alphax_z_ref/2, c.Lx)       #Condition limite utilisant le reste d'une division euclidienne
        Yloc=np.remainder(Y-var.alphay_z_ref/2, c.Ly)       # Le point rentre de l'autre côté du maillage

        Uloc = fu(Xloc, Yloc, grid = False)
        Vloc = fv(Xloc, Yloc, grid = False)
        Uloctm1 = futm1(Xloc, Yloc, grid = False)
        Vloctm1 = fvtm1(Xloc, Yloc, grid = False)

        var.alphax_z_ref=c.dt* (1.5 * Uloc - 0.5 * Uloctm1)
        var.alphay_z_ref=c.dt* (1.5 * Vloc - 0.5 * Vloctm1)

    var.u_z_reftm1 = np.copy(var.u_z_ref)                                     # mis à jour de utm1
    var.v_z_reftm1 = np.copy(var.v_z_ref)                                     # ~ y