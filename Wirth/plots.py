# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:24:47 2019
"""
import matplotlib.pyplot as plt
import constantes as c
import variables as var

def plots(plot_theta, plot_vitesses, t):
    if plot_theta:
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.pcolor(c.X,c.Y,var.theta,cmap=plt.cm.viridis)
        plt.title('theta_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig)
        cbar.ax.set_ylabel("(K)")
        if c.savefig:
            plt.savefig("Theta/theta_{}.png".format(t))
            print("save theta")
            plt.show()
        else:
            plt.show()
            
    if plot_vitesses:
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.pcolor(c.X,c.Y,var.u,cmap=plt.cm.viridis)
        plt.title('u_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig)
        cbar.ax.set_ylabel("(m/s)")
        if c.savefig:
            plt.savefig("U/U_{}.png".format(t))
            print("save U")
            plt.show()
        else:
            plt.show()
        
        plt.figure(figsize=(15,7.5))
        ax = plt.subplot(111)
        ax.set_aspect(1)
        fig = ax.pcolor(c.X,c.Y,var.v,cmap=plt.cm.viridis)
        plt.title('v_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        cbar = plt.colorbar(fig)
        cbar.ax.set_ylabel("(m/s)")
        if c.savefig:
            plt.savefig("V/V_{}.png".format(t))
            print("save V")
            plt.show()
        else:
            plt.show()    