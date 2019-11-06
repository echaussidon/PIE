import numpy as np
import netCDF4 as nc4

import matplotlib.pyplot as plt
import cartopy as cartopy
import cartopy.crs as crs

from tqdm import tqdm

data = nc4.Dataset('Data/PA_THETA_Z_2PVU_2016010100-2016013100.nc','r')

GP = data.variables['GP_GDS0_PVL']
POT = data.variables['POT_GDS0_PVL']
lat = data.variables['g0_lat_1']
long = data.variables['g0_lon_2']
initial_time = data.variables['initial_time0_hours']

for i in tqdm(range(initial_time[:].size)):
    plt.figure(figsize=(7.5,7.8))

    ax1 = plt.subplot(2, 1, 1, projection=crs.PlateCarree())
    fig1 = ax1.contourf(long[:], lat[:], GP[i,:,:], 80, transform=crs.PlateCarree(), cmap=plt.cm.viridis)
    cbar1 = plt.colorbar(fig1, ax=ax1, orientation='horizontal', pad = 0.05)
    ax1.set_aspect('auto', adjustable=None)
    cbar1.ax.set_xlabel("GP [{}]".format(GP.units))
    ax1.add_feature(cartopy.feature.COASTLINE)
    ax1.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=0.5)
    plt.title(r"$t = {} h$".format(initial_time[i]))

    ax2 = plt.subplot(2, 1, 2, projection=crs.PlateCarree())
    fig2 = ax2.contourf(long[:], lat[:], POT[i,:,:], 80, transform=crs.PlateCarree(), cmap=plt.cm.viridis)
    cbar2 = plt.colorbar(fig2, ax=ax2, orientation='horizontal', pad = 0.05)
    ax2.set_aspect('auto', adjustable=None)
    cbar2.ax.set_xlabel("POT [{}]".format(POT.units))
    ax2.add_feature(cartopy.feature.COASTLINE)
    ax2.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=0.5)

    #plt.show()

    plt.savefig("Result/data_t{}.png".format(i), transparent=True)
