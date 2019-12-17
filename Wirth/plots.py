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
        fig = ax.contourf(c.X,c.Y,var.u,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        plt.title('u_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig)
        cbar.ax.set_ylabel("(m/s)")
        if c.savefig:
            plt.savefig("Simulations/{}/U/hsv_U_dt{}_t{}.png".format(c.folder,c.dt,t))
            print("save U")
            plt.show()
        else:
            plt.show()
        
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.contourf(c.X,c.Y,var.v,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        plt.title('v_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig)
        cbar.ax.set_ylabel("(m/s)")
        if c.savefig:
            plt.savefig("Simulations/{}/V/hsv_V_dt{}_t{}.png".format(c.folder,c.dt,t))
            print("save V")
            plt.show()
        else:
            plt.show()   
    
    if c.plot_theta:
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.contourf(c.X,c.Y,var.theta,np.arange(-25,6),cmap=plt.cm.hsv, vmin = -25, vmax = 5)
        plt.title('theta_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig)
        cbar.ax.set_ylabel("(K)")
        if c.savefig:
            plt.savefig("Simulations/{}/Theta/hsv_theta_dt{}_t{}.png".format(c.folder,c.dt,t))
            print("save theta")
            plt.show()
        else:
            plt.show()      
    
    if c.plot_all:
        plt.figure(figsize=(15,22.5))
        ax1 = plt.subplot(311)
        ax1.set_aspect(1)
        fig1 = ax1.contourf(c.X,c.Y,var.theta,np.arange(-25,6),cmap=plt.cm.hsv, vmin = -25, vmax = 5)
        plt.title('theta_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig1)
        cbar.ax.set_ylabel("(K)")
        ax2 = plt.subplot(312)
        ax2.set_aspect(1)
        fig2 = ax2.contourf(c.X,c.Y,var.u,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        plt.title('u_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig2)
        cbar.ax.set_ylabel("(m/s)")
        ax3 = plt.subplot(313)
        ax3.set_aspect(1)
        fig3 = ax3.contourf(c.X,c.Y,var.v,np.arange(-25,26),cmap=plt.cm.hsv, vmin = -25, vmax = 25)
        plt.title('v_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig3)
        cbar.ax.set_ylabel("(m/s)")
        if c.savefig:
            plt.savefig("Simulations/{}/All/hsv_all_dt900_{}.png".format(c.folder,t))
            print("save V")
            plt.show()
        else:
            plt.show()