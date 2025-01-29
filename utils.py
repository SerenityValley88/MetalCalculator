import math
import pandas as pd

def calculate_sheathing(length: float, width: float, height: float, pitch: float, 
                       overhang: float, sheet_width: float) -> dict:
    """
    Calculate sheathing requirements for building construction.
    
    Args:
        length (float): Building length in feet
        width (float): Building width in feet
        height (float): Wall height in feet
        pitch (float): Roof pitch (x/12)
        overhang (float): Overhang length in inches
        sheet_width (float): Sheet width in inches
        
    Returns:
        dict: Dictionary containing sheathing calculations
    """
    # Convert sheet width to feet
    sheet_width_ft = sheet_width / 12

    # Adjust building dimensions for overhangs
    eave_length = length
    gable_width = width + 2 * (overhang / 12)
    roof_run = (gable_width / 2)
    roof_rise = (roof_run * (pitch / 12))
    roof_slope_length = math.sqrt(roof_run**2 + roof_rise**2)
    roof_length = length + 2 * (overhang / 12)

    # Calculate wall sheets
    eave_wall_sheets = math.ceil(eave_length / sheet_width_ft) * 2
    gable_wall_sheets = math.ceil(width / sheet_width_ft) * 2
    wall_sheet_length = height

    # Calculate gable triangle sheets
    gable_triangle_sheets = math.ceil(width / sheet_width_ft) * 2
    gable_triangle_lengths = [11, 12, 13, 14, 15, 15, 14, 13, 12, 11]

    # Calculate roof sheets
    roof_sheets_per_side = math.ceil(roof_length / sheet_width_ft)
    roof_sheet_length = math.ceil(roof_slope_length * 2) / 2
    total_roof_sheets = roof_sheets_per_side * 2

    return {
        "Eave Walls": {
            "Sheets": eave_wall_sheets,
            "Sheet Length": wall_sheet_length
        },
        "Gable Walls": {
            "Sheets": gable_wall_sheets,
            "Sheet Length": wall_sheet_length
        },
        "Gable Triangles": {
            "Sheets": gable_triangle_sheets,
            "Sheet Lengths": gable_triangle_lengths
        },
        "Roof": {
            "Sheets": total_roof_sheets,
            "Sheet Length": roof_sheet_length
        }
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
            formatted_data.append({
                "Section": section,
                "Number of Sheets": details["Sheets"],
                "Sheet Length (ft)": "Variable (11'-15')",
                "Notes": "Staggered lengths for triangular sections"
            })
        else:
            formatted_data.append({
                "Section": section,
                "Number of Sheets": details["Sheets"],
                "Sheet Length (ft)": f"{details['Sheet Length']:.1f}",
                "Notes": ""
            })
    
    return pd.DataFrame(formatted_data)
