#!/usr/bin/env python3
"""
Convert NNDC NuDat CSV export to Maxima format for STACK

Author: Alexander Pitzer
ETH Zurich
2025
"""

import csv
from collections import defaultdict
import re

# Fixed file paths
INPUT_FILE = "/home/alexander/eth_it/STACK-for-Chemistry/nndc_nudat_data_export(1).csv"
OUTPUT_FILE = "/home/alexander/eth_it/STACK-for-Chemistry/nuclidetable.dat"

# Element names by Z (for comments)
ELEMENT_NAMES = {
    0: "Neutron", 1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne",
    11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
    21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn",
    31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y", 40: "Zr",
    41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn",
    51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
    61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb",
    71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
    81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th",
    91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es", 100: "Fm",
    101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt",
    110: "Ds", 111: "Rg", 112: "Cn", 113: "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117: "Ts", 118: "Og"
}

def parse_csv_value(value):
    """Convert CSV value to appropriate format, ignoring uncertainties"""
    if value == '' or value is None:
        return 'null'
    
    # Remove uncertainty information (anything in parentheses)
    if isinstance(value, str) and '(' in value:
        value = value.split('(')[0].strip()
    
    # Special handling for decay modes
    if isinstance(value, str) and value == "EC+B+":
        value = "B+"
    
    # Try to parse as number
    try:
        # Check if it's a float
        if '.' in value or 'e' in value.lower() or 'E' in value:
            return float(value)
        # Otherwise int
        return int(value)
    except ValueError:
        # Return as string (will be quoted later)
        return value

def format_value(val):
    """Format value for Maxima output"""
    if val == 'null':
        return 'null'
    elif isinstance(val, str):
        # Format isotope names with TeX notation
        val = format_isotope_name(val)
        return f'"{val}"'
    elif isinstance(val, float):
        return str(val)
    elif isinstance(val, int):
        return str(val)
    else:
        return 'null'

def format_isotope_name(name):
    """Convert isotope name from '129In' to '^{129}In' format"""
    if isinstance(name, str):
        # Match pattern like '129In' and convert to '^{129}In'
        match = re.match(r'^(\d+)([A-Z][a-z]?)$', name)
        if match:
            mass_number = match.group(1)
            element = match.group(2)
            return f"^{{{mass_number}}}{element}"
    return name

def format_array(arr):
    """Format array for Maxima output"""
    formatted = [format_value(v) for v in arr]
    return '[' + ', '.join(formatted) + ']'

def group_decay_modes(rows):
    """
    Group rows with same Z, N, name, and levelEnergy but different decay modes
    Returns: single entry with arrays for decayModes and branchingRatios
    """
    if len(rows) == 1:
        row = rows[0]
        decay_modes = [parse_csv_value(row['decayMode'])] if row['decayMode'] else ['null']
        branching_ratios = [parse_csv_value(row['branchingRatio'])] if row['branchingRatio'] else ['null']
        
        return {
            'z': int(row['z']),
            'n': int(row['n']),
            'name': row['name'],
            'levelEnergy': parse_csv_value(row['levelEnergy(MeV)']),
            'halflife': parse_csv_value(row['halflife']),
            'halflifeUnit': parse_csv_value(row['halflifeUnit']),
            'decayModes': decay_modes,
            'branchingRatios': branching_ratios
        }
    
    # Multiple rows - collect all decay modes
    base_row = rows[0]
    decay_modes = []
    branching_ratios = []
    
    for row in rows:
        decay_modes.append(parse_csv_value(row['decayMode']) if row['decayMode'] else 'null')
        branching_ratios.append(parse_csv_value(row['branchingRatio']) if row['branchingRatio'] else 'null')
    
    return {
        'z': int(base_row['z']),
        'n': int(base_row['n']),
        'name': base_row['name'],
        'levelEnergy': parse_csv_value(base_row['levelEnergy(MeV)']),
        'halflife': parse_csv_value(base_row['halflife']),
        'halflifeUnit': parse_csv_value(base_row['halflifeUnit']),
        'decayModes': decay_modes,
        'branchingRatios': branching_ratios
    }

def group_by_nuclide_and_levels(rows):
    """
    Group rows by Z, N, name (isotope) and collect all levels
    Returns: dict with isotope as key and list of level data as value
    """
    isotope_groups = defaultdict(list)
    
    for row in rows:
        isotope_key = (int(row['z']), int(row['n']), row['name'])
        isotope_groups[isotope_key].append(row)
    
    return isotope_groups

