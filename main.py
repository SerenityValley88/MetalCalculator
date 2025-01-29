import streamlit as st
import pandas as pd
from utils import calculate_sheathing, format_results

# Page configuration
st.set_page_config(
    page_title="Construction Sheathing Calculator",
    page_icon="🏗️",
    layout="wide"
)

# Load custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title and introduction
st.title("🏗️ Construction Sheathing Calculator")
st.markdown("""
This calculator helps you determine the number of sheets needed for wall and roof sheathing
in your construction project. Enter the building dimensions below to get started.
""")

# Input form
with st.form("sheathing_calculator"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Building Dimensions")
        length = st.number_input(
            "Building Length (ft)",
            min_value=1.0,
            max_value=200.0,
            value=40.0,
            help="Enter the length of the building in feet"
        )
        
        width = st.number_input(
            "Building Width (ft)",
            min_value=1.0,
            max_value=200.0,
            value=30.0,
            help="Enter the width of the building in feet"
        )
        
        height = st.number_input(
            "Wall Height (ft)",
            min_value=1.0,
            max_value=40.0,
            value=10.0,
            help="Enter the height of the walls in feet"
        )

    with col2:
        st.markdown("### Roof Specifications")
        pitch = st.number_input(
            "Roof Pitch (x/12)",
            min_value=1.0,
            max_value=12.0,
            value=4.0,
            help="Enter the roof pitch (rise over run, e.g., 4 for a 4/12 pitch)"
        )
        
        overhang = st.number_input(
            "Overhang (inches)",
            min_value=0.0,
            max_value=48.0,
            value=16.0,
            help="Enter the overhang length in inches"
        )
        
        sheet_width = st.number_input(
            "Sheet Width (inches)",
            min_value=24.0,
            max_value=48.0,
            value=36.0,
            help="Enter the width of the sheathing sheets in inches"
        )

    calculate_button = st.form_submit_button("Calculate Sheathing")

# Calculate and display results
if calculate_button:
    try:
        # Perform calculations
        results = calculate_sheathing(
            length=length,
            width=width,
            height=height,
            pitch=pitch,
            overhang=overhang,
            sheet_width=sheet_width
        )
        
        # Display results
        st.markdown("### 📊 Calculation Results")
        
        # Format and display results table
        results_df = format_results(results)
        st.dataframe(
            results_df,
            hide_index=True,
            use_container_width=True
        )
        
        # Additional information
        st.markdown("### 📝 Notes")
        st.markdown("""
        - Sheet counts are rounded up to the nearest whole number
        - Gable triangle sections use staggered sheet lengths for optimal coverage
        - All measurements assume standard construction practices
        - Additional material should be ordered to account for waste and cuts
        """)
        
    except Exception as e:
        st.error(f"An error occurred during calculations: {str(e)}")
        st.markdown("Please check your input values and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Made for construction professionals | All calculations are estimates</small>
</div>
""", unsafe_allow_html=True)
