# -*- coding: utf-8 -*-
"""
Solución analítica y numérica sistema Sol-Tierra
"""
import math
import numpy as np
import matplotlib.pyplot as plt

# Parámetros
N = 2
G = 8.88743163e-10
Nt = 4*370 
dt = 0.25

M = np.zeros((N))
M[0] = 332970.529136    # Sol.
#M[1] = 0.0552735261     # Mercurio.
#M[2] = 0.814997513      # Venus.
M[1] = 1                # La Tierra.
#M[4] = 0.107446849      # Marte.
#M[5] = 317.828133       # Júpiter.
#M[6] = 95.16            # Saturno.
#M[7] = 14.54            # Urano.
#M[8] = 17.15            # Neptuno.

# Matrices de output.
X = np.zeros((N,Nt,3))
V = np.zeros((N,3))

# Condiciones iniciales.
X[0][0] = [0.0, 0.0, 0.0]
#X[1][0] = [0.466700788, 0.0, 0.056916773]
#X[2][0] = [0.728237503, 0.0, 0.043121576]
X[1][0] = [1.016713884, 0.0, -2.71676e-07]
#X[4][0] = [1.666015896, 0.0, 0.053774992]
#X[5][0] = [5.454635139, 0.0, 0.124169614]
#X[6][0] = [10.05033838, 0.0, 0.435934741]
#X[7][0] = [20.09599544, 0.0, 0.270987774]
#X[8][0] = [30.32823783, 0.0, 0.936783848]

V[0] = [0.0, 0.0, 0.0]
#V[1] = [0.0, 0.022443034, 0.0]
#V[2] = [0.0, 0.020089909, 0.0]
V[1] = [0.0, 0.016917345, 0.0]
#V[4] = [0.0, 0.012689974, 0.0]
#V[5] = [0.0, 0.007185195, 0.0]
#V[6] = [0.0, 0.005278104, 0.0]
#V[7] = [0.0, 0.003745623, 0.0]
#V[8] = [0.0, 0.003110241, 0.0]

# Evolución temporal.

# t - tiempo
# a - masa que se mueve
# b - otras masas
# j - número de k\q del RK4
# i - la componente del vector

def deltaX(t, a, b, j):
    W = X[b][t]-X[a][t]
    
    if j in range(1, 3):
        W = W + (1/2)*dt*K[j-1][b] - (1/2)*dt*K[j-1][a]
    elif j == 3:
        W = W + dt*K[j-1][b] - dt*K[j-1][a]
    
    return W
        
def dist(t, a, b, j):
    return ((deltaX(t, a, b, j)[0])**2+(deltaX(t, a, b, j)[1])**2+(deltaX(t, a, b, j)[2])**2)**(1/2)

def g(t, a, b, j):
    return G*(M[b]/(dist(t, a, b, j))**3)*(deltaX(t, a, b, j))

for t in range(Nt-1):
    Q = np.zeros((4,N,3))
    K = np.zeros((4,N,3))
    
    for j in range(4):
        for a in range(N):
            for b in range(N):
                if b == a:
                    continue
                else:
                    Q[j][a] = Q[j][a] + g(t, a, b, j)
            
            if j == 0:
                K[j][a] = V[a]
            elif j in range(1, 3):
                K[j][a] = V[a] + (dt/2)*Q[j][a]
            else:
                K[j][a] = V[a] + dt*Q[j][a]
    
    for a in range(N):
        V[a] = V[a] + (dt/6)*(Q[0][a]+2*Q[1][a]+2*Q[2][a]+Q[3][a])
        X[a][t+1] = X[a][t] + (dt/6)*(K[0][a]+2*K[1][a]+2*K[2][a]+K[3][a])
        
        if t%7500 == 0:
            print(t, V[a])
            print(t, X[a][t+1])
            
#cambiar orden de los datos nos será útil para la solución analítica y el plot
Xplot = np.zeros((N,3,Nt))
for t in range(Nt):
    for a in range(N):
        for i in range(3):
            Xplot[a][i][t] = X[a][t][i]
            
#Solución analítica
 #Tierra
r0=1.016713884 #UA dist apohelio (cuando theta es 0)
e=0.0167
mu=333001/333000

# Ecuación de la órbita
def yp(x,e,r0):
    return + (((r0)**2-x**2*(1-e**2)+2*e*(r0)*x)**(1/2))*1.000003003

def yn(x,e,r0) :
    return - (((r0)**2-x**2*(1-e**2)+2*e*(r0)*x)**(1/2))*1.000003003

# Error
def A(a,b):   #a semieje mayor; b semieje menor
   return math.pi*a*b  

Aanal=A(1.000001018, 1.000001018*(1-e**2)**(1/2))
Anum=A((max(Xplot[1][0])-min(Xplot[1][0]))/2, (max(Xplot[1][1])-min(Xplot[1][1]))/2 )

print('error relativo', (Aanal-Anum)/Aanal)

# Plot 

plt.figure(figsize=(10, 10))
plt.xlim((-1.2, 1.3))
plt.ylim((-1.2, 1.3))
plt.xlabel('x (UA)', fontsize = 14)
plt.ylabel('y (UA)', fontsize = 14)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
anal= r'$Tierra analítica$'

x=np.linspace(-1.0,1.2, 1000000)
yp=yp(x,e,r0)
yn=yn(x,e,r0)

plt.plot(x, yp, 'g', label=anal)
plt.plot(x, yn, 'g')
  
for a in range(N):
    if a==0:
        s= r'$ Sol$'
        plt.plot(Xplot[a][0], Xplot[a][1], color = 'k',label = s)
    elif a==1:
        t= r'$ Tierra numérica$'
        plt.plot(Xplot[a][0], Xplot[a][1],'b', label=t) 

plt.legend(loc='upper right', prop={'size': 14})
