from polyhedra import Polyhedra
from simplex import Simplex
import numpy as np
from scipy.spatial import ConvexHull

# The Gilbert-Johnson-Keerthi Algorithm to test collission of convex polyhedra
def collision_and_normal_v2(poly1: Polyhedra=None, poly2: Polyhedra=None):
    # Test if two convex polyhedra collide using the GJK algorithm
    
    distance, min_direction, closest_vertices, test = get_direction_and_distance(12, poly1, poly2)
    collision = test
    if collision == True:

        return test, distance, min_direction, closest_vertices
    else:
        return collision, 0, np.array([0, 0, 0]), None
    
def find_direction(normal, poly1, poly2):
    minkowski_point = poly1.support(normal) - poly2.support(-normal)
    return minkowski_point

def get_direction_and_distance(num_samples, poly1, poly2):

    indices = np.arange(0, num_samples, dtype=float) 
    phi = np.arccos(1 - 2 * indices / num_samples)
    theta = np.pi * (1 + 5**0.5) * indices

    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)

    normals_sampler = np.column_stack((x, y, z))
    minkowski_vertices = np.apply_along_axis(find_direction, 1, normals_sampler, poly1, poly2)
   
    minkowski_hull = ConvexHull(np.unique(minkowski_vertices, axis=0))
    normals = minkowski_hull.equations[:, 0:3]
    offsets = minkowski_hull.equations[:, 3]

    test = np.all(np.array([np.dot(eq[:-1], np.array([0., 0., 0.])) + eq[-1] <= 0. for eq in minkowski_hull.equations]))
    
    index = np.argmin(offsets**2) # negative neutral
    min_direction = normals[index, :]

    distance = offsets[index]
    closest_vertices = (poly1.support(min_direction), poly2.support(-min_direction))

    return distance, min_direction, closest_vertices, test