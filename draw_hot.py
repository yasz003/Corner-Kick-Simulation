import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
from config import GOAL_WIDTH, GOAL_HEIGHT

def visualize_goal_distribution(csv_file='corner_kick_goals.csv'):
    """
    Read corner kick goal data and create distribution visualizations
    
    Args:
        csv_file: Path to the CSV file containing goal data
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        print(f"Successfully read {len(df)} goal records")
        
        if len(df) == 0:
            print("No goal data available for analysis")
            return
            
        # Create figure
        fig = plt.figure(figsize=(15, 10))
        
        # 1. Scatter plot - Show all goal positions
        ax1 = fig.add_subplot(221)
        scatter = ax1.scatter(df['y_pos'], df['z_pos'], c=df['is_near_post'].astype(int), 
                             cmap='coolwarm', alpha=0.7, s=50)
        
        # Draw goal frame
        goal_left = -GOAL_WIDTH/2
        goal_right = GOAL_WIDTH/2
        ax1.plot([goal_left, goal_right], [0, 0], 'k-', lw=3)  # Ground line
        ax1.plot([goal_left, goal_left], [0, GOAL_HEIGHT], 'k-', lw=3)  # Left post
        ax1.plot([goal_right, goal_right], [0, GOAL_HEIGHT], 'k-', lw=3)  # Right post
        ax1.plot([goal_left, goal_right], [GOAL_HEIGHT, GOAL_HEIGHT], 'k-', lw=3)  # Crossbar
        
        # Add labels and legend
        ax1.set_xlabel('Y Position (m)', fontsize=12)
        ax1.set_ylabel('Z Position (m)', fontsize=12)
        ax1.set_title('Goal Position Distribution', fontsize=14, fontweight='bold')
        legend = ax1.legend(*scatter.legend_elements(), title="Near Post")
        ax1.add_artist(legend)
        ax1.grid(True, alpha=0.3)
        
        # 2. Heat map - Show goal density
        ax2 = fig.add_subplot(222)
        sns.kdeplot(data=df, x='y_pos', y='z_pos', fill=True, cmap='viridis', ax=ax2)
        
        # Draw goal frame
        ax2.plot([goal_left, goal_right], [0, 0], 'r-', lw=2)  # Ground line
        ax2.plot([goal_left, goal_left], [0, GOAL_HEIGHT], 'r-', lw=2)  # Left post
        ax2.plot([goal_right, goal_right], [0, GOAL_HEIGHT], 'r-', lw=2)  # Right post
        ax2.plot([goal_left, goal_right], [GOAL_HEIGHT, GOAL_HEIGHT], 'r-', lw=2)  # Crossbar
        
        ax2.set_xlabel('Y Position (m)', fontsize=12)
        ax2.set_ylabel('Z Position (m)', fontsize=12)
        ax2.set_title('Goal Density Distribution', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # 3. Histogram - Show Y position distribution (horizontal)
        ax3 = fig.add_subplot(223)
        sns.histplot(data=df, x='y_pos', kde=True, ax=ax3)
        ax3.axvline(goal_left, color='r', linestyle='--', alpha=0.7)
        ax3.axvline(goal_right, color='r', linestyle='--', alpha=0.7)
        ax3.set_xlabel('Y Position (m)', fontsize=12)
        ax3.set_ylabel('Frequency', fontsize=12)
        ax3.set_title('Horizontal Distribution', fontsize=14, fontweight='bold')
        
        # 4. Histogram - Show Z position distribution (height)
        ax4 = fig.add_subplot(224)
        sns.histplot(data=df, x='z_pos', kde=True, ax=ax4)
        ax4.axvline(0, color='r', linestyle='--', alpha=0.7)
        ax4.axvline(GOAL_HEIGHT, color='r', linestyle='--', alpha=0.7)
        ax4.set_xlabel('Z Position (m)', fontsize=12)
        ax4.set_ylabel('Frequency', fontsize=12)
        ax4.set_title('Height Distribution', fontsize=14, fontweight='bold')
        
        # Add parameter distribution info
        plt.suptitle('Corner Kick Goal Distribution Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save figure
        output_file = 'goal_distribution_analysis.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved as: {output_file}")
        
        # Show figure
        plt.show()
        
        # 5. Create additional 2D heatmap of goal area
        plt.figure(figsize=(10, 6))
        
        # Create grid
        y_bins = np.linspace(goal_left, goal_right, 30)
        z_bins = np.linspace(0, GOAL_HEIGHT, 20)
        
        # Calculate 2D histogram
        h, y_edges, z_edges = np.histogram2d(df['y_pos'], df['z_pos'], bins=[y_bins, z_bins])
        
        # Draw heatmap
        plt.pcolormesh(y_edges, z_edges, h.T, cmap='hot')
        plt.colorbar(label='Number of Goals')
        
        # Add goal frame
        plt.plot([goal_left, goal_right], [0, 0], 'w-', lw=2)
        plt.plot([goal_left, goal_left], [0, GOAL_HEIGHT], 'w-', lw=2)
        plt.plot([goal_right, goal_right], [0, GOAL_HEIGHT], 'w-', lw=2)
        plt.plot([goal_left, goal_right], [GOAL_HEIGHT, GOAL_HEIGHT], 'w-', lw=2)
        
        plt.xlabel('Y Position (m)', fontsize=12)
        plt.ylabel('Z Position (m)', fontsize=12)
        plt.title('Goal Area Heatmap', fontsize=14, fontweight='bold')
        
        # Save heatmap
        plt.savefig('goal_heatmap.png', dpi=300, bbox_inches='tight')
        print("Goal heatmap saved as: goal_heatmap.png")
        
        plt.show()
        
        # 6. Output statistics
        print("\nGoal Statistics:")
        print(f"Total goals: {len(df)}")
        print(f"Goals near post: {df['is_near_post'].sum()}")
        print(f"Average goal height: {df['z_pos'].mean():.2f} m")
        
        # Area statistics
        left_area = df[df['y_pos'] < -GOAL_WIDTH/6]
        center_area = df[(df['y_pos'] >= -GOAL_WIDTH/6) & (df['y_pos'] <= GOAL_WIDTH/6)]
        right_area = df[df['y_pos'] > GOAL_WIDTH/6]
        
        print("\nArea Statistics:")
        print(f"Left area goals: {len(left_area)} ({len(left_area)/len(df)*100:.1f}%)")
        print(f"Center area goals: {len(center_area)} ({len(center_area)/len(df)*100:.1f}%)")
        print(f"Right area goals: {len(right_area)} ({len(right_area)/len(df)*100:.1f}%)")
        
        # Height statistics
        lower_third = df[df['z_pos'] <= GOAL_HEIGHT/3]
        middle_third = df[(df['z_pos'] > GOAL_HEIGHT/3) & (df['z_pos'] <= 2*GOAL_HEIGHT/3)]
        upper_third = df[df['z_pos'] > 2*GOAL_HEIGHT/3]
        
        print("\nHeight Statistics:")
        print(f"Lower third goals: {len(lower_third)} ({len(lower_third)/len(df)*100:.1f}%)")
        print(f"Middle third goals: {len(middle_third)} ({len(middle_third)/len(df)*100:.1f}%)")
        print(f"Upper third goals: {len(upper_third)} ({len(upper_third)/len(df)*100:.1f}%)")
        
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    visualize_goal_distribution()