import numpy as np
import matplotlib.pyplot as plt

import cartopy as cartopy
import cartopy.crs as crs

def plot(long, lat, data, label="label=''", title='', show=True, save=False, savename='blabbla'):
    plt.figure(figsize=(8,6))

    ax = plt.axes(projection=crs.PlateCarree())
    plt.contourf(long[:], lat[:], data[:,:], 80, transform=crs.PlateCarree(), cmap=plt.cm.viridis)

    cbar = plt.colorbar(orientation='horizontal', pad = 0.05)
    cbar.ax.set_xlabel(label)
    plt.title(title)

    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=0.5)

    if save:
        plt.savefig(savename + ".png", transparent=True)
    if show:
        plt.show()

def plot_2(long, lat, data1, data2, label1="label1=''", label2="label2=''", title='', show=True, save=False, savename='blabblaaa'):
    plt.figure(figsize=(7.5,7.8))

    ax1 = plt.subplot(2, 1, 1, projection=crs.PlateCarree())
    fig1 = ax1.contourf(long[:], lat[:], data1[:,:], 80, transform=crs.PlateCarree(), cmap=plt.cm.viridis)
    cbar1 = plt.colorbar(fig1, ax=ax1, orientation='horizontal', pad = 0.05)
    ax1.set_aspect('auto', adjustable=None)
    cbar1.ax.set_xlabel(label1)
    ax1.add_feature(cartopy.feature.COASTLINE)
    ax1.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=0.5)
    plt.title(title )

    ax2 = plt.subplot(2, 1, 2, projection=crs.PlateCarree())
    fig2 = ax2.contourf(long[:], lat[:], data2[:,:], 80, transform=crs.PlateCarree(), cmap=plt.cm.viridis)
    cbar2 = plt.colorbar(fig2, ax=ax2, orientation='horizontal', pad = 0.05)
    ax2.set_aspect('auto', adjustable=None)
    cbar2.ax.set_xlabel(label2)
    ax2.add_feature(cartopy.feature.COASTLINE)
    ax2.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=0.5)

    if save:
        plt.savefig(savename + ".png", transparent=True)
    if show:
        plt.show()
