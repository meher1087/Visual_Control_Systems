'''
Program plots gradient of given function w.r.t independent variables
'''

import matplotlib.pyplot as plt
import numpy as np
x,y = np.meshgrid(np.arange(-7, 7, .5), np.arange(-7, 7, 0.5))
z = np.sin(x) + np.cos(y)# x*np.exp(-x**2 - y**2)
v, u = np.gradient(z, .2, .2)  # finds the gradient (change in z for change in x and y) with resolution 0.2 of samples 0.2 in x and 0.2 in y
fig, ax = plt.subplots()
q = ax.quiver(x,y,u,v)  # plots arrows with x,y as point and u,v as directions
plt.show()