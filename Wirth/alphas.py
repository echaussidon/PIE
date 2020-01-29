# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:59:01 2019
"""
import numpy as np
from scipy import interpolate
import constantes as c
import variables as var
import uv
import time_m
from scipy.interpolate import griddata

@time_m.time_measurement
def calc_alpha():
    var.u,var.v = uv.vitesses(var.theta, False)                                # calcul des vitesses à instant t
    fu = interpolate.interp2d(c.y, c.x, var.u, kind='linear')                  # interpolation lineaire de u
    fv = interpolate.interp2d(c.y, c.x, var.v, kind='linear')                  # ~ v
    futm1 = interpolate.interp2d(c.y, c.x, var.utm1, kind='linear')            # interpolation lineaire de utm1
    fvtm1 = interpolate.interp2d(c.y, c.x, var.vtm1, kind='linear')            # ~ v
    vfu=np.vectorize(fu)                                                       # La vectorisation permet d'utiliser les fonctions sur des matrices
    vfv=np.vectorize(fv)
    vfutm1=np.vectorize(futm1)
    vfvtm1=np.vectorize(fvtm1)

    for a in range(2):                                                         # 2 itérations pour calcul de alphas
        X=np.tile(c.x,(c.Ny,1)).transpose()
        Y=np.tile(c.y, (c.Nx, 1))

        Xloc=np.remainder(X-var.alphax/2, c.Lx)
        Yloc=np.remainder(Y-var.alphay/2, c.Ly)

        Uloc = vfu(Yloc, Xloc)
        Vloc = vfv(Yloc, Xloc)
        Uloctm1 = vfutm1(Yloc, Xloc)
        Vloctm1 = vfvtm1(Yloc, Xloc)

        var.alphax=c.dt* (1.5 * Uloc - 0.5 * Uloctm1)
        var.alphay=c.dt* (1.5 * Vloc - 0.5 * Vloctm1)

    var.utm1 = np.copy(var.u)                                                 # mis à jour de utm1
    var.vtm1 = np.copy(var.v)                                                 # ~ y

@time_m.time_measurement
def calc_alpha_z_ref():
    for a in range(2):                                                        # 2 itérations pour calcul de alphas
        var.u_z_ref, var.v_z_ref = uv.vitesses(var.theta, True)                # calcul des vitesses à instant t
        fu = interpolate.interp2d(c.y, c.x, var.u_z_ref, kind='linear')       # interpolation lineaire de u
        fv = interpolate.interp2d(c.y, c.x, var.v_z_ref, kind='linear')       # ~ v
        futm1 = interpolate.interp2d(c.y, c.x, var.u_z_reftm1, kind='linear') # interpolation lineaire de utm1
        fvtm1 = interpolate.interp2d(c.y, c.x, var.v_z_reftm1, kind='linear') # ~ v
        vfu=np.vectorize(fu)                                                  # La vectorisation permet d'utiliser les fonctions sur des matrices
        vfv=np.vectorize(fv)
        vfutm1=np.vectorize(futm1)
        vfvtm1=np.vectorize(fvtm1)

        X=np.tile(c.x,(c.Ny,1)).transpose()
        Y=np.tile(c.y, (c.Nx, 1))

        Xloc=np.remainder(X-var.alphax_z_ref/2, c.Lx)
        Yloc=np.remainder(Y-var.alphay_z_ref/2, c.Ly)

        Uloc = vfu(Yloc, Xloc)
        Vloc = vfv(Yloc, Xloc)
        Uloctm1 = vfutm1(Yloc, Xloc)
        Vloctm1 = vfvtm1(Yloc, Xloc)

        var.alphax_z_ref=c.dt* (1.5 * Uloc - 0.5 * Uloctm1)
        var.alphay_z_ref=c.dt* (1.5 * Vloc - 0.5 * Vloctm1)

    var.u_z_reftm1 = np.copy(var.u_z_ref)                                     # mis à jour de utm1
    var.v_z_reftm1 = np.copy(var.v_z_ref)                                     # ~ y
