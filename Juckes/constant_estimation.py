import numpy as np
import numpy.ma as ma #pour avoir des tableaux avec des masques :)
import matplotlib.pyplot as plt

import netCDF4 as nc4
import cartopy as cartopy
import cartopy.crs as crs
import tqdm as tqdm

import utils

data = nc4.Dataset('Data/PA_THETA_Z_2PVU_2016010100-2016013100.nc','r')

GP = data.variables['GP_GDS0_PVL']
POT = data.variables['POT_GDS0_PVL']
LAT = data.variables['g0_lat_1']
LON = data.variables['g0_lon_2']

mean_GP = np.mean(GP, axis=0) #moyenne temporelle du geopotentiel
mean_POT = np.mean(POT, axis=0) #moyenne temporelle de la temperature potentielle

dGP = np.subtract(GP, mean_GP) #anomalie du geopotentiel
dZ = dGP/9.81 #anomalie de la hauteur de la tropopause
dPOT  = np.subtract(POT, mean_POT) #anomalie de la temperature potentielle

Constante = dZ/dPOT

Constante_mask = ma.array(Constante, mask=np.any([Constante < 0, Constante > 500], axis=0))

mean_t_Constante = Constante_mask.mean(axis=0)

mean_lon_lat_t_Constante = np.mean(mean_t_Constante)

std_dev = np.std(mean_t_Constante)

print("\nValeur moyenne de la Constante = {}, standard deviation = {} \n".format(mean_lon_lat_t_Constante, std_dev))

###############
## Affichage ##
###############

#utils.plot_2(LON, LAT, mean_GP, mean_POT, "GP [{}]".format(GP.units), "POT [{}]".format(POT.units), title="Moyenne temporelle du Geopotentielle et de la température potentielle", save=True, savename="Result/mean_data")
<<<<<<< HEAD
#
#for t in range(0,31):
#    utils.plot_2(LON, LAT, dGP[t], dPOT[t], "dGP [{}]".format(GP.units), "dPOT [{}]".format(POT.units), title="Anomalie du Geopotentielle et de la température potentielle", save=True, savename="Result/Anomalie/Anomalie_t{}".format(t), show=False)
#    utils.plot(LON, LAT, Constante[t], "Constante [m/K]", title="verification de (9.3)", save=True, savename="Result/Constante/constante_t{}".format(t), show=False)
#
#utils.plot(LON, LAT, mean_t_Constante[:,:], "Constante [m/K]", title="moyenne temporelle de la Constante", save=True, savename="Result/mean_Constante", show=False)
=======

for t in tqdm.tqdm(range(0,31)):
    #utils.plot_2(LON, LAT, dGP[t], dPOT[t], "dGP [{}]".format(GP.units), "dPOT [{}]".format(POT.units), title="Anomalie du Geopotentielle et de la température potentielle", save=True, savename="Result/Anomalie/Anomalie_t{}".format(t), show=False)
    utils.plot(LON, LAT, Constante_mask[t], "Constante [m/K]", title="verification de (9.3)", save=True, savename="Result/Constante/constante_t{}".format(t), show=False)

utils.plot(LON, LAT, mean_t_Constante[:,:], "Constante [m/K]", title="Moyenne totale Constante = {}, standard deviation = {}".format(mean_lon_lat_t_Constante, std_dev), save=True, savename="Result/mean_Constante", show=False)
>>>>>>> 2b5cb7044ed1a294e587dd988cf637f7544cb365
