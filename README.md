# Corner Kick Simulation

This repository contains the source code and simulation framework for analyzing and optimizing corner kick strategies in football. The simulation models the trajectory of a ball kicked from a corner using realistic physics, incorporating gravity, air resistance, and the Magnus effect. The goal is to determine the optimal kicking parameters to maximize the chances of scoring an *olímipico*—a goal scored directly from a corner kick.

## Overview

In professional football, only 2–4% of corners result in a goal, and olímipicos are even rarer. Our simulation uses numerical methods to solve a set of coupled, non-linear differential equations that govern the ball’s flight. By performing over 100 million simulated kicks, the project identifies the optimal ranges for initial speed, launch angles (both horizontal and vertical), and ball spin.

## Key Features

- **Physics-Based Trajectory Simulation:**  
  Models the ball as a rigid sphere subject to gravity, air resistance, and the Magnus force. The simulation uses realistic parameters for mass, radius, and standard goal dimensions.
  
- **Numerical Methods:**  
  Implements the Runge-Kutta 4(5) method (via SciPy’s `solve_ivp` with the Dormand–Prince scheme) to integrate the equations of motion with adaptive step-size control.

- **Parameter Optimization:**  
  Analyzes over 100 million random kicks to record the conditions under which goals are scored. Recommended optimal parameters include:  
  - **Initial Velocity:** 23–27 m/s  
  - **Horizontal Launch Angle:** 25–47°  
  - **Vertical Launch Angle:** 6–11°  
  - **Spin Rate:** -50 to -70 rad/s (producing an inswing)

- **Statistical Analysis:**  
  Generates heat maps and distributions of successful kicks to show that goals are more likely at the near post, with a gradual decline in probability toward the far post.

## Methodology

1. **Modeling the Ball:**  
   The ball is treated as a sphere with a mass of 0.45 kg and a radius of 11 cm. It is subject to forces including:
   - **Gravity**
   - **Air Resistance:** Opposes the direction of motion.
   - **Magnus Effect:** Due to spin, causing a curving trajectory in the X-Y plane.

2. **Numerical Integration:**  
   The differential equations of motion are solved using the Dormand–Prince RK45 method provided by SciPy’s `solve_ivp`, ensuring both accuracy and adaptive error control.

3. **Simulation Assumptions:**  
   - The ball is perfectly rigid.  
   - Only horizontal spin (in the X-Y plane) is considered.  
   - No interactions with defenders or goalkeepers are modeled.  
   - Shots that hit the posts are considered misses.

4. **Statistical Evaluation:**  
   Each successful goal’s landing position and parameter set are recorded. This data helps to identify the optimal ranges and suggests that the majority of scoring shots occur near the near post.

## Running the Simulation

### Prerequisites

- Python 3.x  
- SciPy  
- NumPy  
- Matplotlib (for visualization)

### Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/yasz003/Corner-Kick-Simulation.git
cd Corner-Kick-Simulation
pip install -r requirements.txt
### Usage

Run the main simulation script:

```bash
python simulate_corner.py
```

This will execute the simulation, perform the parameter sweep, and output visualizations of the successful kick distributions and heat maps.

## Results and Discussion

The simulation reveals that:
- Goals scored from corners occur in only 0.04% of attempts.
- A higher density of goals is observed near the near post (with approximately 22% of goals scored within the first meter) compared to the far post (12%).
- Vertical positioning plays a lesser role compared to horizontal placement.
- The optimal parameter ranges provide a quantitative guideline for training and technique improvement.

For a detailed discussion of the methodology, assumptions, and full analysis, please refer to the accompanying publication PDF in this repository.

## Future Work

Potential improvements include:
- Incorporating ball deformation and a more complex spin model.
- Modeling the effect of defensive pressure and goalkeeping.
- Extending the simulation to consider variable air density and environmental factors.

## References

- Javorova, J., & Ivanov, A. (2018). *Study of soccer ball flight trajectory*. MATEC Web of Conferences.
- Watanabe, Y., et al. (2013). *Magnus effect on a rotating soccer ball at high Reynolds numbers*. Journal of Wind Engineering and Industrial Aerodynamics.
- Cook, B. G., & Goff, J. E. (2006). *Parameter space for successful soccer kicks*. European Journal of Physics.
- Dormand, J.R., & Prince, P.J. (1980). *A family of embedded Runge-Kutta formulae*. Journal of Computational and Applied Mathematics.

## Developed By

- Yacine Benhamed
- Shuhan Wang

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

