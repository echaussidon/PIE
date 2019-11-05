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
    plt.figure(figsize=(10,6))

    ax = plt.axes(projection=crs.PlateCarree())
    plt.contourf(long[:], lat[:], GP[i,:,:], 80, transform=crs.PlateCarree(), cmap=plt.cm.viridis)

    cbar = plt.colorbar(orientation='horizontal', pad = 0.05)
    cbar.ax.set_xlabel("GP [{}]".format(GP.units))
    plt.title(r"$t = {} h$".format(initial_time[i]))

    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_feature(cartopy.feature.BORDERS, linestyle=':', alpha=0.5)

    plt.savefig("Result/GP_{}.png".format(i), transparent=True)
