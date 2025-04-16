from core.impulse_response import collision_response, surface_response
from core.polyhedra import Polyhedra
from core.grid import Grid
from core.compute_dynamics import compute_dynamics
from viz.export_vtk import show_poly, generate_vtk_file
import numpy as np
from core.gjk import collision_of_polyhedra
from core.collisions_metrics import get_direction_and_distance
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation


from tqdm import tqdm

def compute_all_collisions(grid: Grid):
    for cell_id, polyhedra in grid.cells.items(): 
        polys_in_nbr = grid.get_poly_in_neighborhood(*cell_id) 

        for poly in polyhedra: 
            if poly.settled:
                continue
            poly.color = (0, 0, 255)

            for nearby_poly in polys_in_nbr: 
                if nearby_poly != poly and not nearby_poly.settled: 
                    collision_check = collision_of_polyhedra(poly, nearby_poly)
                    if collision_check:
                        distance, min_direction, closest_vertices = get_direction_and_distance(360, poly, nearby_poly)
                        collision_response(poly, nearby_poly, distance, min_direction, closest_vertices) 
                        poly.color = (255, 0, 0)
                        nearby_poly.color = (255, 0, 0)

            if grid.box is not None:
                grid.box.resolve_contact(poly)
    return None
