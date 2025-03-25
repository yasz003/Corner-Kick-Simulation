"""
Soccer ball physics simulation for corner kicks.
"""
import numpy as np
from scipy.integrate import solve_ivp
from config import *

def simulate_corner_kick(ball_speed, theta, phi, omega, visualize=False):
    """
    Simulate a corner kick with the given parameters and determine
    if it results in a goal near the goalpost.
    
    Args:
        ball_speed: Initial speed (m/s)
        theta: Elevation angle (degrees)
        phi: Horizontal angle (degrees)
        omega: Angular velocity vector (rad/s)
        visualize: Whether to create visualization
    
    Returns:
        Tuple (is_goal, is_near_post, flight_time, min_distance_to_goal)
    """
    # Left and right goalpost positions
    left_post_position = np.array([0, -GOAL_WIDTH/2, 0])
    right_post_position = np.array([0, GOAL_WIDTH/2, 0])
    
    # Initial position (corner)
    ball_position = [0, -FIELD_WIDTH/2, 0]
    
    # Calculate initial velocity components
    vy = ball_speed * np.cos(np.radians(theta)) * np.cos(np.radians(phi))  # Inward
    vx = ball_speed * np.cos(np.radians(theta)) * np.sin(np.radians(phi))  # Forward
    vz = ball_speed * np.sin(np.radians(theta))  # Upward
    
    # Ball velocity array
    ball_velocity = [vx, vy, vz]
    
    # Initial conditions
    states0 = ball_position + ball_velocity
    
    # Time settings
    time = np.linspace(0, MAX_TIME, int(MAX_TIME/TIME_STEP))  # Time array
    
    def ball_dynamics(t, states):
        """Ball dynamics considering drag and Magnus forces"""
        # Extract position and velocity components
        x, y, z, dx, dy, dz = states
        
        # Calculate speed
        v = np.sqrt(dx**2 + dy**2 + dz**2)  # Speed [m/s]
        
        # Initialize accelerations
        ax, ay, az = 0, 0, -GRAVITY  # Start with gravity
        
        if v > 0:
            # Unit velocity vector
            v_unit = np.array([dx, dy, dz]) / v
            
            # Drag force (normalized by mass for acceleration)
            drag_acc = -0.5 * AIR_DENSITY * BALL_AREA * DRAG_COEFFICIENT * v**2 * v_unit / BALL_MASS
            
            # Magnus force (spin effect)
            velocity = np.array([dx, dy, dz])
            cross_val = np.cross(velocity, omega)
            
            if np.linalg.norm(cross_val) > 0:
                magnus_unit = cross_val / np.linalg.norm(cross_val)
                magnus_acc = 0.5 * AIR_DENSITY * BALL_AREA * LIFT_COEFFICIENT * v**2 * magnus_unit / BALL_MASS
            else:
                magnus_acc = np.zeros(3)
            
            # Add to total acceleration
            ax += drag_acc[0] + magnus_acc[0]
            ay += drag_acc[1] + magnus_acc[1]
            az += drag_acc[2] + magnus_acc[2]
        
        return [dx, dy, dz, ax, ay, az]
    
    def event_ball_ground(t, y):
        """Terminate when ball touches the ground (z=0)"""
        z_pos = y[2]
        return z_pos
    
    def event_ball_goal(t, y):
        """Terminate when ball crosses goal line at appropriate height"""
        x_pos, y_pos, z_pos = y[0], y[1], y[2]
        # Check if ball is at the goal line (x=0)
        if abs(x_pos) < 0.1:  # Small tolerance for numerical issues
            # Check if within goal width and height
            if abs(y_pos) < GOAL_WIDTH/2 and z_pos < GOAL_HEIGHT and z_pos > 0:
                return 0
        return 1
    
    # Set termination conditions
    event_ball_ground.terminal = True
    event_ball_ground.direction = -1
    event_ball_goal.terminal = True
    
    # Solve the ODE
    sol = solve_ivp(
        ball_dynamics, 
        [0, MAX_TIME], 
        states0, 
        method='RK45',
        t_eval=time,
        events=[event_ball_ground, event_ball_goal],
        rtol=1e-6
    )
    
    # Extract solution
    t_sol = sol.t
    x = sol.y[0]
    y = sol.y[1]
    z = sol.y[2]
    
    # Check if it's a goal (if the trajectory terminates due to the goal event)
    is_goal = len(sol.t_events[1]) > 0
    
    # Check if the goal is near a goalpost
    is_near_post = False
    if is_goal:
        # Get the position where the ball crosses the goal line
        goal_idx = len(x) - 1
        goal_position = np.array([x[goal_idx], y[goal_idx], z[goal_idx]])
        
        # Calculate distance to each goalpost
        dist_left_post = np.linalg.norm(goal_position - left_post_position)
        dist_right_post = np.linalg.norm(goal_position - right_post_position)
        
        # Check if it's in the target area on the inside of the goalpost
        # For the left post, check if y is greater than -goal_width/2 (on the right side of the post)
        # For the right post, check if y is less than goal_width/2 (on the left side of the post)
        is_near_left = (dist_left_post <= TARGET_RADIUS) and (goal_position[1] > -GOAL_WIDTH/2)
        is_near_right = (dist_right_post <= TARGET_RADIUS) and (goal_position[1] < GOAL_WIDTH/2)
        
        is_near_post = is_near_left or is_near_right
    
    # Flight time until termination
    flight_time = t_sol[-1]
    
    # Calculate minimum distance to goal center
    # Goal center is at (0, 0, goal_height/2)
    goal_center = np.array([0, 0, GOAL_HEIGHT/2])
    
    # Calculate distances from each point of the trajectory to goal center
    distances = []
    for i in range(len(x)):
        point = np.array([x[i], y[i], z[i]])
        dist = np.linalg.norm(point - goal_center)
        distances.append(dist)
    
    min_distance = min(distances) if distances else float('inf')
    
    # Return visualization data if requested
    if visualize:
        return x, y, z, is_goal, is_near_post, flight_time
    
    return is_goal, is_near_post, flight_time, min_distance