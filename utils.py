import math
import pandas as pd

def calculate_sheathing(length: float, width: float, height: float, pitch: float, 
                       overhang: float, sheet_width: float, include_shed: bool = False,
                       shed_width: float = None, shed_depth: float = None,
                       shed_pitch: float = None, shed_height: float = None) -> dict:
    """
    Dynamically calculates the required metal sheets for walls, gable ends, and roof,
    including optional side shed calculations.

    Args:
        length (float): Length of the building in feet
        width (float): Width of the building in feet
        height (float): Wall height in feet
        pitch (float): Roof pitch (x/12)
        overhang (float): Overhang length in inches
        sheet_width (float): Sheet width in inches
        include_shed (bool): Whether to include side shed calculations
        shed_width (float): Width of the side shed in feet
        shed_depth (float): Depth of the side shed in feet
        shed_pitch (float): Roof pitch of the side shed (x/12)
        shed_height (float): Wall height of the side shed in feet

    Returns:
        dict: Dictionary containing sheathing calculations
    """
    # Convert sheet width and overhang from inches to feet
    sheet_width_ft = sheet_width / 12  
    overhang_ft = overhang / 12

    # Main building calculations
    # Adjust building dimensions for overhang
    gable_width = width + 2 * overhang_ft  # Include overhang
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

    results = {
        "Eave Walls": {"Sheets": eave_wall_sheets, "Sheet Length": wall_sheet_length},
        "Gable Triangles": {"Sheets": len(gable_sheet_lengths) * 2, "Sheet Lengths": gable_sheet_lengths},
        "Roof": {"Sheets": total_roof_sheets, "Sheet Length": roof_sheet_length},
    }

    # Side shed calculations if included
    if include_shed and all(x is not None for x in [shed_width, shed_depth, shed_pitch, shed_height]):
        # Side shed walls
        shed_front_back_sheets = math.ceil(shed_width / sheet_width_ft) * 2
        shed_side_sheets = math.ceil(shed_depth / sheet_width_ft)

        # Side shed roof
        shed_peak_height = (shed_width * (shed_pitch / 12))
        shed_roof_slope_length = math.sqrt(shed_width**2 + shed_peak_height**2)
        shed_roof_sheets = math.ceil((shed_depth / sheet_width_ft)) * 1  # One slope only

        results.update({
            "Shed Front/Back Walls": {
                "Sheets": shed_front_back_sheets,
                "Sheet Length": shed_height
            },
            "Shed Side Wall": {
                "Sheets": shed_side_sheets,
                "Sheet Length": f"{shed_height} to {shed_height + shed_peak_height:.1f}"
            },
            "Shed Roof": {
                "Sheets": shed_roof_sheets,
                "Sheet Length": math.ceil(shed_roof_slope_length * 2) / 2  # Round up to 0.5'
            }
        })

    return results

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
                "Sheet Length (ft)": f"{details['Sheet Length']:.1f}" if isinstance(details['Sheet Length'], (int, float)) else details['Sheet Length'],
                "Notes": "Single slope shed roof" if "Shed Roof" in section else ""
            })

    return pd.DataFrame(formatted_data)