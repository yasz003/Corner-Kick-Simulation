"""
Visualization functions for soccer corner kicks trajectories.
"""
import numpy as np
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from config import *

def create_visualization(trajectories):
    """
    Create an interactive 3D visualization of the top 3 ball trajectories.
    
    Args:
        trajectories: List of trajectory data dictionaries
    """
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "scene", "colspan": 2}, None],
            [{"type": "xy"}, {"type": "xy"}]
        ],
        subplot_titles=["3D Field View", "Top View", "Left Goal View"],
        column_widths=[0.5, 0.5],
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05,
        horizontal_spacing=0.05
    )
    
    # Main 3D view - Soccer field
    # Field surface
    fig.add_trace(
        go.Mesh3d(
            x=[0, 0, FIELD_LENGTH, FIELD_LENGTH],
            y=[-FIELD_WIDTH/2, FIELD_WIDTH/2, FIELD_WIDTH/2, -FIELD_WIDTH/2],
            z=[0, 0, 0, 0],
            color='green',
            opacity=0.3,
            name="Field",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Field boundaries
    field_outline_x = [0, FIELD_LENGTH, FIELD_LENGTH, 0, 0]
    field_outline_y = [-FIELD_WIDTH/2, -FIELD_WIDTH/2, FIELD_WIDTH/2, FIELD_WIDTH/2, -FIELD_WIDTH/2]
    field_outline_z = [0, 0, 0, 0, 0]
    
    fig.add_trace(
        go.Scatter3d(
            x=field_outline_x,
            y=field_outline_y,
            z=field_outline_z,
            mode='lines',
            line=dict(color='white', width=3),
            name="Field Outline",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Left penalty area
    left_penalty_x = [0, PENALTY_AREA_LENGTH, PENALTY_AREA_LENGTH, 0, 0]
    left_penalty_y = [-PENALTY_AREA_WIDTH/2, -PENALTY_AREA_WIDTH/2, 
                      PENALTY_AREA_WIDTH/2, PENALTY_AREA_WIDTH/2, -PENALTY_AREA_WIDTH/2]
    left_penalty_z = [0, 0, 0, 0, 0]
    
    fig.add_trace(
        go.Scatter3d(
            x=left_penalty_x,
            y=left_penalty_y,
            z=left_penalty_z,
            mode='lines',
            line=dict(color='white', width=2),
            name="Left Penalty Area",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Goal frame
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0, 0, 0, 0],
            y=[-GOAL_WIDTH/2, GOAL_WIDTH/2, GOAL_WIDTH/2, -GOAL_WIDTH/2, -GOAL_WIDTH/2],
            z=[0, 0, GOAL_HEIGHT, GOAL_HEIGHT, 0],
            mode='lines',
            line=dict(color='red', width=4),
            name="Goal",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Target areas (cylinders around goalposts)
    # Left post target area - only inside the goal
    theta = np.linspace(0, np.pi/2, 20)  # Only draw the quarter circle inside the goal
    z = np.linspace(0, GOAL_HEIGHT, 10)
    T, Z = np.meshgrid(theta, z)
    X = np.ones_like(T) * 0  # At the goal line
    Y = -GOAL_WIDTH/2 + TARGET_RADIUS * np.cos(T)
    Z = Z

    fig.add_trace(
        go.Scatter3d(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            mode='markers',
            marker=dict(
                size=3,
                color='rgba(255,255,0,0.5)',
                opacity=0.3
            ),
            name="Left Post Target Area"
        ),
        row=1, col=1
    )
    
    # Right post target area - only inside the goal
    theta = np.linspace(np.pi/2, np.pi, 20)  # Only draw the quarter circle inside the goal
    T, Z = np.meshgrid(theta, z)
    Y = GOAL_WIDTH/2 + TARGET_RADIUS * np.cos(T)
    
    fig.add_trace(
        go.Scatter3d(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            mode='markers',
            marker=dict(
                size=3,
                color='rgba(255,255,0,0.5)',
                opacity=0.3
            ),
            name="Right Post Target Area"
        ),
        row=1, col=1
    )
    
    # Corner kick position marker
    fig.add_trace(
        go.Scatter3d(
            x=[0],
            y=[-FIELD_WIDTH/2],
            z=[0],
            mode='markers',
            marker=dict(color='yellow', size=8),
            name="Corner Kick Position"
        ),
        row=1, col=1
    )
    
    # Add all trajectories
    for i, traj in enumerate(trajectories):
        params = traj['params']
        x, y, z, is_goal, is_near_post, flight_time = traj['data']
        score = traj['score']
        is_optimal = score < 500  # Check if it's a goal near the post
        color = COLORS[i % len(COLORS)]
        
        # Ball trajectory in 3D view
        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode='lines',
                line=dict(color=color, width=4),
                name=f"Trajectory {i+1} ({flight_time:.6f}s)" + (" ★" if is_optimal else "")
            ),
            row=1, col=1
        )
        
        # End position marker
        fig.add_trace(
            go.Scatter3d(
                x=[x[-1]],
                y=[y[-1]],
                z=[z[-1]],
                mode='markers',
                marker=dict(
                    color=color, 
                    size=10, 
                    symbol='circle',
                    line=dict(color='yellow', width=2) if is_near_post else None
                ),
                name=f"End {i+1}" + (" (Near Post)" if is_near_post else ""),
                showlegend=True
            ),
            row=1, col=1
        )
        
        # Top view (bird's eye view)
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                line=dict(color=color, width=3),
                name=f"Path {i+1}",
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Goal view
        goal_points = np.where(x < 20)[0]
        
        if len(goal_points) > 0:
            # Ball trajectory near goal (y-z projection)
            fig.add_trace(
                go.Scatter(
                    x=y[goal_points],
                    y=z[goal_points],
                    mode='lines',
                    line=dict(color=color, width=3),
                    name=f"Goal View {i+1}",
                    showlegend=False
                ),
                row=2, col=2
            )
    
    # Add target areas to goal view
    # Left post target area - only inside the goal
    theta = np.linspace(0, np.pi/2, 30)  # Only take the 0-90 degree portion, ensuring it's inside the goal
    x = -GOAL_WIDTH/2 + TARGET_RADIUS * np.cos(theta)
    y = TARGET_RADIUS * np.sin(theta)
    
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='yellow', width=2, dash='dash'),
            fill='toself',
            fillcolor='rgba(255,255,0,0.1)',
            name="Left Post Target",
            showlegend=False
        ),
        row=2, col=2
    )
    
    # Right post target area - only inside the goal
    theta = np.linspace(np.pi/2, np.pi, 30)  # Only take the 90-180 degree portion, ensuring it's inside the goal
    x = GOAL_WIDTH/2 + TARGET_RADIUS * np.cos(theta)
    
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='yellow', width=2, dash='dash'),
            fill='toself',
            fillcolor='rgba(255,255,0,0.1)',
            name="Right Post Target",
            showlegend=False
        ),
        row=2, col=2
    )
    
    # Add goal outline to goal view
    fig.add_trace(
        go.Scatter(
            x=[-GOAL_WIDTH/2, GOAL_WIDTH/2, GOAL_WIDTH/2, -GOAL_WIDTH/2, -GOAL_WIDTH/2],
            y=[0, 0, GOAL_HEIGHT, GOAL_HEIGHT, 0],
            mode='lines',
            line=dict(color='red', width=3),
            fill='toself',
            fillcolor='rgba(255,0,0,0.1)',
            name="Goal",
            showlegend=False
        ),
        row=2, col=2
    )
    
    # Top view field outline
    fig.add_trace(
        go.Scatter(
            x=[0, FIELD_LENGTH, FIELD_LENGTH, 0, 0],
            y=[-FIELD_WIDTH/2, -FIELD_WIDTH/2, FIELD_WIDTH/2, FIELD_WIDTH/2, -FIELD_WIDTH/2],
            mode='lines',
            line=dict(color='white', width=2),
            fill='toself',
            fillcolor='green',
            opacity=0.6,
            name="Field",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Configure 3D scene
    fig.update_scenes(
        aspectmode='data',
        xaxis_title="X [m]",
        yaxis_title="Y [m]",
        zaxis_title="Z [m]",
        camera=dict(
            eye=dict(x=-0.5, y=-1.5, z=1.5)
        )
    )
    
    # Configure 2D plots
    fig.update_xaxes(range=[-5, FIELD_LENGTH+5], title_text="X [m]", row=2, col=1)
    fig.update_yaxes(title_text="Y [m]", row=2, col=1)
    fig.update_xaxes(range=[-GOAL_WIDTH/2-TARGET_RADIUS-1, GOAL_WIDTH/2+TARGET_RADIUS+1], title_text="Y [m]", row=2, col=2)
    fig.update_yaxes(range=[0, GOAL_HEIGHT+1], title_text="Z [m]", row=2, col=2)
    
    # Create parameter summary
    param_text = "<br>".join([
        f"<b>Trajectory {i+1}:</b> {traj['data'][5]:.6f}s" +
        (f" <b style='color:gold'>★</b>" if traj['score'] < 500 else "") +
        f"<br>Near Post: {'Yes' if traj['data'][4] else 'No'}" +
        f"<br>Speed: {params[0]:.1f} m/s" +
        f"<br>Elevation: {params[1]:.1f}°" +
        f"<br>Horizontal: {params[2]:.1f}°" +
        f"<br>Spin: {params[3]:.1f} rad/s<br>"
        for i, (traj, params) in enumerate(zip(trajectories, [t['params'] for t in trajectories]))
    ])
    
    # Set layout with annotations
    fig.update_layout(
        title_text="Top 3 Olympic Goals Targeting Goalposts",
        height=900,
        width=1000,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        annotations=[
            dict(
                text="OPTIMAL GOAL TRAJECTORIES",
                x=0.5,
                y=0.02,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(
                    size=20,
                    color="red"
                )
            ),
            dict(
                text=param_text,
                x=0.98,
                y=0.98,
                xref="paper",
                yref="paper",
                showarrow=False,
                align="right"
            )
        ]
    )
    
    # Save to HTML file
    output_file = 'optimal_corner_kicks.html'
    pio.write_html(fig, file=output_file, auto_open=True)
    print(f"Interactive visualization saved to {os.path.abspath(output_file)}")
    
    return fig