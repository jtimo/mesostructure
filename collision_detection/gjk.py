from polyhedra import Polyhedra
from simplex import Simplex
import numpy as np
from scipy.spatial import ConvexHull

# The Gilbert-Johnson-Keerthi Algorithm to test collission of convex polyhedra
def collision_of_polyhedra(poly1: Polyhedra=None, poly2: Polyhedra=None):
    # Test if two convex polyhedra collide using the GJK algorithm
    
    collision: bool = False
    simplex_in_polyhedra = Simplex(points=[])
    iterations = 0
    #direction = np.array([1, 0, 0]) 
    direction = poly1.position - poly2.position

    while iterations < 30:
        iterations += 1
        #print(iterations)

        vertex_for_simplex = poly1.support(direction) - poly2.support(-direction)
        simplex_in_polyhedra.add(vertex_for_simplex)
  
        if simplex_in_polyhedra.num_points() > 1 and np.dot(vertex_for_simplex, direction) < 0:
            collision = False
            break
        
        simplex_in_polyhedra.process()
        if simplex_in_polyhedra.containing_origin:
            collision = True
            break
        
        simplex_in_polyhedra, direction = simplex_in_polyhedra.get_next()

    if collision:    
        return True
    else:
        return False
