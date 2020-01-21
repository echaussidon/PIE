"""

Sauvegarde les valeurs calculées dans un fichier netcdf4

petit tuto : http://pyhogs.github.io/intro_netcdf4.html

"""

import numpy as np
import netCDF4 as nc4

import constantes as c
import variables as v


def initialisation(filename='result.nc'):

    f = nc4.Dataset(filename,'w', format='NETCDF4')

    tempgrp = f.createGroup('Theta_data')

    tempgrp.createDimension('x', len(c.x))
    tempgrp.createDimension('y', len(c.y))
    tempgrp.createDimension('time', c.Nitplot) #none = dimension infinie

    X = tempgrp.createVariable('X', 'f4', 'x')
    Y = tempgrp.createVariable('Y', 'f4', 'y')
    time = tempgrp.createVariable('Time', 'i4', 'time')
    theta = tempgrp.createVariable('Theta', 'f4', ('time', 'x', 'y'))

    X[:] = c.x #[:] is necessary
    Y[:] = c.y
    theta[0,:,:] = v.theta
    time[0] = 0

    #Add global attributes
    f.description = "Dataset of the simulation containing the value of Theta for a certain value of time"
    from datetime import datetime
    today = datetime.today()
    f.history = "Created " + today.strftime("%d/%m/%y")

    #Add local attributes to variable instances
    X.units = 'Meters'
    Y.units = 'Meters'
    time.units = 'Seconds'
    theta.units = 'Kelvin'

    return f, theta, time

def save_step(theta, time, temps, iteration):
    theta[iteration, :, :] = v.theta
    time[iteration] = temps

def close_file(f):
    f.close()

#pour explorer le fichier que l'on vient juste de créer
def read_and_explore(filename='result.nc'):
    f = nc4.Dataset(filename,'r')
    tempgrp = f.groups['Theta_data']

    print("meta data for the dataset:")
    print(f)
    print("meta data for the Theta_data group:")
    print(tempgrp)
    print("meta data for Theta variable:")
    print(tempgrp.variables['Theta'])
    print(tempgrp.variables['Theta'][3,:,:])
