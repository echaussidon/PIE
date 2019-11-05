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
initial_time = data.variables['initial_time0_hours']
initial_time0_encoded = data.variables['initial_time0_encoded']
initial_time0 = data.variables['initial_time0']

print("GP : shape = {} | units = {}".format(GP.shape, GP.units))
print("POT : shape = {} | units = {}".format(POT.shape, POT.units))
print("lat : shape = {} | units = {}".format(lat.shape, lat.units))
print("long : shape = {} | units = {}".format(long.shape, long.units))
print("initial time : shape = {} | units = {}".format(initial_time.shape, initial_time.units))

print(GP.units)
