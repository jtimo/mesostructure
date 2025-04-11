from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull
import random
import vtk


import numpy as np

import vtk
import numpy as np

def generate_vtk_file(my_grid, filename):
    # Create a VTK unstructured grid
    grid = vtk.vtkUnstructuredGrid()

    # Create a VTK points object to store the vertices
    points = vtk.vtkPoints()

    # Create a VTK cell array to store the cells
    cells = vtk.vtkCellArray()

    # Create a VTK cell data object to store the cell colors
    cell_data = vtk.vtkUnsignedCharArray()
    cell_data.SetName("Colors")
    cell_data.SetNumberOfComponents(3)

    # Track the vertex offset for each polyhedron
    vertex_offset = 0

    # Iterate over each polyhedron object
    for polyhedron in my_grid.get_poly():
        vertices = polyhedron.vertices
        for vertex in vertices:
            points.InsertNextPoint(vertex)

        faces = polyhedron.faces
        color = polyhedron.color

        # Add vertices to the points object

        # Add faces as cells to the cell array
        for face in faces:
            # Create a VTK polygon cell for each face
            cell = vtk.vtkPolygon()
            cell.GetPointIds().SetNumberOfIds(len(face))  # Set the number of points and the point IDs for the cell

            for i, vertex_index in enumerate(face):
                cell.GetPointIds().SetId(i, vertex_index + vertex_offset)

            # Add the cell to the cell array
            cells.InsertNextCell(cell)

            # Assign color to the cell
            #cell_data.InsertNextTuple(color)
            cell_data.InsertNextTypedTuple(np.array(color, dtype=np.uint8))

        # Increment the vertex offset for the next polyhedron
        vertex_offset += len(vertices)

    # Add vectors as lines to the cell array
    
    # Set the points in the unstructured grid
    grid.SetPoints(points)

    # Set the cells in the unstructured grid
    grid.SetCells(vtk.VTK_POLYGON, cells)

    # Set the cell data in the unstructured grid
    grid.GetCellData().SetScalars(cell_data)

    # Optional: export the bounding box if available
    if  my_grid.box is not None:
        bounds = my_grid.box  # [x, y, z]
        cube = vtk.vtkCubeSource()
        cube.SetBounds(0, bounds[0], 0, bounds[1], 0, bounds[2])
        cube.Update()

        box_mapper = vtk.vtkPolyDataMapper()
        box_mapper.SetInputConnection(cube.GetOutputPort())

        box_actor = vtk.vtkActor()
        box_actor.SetMapper(box_mapper)
        box_actor.GetProperty().SetColor(1.0, 1.0, 1.0)
        box_actor.GetProperty().SetOpacity(0.1)

        # Write the box to a separate VTK file
        box_writer = vtk.vtkPolyDataWriter()
        box_writer.SetFileName(filename.replace(".vtk", "_box.vtk"))
        box_writer.SetInputData(cube.GetOutput())
        box_writer.Write()

    # Write the unstructured grid to a VTK file
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(grid)
    writer.Write()

# Usage example:
# generate_vtk_file(my_grid, vectors, "output.vtk")


def show_poly(grid):

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    for i, poly in enumerate(grid.get_poly()):
        if poly.collision > 0:
            col = ('r')
        else:
            col = ('b')

        hull = poly.chull
    # draw the polygons of the convex hull
        for s in hull.simplices:
            tri = Poly3DCollection([hull.points[s]])
            tri.set_color(col)
            tri.set_alpha(0.4)
            ax.add_collection3d(tri)
    # draw the vertices
        
        ax.scatter(poly.vertices[:, 0], poly.vertices[:, 1], poly.vertices[:, 2], s=1, marker='o', color='purple')
        ax.quiver(poly.position[0], 
                  poly.position[1], 
                  poly.position[2], 
                  poly.contact_direction[0] * 30, 
                  poly.contact_direction[1] * 30, 
                  poly.contact_direction[2] * 30, color="green")
    plt.show()