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
u,v = uv.vitesses(theta)                                    # initialisation des vitesses 
utm1 = np.copy(u)                                           # vitesses à instant t-dt
vtm1 = np.copy(v)                                           # ~ y
alphax = np.zeros((c.Nx,c.Ny))                              # déplacements en x des particules de instant t à t+c.dt
alphay = np.zeros((c.Nx,c.Ny))                              # ~ y