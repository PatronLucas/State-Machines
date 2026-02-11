"""
Interactive 8-Puzzle Visualizer using Streamlit

This app allows you to:
1. Visualize the 8-puzzle state machine
2. Try to solve impossible puzzles
3. Understand the inversion invariant
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lessons.lesson2_eight_puzzle import EightPuzzle, count_inversions, has_odd_inversions
import plotly.graph_objects as go


def create_puzzle_visualization(state, title="Puzzle State"):
    """Create a visual representation of the puzzle using Plotly."""
    # Create a 3x3 grid
    grid_values = []
    grid_text = []
    
    for i in range(3):
        row_values = []
        row_text = []
        for j in range(3):
            val = state[i * 3 + j]
            if val == 0:
                row_values.append(0.5)  # Gray for empty
                row_text.append("*")
            else:
                row_values.append(val)
                row_text.append(str(val))
        grid_values.append(row_values)
        grid_text.append(row_text)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=grid_values,
        text=grid_text,
        texttemplate="<b>%{text}</b>",
        textfont={"size": 40},
        colorscale=[[0, 'lightgray'], [0.5, 'lightgray'], [1, 'lightblue']],
        showscale=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=title,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=400,
        height=400,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def main():
    st.set_page_config(page_title="8-Puzzle Visualizer", layout="wide")
    
    st.title("🧩 The 8-Puzzle Interactive Visualizer")
    st.markdown("### Proving Impossibility with the Invariant Principle")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Predefined configurations
    preset = st.sidebar.selectbox(
        "Choose a preset:",
        ["Classic Impossible", "Solvable", "Already Solved", "Custom"]
    )
    
    if preset == "Classic Impossible":
        initial_state = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    elif preset == "Solvable":
        initial_state = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    elif preset == "Already Solved":
        initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    else:  # Custom
        st.sidebar.markdown("Enter tiles (use 0 for blank):")
        custom_input = st.sidebar.text_input(
            "9 numbers separated by spaces",
            "1 2 3 4 5 6 8 7 0"
        )
        try:
            initial_state = tuple(int(x) for x in custom_input.split())
            if len(initial_state) != 9 or set(initial_state) != set(range(9)):
                st.sidebar.error("Invalid input! Use digits 0-8 exactly once.")
                initial_state = (1, 2, 3, 4, 5, 6, 8, 7, 0)
        except:
            st.sidebar.error("Invalid format!")
            initial_state = (1, 2, 3, 4, 5, 6, 8, 7, 0)
    
    # Create puzzle
    puzzle = EightPuzzle(initial_state)
    
    # Two columns for current and target
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current State")
        fig1 = create_puzzle_visualization(puzzle.current_state, "Current Configuration")
        st.plotly_chart(fig1, use_container_width=True)
        
        inversions = count_inversions(puzzle.current_state)
        parity = "ODD" if inversions % 2 == 1 else "EVEN"
        
        st.metric("Inversions", inversions)
        st.metric("Parity", parity)
    
    with col2:
        st.subheader("Target State (Solved)")
        target = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        fig2 = create_puzzle_visualization(target, "Goal Configuration")
        st.plotly_chart(fig2, use_container_width=True)
        
        target_inversions = count_inversions(target)
        target_parity = "ODD" if target_inversions % 2 == 1 else "EVEN"
        
        st.metric("Inversions", target_inversions)
        st.metric("Parity", target_parity)
    
    # Analysis
    st.markdown("---")
    st.header("🔍 Reachability Analysis")
    
    if parity == target_parity:
        st.success("✅ **POTENTIALLY SOLVABLE!** Both states have the same parity.")
        st.info("This doesn't guarantee a solution exists, but it's necessary!")
    else:
        st.error("❌ **IMPOSSIBLE TO SOLVE!** Different parities.")
        st.warning(f"""
        **Proof by Invariant Principle:**
        
        1. Initial state has **{parity}** parity ({inversions} inversions)
        2. Target state has **{target_parity}** parity ({target_inversions} inversions)
        3. The parity is an **invariant** (preserved by all moves)
        4. Therefore, the target state is **UNREACHABLE**!
        """)
    
    # Available moves
    st.markdown("---")
    st.header("🎮 Available Moves")
    
    if 'execution_history' not in st.session_state:
        st.session_state.execution_history = [puzzle.current_state]
    
    transitions = puzzle.get_transitions(puzzle.current_state)
    
    if transitions:
        st.write(f"From the current state, you can make **{len(transitions)}** moves:")
        
        cols = st.columns(min(len(transitions), 4))
        
        for i, next_state in enumerate(transitions):
            with cols[i % 4]:
                next_inversions = count_inversions(next_state)
                next_parity = "ODD" if next_inversions % 2 == 1 else "EVEN"
                
                st.write(f"**Move {i+1}**")
                mini_fig = create_puzzle_visualization(next_state, f"Move {i+1}")
                mini_fig.update_layout(width=200, height=200)
                st.plotly_chart(mini_fig, use_container_width=True)
                
                st.caption(f"Inversions: {next_inversions} ({next_parity})")
                
                if st.button(f"Make Move {i+1}", key=f"move_{i}"):
                    puzzle.step(next_state)
                    st.session_state.execution_history.append(next_state)
                    st.experimental_rerun()
    else:
        st.info("🏁 No moves available (final state)")
    
    # Explanation
    st.markdown("---")
    st.header("📚 Understanding Inversions")
    
    with st.expander("What is an inversion?"):
        st.markdown("""
        An **inversion** is a pair of tiles (i, j) where:
        - Tile i appears before tile j in the sequence
        - But i has a larger number than j
        
        Example: In sequence [3, 1, 2], there are 2 inversions:
        - (3, 1): 3 comes before 1, but 3 > 1
        - (3, 2): 3 comes before 2, but 3 > 2
        
        We ignore the blank tile (0) when counting inversions.
        """)
    
    with st.expander("Why is parity preserved?"):
        st.markdown("""
        **Horizontal moves**: Don't change the sequence (just swap blank with neighbor)
        - Inversions stay the same
        
        **Vertical moves**: Shuffle 3 adjacent elements
        - Change inversions by ±2
        - Parity (odd/even) is preserved!
        
        Since all moves preserve parity, it's an **invariant**!
        """)
    
    # Show inversion details
    with st.expander("See detailed inversion calculation"):
        sequence = [x for x in puzzle.current_state if x != 0]
        st.write(f"Sequence (without blank): {sequence}")
        
        inversions_list = []
        for i in range(len(sequence)):
            for j in range(i + 1, len(sequence)):
                if sequence[i] > sequence[j]:
                    inversions_list.append((sequence[i], sequence[j]))
        
        if inversions_list:
            st.write(f"Inversions found ({len(inversions_list)}):")
            for pair in inversions_list:
                st.write(f"  - {pair[0]} > {pair[1]}")
        else:
            st.write("No inversions! (Sorted sequence)")


if __name__ == "__main__":
    main()
