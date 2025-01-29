import math
import pandas as pd

def calculate_sheathing(length: float, width: float, height: float, pitch: float, 
                       overhang: float, sheet_width: float) -> dict:
    """
    Dynamically calculates the required metal sheets for walls, gable ends, and roof.

    Args:
        length (float): Length of the building in feet
        width (float): Width of the building in feet
        height (float): Wall height in feet
        pitch (float): Roof pitch (x/12)
        overhang (float): Overhang length in inches
        sheet_width (float): Sheet width in inches

    Returns:
        dict: Dictionary containing sheathing calculations
    """
    # Convert sheet width and overhang from inches to feet
    sheet_width_ft = sheet_width / 12  
    overhang_ft = overhang / 12

    # Adjust building dimensions for overhang
    gable_width = width + 2 * overhang_ft  # Include overhang
    half_gable_width = gable_width / 2  # Half-width for triangle calculations

    # Calculate peak height using pitch
    peak_height = (half_gable_width) * (pitch / 12)
    total_gable_height = height + peak_height

    # Calculate number of sheets needed for gable width
    num_sheets = math.ceil(width / sheet_width_ft)

    # Calculate sheet length increment based on peak height and number of sheets
    length_increment = 1.0  # Fixed 1 foot increment as per requirement

    # Generate gable sheet lengths starting 1ft below peak height
    gable_sheet_lengths = []
    start_length = math.floor(total_gable_height) - (num_sheets - 1)

    for i in range(num_sheets):
        sheet_length = start_length + (i * length_increment)
        gable_sheet_lengths.append(sheet_length)

    # Walls
    eave_wall_sheets = math.ceil(length / sheet_width_ft) * 2
    wall_sheet_length = height

    # Roof
    roof_run = half_gable_width
    roof_slope_length = math.sqrt(roof_run**2 + peak_height**2)
    roof_length = length + 2 * overhang_ft
    roof_sheets_per_side = math.ceil(roof_length / sheet_width_ft)
    roof_sheet_length = math.ceil(roof_slope_length * 2) / 2  # Round up to 0.5'
    total_roof_sheets = roof_sheets_per_side * 2

    return {
        "Eave Walls": {"Sheets": eave_wall_sheets, "Sheet Length": wall_sheet_length},
        "Gable Triangles": {"Sheets": num_sheets * 2, "Sheet Lengths": gable_sheet_lengths},
        "Roof": {"Sheets": total_roof_sheets, "Sheet Length": roof_sheet_length},
    }

def format_results(results: dict) -> pd.DataFrame:
    """
    Format calculation results into a pandas DataFrame.

    Args:
        results (dict): Dictionary containing sheathing calculations

    Returns:
        pd.DataFrame: Formatted results
    """
    formatted_data = []

    for section, details in results.items():
        if section == "Gable Triangles":
            lengths_str = ", ".join(f"{length:.1f}'" for length in details["Sheet Lengths"])
            formatted_data.append({
                "Section": section,
                "Number of Sheets": details["Sheets"],
                "Sheet Length (ft)": f"Variable: {lengths_str}",
                "Notes": "Staggered lengths for optimal coverage"
            })
        else:
            formatted_data.append({
                "Section": section,
                "Number of Sheets": details["Sheets"],
                "Sheet Length (ft)": f"{details['Sheet Length']:.1f}",
                "Notes": ""
            })

    return pd.DataFrame(formatted_data)