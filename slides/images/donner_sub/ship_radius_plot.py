import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x = np.linspace(-1, 1, 101)
y = np.linspace(-1, 1, 101)

X, Y = np.meshgrid(x, y)
Z = np.sqrt(X*X + Y*Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
CS = ax.plot_surface(X, Y, Z, cmap=plt.cm.viridis)
fig.suptitle(r'$r_{ship}$ vs. $x$ vs $y$')
ax.set_xlabel('x')
ax.set_ylabel('y')
# ax.grid(True)
plt.savefig('ship_radius_plot.png')


Z2 = X*X + Y*Y

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
CS = ax.plot_surface(X, Y, Z2, cmap=plt.cm.viridis)
fig.suptitle(r'$r_{ship}^2$ vs. $x$ vs $y$')
ax.set_xlabel('x')
ax.set_ylabel('y')


plt.savefig('ship_radius_plot2.png')

plt.show()