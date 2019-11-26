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
        plt.pcolor(c.X,c.Y,var.theta,cmap=plt.cm.viridis)
        plt.title('theta_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar()
        if c.savefig:
            plt.savefig("Theta/theta_{}.png".format(t))
            print("save theta")
        else:
            plt.show()
            
    if plot_vitesses:
        plt.figure(figsize=(15,7.5))
        plt.pcolor(c.X,c.Y,var.u,cmap=plt.cm.viridis)
        plt.title('u_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar()
        if c.savefig:
            plt.savefig("U/U_{}.png".format(t))
            print("save U")
        else:
            plt.show()
        
        plt.figure(figsize=(15,7.5))
        plt.pcolor(c.X,c.Y,var.v,cmap=plt.cm.viridis)
        plt.title('v_'+str(t))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar()
        if c.savefig:
            plt.savefig("V/V_{}.png".format(t))
            print("save V")
        else:
            plt.show()

#def plot_theta(t):
#    
#
#def plot_vitesses(t):
    