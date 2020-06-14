import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import cmath

#%matplotlib inline

# num = [1,0.2]
# den = [1,3,4]
# zeros = np.roots(num)
# poles = np.roots(den)


n=[1,0]              #numerator of tarnsfer function (can be edited)
d= [1,4,0,0]            # denominator of tarnsfer function (can be edited)

num = np.poly1d(n)
den = np.poly1d(d)

zeros = num.roots
poles = den.roots

# collect all zeros and poles
roots = np.append(zeros.real,poles.real)
roots = np.append(roots,poles.imag)
roots = np.append(roots,zeros.imag)

# Fix grid size to fit all roots 
if(roots.max()):
    g_min = -2*roots.max()
    g_max = 2*roots.max()
    print(1)
else:
    g_min = -2*roots.min()
    g_max = 2*roots.min()
    print(2)

grid_resolution = 30  # 30x30x30 grid 
x1=np.linspace(g_min,g_max,grid_size) # real axis with 30 points
y1=np.linspace(g_min,g_max,grid_size) # imaginary axis with 30 points
g=np.meshgrid(x1,y1)  # generating mesh for x and y 
grid = np.append(g[0].reshape(-1,1),g[1].reshape(-1,1),axis=1)
ss=[complex(point[0],point[1]) for point in grid] # generate complex plane (s-plane)

nn= [np.polyval(num,number) for number in ss]          # substitute the numerator by ss
dd= [np.polyval(den,number) for number in ss]          # substitute the denominator by ss

f=[abs(nn[i]/dd[i]) for i in range(len(dd))]          # transfer function
f = np.array(f)
f1 = f.reshape(grid_size,grid_size)  # magnitudes fo all 30x30 points

# Plot S plane with magnitude
fig = plt.figure()
ax = plt.axes(projection='3d')
#ax.autoscale(enable=True, axis='both', tight=None)
ax.set_xlim([g_min,g_max])
ax.set_ylim([g_min,g_max])
#ax.contour3D(g[0], g[1], f1, grid_size, cmap='binary')
#ax.plot_surface(g[0], g[1], f1)#,rstride=1, cstride=1,cmap='viridis', edgecolor='none')
ax.plot_wireframe(g[0], g[1], f1, color = 'black')

ax.set_xlabel('real')
ax.set_ylabel('imagninary')
ax.set_zlabel('magnitude')


print(zeros,poles)
plt.plot(zeros.real, zeros.imag, linestyle='none', marker='o',markersize=10,markerfacecolor='red')
plt.plot(poles.real, poles.imag, linestyle='none', marker='*',markersize=10,markerfacecolor='blue')
plt.show()


