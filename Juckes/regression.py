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


#calcul des tableaux correspondant aux moyennes zonales
nb_point_lat = 10 #correspond au nombre de points en haut et en bas sur lesquels on va moyenner
nb_point_lon = 30 #correspond au nombre de points à gauche et à droite sur lesquels on va moyenner
GP_zonal_mean = np.zeros((LAT.size,LON.size))
POT_zonal_mean = np.zeros((LAT.size,LON.size))

for i in range(LAT.size):
    print(i)
    for j in range(LON.size):
        if(i-nb_point_lat>0):
            lim_inf_lat=i-nb_point_lat
        else: lim_inf_lat=0

        if(i+nb_point_lat<LAT.size):
            lim_sup_lat=i+nb_point_lat
        else: lim_inf_lat=LAT.size

        if(i-nb_point_lon>0):
            lim_inf_lon=i-nb_point_lon
        else: lim_inf_lon=0

        if(i+nb_point_lon<LON.size):
            lim_sup_lon=i+nb_point_lon
        else: lim_inf_lon=LON.size

        GP_zonal_mean[i,j] = np.mean(GP_tot[:, lim_inf_lat:lim_sup_lat, lim_inf_lon:lim_sup_lon])
        POT_zonal_mean[i,j] = np.mean(POT_tot[:, lim_inf_lat:lim_sup_lat, lim_inf_lon:lim_sup_lon])


