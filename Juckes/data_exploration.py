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
initial_time0 = data.variables['initial_time0_hours']
initial_time1 = data.variables['initial_time0_encoded']
initial_time2 = data.variables['initial_time0']

print("GP : shape = {} | units = {}".format(GP.shape, GP.units))
print("POT : shape = {} | units = {}".format(POT.shape, POT.units))
print("lat : shape = {} | units = {}".format(lat.shape, lat.units))
print("long : shape = {} | units = {}".format(long.shape, long.units))
print("initial time 0 : shape = {} | units = {}".format(initial_time0.shape, initial_time0.units))
print("initial time 1 : shape = {} | units = {}".format(initial_time1.shape, initial_time1.units))
print("initial time 2 : shape = {} | units = {}\n".format(initial_time2.shape, initial_time2.units))

#print(POT)
