from core.grid import Grid
from core.compute_dynamics import compute_dynamics
from viz.export_vtk import generate_vtk_file
from core.compute_collisions import compute_all_collisions
from tqdm import tqdm



def simulate(grid:Grid, 
             dt=1, 
             gravity=-9.81, 
             angular_damping=0.9, 
             linear_drag=2.0, 
             rotational_drag=1.0, 
             steps=10,
             global_step=0):
        
    for i in tqdm(range(steps)):
        filename =  './data/animations/aggregates_{0}.vtk'.format(i + global_step)
        generate_vtk_file(grid, filename)
        compute_all_collisions(grid)
        compute_dynamics(grid, dt, gravity, angular_damping, linear_drag, rotational_drag)
        grid.reset()
