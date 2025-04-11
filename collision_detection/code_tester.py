
from impulse_response import collision_response
from polyhedra import Polyhedra
from grid import Grid
from export_vtk import show_poly, generate_vtk_file
import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation
from simulate_dynamics import simulate
from tqdm import tqdm

#----------------------------------------------------------------
# Specify the simulation environment
w, h, d = 200, 200, 200

grid = Grid(width=w, height=h, depth=d, cell_size=100) # keep cell_size big !
#----------------------------------------------------------------


points_1 = np.array([[25, 25, 25], 
                     [25, 25, 75], 
                     [25, 75, 75], 
                     [25, 75, 25],
                     [75, 25, 25], 
                     [75, 25, 75], 
                     [75, 75, 75], 
                     [75, 75, 25]])


# mid-points of the polyhedra 

points_2 = np.array([[25, 25, -25], 
                     [25, 25, -75], 
                     [25, 75, -75], 
                     [25, 75, -25],
                     [75, 25, -25], 
                     [75, 25, -75], 
                     [75, 75, -75], 
                     [75, 75, -25]])



# create a polyhedra object with the above properties
polyhedra_1 = Polyhedra(points=points_1 + np.array([-40, 0, 0]), 
                        orientation=np.eye(3), 
                        rotation_angles=np.array([0., 0., 0.]), 
                        velocity=np.array([0, 0, 0]), 
                        angular_velocity=np.random.uniform(-0.0, 0.0, size=(3,)), 
                        mass=1)

polyhedra_2 = Polyhedra(points=points_2, 
                        orientation=np.eye(3), 
                        rotation_angles=np.array([0., 0., 0.]), 
                        velocity= np.array([0, 0, 2]), 
                        angular_velocity=np.random.uniform(-0.0, 0.0, size=(3,)), 
                        mass=1)

polyhedra_3 = Polyhedra(points=points_1 + np.array([+40, 0, 0]), 
                        orientation=np.eye(3), 
                        rotation_angles=np.array([0., 0., 0.]), 
                        velocity=np.array([-2, 0, 0]), 
                        angular_velocity=np.random.uniform(-0.0, 0.0, size=(3,)), 
                        mass=1)

polyhedra_4 = Polyhedra(points=points_2 + np.array([+60, 0, 0]), 
                        orientation=np.eye(3), 
                        rotation_angles=np.array([0., 0., 0.]), 
                        velocity=np.array([0, 0, -0.1]), 
                        angular_velocity=np.random.uniform(-0.0, 0.0, size=(3,)), 
                        mass=1)

# add polyhedra to the grid
grid.add_polyhedra(polyhedra_1)
#grid.add_polyhedra(polyhedra_2)
grid.add_polyhedra(polyhedra_3)
#grid.add_polyhedra(polyhedra_4)


#----------------------------------------------------------------------------
# simulate the motion of the stones for 10 time steps with a time step of 0.1
simulate(grid, dt=0.08, gravity=-9.81, damping=0.00, steps=500, box=None)
#----------------------------------------------------------------------------










