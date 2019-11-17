# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:03:18 2019

@author: Jan
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from scipy import interpolate

# ce code calcule les vitesses u et v à base des valeurs de theta qui sont connues (méthode spectrale)

# initialisations
n = 100 # nombre de points en x
m = 50 # nombre de points en y
x = [] # coordonnées (points du maillage)
y = [] # coordonnées (points du maillage)
u = [] # vitesse en x
v = [] # vitesse en y
k = [] # nombres d'onde en x (longueur = n)
l = [] # nombres d'onde en y (longueur = m)

dx = np.pi*2/(n-1) # pas en x pour que x soit entre 0 et 2*pi
dy = np.pi*2/(m-1) # pas en y pour que y soit entre 0 et 2*pi

theta = np.zeros((n,m)) # initialisation de theta comme array

x = np.arange(0,2*np.pi+dx,dx) # dans ce code on prend x = [0, dx, ... 2*pi]
y = np.arange(0,2*np.pi+dy,dy) # pareil pour y

# premier essai de reproduire les conditions initiales de Wirth
x1 = m/4
x2 = m/2
x3 = 3*m/4
def exemple(i,j):
    if (j > x1 and j < x2):
        res = -(j-x1)/20
    elif (j >= x2 and j < x3):
        res = (j-x3)/20
    else:
        res = 0
    return res

# remplir theta, plusieurs choix pour tester
for i in range(n):
    for j in range(m):
        # données initiales de theta (quelques choix)
        theta[i][j] = np.sin(x[i])
#        theta[i][j] = np.sin(x[i]/2)*np.sin(y[j]/2)
#        theta[i][j] = np.sin(x[i])*np.sin(y[j]/2)
#        theta[i][j] = 0
#        theta[i][j] = exemple(i,j)

# plot theta
y,x = np.meshgrid(y,x)
fig = plt.figure()
plt.pcolor(x,y,theta)
plt.title('theta')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()

# calculer la transformation de Fourier de theta
Theta = np.fft.fft2(theta)

# les nombres d'onde k qui appartiennent à la transformation de Fourier
if np.mod(n,2) == 0: # ça diffère si n est pair ou impair
    # k = [0, 1, ... n/2 - 1, -n/2, -n/2 + 1, ... -1]
    for i in range((int) (n/2)):
        k.append(i)
    for i in range((int) (n/2)):
        k.append(-n/2+i)
else:
    # k = [0, 1, ... n/2 - 1, n/2, -n/2, -n/2 + 1, ... -1]
    for i in range((int) ((n-1)/2 + 1)):
        k.append(i)
    for i in range((int) ((n-1)/2)):
        k.append(-(n-1)/2+i)

# pareil pour l, mais m peut différer de n, donc la taille de k et l peut différer
if np.mod(m,2) == 0:
    for i in range((int) (m/2)):
        l.append(i)
    for i in range((int) (m/2)):
        l.append(-m/2+i)
else:
    for i in range((int) ((m-1)/2 + 1)):
        l.append(i)
    for i in range((int) ((m-1)/2)):
        l.append(-(m-1)/2+i)

ThetaV = np.copy(Theta)                         # copie de Theta, pour multiplier avec 1j * k et 1j * l
for i in range(n):
    for j in range(m):
        ThetaV[i][j] = Theta[i][j] * 1j * k[i]  # multiplication avec k[i] pour dérivée de x
        Theta[i][j] = Theta[i][j] * 1j * l[j]   # multiplication avec l[j] pour dérivée de y

u = np.real(np.fft.ifft2(Theta))
v = np.real(np.fft.ifft2(ThetaV))

# plot u (dérivée par rapport à y)
fig = plt.figure()
plt.pcolor(x,y,u)
plt.title('u')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()

# plot v (dérivée par rapport à x)
fig = plt.figure()
plt.pcolor(x,y,v)
plt.title('v')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()