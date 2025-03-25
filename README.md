# Corner Kick Simulation

This project simulates the detailed trajectory of a football during a corner kick, factoring in key physical and aerodynamic elements. It specifically models how gravity, aerodynamic drag, Magnus force (spin-induced lift), and initial impulse affect the ball's path. The simulation accounts for both horizontal and vertical components, allowing detailed analysis of how different angles, velocities, and spin conditions influence the final trajectory.

## Features

- **Detailed 3D Simulation**: Visualizes the full trajectory of a football in three-dimensional space, accounting for vertical and horizontal displacement.
- **Comprehensive Physics Modeling**: Incorporates gravity, aerodynamic drag, Magnus effect, and initial impulse conditions.
- **Customizable Kick Parameters**: Adjust initial speed, vertical launch angle, horizontal directional angle, spin rate, and rotational axis.
- **Graphical Visualization**: Clearly displays simulated corner kick trajectories, aiding tactical analysis and training.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yasz003/Corner-Kick-Simulation.git
cd Corner-Kick-Simulation
```

2. (Optional) Set up a virtual environment:

```bash
python -m venv env
source env/bin/activate  # Windows: .\env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the simulation:

```bash
cd src
python main.py
```

2. Adjust simulation parameters in the `config.json` file within the `src` directory to modify conditions such as initial velocities, launch angles (both horizontal and vertical), and spin properties.

## Authors

This simulation was developed by Yacine Benhamed and Shuhan Wang.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

