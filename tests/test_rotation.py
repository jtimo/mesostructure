from core.grid import Grid
from core.polyhedra import Polyhedra
from core.simulate_dynamics import simulate
import numpy as np
from viz.export_vtk import remove_animations

remove_animations()
# Static grid just to hold one object
grid = Grid(width=100, height=100, depth=100, cell_size=50)

# Define a tetrahedron
points = np.array([
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, -1],
    [1, -1, -1]
]) * 10  # scale

# Create spinning object
stone = Polyhedra(points=points)
stone.mass = 1.0
stone.velocity = np.zeros(3)
stone.angular_velocity = np.array([0.0, 0.5, 0.0])  # spin around y-axis
stone.rotation_angles = np.zeros(3)
stone.orientation = np.eye(3)

grid.add_polyhedra(stone)

# Simulate with no gravity and no damping
simulate(
    grid,
    dt=0.05,
    gravity=0.0,
    angular_damping=1.0,
    linear_drag=0.0,
    rotational_drag=0.0,
    steps=200)
