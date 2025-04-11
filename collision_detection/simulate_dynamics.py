from impulse_response import collision_response, surface_response

from polyhedra import Polyhedra
from grid import Grid
from export_vtk import show_poly, generate_vtk_file
import numpy as np
from gjk import collision_of_polyhedra
from collisions_metrics import get_direction_and_distance
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation
import copy

import os
import glob
from tqdm import tqdm


animations = glob.glob('./Mesostructure/animations/*')

def simulate(grid:Grid, dt=1, gravity=-9.81, damping=0.1, steps=10, box=None, global_step=0):
    for animation in animations:
        try:
            os.remove(animation)
        except FileNotFoundError:
            pass
        
    for i in tqdm(range(steps)):

        filename =  './Mesostructure/animations/aggregates_{0}.vtk'.format(i + global_step)
        generate_vtk_file(grid, filename)

        for cell_id, polyhedra in grid.cells.items(): 

            polys_in_nbr = grid.get_poly_in_neighborhood(*cell_id) 

            for poly in polyhedra: 
                if poly.settled:
                    continue
                poly.color = (255, 0, 0)

                for nearby_poly in polys_in_nbr: 
                    if nearby_poly != poly and not nearby_poly.settled: 
                        collision_check = collision_of_polyhedra(poly, nearby_poly)
                        if collision_check:
                            distance, min_direction, closest_vertices = get_direction_and_distance(360, poly, nearby_poly)
                            collision_response(poly, nearby_poly, distance, min_direction, closest_vertices) 
                            poly.color = (0, 0, 255)
                            nearby_poly.color = (0, 0, 255)

                if box is not None:
                    surface_response(poly, np.array([0., 0., 1.]), np.array([0., 0., 0.]))
                    surface_response(poly, np.array([0., 0., -1.]), np.array([0., 0., box[2]]))
                    surface_response(poly, np.array([1., 0., 0.]), np.array([0., 0., 0.]))
                    surface_response(poly, np.array([-1., 0., 0.]), np.array([box[0], 0., 0.]))
                    surface_response(poly, np.array([0., 1., 0.]), np.array([0., 0., 0.]))
                    surface_response(poly, np.array([0., -1., 0.]), np.array([0., box[1], 0.]))

        for cell_id, polys_in_cell in grid.cells.items():
            for poly in polys_in_cell:
                if poly.settled:
                    continue
                poly.prev_orientation = poly.orientation.copy()
                poly.history.append(copy.deepcopy(poly.position))
                force = np.array([0, 0, poly.mass * gravity]) 
                acceleration = force/poly.mass 

                drag_coeff = 2.0
                drag_force = -drag_coeff * poly.velocity
                acceleration += drag_force / poly.mass

                rot_drag_coeff = 1.0
                poly.angular_velocity *= np.exp(-rot_drag_coeff * dt)

                poly.position += poly.velocity * dt + 0.5 * acceleration * dt * dt
                poly.velocity = (poly.velocity + acceleration * dt)

                if np.linalg.norm(poly.velocity) < 0.05 and np.linalg.norm(poly.angular_velocity) < 0.01:
                    poly.settled = True
                    continue

                poly.angular_velocity *= 0.9  
                poly.rotation_angles += poly.angular_velocity * dt
                poly.update_orientation()

                delta_pos = poly.position - poly.history[-1]
                delta_rot = poly.orientation @ poly.prev_orientation.T

                poly.vertices = (delta_rot @ (poly.vertices - poly.history[-1]).T).T + poly.history[-1] + delta_pos
            
        grid.reset()
