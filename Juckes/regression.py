import numpy as np
import numpy.ma as ma #pour avoir des tableaux avec des masques :)
import matplotlib.pyplot as plt
from scipy import stats

import netCDF4 as nc4
import cartopy as cartopy
import cartopy.crs as crs
import tqdm as tqdm

import utils

data = nc4.Dataset('Data/PA_THETA_Z_2PVU_2016010100-2016013100.nc','r')

GP_tot = data.variables['GP_GDS0_PVL']
POT_tot = data.variables['POT_GDS0_PVL']
LAT = data.variables['g0_lat_1']
LON = data.variables['g0_lon_2']

def regression_latmin_latmax(L_min, L_max, save=False, savename='blabblaaa', show=True):
    GP = np.array([])
    POT = np.array([])
    for i in range(data.variables['initial_time0_hours'].size):
        GP = np.append(GP, GP_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :])
        POT = np.append(POT, POT_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :])

    GH = GP/9.81

    slope, intercept, r_value, p_value, std_err = stats.linregress(POT, GH)

    plt.figure(figsize=(16,8))
    plt.scatter(POT, GH, s=1, label="Lmin = {} | Lmax = {} | #points = {}".format(L_min, L_max, GH.size))
    plt.plot(POT, intercept + slope*POT, 'r', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope, 1/slope*1000, intercept, r_value**2))
    plt.xlabel(r'Potential Temperature [K]')
    plt.ylabel(r'Geopential Height [m]')
    plt.title(r"Representation of (9.3)")
    plt.legend()

    dGH = GH - np.mean(GH)
    dPOT = POT - np.mean(POT)

    slope, intercept, r_value, p_value, std_err = stats.linregress(dPOT, dGH)

    plt.figure(figsize=(16,8))
    plt.scatter(dPOT, dGH, s=1, label="Lmin = {} | Lmax = {} | #points = {}".format(L_min, L_max, dGH.size))
    plt.plot(dPOT, intercept + slope*dPOT, 'r', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope, 1/slope*1000, intercept, r_value**2))
    plt.xlabel(r'Potential Temperature Anomaly [K]')
    plt.ylabel(r'Geopential Height Anomaly [m]')
    plt.title(r"Representation of (9.3)")
    plt.legend()

    if show:
        plt.show()
    if save:
        plt.savefig("Regression/" + savename + "_{}_{}.png".format(L_min, L_max), transparent=True)

regression_latmin_latmax(0,10, save=True, savename='regression', show=False)
