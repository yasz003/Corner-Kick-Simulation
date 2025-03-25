"""
Optimization algorithms for finding optimal corner kick parameters.
"""
import numpy as np
import time
from config import *
from soccer_physics import simulate_corner_kick

def evaluate_kick(params):
    """
    Evaluate a set of kick parameters.
    Returns flight time if goal is scored near goalpost, or penalty + distance if not.
    """
    # Extract parameters from the input array
    ball_speed, theta, phi, omega_z = params
    
    # Convert omega to array format (only z-axis spin for simplicity)
    omega = np.array([0, 0, omega_z])
    
    # Run simulation with these parameters
    result = simulate_corner_kick(ball_speed, theta, phi, omega)
    
    # Extract results
    is_goal, is_near_post, flight_time, min_distance = result
    
    # Penalty for not scoring
    if not is_goal:
        return 1000 + min_distance  # Large penalty + minimum distance to goal
    
    # Additional penalty if not near the goalpost
    if not is_near_post:
        return 500 + flight_time  # Medium penalty + flight time
    
    # If it's a goal near the goalpost, return the flight time (to minimize)
    return flight_time

def optimize_corner_kick_parameters():
    """
    Optimize the parameters of a soccer corner kick to score an Olympic goal
    near the goalpost in minimum time.
    
    Returns:
        The optimal parameters and the visualization of the optimal trajectory.
    """
    from visualization import create_visualization
    
    print("Starting optimization. This may take several minutes...")
    start_time = time.time()
    
    # Create parameter grid
    speeds = np.linspace(PARAMETER_BOUNDS[0][0], PARAMETER_BOUNDS[0][1], N_SPEED)
    thetas = np.linspace(PARAMETER_BOUNDS[1][0], PARAMETER_BOUNDS[1][1], N_THETA)
    phis = np.linspace(PARAMETER_BOUNDS[2][0], PARAMETER_BOUNDS[2][1], N_PHI)
    omegas = np.linspace(PARAMETER_BOUNDS[3][0], PARAMETER_BOUNDS[3][1], N_OMEGA)
    
    # Store all successful goal trajectories
    all_goal_trajectories = []
    
    # Run grid search
    total_iterations = N_SPEED * N_THETA * N_PHI * N_OMEGA
    counter = 0
    
    for speed in speeds:
        for theta in thetas:
            for phi in phis:
                for omega in omegas:
                    # Update progress
                    counter += 1
                    if counter % 100 == 0:
                        progress = counter / total_iterations * 100
                        elapsed = time.time() - start_time
                        estimated_total = elapsed / (counter / total_iterations)
                        remaining = estimated_total - elapsed
                        print(f"Progress: {progress:.1f}% - Time remaining: {remaining:.1f}s")
                    
                    # Evaluate parameters
                    params = [speed, theta, phi, omega]
                    score = evaluate_kick(params)
                    
                    # If it's a goal near the goalpost (score < 500), add to all trajectories
                    if score < 500:
                        # Store as (score, params) for easy sorting
                        all_goal_trajectories.append((score, params))
    
    end_time = time.time()
    print(f"Optimization completed in {end_time - start_time:.2f} seconds")
    
    # If no goals found near the goalpost
    if not all_goal_trajectories:
        print("No successful goals found near the goalpost. Checking for any goals...")
        # Try again for any goals (not just near the goalpost)
        for speed in speeds:
            for theta in thetas:
                for phi in phis:
                    for omega in omegas:
                        params = [speed, theta, phi, omega]
                        # Run simulation directly to check
                        result = simulate_corner_kick(speed, theta, phi, np.array([0, 0, omega]))
                        is_goal = result[0]
                        flight_time = result[2]
                        if is_goal:
                            all_goal_trajectories.append((500 + flight_time, params))
        
        if not all_goal_trajectories:
            print("No successful goals found at all. Try expanding the parameter bounds.")
            return None
    
    # Sort all goal trajectories by flight time
    all_goal_trajectories.sort()
    
    # Select trajectories with sufficient time difference
    selected_trajectories = []
    selected_trajectories.append(all_goal_trajectories[0])  # Always take the fastest
    
    # Find 2 more trajectories that are sufficiently different
    for score, params in all_goal_trajectories[1:]:
        # Check if this trajectory is different enough from all selected ones
        if all(abs(score - prev_score) >= MIN_TIME_DIFF for prev_score, _ in selected_trajectories):
            selected_trajectories.append((score, params))
            
        # Stop once we have 3
        if len(selected_trajectories) >= 3:
            break
    
    # If we couldn't find 3 sufficiently different ones, relax the constraint
    if len(selected_trajectories) < 3:
        print(f"Could not find 3 trajectories with time difference >= {MIN_TIME_DIFF}s")
        print("Taking the fastest available trajectories instead")
        # Just take the fastest trajectories
        selected_trajectories = all_goal_trajectories[:min(3, len(all_goal_trajectories))]
    
    # Print results
    near_post_count = sum(1 for score, _ in selected_trajectories if score < 500)
    print(f"\nTotal goals found: {len(all_goal_trajectories)}")
    print(f"Goals near goalposts: {near_post_count} out of {len(selected_trajectories)} selected")
    print("\nTop 3 Trajectories:")
    trajectories = []
    
    for i, (score, params) in enumerate(selected_trajectories):
        ball_speed, theta, phi, omega_z = params
        optimal_omega = np.array([0, 0, omega_z])
        
        print(f"\nTrajectory {i+1}:")
        print(f"Flight Time: {score if score < 500 else score-500:.6f} s")
        print(f"Near Goalpost: {'Yes' if score < 500 else 'No'}")
        print(f"Ball Speed: {ball_speed:.2f} m/s")
        print(f"Elevation Angle (theta): {theta:.2f} degrees")
        print(f"Horizontal Angle (phi): {phi:.2f} degrees")
        print(f"Spin Rate (omega_z): {omega_z:.2f} rad/s")
        
        # Run the simulation with these parameters and save trajectory
        x, y, z, is_goal, is_near_post, flight_time = simulate_corner_kick(
            ball_speed, theta, phi, optimal_omega, visualize=True
        )
        
        trajectories.append({
            'params': params,
            'data': (x, y, z, is_goal, is_near_post, flight_time),
            'score': score
        })
    
    # Visualize top 3 trajectories
    create_visualization(trajectories)
    
    return [result[1] for result in selected_trajectories]