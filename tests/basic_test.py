from core.grid import Grid
from core.polyhedra import Polyhedra
from core.simulate_dynamics import simulate
import numpy as np
from viz.export_vtk import remove_animations

remove_animations()
# Create grid
box_size = 200
grid = Grid(width=box_size, height=box_size, depth=box_size, cell_size=30, box=np.array([box_size, box_size, box_size]))

# Create irregular shapes with larger size
num_layers = 2
stones_per_layer = 30
shapes = [np.random.uniform(-r, r, size=(np.random.randint(30, 80), 3))
          for r in np.random.uniform(10, 20, size=num_layers * stones_per_layer)]

# Define grid layout
spacing = 20
x_vals = np.arange(20, box_size - 20, spacing)
y_vals = np.arange(20, box_size - 20, spacing)

shape_index = 0
layer_height = 20
global_step = 0

for layer in range(num_layers):
    z = (layer + 1) * layer_height
    if z >= box_size:
        break
    positions = []
    for x in x_vals:
        for y in y_vals:
            jitter = np.random.uniform(-spacing / 2, spacing / 2, size=2)
            position = np.array([x + jitter[0], y + jitter[1], z])
            positions.append(position)

    np.random.shuffle(positions)
    for i in range(min(stones_per_layer, len(positions))):
        shape = shapes[shape_index]
        shape_index += 1
        stone = Polyhedra(points=shape + positions[i])
        stone.mass = 10.0
        stone.velocity = np.random.uniform(-0.05, 0.05, size=3)
        stone.angular_velocity = np.zeros(3)
        stone.rotation_angles = np.zeros(3)
        stone.orientation = np.eye(3)
        grid.add_polyhedra(stone)

    # Run simulation to settle current layer
    simulate(
        grid,
        dt=0.05,
        gravity=-9.81,
        steps=100,
        box=np.array([box_size, box_size, box_size]),
        global_step=global_step,
    )
    global_step += 100

