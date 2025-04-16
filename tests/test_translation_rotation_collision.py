from core.grid import Grid
from core.polyhedra import Polyhedra
from core.simulate_dynamics import simulate
import numpy as np
from viz.export_vtk import remove_animations
from core.constraints import Box

remove_animations()
# Static grid to hold two cubes
box = Box([100, 100, 100])
grid = Grid(width=100, height=100, depth=100, cell_size=50, box=box)

# Define cube geometry
cube_size = 10
cube_points = np.array([
    [-1, -1, -1],
    [-1, -1,  1],
    [-1,  1, -1],
    [-1,  1,  1],
    [ 1, -1, -1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [ 1,  1,  1]
], dtype=float) * cube_size

# First cube: moving toward the second
cube1 = Polyhedra(points=cube_points.copy())
cube1.mass = 1.0
cube1.velocity = np.array([10.0, 0.0, 0.0])  # move along x-axis
cube1.angular_velocity = np.zeros(3)
cube1.rotation_angles = np.zeros(3)
cube1.orientation = np.eye(3)

# Shift first cube to the left
cube1_shift = np.array([0.0, 0.0, 0.0])
cube1.vertices += cube1_shift
cube1.position = cube1_shift
grid.add_polyhedra(cube1)

# Second cube: stationary
cube2 = Polyhedra(points=cube_points.copy())
cube2.mass = 1.0
cube2.velocity = np.zeros(3)
cube2.angular_velocity = np.zeros(3)
cube2.rotation_angles = np.zeros(3)
cube2.orientation = np.eye(3)

# Shift second cube to the right, aligned with first
cube2_shift = np.array([25.0, 15.0, 0.0])
cube2.vertices += cube2_shift
cube2.position = cube2_shift
grid.add_polyhedra(cube2)

# Simulate with no gravity and no damping
simulate(
    grid,
    dt=0.05,
    gravity=0.0,
    angular_damping=1.0,
    linear_drag=0.0,
    rotational_drag=0.0,
    steps=1000)
