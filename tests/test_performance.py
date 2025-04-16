import numpy as np
from grid import Grid
from polyhedra import Polyhedra
from simulate_dynamics import simulate

# Parameters
box_size = 400
cell_size = 10        # Modify to test performance
num_stones = 800      # Number of polyhedra

# Create grid
grid = Grid(width=box_size, height=box_size, depth=box_size,
            cell_size=cell_size, box=np.array([box_size, box_size, box_size]))

# Create variable-size aggregates
shapes = []
for _ in range(num_stones):
    num_pts = np.random.randint(20, 40)
    raw = np.random.uniform(-1, 1, size=(num_pts, 3))
    scale = np.random.uniform(5, 15)
    shapes.append(raw * scale)

# Add stones to the grid
for shape in shapes:
    shape_min = np.min(shape, axis=0)
    shape_max = np.max(shape, axis=0)
    available_space = box_size - (shape_max - shape_min)
    offset = np.random.uniform(0, available_space, size=3)
    stone = Polyhedra(points=shape + offset)
    stone.mass = 10.0
    stone.velocity = np.zeros(3)
    stone.angular_velocity = np.random.uniform(0, 0, size=3)
    stone.rotation_angles = np.zeros(3)
    stone.orientation = np.eye(3)
    grid.add_polyhedra(stone)

# Run the simulation
simulate(
    grid,
    dt=0.05,
    gravity=-9.81,
    damping=0.0,
    steps=300,
    box=np.array([box_size, box_size, box_size])
)