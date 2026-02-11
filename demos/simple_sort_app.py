"""
Interactive Simple Sort Visualizer using Streamlit

This app demonstrates:
1. The simple sort algorithm
2. How the potential function (inversions) decreases
3. Proof of termination
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lessons.lesson3_simple_sort import SimpleSortMachine, count_inversions
import plotly.graph_objects as go
import time


def create_bar_chart(sequence, title="Current Sequence", highlight_indices=None):
    """Create a bar chart visualization of the sequence."""
    colors = ['lightblue'] * len(sequence)
    
    if highlight_indices:
        for idx in highlight_indices:
            if 0 <= idx < len(sequence):
                colors[idx] = 'orange'
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(range(len(sequence))),
            y=list(sequence),
            text=list(sequence),
            textposition='auto',
            marker_color=colors,
            textfont=dict(size=16, color='white'),
        )
    ])
    
    fig.update_layout(
        title=title,
        xaxis_title="Position",
        yaxis_title="Value",
        height=400,
        showlegend=False,
        xaxis=dict(tickmode='linear'),
    )
    
    return fig


def create_potential_chart(history):
    """Create a line chart showing the potential function over time."""
    inversions = [count_inversions(state) for state in history]
    
    fig = go.Figure(data=[
        go.Scatter(
            x=list(range(len(inversions))),
            y=inversions,
            mode='lines+markers',
            marker=dict(size=10, color='blue'),
            line=dict(width=2, color='blue'),
            fill='tozeroy',
            fillcolor='rgba(0, 100, 255, 0.2)'
        )
    ])
    
    fig.update_layout(
        title="Potential Function Over Time",
        xaxis_title="Step",
        yaxis_title="Number of Inversions",
        height=300,
    )
    
    return fig


def main():
    st.set_page_config(page_title="Simple Sort Visualizer", layout="wide")
    
    st.title("Simple Sort Algorithm Visualizer")
    st.markdown("### Proving Termination with Potential Functions")
    
    # Sidebar
    st.sidebar.header("Configuration")
    
    # Choose preset or custom
    preset = st.sidebar.selectbox(
        "Choose a preset:",
        ["Random Small", "Reversed", "Nearly Sorted", "Custom"]
    )
    
    if preset == "Random Small":
        initial_sequence = [4, 1, 3, 2]
    elif preset == "Reversed":
        initial_sequence = [5, 4, 3, 2, 1]
    elif preset == "Nearly Sorted":
        initial_sequence = [1, 3, 2, 4, 5]
    else:  # Custom
        custom_input = st.sidebar.text_input(
            "Enter numbers separated by spaces",
            "4 1 3 2"
        )
        try:
            initial_sequence = [int(x) for x in custom_input.split()]
            if len(initial_sequence) < 2:
                st.sidebar.error("Need at least 2 numbers!")
                initial_sequence = [4, 1, 3, 2]
        except:
            st.sidebar.error("Invalid format!")
            initial_sequence = [4, 1, 3, 2]
    
    # Speed control
    animation_speed = st.sidebar.slider("Animation Speed", 0.1, 2.0, 0.5, 0.1)
    
    # Initialize session state
    if 'sorter' not in st.session_state or st.sidebar.button("Reset"):
        st.session_state.sorter = SimpleSortMachine(initial_sequence)
        st.session_state.history = [st.session_state.sorter.current_state]
        st.session_state.step_count = 0
        st.session_state.is_running = False
    
    sorter = st.session_state.sorter
    
    # Main display area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current State")
        
        # Find which elements are out of order
        current = sorter.current_state
        highlight = []
        for i in range(len(current) - 1):
            if current[i] > current[i + 1]:
                highlight.extend([i, i + 1])
                break
        
        fig = create_bar_chart(
            current,
            f"Step {st.session_state.step_count}",
            highlight
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Statistics")
        
        inversions = count_inversions(current)
        is_sorted = sorter.is_sorted()
        
        st.metric("Current Step", st.session_state.step_count)
        st.metric("Inversions (Potential)", inversions)
        st.metric("Status", "Sorted" if is_sorted else "Sorting")
        
        # Max possible inversions
        n = len(current)
        max_inversions = n * (n - 1) // 2
        st.metric("Max Possible Steps", max_inversions)
    
    # Controls
    st.markdown("---")
    control_cols = st.columns(4)
    
    with control_cols[0]:
        if st.button("Step", disabled=st.session_state.is_running):
            transitions = sorter.get_transitions(sorter.current_state)
            if transitions:
                sorter.step(transitions[0])
                st.session_state.history.append(sorter.current_state)
                st.session_state.step_count += 1
                st.experimental_rerun()
    
    with control_cols[1]:
        if st.button("Run to Completion", disabled=st.session_state.is_running):
            st.session_state.is_running = True
            
    with control_cols[2]:
        if st.button("Reset"):
            st.session_state.sorter = SimpleSortMachine(initial_sequence)
            st.session_state.history = [st.session_state.sorter.current_state]
            st.session_state.step_count = 0
            st.session_state.is_running = False
            st.experimental_rerun()
    
    # Auto-run
    if st.session_state.is_running:
        if not sorter.is_sorted():
            time.sleep(animation_speed)
            transitions = sorter.get_transitions(sorter.current_state)
            if transitions:
                sorter.step(transitions[0])
                st.session_state.history.append(sorter.current_state)
                st.session_state.step_count += 1
                st.experimental_rerun()
        else:
            st.session_state.is_running = False
            st.experimental_rerun()
    
    # Potential function chart
    if len(st.session_state.history) > 1:
        st.markdown("---")
        st.subheader("Potential Function Visualization")
        
        pot_fig = create_potential_chart(st.session_state.history)
        st.plotly_chart(pot_fig, use_container_width=True)
        
        st.info("""
        **Key Observation**: The potential function (number of inversions) 
        **strictly decreases** with each step. Since it's a natural number 
        and can't go below 0, the algorithm **must terminate**!
        """)
    
    # Show available transitions
    if not sorter.is_sorted():
        st.markdown("---")
        st.subheader("Available Swaps")
        
        transitions = sorter.get_transitions(sorter.current_state)
        
        if transitions:
            st.write(f"Found **{len(transitions)}** pairs of adjacent elements out of order:")
            
            trans_cols = st.columns(min(len(transitions), 4))
            
            for i, next_state in enumerate(transitions):
                with trans_cols[i % 4]:
                    next_inversions = count_inversions(next_state)
                    decrease = inversions - next_inversions
                    
                    st.write(f"**Option {i+1}**")
                    st.write(f"Result: {list(next_state)}")
                    st.write(f"Inversions: {inversions} → {next_inversions}")
                    st.write(f"Decrease: -{decrease}")
    else:
        st.success("**Sorting Complete!** Reached the final state.")
    
    # Educational content
    st.markdown("---")
    st.header("Understanding Termination Proofs")
    
    with st.expander("What is a Potential Function?"):
        st.markdown("""
        A **potential function** (or derived variable) is a function that maps 
        states to real numbers. For the simple sort algorithm:
        
        **f(state) = number of inversions in the state**
        
        Key properties:
        1. Maps to **natural numbers** (0, 1, 2, ...)
        2. **Strictly decreasing**: f(next) < f(current) for all transitions
        3. Natural numbers can't decrease forever
        4. Therefore: algorithm **must terminate**!
        """)
    
    with st.expander("Why does it strictly decrease?"):
        st.markdown("""
        In each step of simple sort:
        1. We find indices i where a[i] > a[i+1]
        2. We swap them
        3. This converts one inversion into a non-inversion
        4. No other pairs change their inversion status
        5. Therefore: inversions decrease by **exactly 1**
        
        Since we only make swaps when elements are out of order, 
        the potential function is **strictly decreasing**!
        """)
    
    with st.expander("Termination Proof"):
        st.markdown(f"""
        **Theorem**: Simple sort terminates in at most n(n-1)/2 steps.
        
        **Proof**:
        1. Initial inversions ≤ n(n-1)/2 (for sequence of length n)
        2. Each step decreases inversions by 1
        3. Inversions cannot be negative
        4. Therefore, max steps = initial inversions ≤ n(n-1)/2
        
        For your sequence of length {len(initial_sequence)}:
        - Maximum inversions = {len(initial_sequence)} × {len(initial_sequence)-1} / 2 = {max_inversions}
        - Therefore: guaranteed to terminate in ≤ {max_inversions} steps
        """)
    
    # Show execution history
    if st.session_state.step_count > 0:
        with st.expander("View Execution History"):
            for i, state in enumerate(st.session_state.history):
                inv = count_inversions(state)
                st.write(f"Step {i}: {list(state)} (inversions: {inv})")


if __name__ == "__main__":
    main()
