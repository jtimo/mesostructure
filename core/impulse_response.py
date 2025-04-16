import numpy as np

def collision_response(poly1, poly2, distance, normal_direction, vertices_m):
    # calculate the relative velocity between the stones
    v_relative = poly2.velocity - poly1.velocity

    r1 = poly2.position - poly1.position
    r2 = poly1.position - poly2.position

    #normal_direction[np.abs(normal_direction) < 1e-8] = 0
    # calculate the relative velocity in the direction of the collision normal
    normal_velocity = np.dot(v_relative, normal_direction)
  
    # if the stones are already moving away from each other, there is no need to apply a collision response
    if normal_velocity < 0:
    
        e = 0.9 # restitution coefficient for bounce back
        m1, m2 = poly1.mass, poly2.mass

        I1, I2 = poly1.moment_of_inertia, poly2.moment_of_inertia

        I1 = poly1.orientation @ I1 @ poly1.orientation.T
        I2 = poly2.orientation @ I2 @ poly2.orientation.T

        I1_inv = np.linalg.inv(I1)
        I2_inv = np.linalg.inv(I2)

        # Calculate cross products
        r1_cross_N = np.cross(r1, normal_direction)
        r2_cross_N = np.cross(r2, normal_direction)

        a = I1_inv @ r1_cross_N
        b = I2_inv @ r2_cross_N
        za = np.dot(normal_direction, np.cross(a, r1))
        zb = np.dot(normal_direction, np.cross(b, r2))
       
        # Calculate denominator
        denominator = (1 / m1) + (1 / m2) + za + zb

        # Calculate impulse
        impulse = -(1 + e) * (normal_velocity)  / denominator
      
        # Calculate the change in angular velocity (using cross product)
        poly1.velocity -= (impulse * normal_direction / m1) 
        poly2.velocity += (impulse * normal_direction / m2) 

        # Angular velocity update
        poly1.angular_velocity -= np.dot(I1_inv, np.cross(r1, impulse * normal_direction)) 
        poly2.angular_velocity += np.dot(I2_inv, np.cross(r2, impulse * normal_direction)) 
   
 
def surface_response(poly, surface_normal, point_on_surface):

    normal_direction = surface_normal
    plane_point = point_on_surface # A point on the plane
    
    # Calculate the distances from the vertices to the plane
    distances = np.dot(poly.vertices - plane_point, normal_direction)
    #print(poly.chull.equations())

    
    # Check if all distances are on one side of the plane
    truth_value =  np.any(distances <= 0) 
    

    index = np.argmin(distances)
    crit_vertex = poly.vertices[index, :]
    normal_velocity = np.dot(poly.velocity, normal_direction)

    if truth_value and normal_velocity < 0:
        poly.color = (180, 0, 0)
        

        r1 = poly.position - crit_vertex

        e = 0.9
        m1 = poly.mass

        I1 = poly.moment_of_inertia
        I1 = poly.orientation @ I1 @ poly.orientation.T
        I1_inv = np.linalg.inv(I1)

        # Calculate cross products
        r1_cross_N = np.cross(r1, normal_direction)

        a = I1_inv @ r1_cross_N
        za = np.dot(normal_direction, np.cross(a, r1))

        # Calculate denominator
        denominator = (1 / m1) + za 

        # Calculate impulse
        impulse = -(1 + e) * (normal_velocity)  / denominator
      
        # Calculate the change in angular velocity (using cross product)
        poly.velocity += (impulse * normal_direction / m1) 
        #poly.velocity  = 0.5 * poly.velocity 
        
        # Angular velocity update
        poly.angular_velocity -= np.dot(I1_inv, np.cross(r1, impulse * normal_direction)) 
        
        # Tangential friction
        vel_at_contact = poly.velocity + np.cross(poly.angular_velocity, r1)
        v_n = np.dot(vel_at_contact, normal_direction) * normal_direction
        v_t = vel_at_contact - v_n

        if np.linalg.norm(v_t) > 1e-6:
            
            mu = 0.5  # friction coefficient
            t_dir = -v_t / np.linalg.norm(v_t)
            jt_max = mu * impulse  # friction cap

            r1_cross_T = np.cross(r1, t_dir)
            a_t = I1_inv @ r1_cross_T
            z_t = np.dot(t_dir, np.cross(a_t, r1))
            denom_t = (1 / m1) + z_t

            jt = min(jt_max, np.linalg.norm(v_t) / denom_t)

            poly.velocity += (jt * t_dir / m1)
            poly.angular_velocity += I1_inv @ np.cross(r1, jt * t_dir)