import numpy as np
from core.impulse_response import surface_response

class Box:
    def __init__(self, dimensions):
        # dimensions: (width, height, depth)
        self.dim = np.array(dimensions)
        self.half = self.dim / 2.0  # Half dimensions for centering

        # Define box surfaces as (normal, point_on_surface) pairs
        self.surfaces = [
            (np.array([1., 0., 0.]),  np.array([-self.half[0], 0., 0.])),   # left
            (np.array([-1., 0., 0.]), np.array([self.half[0], 0., 0.])),    # right
            (np.array([0., 1., 0.]),  np.array([0., -self.half[1], 0.])),   # bottom
            (np.array([0., -1., 0.]), np.array([0., self.half[1], 0.])),    # top
            (np.array([0., 0., 1.]),  np.array([0., 0., -self.half[2]])),   # back
            (np.array([0., 0., -1.]), np.array([0., 0., self.half[2]])),    # front
        ]

    def resolve_contact(self, poly):
        for normal, point in self.surfaces:
            surface_response(poly, normal, point)
