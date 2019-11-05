import numpy as np
import netCDF4 as nc4   #bibliothèque de lecture pour le format netCDF4
import matplotlib.pyplot as plt

data = nc4.Dataset('Data/PA_THETA_Z_2PVU_2016010100-2016013100.nc','r')

print(" ")
print(data.variables.keys())
print(" ")
print(data.dimensions.keys())


pot_temp = data.variables['POT_GDS0_PVL'][20,:,:]   #la température potentielle
geopot = data.variables['GP_GDS0_PVL'][20,:,:]  #le géopotentiel
lat = data.variables['g0_lat_1'][:]     #latitude
lon = data.variables['g0_lon_2'][:]     #longitude

LON, LAT = np.meshgrid(lon, lat)


def plot_2d(variable):
    "Affiche la représentation 2d du tableau variable sur une carte selon la longitude et la latitude"

    plt.contourf(LON, LAT,variable, cmap='RdGy')
    plt.colorbar()

    plt.show()




#Obtention de la hauteur moyenne et de la température potentielle moyenne de la tropopause
#Nécessaire pour pouvoir en déduire l'anomalie de température et la variation de hauteur 
#Question: laquelle des myennes suivantes faut-il utiliser ?
    
    
#Calcul des valeurs moyennes pour toutes les latitudes et longitudes
mean_geopot=np.zeros((361,720))
mean_pot_temp =np.zeros((361,720))
for k in range(0,31):
    mean_geopot = mean_geopot + data.variables['GP_GDS0_PVL'][k,:,:]
    mean_pot_temp = mean_pot_temp + data.variables['POT_GDS0_PVL'][k,:,:]

mean_geopot = mean_geopot/31
mean_pot_temp = mean_pot_temp/31

plot_2d(mean_geopot)

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