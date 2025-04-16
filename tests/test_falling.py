from core.grid import Grid
from core.polyhedra import Polyhedra
from core.simulate_dynamics import simulate
import numpy as np

# Create grid
box_size = 200
grid = Grid(width=box_size, height=box_size, depth=box_size, cell_size=50, box=np.array([box_size, box_size, box_size]))

# Simple irregular shape (stone-like)
points = np.random.uniform(-10, 10, size=(50, 3))

# Create multiple stones
num_stones = 50
shapes = [np.random.uniform(-10, 10, size=(np.random.randint(20, 40), 3)) for _ in range(num_stones)]
for i in range(num_stones):
    offset = np.random.uniform(50, 150, size=3)  # drop from above
    stone = Polyhedra(points=points + offset)
    stone = Polyhedra(points=shapes[i] + offset)
    stone.mass = 10.0
    stone.velocity = np.zeros(3)
    stone.angular_velocity = np.random.uniform(-0.1, 0.1, size=3)
    stone.rotation_angles = np.zeros(3)
    stone.orientation = np.eye(3)

    grid.add_polyhedra(stone)

# Call simulation
simulate(
    grid,
    dt=0.05,
    gravity=-9.81,
    damping=0.0,
    steps=300,
    box=np.array([box_size, box_size, box_size])  # used for walls
)