# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:35:14 2019
"""
import numpy as np
import constantes as c

def theta_initialization(Nx,Ny,k):
    """Initialisation de la température
    k=1: sinusoïdale
    k=2: allongée verticalement
    k=3: allongée horizontalement
    """
    theta = np.zeros((Nx,Ny))                                   # les inconnues à l'instant t
    if(k==1):
        for i in range(Nx):
            for j in range(Ny):
                theta[i][j] = -20 * np.sin(np.pi * i / Nx)*np.sin(np.pi * j / Ny)
    
    elif(k==2 or k==3):
        delta = 0.14            # épaisseur de l'intrusion                                
        if (k == 2):            # intrusion horizontale (comme l'article)
            a_x = 0.1           # point où l'intrusion commence (0.1 -> 10%)
            a_y = 0.5-delta     # ~ y
            
        elif (k == 3):          # intrusion verticale
            a_y = 0.1
            a_x = 0.5-delta
        L_x = 1-(delta+a_x)*2   # longueur de la partie droite en x
        L_y = 1-(delta+a_y)*2   # ~ y
        
        #définition de theta_x
        theta_x = np.zeros(Nx)
        u = 0
        v = int(a_x*Nx)
        for i in range(u,v):
            theta_x[i]=0
        u = v
        v = int((a_x+delta)*Nx)
        for i in range(u,v):
            theta_x[i]=(1+np.sin(np.pi*(i-u)/(v-u)-np.pi/2))/2
        u = v
        v = int((a_x+delta+L_x)*Nx)
        for i in range(u,v):
            theta_x[i]=1
        u = v
        v = int((a_x+delta+L_x+delta)*Nx)
        for i in range(u,v):
            theta_x[i]=(1-np.sin(np.pi*(i-u)/(v-u)-np.pi/2))/2
        u = v
        v = Nx
        for i in range(u,v):
            theta_x[i]=0
        
        #définition de theta_y
        theta_y = np.zeros(Ny)
        u = 0
        v = int(a_y*Ny)
        for i in range(u,v):
            theta_y[i]=0
        u = v
        v = int((a_y+delta)*Ny)
        for i in range(u,v):
            theta_y[i]=(1+np.sin(np.pi*(i-u)/(v-u)-np.pi/2))/2
        u = v
        v = int((a_y+delta+L_y)*Ny)
        for i in range(u,v):
            theta_y[i]=1
        u = v
        v = int((a_y+delta+L_y+delta)*Ny)
        for i in range(u,v):
            theta_y[i]=(1-np.sin(np.pi*(i-u)/(v-u)-np.pi/2))/2
        u = v
        v = Ny
        for i in range(u,v):
            theta_y[i]=0
        
        #définition de theta 
        for i in range(Nx):
            for j in range(Ny):
                theta[i][j] = -20 * theta_x[i] * theta_y[j]
    
    elif(k==4):
        ampl = -20;
        delta_y = 0.14            # épaisseur de l'intrusion 
        delta_x = delta_y * c.Ly/c.Lx                               
        a_x = 0.1           # point où l'intrusion commence (0.1 -> 10%)
        a_y = 0.5-delta_y     # ~ y
        L_x = 1-(delta_x+a_x)*2   # longueur de la partie droite en x
        L_y = 1-(delta_y+a_y)*2   # ~ y
        R = delta_y * c.Ly
        u = 0
        v = int((a_x+delta_x)*Nx)
        for i in range(u,v):
            for j in range(Ny):
                r = np.sqrt((c.x[i]-a_x*c.Lx-R)**2 + (c.y[j]-0.5*c.Ly)**2)
                if (r > R):
                    theta[i][j] = 0
                else:
                    theta[i][j] = ampl * (1+np.sin(np.pi*r/R+np.pi/2))/2
        u = v
        v = int((a_x+delta_x+L_x)*Nx)
        for i in range(u,v):
            for j in range(Ny):
                if (c.y[j] < a_y * c.Ly):
                    theta[i][j] = 0
                elif (c.y[j] > (a_y+2*delta_y) * c.Ly):
                    theta[i][j] = 0
                else:
                    theta[i][j] = ampl * (1+np.sin(np.pi*(c.y[j]-0.5*c.Ly)/R+np.pi/2))/2
        
        u = v
        v = Nx
        for i in range(u,v):
            for j in range(Ny):
                r = np.sqrt((c.x[i]-L_x *c.Lx - a_x*c.Lx-R)**2 + (c.y[j]-0.5*c.Ly)**2)
                if (r > R):
                    theta[i][j] = 0
                else:
                    theta[i][j] = ampl * (1+np.sin(np.pi*r/R+np.pi/2))/2
    return theta