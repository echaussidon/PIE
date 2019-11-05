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
theta = []
n = 100 # nombre de points en x
m = 100 # nombre de points en y
x = [] # coordonnées (points du maillage)
y = [] # coordonnées (points du maillage)
u = [] # vitesse en x
v = [] # vitesse en y
k = [] # nombres d'onde en x (longueur = n)
l = [] # nombres d'onde en y (longueur = m)
K = [] # sqrt(k^2+l^2)

dx = np.pi*2/(n-1) # pas en x pour que x soit entre 0 et 2*pi
dy = np.pi*2/(m-1) # pas en y pour que y soit entre 0 et 2*pi

# remplir theta, x et y
for i in range(n):
    tempx = []
    tempy = []
    ligne = []
    for j in range(m):
        xp = i * dx
        yp = j * dy
        tempx.append(xp)
        tempy.append(yp)
        # données initiales de theta (quelques choix)
        ligne.append(np.sin(xp/2)*np.sin(yp/2)) 
#        ligne.append(np.sin(xp)*np.sin(yp/2))
#        ligne.append(np.sin(xp))
#        ligne.append(0)
    x.append(tempx)
    y.append(tempy)
    theta.append(ligne)

#x1 = n/4
#x2 = n/2
#x3 = 3*n/4
#for i in range(n):
#    tempx = []
#    tempy = []
#    ligne = []
#    for j in range(m):
#        xp = i * dx
#        yp = j * dy
#        tempx.append(xp)
#        tempy.append(yp)
#        # données initiales de theta (quelques choix)
#        if (i > x1 and i < x2):
#            ligne.append(-(i-x1)/20)
#        elif (i >= x2 and i < x3):
#            ligne.append((i-x3)/20)
#        else:
#            ligne.append(0)
#    x.append(tempx)
#    y.append(tempy)
#    theta.append(ligne)

theta = np.array(theta)

# plot theta
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, theta)
plt.title('theta')
plt.xlabel('x')
plt.ylabel('y')
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

# calcul de K (matrice n sur m)
for i in range(n):
    tempK = []
    for j in range(m):
        tempK.append(np.sqrt(k[i]**2 + l[j]**2))
    K.append(tempK)

# plot transformée de Fourier
freqx, freqy = np.meshgrid(l, k)
fig1 = plt.figure()
ax = fig1.add_subplot(111, projection='3d')
ax.plot_surface(freqx, freqy, np.abs(Theta)/n/m) # normalisation : /n/m
plt.title('Fourier')
plt.xlabel('k')
plt.ylabel('l')
plt.show()

#for i in range(n):
#    tempu = []
#    for j in range(m):
#        tempu.append(0)
#    u.append(tempu)
#u = np.array(u)
#
#for i in range(n):
#    for j in range(m):
#        tempu = 0
#        for p in range(n):
#            for q in range(m):
#                tempu += np.real(Theta[p][q] * np.exp(1j * (k[p] * (x[i][j]+0.01) + l[q] * (y[i][j]+0.01) ) ) )
#        u[i][j] = np.real(tempu)

#test = 0;
#for p in range(n):
#    for q in range(m):
#        test += np.real(Theta[p][q] * np.exp(1j * (k[p] * np.pi/2 + l[q] * np.pi) ) )
#test = np.real(test)/n/m
#print(test)

# Pour le calcul des dérivées on change les coefficients Theta par multiplier avec 1j*k ou 1j*l
ThetaV = [];
for i in range(n):
    temp = []
    for j in range(m):
        temp.append(0j)
    ThetaV.append(temp)
ThetaV = np.array(ThetaV)

for i in range(n):
    for j in range(m):
        ThetaV[i][j] = Theta[i][j] * 1j * k[i]
        Theta[i][j] = Theta[i][j] * 1j * l[j]

u = np.real(np.fft.ifft2(Theta))
v = np.real(np.fft.ifft2(ThetaV))

#f = interpolate.interp2d(x, y, u, kind='linear')
#for i in range(n):
#    for j in range(m):
#        u[i][j] = f(x[i][j]+0.01, y[i][j]+0.01)

# plot u
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, u)
plt.title('u')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# plot v
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, v)
plt.title('v')
plt.xlabel('x')
plt.ylabel('y')
plt.show()