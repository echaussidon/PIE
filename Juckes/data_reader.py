import numpy as np
import netCDF4 as nc4

data = nc4.Dataset('Data/PA_THETA_Z_2PVU_2016010100-2016013100.nc','r')


print(" ")
print(data.variables.keys())
print(" ")


GP = data.variables['GP_GDS0_PVL']
POT = data.variables['POT_GDS0_PVL']
lat = data.variables['g0_lat_1']
long = data.variables['g0_lon_2']

print(GP.shape)
print(POT.shape)
print(lat.shape)
print(long.shape)
