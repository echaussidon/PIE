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
    GP_plus = np.array([])
    POT_plus = np.array([])

    GP_moins = np.array([])
    POT_moins = np.array([])

    for i in range(data.variables['initial_time0_hours'].size):
        GP_plus = np.append(GP_plus, GP_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :])
        POT_plus = np.append(POT_plus, POT_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :])
        GP_moins = np.append(GP_moins, GP_tot[i,( -LAT[:] > L_min) & (-LAT[:] < L_max), :])
        POT_moins = np.append(POT_moins, POT_tot[i,(-LAT[:] > L_min) & (-LAT[:] < L_max), :])

    GH_plus = GP_plus/9.81
    GH_moins = GP_moins/9.81

    """slope, intercept, r_value, p_value, std_err = stats.linregress(POT, GH)

    plt.figure(figsize=(16,8))
    plt.scatter(POT, GH, s=1, label="Lmin = {} | Lmax = {} | #points = {}".format(L_min, L_max, GH.size))
    plt.plot(POT, intercept + slope*POT, 'r', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope, 1/slope*1000, intercept, r_value**2))
    plt.xlabel(r'Potential Temperature [K]')
    plt.ylabel(r'Geopential Height [m]')
    plt.title(r"Representation of (9.3)")
    plt.legend() """

    dGH_plus = GH_plus - np.mean(GH_plus)
    dPOT_plus = POT_plus - np.mean(POT_plus)
    dGH_moins = GH_moins - np.mean(GH_moins)
    dPOT_moins = POT_moins - np.mean(POT_moins)

    slope, intercept, r_value, p_value, std_err = stats.linregress(dPOT_plus, dGH_plus)
    plt.figure(figsize=(16,8))
    plt.scatter(dPOT_plus, dGH_plus, s=1, c='b', alpha=0.6, label="Lmin = {} | Lmax = {} | #points = {}".format(L_min, L_max, dGH_plus.size))
    plt.plot(dPOT_plus, intercept + slope*dPOT_plus, 'r', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope, 1/slope*1000, intercept, r_value**2))

    slope, intercept, r_value, p_value, std_err = stats.linregress(dPOT_moins, dGH_moins)
    plt.scatter(dPOT_moins, dGH_moins, s=1, c='c', alpha = 0.6, label="Lmin = {} | Lmax = {} | #points = {}".format(-L_max, -L_min, dGH_moins.size))
    plt.plot(dPOT_moins, intercept + slope*dPOT_moins, 'g', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope, 1/slope*1000, intercept, r_value**2))
    plt.legend()
    plt.xlabel(r'Potential Temperature Anomaly [K]')
    plt.ylabel(r'Geopential Height Anomaly [m]')
    plt.title(r"Representation of (9.3)")

    if show:
        plt.show()
    if save:
        plt.savefig("Regression/" + savename + "_{}_{}.png".format(L_min, L_max), transparent=True)

L_min = [0, 15, 30, 45, 60, 75]
L_max = [15, 30, 45, 60, 75, 90]

for i in range(len(L_min)):
    regression_latmin_latmax(L_min[i], L_max[i], save=True, savename='regression', show=False)
