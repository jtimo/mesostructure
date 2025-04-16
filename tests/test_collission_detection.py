
from polyhedra import Polyhedra
from gjk import collision_and_normal

from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



# specify the vertices of the polyhedron
points_1 = np.array([[25, 25,  25], [25, 25,  75], [25, 75,  75], [25, 75,  25], [75, 25,  25], [75, 25,  75], [75, 75,  75], [75, 75,  25]])
points_2 = np.array([[25, 25, -25], [25, 25, -75], [25, 75, -75], [25, 75, -25], [75, 25, -25], [75, 25, -75], [75, 75, -75], [75, 75, -25]])

# control collission
points_1 = points_1 + np.array([0, 0, -60])
# create a polyhedra object with the above properties
polyhedra_1 = Polyhedra(points=points_1)
polyhedra_2 = Polyhedra(points=points_2)




a, b, c, d = collision_and_normal(polyhedra_1, polyhedra_2)
print(a)
print(b)
print(c)
print(d)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(points_1[:, 0], points_1[:, 1], points_1[:, 2])
ax.scatter(points_2[:, 0], points_2[:, 1], points_2[:, 2])
ax.scatter(d[0][0], d[0][1], d[0][2])
ax.scatter(d[1][0], d[1][1], d[1][2])

# Set equal aspect ratio
ax.set_box_aspect([1, 1, 1])  # Important for a sphere

# Labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('Distribution of Points on a Sphere')

plt.show()



