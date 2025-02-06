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
    eave_length = length + 2 * overhang_ft  # Include overhang
    half_gable_width = gable_width / 2  # Half-width for triangle calculations

    # Calculate peak height using pitch
    peak_height = (half_gable_width) * (pitch / 12)

    # Calculate number of sheets needed for one side of gable
    sheets_per_side = math.ceil(width / (2 * sheet_width_ft))

    # Calculate rise increment per sheet width
    rise_per_sheet_inches = math.ceil((sheet_width * pitch) / 12)  # Round up to nearest inch
    rise_per_sheet_feet = rise_per_sheet_inches / 12

    # Generate ascending and descending gable sheet lengths
    gable_sheet_lengths = []
    start_length = height + rise_per_sheet_feet  # Start with first increment above wall height

    # Ascending lengths
    for i in range(sheets_per_side):
        sheet_length = start_length + (i * rise_per_sheet_feet)
        # Round to nearest inch (1/12 of a foot)
        sheet_length = round(sheet_length * 12) / 12
        gable_sheet_lengths.append(sheet_length)

    # Descending lengths (excluding the peak to avoid duplication)
    for i in range(sheets_per_side - 1, -1, -1):
        sheet_length = start_length + (i * rise_per_sheet_feet)
        # Round to nearest inch (1/12 of a foot)
        sheet_length = round(sheet_length * 12) / 12
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

    # Calculate total linear feet for each section
    wall_linear_feet = eave_wall_sheets * wall_sheet_length
    gable_linear_feet = sum(gable_sheet_lengths) * 2  # Double for both sides
    roof_linear_feet = total_roof_sheets * roof_sheet_length

    # Calculate total perimeter feet of roofline
    perimeter_feet = (eave_length * 2) + (gable_width * 2)  # Total perimeter including overhang

    return {
        "Eave Walls": {
            "Sheets": eave_wall_sheets, 
            "Sheet Length": wall_sheet_length,
            "Linear Feet": wall_linear_feet,
            "Perimeter Feet": eave_length * 2
        },
        "Gable Triangles": {
            "Sheets": len(gable_sheet_lengths) * 2, 
            "Sheet Lengths": gable_sheet_lengths,
            "Linear Feet": gable_linear_feet,
            "Perimeter Feet": gable_width * 2
        },
        "Roof": {
            "Sheets": total_roof_sheets, 
            "Sheet Length": roof_sheet_length,
            "Linear Feet": roof_linear_feet,
            "Perimeter Feet": perimeter_feet
        },
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
    total_linear_feet = 0

    for section, details in results.items():
        if section == "Gable Triangles":
            lengths_str = ", ".join(f"{length:.1f}'" for length in details["Sheet Lengths"])
            formatted_data.append({
                "Section": section,
                "Number of Sheets": details["Sheets"],
                "Sheet Length (ft)": f"Variable: {lengths_str}",
                "Total Linear Feet (3' Sections)": f"{math.ceil(details['Linear Feet'] / 3) * 3:.1f}'",
                "Perimeter Feet": f"{details['Perimeter Feet']:.1f}'",
                "Notes": "Staggered lengths for optimal coverage"
            })
        else:
            formatted_data.append({
                "Section": section,
                "Number of Sheets": details["Sheets"],
                "Sheet Length (ft)": f"{details['Sheet Length']:.1f}'",
                "Total Linear Feet (3' Sections)": f"{math.ceil(details['Linear Feet'] / 3) * 3:.1f}'",
                "Perimeter Feet": f"{details['Perimeter Feet']:.1f}'",
                "Notes": ""
            })
        total_linear_feet += math.ceil(details['Linear Feet'] / 3) * 3

    # Add total row
    formatted_data.append({
        "Section": "TOTAL",
        "Number of Sheets": sum(details["Sheets"] for section, details in results.items()),
        "Sheet Length (ft)": "-",
        "Total Linear Feet (3' Sections)": f"{total_linear_feet:.1f}'",
        "Perimeter Feet": f"{results['Roof']['Perimeter Feet']:.1f}'",
        "Notes": "Total linear feet required"
    })

    return pd.DataFrame(formatted_data)