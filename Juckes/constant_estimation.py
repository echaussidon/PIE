import numpy as np
import matplotlib.pyplot as plt

import netCDF4 as nc4
import cartopy as cartopy
import cartopy.crs as crs

import utils


data = nc4.Dataset('Data/PA_THETA_Z_2PVU_2016010100-2016013100.nc','r')

GP = data.variables['GP_GDS0_PVL']
POT = data.variables['POT_GDS0_PVL']
LAT = data.variables['g0_lat_1']
LON = data.variables['g0_lon_2']
initial_time = data.variables['initial_time0_hours']


#Obtention de la hauteur moyenne et de la température potentielle moyenne de la tropopause
#On fait une moyenne temporelle (GP et POT ne sont pas uniforme selon LAT et LON)

mean_GP = np.mean(GP, axis=0)
mean_POT = np.mean(POT, axis=0)


utils.plot_2(LON, LAT, mean_GP, mean_POT, "GP [{}]".format(GP.units), "POT [{}]".format(POT.units), title="Moyenne temporelle du Geopotentielle et de la température potentielle")


"""
# évolution de la température selon la latitude moyennée sur toutes les longitudes
mean_geopot_over_long=np.zeros((361))
for k in range(0,720):
    mean_geopot_over_long = mean_geopot_over_long + np.array(mean_geopot[:,k])
mean_geopot_over_long = mean_geopot_over_long/720

#plot du géopotentiel moyen en fonction de la latitude
plt.plot(lat, mean_geopot_over_long)
plt.show()


# Calcul des anomalies de températue et de la variation de hauteur de la tropopause
temp_anomaly = data.variables['POT_GDS0_PVL'][:,:,:] #l'anomalie en température de la tropopause
dz_trop  = data.variables['GP_GDS0_PVL'][:,:,:]     #la perturbation de hauteur de la tropopause
for k in range(0,31):
    temp_anomaly[k,:,:] = temp_anomaly[k,:,:]-mean_pot_temp
    dz_trop[k,:,:] = dz_trop[k,:,:]-mean_geopot
dz_trop = dz_trop/9.81    #on se ramène à une altitude

Const_tab = dz_trop/temp_anomaly   #array contenant les rapports dz sur anomalie
Const = np.mean(Const_tab[:,:,:])
std_dev = np.std(Const_tab[:,:,:])

"""
