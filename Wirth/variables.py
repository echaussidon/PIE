# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:21:21 2019
"""
import numpy as np
import constantes as c
import init_theta
import uv

theta = init_theta.theta_initialization(c.Nx,c.Ny,c.init)   # initialisation des inconnues
thetatp1 = np.copy(theta)                                   # les inconnues à instant t+dt (à calculer dans l'avancement)
thetatm1 = np.copy(theta)                                   # ~ t-dt (pour estimation de la vitesse verticale)
u,v = uv.vitesses(theta, False)                             # initialisation des vitesses
utm1 = np.copy(u)                                           # vitesses à instant t-dt
vtm1 = np.copy(v)                                           # ~ y
u_z_ref,v_z_ref = uv.vitesses(theta, True)                  # vitesses sur la couche en dessous (z_ref)
u_z_reftm1 = np.copy(u_z_ref)                               # vitesses à instant t-dt
v_z_reftm1 = np.copy(v_z_ref)                               # ~ y
alphax = np.zeros((c.Nx,c.Ny))                              # déplacements en x des particules de instant t à t+c.dt
alphay = np.zeros((c.Nx,c.Ny))                              # ~ y
alphax_z_ref = np.zeros((c.Nx,c.Ny))                        # déplacements en x des particules de instant t à t+c.dt
alphay_z_ref = np.zeros((c.Nx,c.Ny))                        # ~ y
DT_hist = np.copy(theta) * c.g / c.Nt / c.Ns / c.theta_ref * c.gamma1 # équation (17)
DT_histtp1 = np.copy(DT_hist)                               # stockage t+dt
w = np.zeros((c.Nx,c.Ny))                                   # vitesse verticale
DT_disp = np.zeros((c.Nx,c.Ny))                             # DT_disp initialisé comme 0
DT_disptp1 = np.zeros((c.Nx,c.Ny))                          # stockage t+dt
DT_cloud = np.zeros((c.Nx,c.Ny))