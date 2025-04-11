import numpy as np
import copy


class Grid:
    def __init__(self, width, height, depth, cell_size, box=None):
        """_summary_

        Args:
            width (_type_): _description_
            height (_type_): _description_
            depth (_type_): _description_
            cell_size (_type_): _description_
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.cell_size = cell_size
        self.cells = {}
        self.box = box
      
    def reset(self):
        all_poly = self.get_poly()
        self.cells = {}
        for poly in all_poly:
            self.add_polyhedra(poly)
    
    def add_polyhedra(self, polyhedron):
        """_summary_

        Args:
            polyhedron (_type_): _description_
        """
        x, y, z = polyhedron.position
        cell_x = int(x / self.cell_size)
        cell_y = int(y / self.cell_size)
        cell_z = int(z / self.cell_size)
        cell = self.cells.setdefault((cell_x, cell_y, cell_z), [])
        cell.append(polyhedron)
    
    def get_poly_in_neighborhood(self, cell_x, cell_y, cell_z):
        """_summary_

        Args:
            cell_x (_type_): _description_
            cell_y (_type_): _description_
            cell_z (_type_): _description_

        Returns:
            _type_: _description_
        """
        neighborhood = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    x, y, z = cell_x + dx, cell_y + dy, cell_z + dz
                    if (x, y, z) in self.cells:
                        neighborhood.extend(self.cells[(x, y, z)])
        return neighborhood
    
    def get_all_poly_in_neighborhood(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        all_neighborhoods = {}
        for cell_x in range(int(self.width / self.cell_size)):
            for cell_y in range(int(self.height / self.cell_size)):
                for cell_z in range(int(self.height / self.cell_size)):
                    all_neighborhoods[(cell_x, cell_y, cell_z)] = self.get_poly_in_neighborhood(cell_x, cell_y, cell_z)
        return all_neighborhoods
    
    def get_poly(self):
        all_poly = []
        for key, item in self.cells.items():
            all_poly.extend(item)
        return all_poly
