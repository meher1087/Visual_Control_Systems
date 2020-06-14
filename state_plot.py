'''
Pogram takes transfer function converts to state matrix and plot the states applied on it.
In a way it must be same as plot of gradient of solution of tf.

'''
import control
import numpy as np
import matplotlib.pyplot as plt

n = [1,0]
d = [1,4,0,0]

sys = control.tf2ss(n,d)
basis = sys.A
#basis = np.array([[1,0],[0,2]])
origin = [0,0]

x =np.arange(-10,10,1)
y = np.arange(-10,10,1)
X,Y = np.meshgrid(x,y) 
"""
meshgird return X as 2D matrix of x values and Y 
as corresponding  2D matrix of y values. we have to
create row vectors out of it with below command

"""
tmp = list(map(tuple,np.dstack((X,Y)).reshape(-1,2)))
state = np.array(tmp) # creates rows as vectors as reshape is inidicating two columns
#for basis by convention we keep vectors as rows to do state multiplication A*x where A is transpose of column vector matrix

dir = [] #list created

for vec in state:    # for loop do row interation so transpose not required 
	temp = basis.dot(vec)  # creates row vector as basis has row vector.
	dir.append(temp)

direct = np.array(dir) # list of row vectors thus column is component of vector

#reorder to mesh grid

direcs = direct.T.reshape(2,np.shape(x)[0],np.shape(y)[0])
x_dir = direcs[0,:,:]
y_dir = direcs[1,:,:]

#get eigen values
w,v = np.linalg.eig(basis) # w,v 
fig, ax = plt.subplots(1,1)
Q = ax.quiver(x,y,x_dir,y_dir)
#Q = ax.quiver(origin,basis.transpose()[:,0],basis.transpose()[:,1],color=('r','b')) 
#Q = ax.quiver([0,0],v[0,:],v[1,:],color='m',scale = 5) #v[:,0],v[:,1]
ax.grid()
ax.set_xlim([-10,10])
ax.set_ylim([-10,10])
plt.show()