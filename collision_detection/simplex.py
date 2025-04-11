import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from polyhedra import Polyhedra



class Simplex:  

    def __init__(self, points=[]):

        self.points = points
        self.containing_origin = False
        self.O = np.array([0, 0, 0])
        self.next_direction = np.array([1, 0, 0])
        self.next_simplex = None

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(np.array(self.points)[:, 0], np.array(self.points)[:, 1], np.array(self.points)[:, 2])

        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])  # Important for a sphere

        # Labels and title
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.set_title('Distribution of Points on a Sphere')

        plt.show()


    def add(self, point):
        """
        Add a point to the simplex !

        Args:
            point (numpy array): position vector
        """
        self.points.append(point)
    
    def remove(self, point):
        """
        Add a point to the simplex !

        Args:
            point (numpy array): position vector
        """
        self.points.append(point)
    
    def num_points(self):
        """
        returns the number of points in the Simplex !

        Returns:
            integer : number of points in the simplex
        """
        return len(self.points)
    
    def get_next(self):
 
        return self.next_simplex, self.next_direction

    
    def process_0simplex(self): 
        if np.array_equal(self.points[0], np.array([0, 0, 0])): 
            self.containing_origin = True
        else:
            self.next_direction =  - self.points[0]
            #print('pr0')
            self.next_simplex = self
    
    def process_1simplex(self):
        self.A = self.points[1]
        self.B = self.points[0]
        AB = self.B - self.A
        AO = self.O - self.A
        direction = np.cross(np.cross(AB, AO), AB)

        if np.array_equal(direction, self.O):
            self.containing_origin = True
        else:
            self.next_direction = direction
            #print('pr1:' + str(self))
            self.next_simplex = self

    def process_2simplex(self):
        self.A = self.points[2]
        self.B = self.points[1]
        self.C = self.points[0]
        #print('back here')
        AB = self.B - self.A
        AO = self.O - self.A
        AC = self.C - self.A

        ABCn = np.cross(AB, AC)
        ACn = np.cross(ABCn, AC)
        ABn = np.cross(AB, ABCn)

        if np.dot(ABn, AO) > 0:
            self.next_direction = np.cross(np.cross(AB, AO), AB)
            self.next_simplex = Simplex(points=[self.B, self.A])
            #print('here out2')
        elif np.dot(ACn, AO) > 0:
            self.next_direction = np.cross(np.cross(AC, AO), AC)
            self.next_simplex = Simplex(points=[self.C, self.A])
            #print('here out1')
        else:
            v = np.dot(ABCn, AO)
            if v == 0:
                #print('leave')
                self.containing_origin = True
            elif v > 0:
                self.next_direction = ABCn
                #print('pr2')
                self.next_simplex = self
            else:
                self.next_direction = -ABCn
                self.next_simplex = Simplex(points=[self.C, self.A, self.B])
                #print('here out')

    def process_3simplex(self):

        self.A = self.points[3]
        self.B = self.points[2]
        self.C = self.points[1]
        self.D = self.points[0]

        AB = self.B - self.A
        AO = self.O - self.A
        AC = self.C - self.A
        AD = self.D - self.A

        ABCn = np.cross(AB, AC)
        ACDn = np.cross(AC, AD)
        ADBn = np.cross(AD, AB)

        if np.dot(ABCn, AO) > 0:
            ACn = np.cross(ABCn, AC)
            ABn = np.cross(AB, ABCn)
            if np.dot(ACn, AO) > 0:
                self.next_simplex = Simplex(points=[self.C, self.A])
                self.next_direction = np.cross(np.cross(AC, AO), AC)
            elif np.dot(ABn, AO) > 0:
                self.next_simplex = Simplex(points=[self.B, self.A])
                self.next_direction = np.cross(np.cross(AB, AO), AB)
            else:
                self.next_direction = ABCn
                self.next_simplex = Simplex(points=[self.C, self.B, self.A])
        
        elif np.dot(ACDn, AO) > 0:
            ADn = np.cross(ACDn, AD)
            ACn = np.cross(AC, ACDn)

            if np.dot(ADn, AO) > 0:
                self.next_simplex = Simplex(points=[self.D, self.A])
                self.next_direction = np.cross(np.cross(AD, AO), AD)
            elif np.dot(ACn, AO) > 0:
                self.next_simplex = Simplex(points=[self.C, self.A])
                self.next_direction = np.cross(np.cross(AC, AO), AC)
            else:
                self.next_simplex = Simplex(points=[self.D, self.C, self.A])
                self.next_direction = ACDn
        
        elif np.dot(ADBn, AO) > 0:
            ABn = np.cross(ADBn, AB)
            ADn = np.cross(AD, ADBn)

            if np.dot(ABn, AO) > 0:
                self.next_simplex = Simplex(points=[self.B, self.A])
                self.next_direction = np.cross(np.cross(AB, AO), AB)

            elif np.dot(ADn, AO) > 0:
                self.next_simplex = Simplex(points=[self.D, self.A])
                self.next_direction = np.cross(np.cross(AD, AO), AD)

            else:
                self.next_simplex = Simplex(points=[self.B, self.D, self.A])
                self.next_direction = ADBn
        
        else:
            self.containing_origin = True


    def process(self):
        # depending on the number of points in the simplex, process to find if the origin is identified
        if self.num_points()   == 1: 
            self.process_0simplex()
        elif self.num_points() == 2: 
            self.process_1simplex()
        elif self.num_points() == 3: 
            self.process_2simplex()
        elif self.num_points() == 4: 
            self.process_3simplex()





