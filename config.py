"""
Configuration parameters for soccer corner kick simulation.
"""
import numpy as np

# Ball properties
BALL_MASS = 0.45         # ball mass (kg)
BALL_RADIUS = 0.11       # ball radius (m)
BALL_AREA = np.pi * BALL_RADIUS**2  # cross-sectional area (m^2)
GRAVITY = 9.81           # gravitational acceleration (m/s^2)
AIR_DENSITY = 1.2        # air density (kg/m^3)

# Aerodynamic coefficients
DRAG_COEFFICIENT = 0.33  # Drag coefficient
LIFT_COEFFICIENT = 0.30  # Lift (Magnus) coefficient

# Field parameters
FIELD_LENGTH = 20        # meters (modified from original)
FIELD_WIDTH = 68         # meters

# Goal dimensions
GOAL_WIDTH = 7.32        # meters
GOAL_HEIGHT = 2.44       # meters

# Penalty area dimensions
PENALTY_AREA_WIDTH = 40.2  # meters
PENALTY_AREA_LENGTH = 16.5  # meters

# Target area (within 2 ball diameters of the goalpost)
TARGET_RADIUS = 2 * (2 * BALL_RADIUS)  # 2 times the ball diameter

# Optimization parameters
PARAMETER_BOUNDS = [
    (20, 35),     # ball_speed (m/s) - realistic range for corner kicks
    (10, 30),     # theta (degrees) - elevation angle
    (5, 45),      # phi (degrees) - horizontal angle 
    (-120, -70)   # omega_z (rad/s) - spin rate (negative for inswing)
]

# Grid search resolution
N_SPEED = 12
N_THETA = 12
N_PHI = 12
N_OMEGA = 12

# Minimum time difference between trajectories (seconds)
MIN_TIME_DIFF = 0.05

# Simulation settings
MAX_TIME = 7             # Final time [s]
TIME_STEP = 0.02         # Time resolution [s]

# Visualization settings
COLORS = ['red', 'blue', 'green']
OUTPUT_FILE = 'optimal_corner_kicks.html'