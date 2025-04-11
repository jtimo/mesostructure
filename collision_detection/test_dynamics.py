
from impulse_response import collision_response

from polyhedra import Polyhedra
from grid import Grid
from export_vtk import show_poly, generate_vtk_file
import numpy as np
from gjk import collision_of_polyhedra
from scipy.spatial import ConvexHull
from simulate_dynamics import simulate
from tqdm import tqdm
import random

import cProfile


#----------------------------------------------------------------
# Specify the simulation environment
w, h, d = 100, 100, 100

grid = Grid(width=w, height=h, depth=d, cell_size=40) # keep cell_size big !
#----------------------------------------------------------------

# specify the polyhedra
number_of_polyhedra = 100
num_vertices = 40

# Set the maximum coordinate value for each vertex
poly_left, poly_right = -10, 10

np.random.seed(50)

#---------------------------------------------------------------------------------------
# Generate Polyhedra
import random
for i in range(number_of_polyhedra):

    # mid-points of the polyhedra 
    position = np.random.uniform(0, w - poly_left, size=(3,))

    # generate points around the position
    points = position + random.choice([0.5, 1])*np.random.uniform(poly_left, poly_right, size=(num_vertices, 3))

    # orientation is a 3d matrix
    initial_orientation = np.eye(3)

    # euler angles
    angle = np.array([0., 0., 0.])

    # initial linear and angular velocity
    velocity = np.random.uniform(-2, 2, size=(3,))
    angular_velocity = np.random.uniform(-0.0, 0.0, size=(3,))
    
    # create a polyhedra object with the above properties
    polyhedra = Polyhedra(points=points, orientation=initial_orientation, rotation_angles=angle, velocity=velocity, angular_velocity=angular_velocity, mass=1)
    
    # add polyhedra to the grid
    grid.add_polyhedra(polyhedra)

#----------------------------------------------------------------------------
# simulate the motion of the stones for 10 time steps with a time step of 0.1
simulate(grid, dt=0.06, gravity=0, damping=0.00, steps=100, box=None)
#cProfile.run('')
#----------------------------------------------------------------------------