def regression_latmin_latmax(L_min, L_max, save=False, savename='blabblaaa', show=True):
    """ Renvoie un tableau contenant les coefficients reliant température potentielle et hauteur de trapopause. Unité: K/km.
    Le tableau contient les coeff pour l'hémisphère nord, puis sud, puis la même chose sans la moyenne zonale"""
    GP_plus = np.array([])
    POT_plus = np.array([])

    GP_moins = np.array([])
    POT_moins = np.array([])

    dGP_plus = np.array([])
    dPOT_plus = np.array([])

    dGP_moins = np.array([])
    dPOT_moins = np.array([])

    #Les valeurs des géopotentiels et des températures potentielles sont mises dans une liste unique selon une seule dimension ( plus pratique pour la régression)
    for i in range(data.variables['initial_time0_hours'].size):
        GP_plus = np.append(GP_plus, GP_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :])
        POT_plus = np.append(POT_plus, POT_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :])
        GP_moins = np.append(GP_moins, GP_tot[i,( -LAT[:] > L_min) & (-LAT[:] < L_max), :])
        POT_moins = np.append(POT_moins, POT_tot[i,(-LAT[:] > L_min) & (-LAT[:] < L_max), :])

        dGP_plus = np.append(dGP_plus, GP_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :] - GP_zonal_mean[(LAT[:] > L_min) & (LAT[:] < L_max), :])
        dPOT_plus = np.append(dPOT_plus, POT_tot[i,(LAT[:] > L_min) & (LAT[:] < L_max), :] - POT_zonal_mean[(LAT[:] > L_min) & (LAT[:] < L_max), :])
        dGP_moins = np.append(dGP_moins, GP_tot[i,( -LAT[:] > L_min) & (-LAT[:] < L_max), :] - GP_zonal_mean[( -LAT[:] > L_min) & (-LAT[:] < L_max), :])
        dPOT_moins = np.append(dPOT_moins, POT_tot[i,(-LAT[:] > L_min) & (-LAT[:] < L_max), :] - POT_zonal_mean[(-LAT[:] > L_min) & (-LAT[:] < L_max), :])

    GH_plus = GP_plus/9.81
    GH_moins = GP_moins/9.81
    dGH_plus = dGP_plus/9.81
    dGH_moins = dGP_moins/9.81

    #Plot des variables complètes ie sans avoir enlevé la moyenne zonale. D'abord pour l'hémisphère nord puis pour l'hémisphère sud
    slope_N, intercept, r_value, p_value, std_err = stats.linregress(POT_plus, GH_plus)
    plt.figure(figsize=(16,8))
    plt.scatter(POT_plus, GH_plus, s=1, c='b', alpha=0.6, label="Lmin = {} | Lmax = {} | #points = {}".format(L_min, L_max, GH_plus.size))
    plt.plot(POT_plus, intercept + slope_N*POT_plus, 'r', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope_N, 1/slope_N*1000, intercept, r_value**2))

    slope_S, intercept, r_value, p_value, std_err = stats.linregress(POT_moins, GH_moins)
    plt.scatter(POT_moins, GH_moins, s=1, c='c', alpha = 0.6, label="Lmin = {} | Lmax = {} | #points = {}".format(-L_max, -L_min, GH_moins.size))
    plt.plot(POT_moins, intercept + slope_S*POT_moins, 'g', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope_S, 1/slope_S*1000, intercept, r_value**2))

    plt.legend()
    plt.xlabel(r'Potential Temperature Anomaly [K]')
    plt.ylabel(r'Geopential Height Anomaly [m]')
    plt.title(r"Representation of (9.3)")

    if show:
        plt.show()
    if save:
        plt.savefig("Regression/" + savename + "_global_{}_{}.png".format(L_min, L_max), transparent=True)


    #Plot des variables auxquelles on a retiré la moyenne zonale
    slope_N_zonal, intercept, r_value, p_value, std_err = stats.linregress(dPOT_plus, dGH_plus)
    plt.figure(figsize=(16,8))
    plt.scatter(dPOT_plus, dGH_plus, s=1, c='b', alpha=0.6, label="Lmin = {} | Lmax = {} | #points = {}".format(L_min, L_max, dGH_plus.size))
    plt.plot(dPOT_plus, intercept + slope_N_zonal*dPOT_plus, 'r', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope_N_zonal, 1/slope_N_zonal*1000, intercept, r_value**2))

    slope_S_zonal, intercept, r_value, p_value, std_err = stats.linregress(dPOT_moins, dGH_moins)
    plt.scatter(dPOT_moins, dGH_moins, s=1, c='c', alpha=0.6, label="Lmin = {} | Lmax = {} | #points = {}".format(-L_min, -L_max, dGH_moins.size))
    plt.plot(dPOT_moins, intercept + slope_S_zonal*dPOT_moins, 'g', label='a*x + b with \na = {:.2f} [m/K] | 1/a = {:.2f} [K/km] \nb={:.2f} \nR^2 = {:.3f}'.format(slope_S_zonal, 1/slope_S_zonal*1000, intercept, r_value**2))

    plt.legend()
    plt.xlabel(r'Potential Temperature Anomaly [K]')
    plt.ylabel(r'Geopential Height Anomaly [m]')
    plt.title(r"Representation of (9.3) with substraction of the zonal mean")

    if show:
        plt.show()
    if save:
        plt.savefig("Regression/" + savename + "_zonal_{}_{}.png".format(L_min, L_max), transparent=True)

    return [1/slope_N*1000, 1/slope_S*1000, 1/slope_N_zonal*1000, 1/slope_S_zonal*1000]


L_min = [0., 15., 30., 45., 60., 75.]
L_max = [15., 30., 45., 60., 75., 90.]
slope_N=[]
slope_S=[]
slope_N_zonal=[]
slope_S_zonal=[]

for i in range(len(L_min)):
    regression = regression_latmin_latmax(L_min[i], L_max[i], save=False, savename='regression', show=False)
    slope_N.append(regression[0])
    slope_S.append(regression[1])
    slope_N_zonal.append(regression[2])
    slope_S_zonal.append(regression[3])

plt.figure()
plt.plot([(x+y)/2 for x,y in zip(L_min, L_max)], slope_N, label="Pente dans l'hemisphère nord")
plt.plot([(x+y)/2 for x,y in zip(L_min, L_max)], slope_S, label="Pente dans l'hemisphère sud")
plt.plot([(x+y)/2 for x,y in zip(L_min, L_max)], slope_N_zonal, label="Pente dans l'hemisphère nord sans la moyenne zonale")
plt.plot([(x+y)/2 for x,y in zip(L_min, L_max)], slope_S_zonal, label="Pente dans l'hemisphère sud sans la moyenne zonale")
plt.legend()
plt.savefig("Regression/" + "evolution_de_la_pente_avec_la_latitude")
plt.show()
