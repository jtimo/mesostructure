from core.grid import Grid
import numpy as np
import copy


def compute_dynamics(grid: Grid, dt=1, gravity=-9.81, angular_damping=1, linear_drag=0, rotational_drag=0):
    for cell_id, polys_in_cell in grid.cells.items():
        for poly in polys_in_cell:
            if poly.settled:
                continue
            poly.prev_orientation = poly.orientation.copy()
            poly.history.append(copy.deepcopy(poly.position))
            force = np.array([0, 0, poly.mass * gravity]) 
            acceleration = force/poly.mass 

            drag_force = -linear_drag * poly.velocity
            acceleration += drag_force / poly.mass

            poly.angular_velocity *= np.exp(-rotational_drag * dt)

            poly.position += poly.velocity * dt + 0.5 * acceleration * dt * dt
            poly.velocity = (poly.velocity + acceleration * dt)

            poly.angular_velocity *= angular_damping  
            poly.rotation_angles += poly.angular_velocity * dt
            poly.update_orientation()

            # if np.linalg.norm(poly.velocity) < 0.00001 and np.linalg.norm(poly.angular_velocity) < 0.00000001:
            #     poly.settled = True
            #     continue

            delta_pos = poly.position - poly.history[-1]
            delta_rot = poly.orientation @ poly.prev_orientation.T

            poly.vertices = (delta_rot @ (poly.vertices - poly.history[-1]).T).T + poly.history[-1] + delta_pos