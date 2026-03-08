"""
Visualization utilities for state machines

This module provides helper functions for visualizing state machines,
executions, and other concepts using matplotlib and plotly.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Any
import numpy as np


def visualize_puzzle_state(state: Tuple, title: str = "Puzzle State"):
    """
    Visualize an 8-puzzle state using matplotlib.
    
    Args:
        state: Tuple of 9 elements representing the puzzle
        title: Title for the plot
    """
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    
    # Draw grid
    for i in range(3):
        for j in range(3):
            val = state[i * 3 + j]
            
            # Draw cell
            rect = patches.Rectangle(
                (j, 2-i), 1, 1,
                linewidth=2,
                edgecolor='black',
                facecolor='lightblue' if val != 0 else 'lightgray'
            )
            ax.add_patch(rect)
            
            # Add text
            if val != 0:
                ax.text(
                    j + 0.5, 2 - i + 0.5, str(val),
                    ha='center', va='center',
                    fontsize=24, fontweight='bold'
                )
            else:
                ax.text(
                    j + 0.5, 2 - i + 0.5, '*',
                    ha='center', va='center',
                    fontsize=24, fontweight='bold',
                    color='gray'
                )
    
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig


def visualize_sequence(sequence: List, title: str = "Sequence", highlight_indices: List[int] = None):
    """
    Visualize a sequence as a bar chart.
    
    Args:
        sequence: List of numbers to visualize
        title: Title for the plot
        highlight_indices: Indices to highlight in a different color
    """
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    
    colors = ['steelblue'] * len(sequence)
    if highlight_indices:
        for idx in highlight_indices:
            if 0 <= idx < len(sequence):
                colors[idx] = 'orange'
    
    bars = ax.bar(range(len(sequence)), sequence, color=colors, edgecolor='black')
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, sequence)):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2., height,
            str(val),
            ha='center', va='bottom',
            fontsize=12, fontweight='bold'
        )
    
    ax.set_xlabel('Position', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(sequence)))
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def visualize_potential_function(history: List[Tuple], potential_func):
    """
    Visualize how a potential function changes over execution.
    
    Args:
        history: List of states in the execution
        potential_func: Function that takes a state and returns a number
    """
    values = [potential_func(state) for state in history]
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    
    ax.plot(values, marker='o', linewidth=2, markersize=8, color='steelblue')
    ax.fill_between(range(len(values)), values, alpha=0.3, color='steelblue')
    
    ax.set_xlabel('Step', fontsize=12)
    ax.set_ylabel('Potential Function Value', fontsize=12)
    ax.set_title('Potential Function Over Time', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Annotate start and end
    ax.annotate(
        f'Start: {values[0]}',
        xy=(0, values[0]),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
    )
    
    if len(values) > 1:
        ax.annotate(
            f'End: {values[-1]}',
            xy=(len(values)-1, values[-1]),
            xytext=(10, -10),
            textcoords='offset points',
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )
    
    plt.tight_layout()
    return fig


def visualize_state_graph(state_machine, max_states: int = 20):
    """
    Visualize the state transition graph (for small state spaces).
    
    Note: This uses a simple layout. For complex graphs, consider using networkx.
    
    Args:
        state_machine: The state machine to visualize
        max_states: Maximum number of states to visualize
    """
    # BFS to explore states
    initial = state_machine.get_initial_state()
    visited = {initial}
    queue = [initial]
    edges = []
    states = [initial]
    
    while queue and len(states) < max_states:
        state = queue.pop(0)
        
        for next_state in state_machine.get_transitions(state):
            edges.append((state, next_state))
            
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
                states.append(next_state)
    
    # Simple visualization
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Arrange states in a circle
    n = len(states)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    
    # State positions
    state_pos = {}
    for i, state in enumerate(states):
        x = np.cos(angles[i])
        y = np.sin(angles[i])
        state_pos[state] = (x, y)
    
    # Draw edges
    for start, end in edges:
        if start in state_pos and end in state_pos:
            x1, y1 = state_pos[start]
            x2, y2 = state_pos[end]
            
            ax.annotate(
                '',
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->',
                    lw=1.5,
                    color='gray',
                    connectionstyle='arc3,rad=0.1'
                )
            )
    
    # Draw states
    for state, (x, y) in state_pos.items():
        # Highlight initial state
        if state == initial:
            color = 'lightgreen'
            size = 800
        # Highlight final states
        elif state_machine.is_final_state(state):
            color = 'lightcoral'
            size = 800
        else:
            color = 'lightblue'
            size = 600
        
        ax.scatter([x], [y], s=size, c=color, edgecolors='black', linewidths=2, zorder=3)
        
        # State label
        label = str(state)
        if len(label) > 15:
            label = label[:12] + "..."
        
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', zorder=4)
    
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(
        'State Transition Graph\n(Green=Initial, Red=Final)',
        fontsize=14,
        fontweight='bold'
    )
    
    plt.tight_layout()
    return fig


def save_visualization(fig, filename: str):
    """
    Save a matplotlib figure to a file.
    
    Args:
        fig: Matplotlib figure
        filename: Output filename (with extension)
    """
    fig.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved visualization to {filename}")


if __name__ == "__main__":
    # Test visualizations
    print("Testing visualization utilities...")
    
    # Test puzzle visualization
    puzzle_state = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    fig1 = visualize_puzzle_state(puzzle_state, "Test Puzzle")
    save_visualization(fig1, "/tmp/test_puzzle.png")
    
    # Test sequence visualization
    sequence = [4, 1, 3, 2]
    fig2 = visualize_sequence(sequence, "Test Sequence", highlight_indices=[0, 1])
    save_visualization(fig2, "/tmp/test_sequence.png")
    
    print("Visualizations created successfully!")
