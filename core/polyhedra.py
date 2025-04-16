

import numpy as np
from scipy.spatial import ConvexHull
import copy



class Polyhedra:
    def __init__(self, points=None, 
                 orientation=np.eye(3), 
                 rotation_angles=np.array([0., 0., 0.]), 
                 velocity=np.random.uniform(-0.0, 0.0, size=(3,)), 
                 angular_velocity=np.random.uniform(-0.0, 0.0, size=(3,)), 
                 mass=1):
        """
        Create a polyhedra object by supplying points in 3d space. The points are then used to compute the comvex hull.
        The convex hull package is used from scipy !

        Args:
            points (_type_, optional): _description_. Defaults to None.
            orientation (_type_, optional): _description_. Defaults to np.eye(3).
            rotation_angles (_type_, optional): _description_. Defaults to np.array([0., 0., 0.]).
            velocity (_type_, optional): _description_. Defaults to np.random.uniform(-0.0, 0.0, size=(3,)).
            angular_velocity (_type_, optional): _description_. Defaults to np.random.uniform(-0.0, 0.0, size=(3,)).
            mass (int, optional): _description_. Defaults to 1.
        """
        
        # geometry 
        self.chull = ConvexHull(points)  # extract the outermost points
        self.vertices = points[self.chull.vertices, :]
        self.original_vertices = self.vertices.copy()
          # Create a mapping dictionary
        vertex_mapping = {vertex_index: i for i, vertex_index in enumerate(self.chull.vertices)}

        # Map simplices indices to vertex indices
        mapped_simplices = [[vertex_mapping[i] for i in simplex] for simplex in self.chull.simplices]

        self.faces = np.array(mapped_simplices) 
        # kinematics
        self.position = np.mean(self.vertices, axis=0) # centroid of the polyhedra
        self.orientation = orientation # defined by a rotation matrix
        self.rotation_angles = rotation_angles # rotation angle around the three axii

        # kinetics
        self.velocity = velocity
        self.angular_velocity = angular_velocity
 
        # dynamic state
        self.collision = 0
        self.penetration = 0
        self.contact_direction = np.array([0, 0, 0])

        # no update
        self.mass = mass
        self.moment_of_inertia = 0
        self.color = (0, 0, 255)
        self.settled = False

        # record state history
        self.history = []
        self.has_collided = False
        self.compute_moment_of_inertia()
    

    def support(self, direction: np.ndarray =np.array([1, 0, 0])) -> np.ndarray :
        """
        Computes the support as the farthest vertex in the direction of the provided vector 
        Args:
            direction (np.ndarray, optional): vector direction. Defaults to np.array([1, 0, 0]).
        Returns:
            np.ndarray: the farthes point in the polyhedra
        """
        # Get the farthest point in poly1 in the direction of the vector
        return self.vertices[np.argmax(np.dot(self.vertices, direction))]
    
    def compute_moment_of_inertia(self):
        """
        Compute the moment of inertia of the polyhedron
        """

        # Shift the vertices so that the center of mass is at the origin
        shifted_vertices = self.vertices - self.position
        
        # Calculate the moment of inertia tensor
        moment_of_inertia_tensor = np.zeros((3, 3))

        for vertex in shifted_vertices:
            x, y, z = vertex
            moment_of_inertia_tensor[0][0] += (y**2 + z**2)
            moment_of_inertia_tensor[1][1] += (x**2 + z**2)
            moment_of_inertia_tensor[2][2] += (x**2 + y**2)
            moment_of_inertia_tensor[0][1] -= (x * y)
            moment_of_inertia_tensor[1][0] -= (x * y)
            moment_of_inertia_tensor[0][2] -= (x * z)
            moment_of_inertia_tensor[2][0] -= (x * z)
            moment_of_inertia_tensor[1][2] -= (y * z)
            moment_of_inertia_tensor[2][1] -= (y * z)

        self.moment_of_inertia =  moment_of_inertia_tensor


    def update_orientation(self):
        """
        Compute the rotation matrix from the given angles
        """

        rotation_angles = self.rotation_angles
        # Calculate the rotation matrices for each axis
        rotation_x = np.array([[1, 0, 0], 
                               [0, np.cos(rotation_angles[0]), -np.sin(rotation_angles[0])],
                               [0, np.sin(rotation_angles[0]), np.cos(rotation_angles[0])]])

        rotation_y = np.array([[np.cos(rotation_angles[1]), 0, np.sin(rotation_angles[1])],
                               [0, 1, 0],
                               [-np.sin(rotation_angles[1]), 0, np.cos(rotation_angles[1])]])

        rotation_z = np.array([[np.cos(rotation_angles[2]), -np.sin(rotation_angles[2]), 0],
                               [ np.sin(rotation_angles[2]), np.cos(rotation_angles[2]), 0],
                               [0, 0, 1]])
        
        self.orientation = rotation_z @ rotation_y @ rotation_x








        




