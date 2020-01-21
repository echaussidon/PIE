# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:24:47 2019
"""
import numpy as np
import matplotlib.pyplot as plt
import constantes as c
import variables as var

def plots(t):    
    if c.plot_vitesses:
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.contourf(c.X,c.Y,var.u, np.arange(-25,26), cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        labels_title(fig, 'u_'+str(t), "(m/s)")
        show_save("Simulations/{}/U/hsv_U_dt{}_t{}.png".format(c.folder,c.dt,t))
        
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.contourf(c.X,c.Y,var.v, np.arange(-25,26), cmap = plt.cm.hsv, vmin = -25, vmax = 25)
        labels_title(fig, 'v_'+str(t), "(m/s)")
        show_save("Simulations/{}/V/hsv_V_dt{}_t{}.png".format(c.folder,c.dt,t))
        
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.contourf(c.X,c.Y,var.w, cmap = plt.cm.hsv, vmin = -0.025, vmax = 0.025)
        labels_title(fig, 'w_'+str(t), "(m/s)")
        show_save("Simulations/{}/W/hsv_W_dt{}_t{}.png".format(c.folder,c.dt,t))
        
    if c.plot_theta:
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.contourf(c.X,c.Y,var.theta, np.arange(-25,6), cmap = plt.cm.hsv, vmin = -25, vmax = 5)
        labels_title(fig, 'theta_'+str(t), "(K)")
        show_save("Simulations/{}/Theta/hsv_theta_dt{}_t{}.png".format(c.folder,c.dt,t))
     
    
    if c.plot_all:
        plt.figure(figsize=(15,22.5))
        
        ax1 = plt.subplot(311)
        ax1.set_aspect(1)
        fig1 = ax1.contourf(c.X,c.Y,var.theta,np.arange(-25,6), vmin = -25, vmax = 5)
        labels_title(fig1, 'theta_'+str(t), "(K)")
        
        ax2 = plt.subplot(312)
        ax2.set_aspect(1)
        fig2 = ax2.contourf(c.X,c.Y,var.u,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        labels_title(fig2, 'u_'+str(t), "(m/s)")
        
        ax3 = plt.subplot(313)
        ax3.set_aspect(1)
        fig3 = ax3.contourf(c.X,c.Y,var.v,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        labels_title(fig3, 'v_'+str(t), "(m/s)")
        show_save("Simulations/{}/All/hsv_all_dt900_{}.png".format(c.folder,t))

def plotW(t):   # plot vitesses verticales
    plt.figure(figsize=(15,7.5))
    ax = plt.subplot(111)
    ax.set_aspect(1)
    fig = ax.contourf(c.X,c.Y,var.w)
    labels_title(fig, 'w_'+str(t), "(m/s)")
    plt.show()
    
def plotTheta_z_ref(theta): # plot theta sur la couche en dessous
    plt.figure(figsize=(15,7.5))
    ax = plt.subplot(111)
    ax.set_aspect(1)
    fig = ax.contourf(c.X,c.Y,theta)
    labels_title(fig, 'theta_z_ref', "(K)")
    plt.show()
    
def plotDT(t):  # plot image vapeur d'eau
    plt.figure(figsize=(15,7.5))
    ax = plt.subplot(111)
    ax.set_aspect(1)
    fig = ax.contourf(c.X,c.Y,var.DT_disp + var.DT_hist + var.DT_cloud)#,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
    labels_title(fig, 'DT vapeur d eau '+str(t), "(K)")
    plt.show()
    
def show_save(title):   # show plot, save under title if indicated in constantes
    if c.savefig:
        plt.savefig(title)
        print("save {}".format(title))
        plt.show()
    else:
        plt.show()
        
def labels_title(fig, title, unit): # add x,y labels, title and colorbar with unit
    plt.title(title)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    cbar = plt.colorbar(fig)
    cbar.ax.set_ylabel(unit)