def create_combined_entry(isotope_rows):
    """
    Create a single entry combining ground state and all excited states
    Returns: dict with combined data for all levels
    """
    # Group by level energy first, then by decay mode within each level
    level_groups = defaultdict(list)
    for row in isotope_rows:
        level_energy = parse_csv_value(row['levelEnergy(MeV)'])
        level_groups[level_energy].append(row)
    
    # Sort levels by energy (ground state first)
    def sort_key(item):
        level_energy = item[0]
        if level_energy == 'null' or level_energy is None or level_energy == 0:
            return 0.0
        elif isinstance(level_energy, (int, float)):
            return float(level_energy)
        else:
            return 0.0
    
    sorted_levels = sorted(level_groups.items(), key=sort_key)
    
    # Base data from first row
    base_row = isotope_rows[0]
    
    # Arrays to store data for all levels
    level_energies = []
    halflives = []
    halflife_units = []
    decay_modes_per_level = []
    branching_ratios_per_level = []
    
    # Process each level
    for level_energy, level_rows in sorted_levels:
        level_energies.append(level_energy)
        
        # For this level, group decay modes
        level_data = group_decay_modes(level_rows)
        
        halflives.append(level_data['halflife'])
        halflife_units.append(level_data['halflifeUnit'])
        decay_modes_per_level.append(level_data['decayModes'])
        branching_ratios_per_level.append(level_data['branchingRatios'])
    
    return {
        'z': int(base_row['z']),
        'n': int(base_row['n']),
        'name': base_row['name'],
        'levelEnergies': level_energies,
        'halflives': halflives,
        'halflifeUnits': halflife_units,
        'decayModes': decay_modes_per_level,
        'branchingRatios': branching_ratios_per_level
    }

def format_nuclide_entry_combined(nuclide_id, data):
    """Format a single nuclide entry with all levels for Maxima"""
    z = data['z']
    n = data['n']
    name = format_value(data['name'])
    
    # Format arrays for all levels
    level_energies = format_array(data['levelEnergies'])
    halflives = format_array(data['halflives'])
    halflife_units = format_array(data['halflifeUnits'])
    
    # Format nested arrays for decay modes (one array per level)
    decay_modes_formatted = '[' + ', '.join(format_array(modes) for modes in data['decayModes']) + ']'
    branching_formatted = '[' + ', '.join(format_array(ratios) for ratios in data['branchingRatios']) + ']'
    
    # Format the nuclide_id with TeX notation
    formatted_nuclide_id = format_isotope_name(nuclide_id)
    
    return f'    ["{formatted_nuclide_id}", [{z}, {n}, {level_energies}, {halflives}, {halflife_units}, {decay_modes_formatted}, {branching_formatted}]]'

def should_exclude_nuclide(data):
    """
    Check if nuclide should be excluded based on half-life criteria
    Exclude if: 1) no half-life or 2) half-life units are energy units (keV, MeV, eV)
    """
    halflives = data['halflives']
    halflife_units = data['halflifeUnits']
    
    # Check each level
    for i, (halflife, unit) in enumerate(zip(halflives, halflife_units)):
        # If any level has no half-life, exclude the entire nuclide
        if halflife == 'null' or halflife is None or halflife == '' or halflife == 0:
            return True
        
        # Additional check for string 'null'
        if isinstance(halflife, str) and halflife.strip().lower() == 'null':
            return True
            
        # If any level has energy units instead of time units, exclude
        if unit != 'null' and unit is not None:
            unit_str = str(unit).strip()
            energy_units = ['keV', 'MeV', 'eV', 'kev', 'mev', 'ev']
            if any(energy_unit in unit_str for energy_unit in energy_units):
                return True
    
    return False

def main():
    input_file = INPUT_FILE
    output_file = OUTPUT_FILE
    
    # Read CSV
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"Found {len(rows)} rows")
    
    # Group by isotope (Z, N, name) - combining all levels
    isotope_groups = group_by_nuclide_and_levels(rows)
    
    print(f"Grouped into {len(isotope_groups)} unique isotopes")
    
    # Process each isotope (combining all its levels)
    nuclides = {}
    excluded_count = 0
    for (z, n, name), isotope_rows in isotope_groups.items():
        data = create_combined_entry(isotope_rows)
        
        # Check if this nuclide should be excluded
        if should_exclude_nuclide(data):
            excluded_count += 1
            continue
            
        nuclide_id = name  # Use just the name as ID (e.g., "185Tl")
        nuclides[nuclide_id] = data
    
    # Sort by Z, then N
    sorted_nuclides = sorted(nuclides.items(), key=lambda x: (x[1]['z'], x[1]['n']))
    
    # Write output
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('%_NUCLIDE_DATA: [\n')
        
        current_z = None
        for i, (nuclide_id, data) in enumerate(sorted_nuclides):
            z = data['z']
            
            # Add element comment when Z changes
            if z != current_z:
                if current_z is not None:
                    f.write('\n')
                element_name = ELEMENT_NAMES.get(z, f"Z={z}")
                f.write(f'    /* {element_name} (Z={z}) */\n')
                current_z = z
            
            # Write entry
            entry = format_nuclide_entry_combined(nuclide_id, data)
            
            # Add comma except for last entry
            if i < len(sorted_nuclides) - 1:
                entry += ','
            
            f.write(entry + '\n')
        
        f.write(']$\n')
    
    print(f"Successfully converted {len(sorted_nuclides)} nuclides to {output_file}")
    print(f"Excluded {excluded_count} nuclides (no half-life or energy units)")
    print(f"Covers {len(set(d['z'] for d in nuclides.values()))} elements")
    
    # Print statistics
    num_with_excited = sum(1 for d in nuclides.values() if len(d['levelEnergies']) > 1)
    print(f"Isotopes with excited states: {num_with_excited}")

if __name__ == '__main__':
    main()
