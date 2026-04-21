# STACK Chemistry Functions

This repository contains chemistry functions and databases for the STACK question type in Moodle. STACK (System for Teaching and Assessment using a Computer algebra Kernel) is a question type for Moodle that enables mathematical and scientific assessment.

## Table of Contents

- [Purpose](#purpose)
- [Modules](#modules)
  - [Module Loading and Dependencies](#module-loading-and-dependencies)
  - [Periodic Table Module (`pse.mac`)](#periodic-table-module-psemac)
  - [Acid-Base Chemistry Module (`acidbase.mac`)](#acid-base-chemistry-module-acidbasemac)
  - [Thermodynamic Tables Module (`thermodynamictables.mac`)](#thermodynamic-tables-module-thermodynamictablesmac)
  - [Chemical Reactions Module (`reactions.mac`)](#chemical-reactions-module-reactionsmac)
  - [Nuclide Database Module (`nuclidetable.mac`)](#nuclide-database-module-nuclidetablemac)
- [Using Chemical Formulas in Questions](#using-chemical-formulas-in-questions)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Purpose

The goal of this project is to develop new chemistry functions and comprehensive databases for STACK in Moodle. This includes:

- **Periodic table data**: Complete element information including atomic numbers, masses, electron configurations, and physical properties
- **Acid-base chemistry**: Comprehensive database of acids and bases with pKa/pKb values, automatic conjugate acid/base lookup
- **Molecule parsing**: Parse chemical formulas and calculate molar masses
- **Multi-language support**: Element names in multiple languages (currently English, German, and Finnish)
- **Unit support**: Integration with STACK's units system for physical quantities
- **Extensible framework**: Easy-to-maintain structure for adding new chemical data and languages

## Modules

### Module Loading and Dependencies

Most modules are independent and can be loaded in any order. Two modules expose optional cross-module functionality:

| Module | Status | Notes |
|--------|--------|-------|
| `pse.mac` | ✅ Independent | Periodic table data and molar mass calculations |
| `acidbase.mac` | ✅ Independent | Acid-base chemistry with flat database |
| `reactions.mac` | ✅ Independent | Chemical reactions database |
| `nuclidetable.mac` | ✅ Independent* | Core nuclide lookups are standalone; ID generation, decay-product helpers, and ionization helpers also require `pse.mac` |
| `thermodynamictables.mac` | ✅ Independent* | Core thermodynamic data is standalone; `*_by_name` functions require `reactions.mac` |

**Quick Start:**
```maxima
/* Load only the modules you need - order doesn't matter */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/pse.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/acidbase.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/reactions.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/thermodynamictables.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/nuclidetable.mac");

/* For reaction-based thermodynamic calculations, load both: */
stack_include_contrib("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/reactions.mac");
stack_include_contrib("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/thermodynamictables.mac");
/* Then use: chem_reaction_enthalpy_by_name("CombustionMethane") */

/* For PSE-backed nuclide helpers, load both: */
stack_include_contrib("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/pse.mac");
stack_include_contrib("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/nuclidetable.mac");
/* Then use: chem_nuc_id_from_ZN(6, 8) or chem_nuc_ionize("^{14}C", 2) */
```

**Important Note on Forbidden Functions:**
Due to STACK restrictions, certain Maxima functions are not allowed:
- `read()` - String parsing (replaced with ASCII arithmetic)
- `print()` - Console output (errors return `false` instead)
- `?fboundp()` - Function existence checks (replaced with documentation)

See the [detailed documentation](ChemLibraryDocumentation.md#forbidden-maxima-functions) for complete information on forbidden functions and workarounds.

See the [detailed documentation](ChemLibraryDocumentation.md#module-dependencies) for specific use cases and loading patterns.

### Periodic Table Module (`pse.mac`)

Functions for accessing periodic table data:
- `chem_data` - Retrieve specific chemical properties
- `chem_data_units` - Get data with appropriate units
- `chem_data_all` - Access complete element information
- `chem_element` - Get element symbol by atomic number
- `chem_element_array` - Get arrays of elements by various criteria
- `chem_electron_config` - Get formatted electron configurations
- `chem_units` - Get units for specific properties
- `chem_parse_formula` - Parse chemical formula into element-count pairs
- `chem_molar_mass` - Calculate molar mass from chemical formula
- `chem_display` - Wrap formula in `\ce{...}` for LaTeX rendering

#### Examples:
```maxima
/* Get atomic mass of iron */
mass_Fe: chem_data("Fe", "AtomicMass");  /* Returns 55.85 */

/* Get atomic mass with units */
mass_Fe_units: chem_data_units("Fe", "AtomicMass");  /* Returns 55.85*g*mol^(-1) */

/* Get electronegativity of oxygen */
en_O: chem_data("O", "Electronegativity");  /* Returns 3.44 */

/* Get melting point of sodium with units */
mp_Na: chem_data_units("Na", "MeltingPoint");  /* Returns 370.95*K */

/* Find element by atomic number */
elem_26: chem_element(26);  /* Returns "Fe" */

/* Get all halogens (group 17) */
halogens: chem_element_group(17);  /* Returns ["F", "Cl", "Br", "I", "At", "Ts"] */

/* Get all noble gases (main group 8) */
noble_gases: chem_element_maingroup(8);  /* Returns ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"] */

/* Get all main group elements */
main_group: chem_element_array_maingroup();  /* Returns elements with MainGroup > 0 */

/* Get elements in period 3 */
period3: chem_element_period(3);  /* Returns ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"] */

/* Get element at specific position in periodic table */
elem_period4_group6: chem_element_period_group(4, 6);  /* Returns "Cr" */

/* Get element by period and main group */
elem_p3_mg1: chem_element_period_maingroup(3, 1);  /* Returns "Na" */

/* Parse a chemical formula */
parsed: chem_parse_formula("H2SO4");  /* Returns [["H", 2], ["S", 1], ["O", 4]] */

/* Calculate molar mass of sulfuric acid */
M_H2SO4: chem_molar_mass("H2SO4");  /* Returns 98.09*g*mol^(-1) */

/* Calculate molar mass of glucose */
M_glucose: chem_molar_mass("C6H12O6");  /* Returns 180.18*g*mol^(-1) */

/* Wrap formula for LaTeX display */
formula_display: chem_display("H2SO4");  /* Returns "\\ce{H2SO4}" */

/* Get formatted electron configuration for display */
config_Fe: chem_electron_config("Fe");  
/* Returns "[\mathrm{Ar}] 4\mathrm{s}^{2} 3\mathrm{d}^{6}" for LaTeX display */
```

### Acid-Base Chemistry Module (`acidbase.mac`)

A standalone module providing acid-base chemistry data through database lookup:

**Data Retrieval Functions:**
- `chem_acidbase_pKa(acid)` - Get pKa value for an acid
- `chem_acidbase_pKb(base)` - Get pKb value for a base
- `chem_acidbase_Ka(acid)` - Calculate Ka from pKa (returns 10^(-pKa))
- `chem_acidbase_Kb(base)` - Calculate Kb from pKb (returns 10^(-pKb))
- `chem_acidbase_nH(acid)` - Get number of acidic protons for an acid

**Conjugate Pair Functions:**
- `chem_acidbase_conjugate_base(acid)` - Get conjugate base for an acid
- `chem_acidbase_conjugate_acid(base)` - Get conjugate acid for a base

**Array Functions for Random Selection:**
- `chem_acid_array()` - Get array of all acids in database
- `chem_base_array()` - Get array of all bases in database
- `chem_weak_acid_array()` - Get array of weak acids (pKa > 0)
- `chem_strong_acid_array()` - Get array of strong acids (pKa < 0)
- `chem_weak_base_array()` - Get array of weak bases (0 < pKb < 14)
- `chem_strong_base_array()` - Get array of strong bases (pKb ≤ 0)

**Array Functions by Number of Acidic Protons:**
- `chem_acid_array_nH(n)` - Get array of acids with exactly n acidic protons
- `chem_strong_acid_array_nH(n)` - Get array of strong acids with n acidic protons
- `chem_weak_acid_array_nH(n)` - Get array of weak acids with n acidic protons

#### Examples:
```maxima
/* Get pKa of acetic acid */
pka: chem_acidbase_pKa("CH3COOH");  /* Returns 4.76 */

/* Get Ka from pKa */
ka: chem_acidbase_Ka("CH3COOH");    /* Returns 10^(-4.76) */

/* Get conjugate base */
base: chem_acidbase_conjugate_base("CH3COOH");  /* Returns "CH3COO-" */

/* Get pKb of the conjugate base */
pkb: chem_acidbase_pKb("CH3COO-");  /* Returns 9.24 */

/* Get number of acidic protons */
nH: chem_acidbase_nH("H2SO4");      /* Returns 2 */
nH: chem_acidbase_nH("CH3COOH");    /* Returns 1 */

/* ===== RANDOM SELECTION EXAMPLES ===== */

/* Select a random acid from ALL acids in database */
random_acid: rand(chem_acid_array());

/* Select a random WEAK acid (pKa > 0) */
random_weak_acid: rand(chem_weak_acid_array());

/* Select a random STRONG acid (pKa < 0) */
random_strong_acid: rand(chem_strong_acid_array());

/* Select a random base */
random_base: rand(chem_base_array());

/* Select a random weak base */
random_weak_base: rand(chem_weak_base_array());

/* ===== RANDOM SELECTION BY NUMBER OF ACIDIC PROTONS ===== */

/* Select a random monoprotic acid (1 acidic proton) */
random_monoprotic: rand(chem_acid_array_nH(1));

/* Select a random diprotic acid (2 acidic protons) */
random_diprotic: rand(chem_acid_array_nH(2));

/* Select a random triprotic acid (3 acidic protons) */
random_triprotic: rand(chem_acid_array_nH(3));

/* Select a random WEAK diprotic acid */
random_weak_diprotic: rand(chem_weak_acid_array_nH(2));

/* Select a random STRONG monoprotic acid */
random_strong_monoprotic: rand(chem_strong_acid_array_nH(1));

/* ===== COMPLETE QUESTION VARIABLE EXAMPLE ===== */
/* For a pH calculation question with a random weak acid: */
acid: rand(chem_weak_acid_array());
acid_display: chem_display(acid);           /* For LaTeX display */
pka_value: chem_acidbase_pKa(acid);         /* Get pKa */
ka_value: chem_acidbase_Ka(acid);           /* Get Ka */
conj_base: chem_acidbase_conjugate_base(acid);  /* Get conjugate base */
conj_base_display: chem_display(conj_base);     /* For LaTeX display */
num_protons: chem_acidbase_nH(acid);        /* Number of acidic H */

/* Get all diprotic acids (2 acidic protons) */
diprotic: chem_acid_array_nH(2);    /* Returns ["H2SO4", "H2CO3", "H2S", ...] */
```

**Note:** This module uses a flat database structure. All acid-base pairs and their pKa/pKb values are stored directly - no formula parsing is performed. Returns `null` for unknown substances or `""` for conjugate lookups that fail.

### Thermodynamic Tables Module (`thermodynamictables.mac`)

Functions for thermodynamic calculations:
- `chem_thermo_data` - Retrieve standard formation enthalpies (ΔHf°), entropies (S°), and Gibbs free energies (ΔGf°)
- `chem_thermo_data_units` - Get thermodynamic data with appropriate units
- `chem_reaction_enthalpy` - Calculate reaction enthalpy from stoichiometry
- `chem_reaction_entropy` - Calculate reaction entropy from stoichiometry
- `chem_reaction_gibbs` - Calculate reaction Gibbs free energy from stoichiometry
- `chem_reaction_enthalpy_by_name` - Calculate ΔH° for named reactions
- `chem_reaction_entropy_by_name` - Calculate ΔS° for named reactions
- `chem_reaction_gibbs_by_name` - Calculate ΔG° for named reactions
- `chem_equilibrium_constant` - Calculate K from ΔG°
- `chem_thermo_substance_array` - Get arrays of substances by state

#### Examples:
```maxima
/* Get standard enthalpy of formation of liquid water */
DeltaHf_H2O: chem_thermo_data("H2O", "DeltaHf", "l");  /* Returns -285.8 kJ/mol */

/* Get standard entropy of gaseous CO2 */
S_CO2: chem_thermo_data("CO2", "S", "g");  /* Returns 213.8 J/(mol·K) */

/* Calculate reaction enthalpy for: CH4(g) + 2O2(g) → CO2(g) + 2H2O(l) */
products: [["CO2", "g", 1], ["H2O", "l", 2]];
reactants: [["CH4", "g", 1], ["O2", "g", 2]];
DeltaH_combustion: chem_reaction_enthalpy(products, reactants);  /* Returns -890.4 kJ/mol */

/* Calculate equilibrium constant from ΔG° */
K_eq: chem_equilibrium_constant(-33.0, 298);  /* K = exp(-ΔG°/RT) */
```

### Chemical Reactions Module (`reactions.mac`)

Database of common chemical reactions with stoichiometry:
- `chem_reaction_data` - Retrieve complete reaction information
- `chem_reaction_reactants` / `chem_reaction_products` - Get reactants or products
- `chem_reaction_equation` - Generate text equation
- `chem_reaction_equation_latex` - Generate LaTeX formatted equation with `\ce{...}`
- `chem_reaction_array` - Get all reaction names
- `chem_reaction_combustion_array` - Get combustion reactions
- `chem_reaction_formation_array` - Get formation reactions
- `chem_reaction_synthesis_array` - Get synthesis reactions
- `chem_reaction_decomposition_array` - Get decomposition reactions

#### Examples:
```maxima
/* Get complete reaction data for methane combustion */
rxn_data: chem_reaction_data("CombustionMethane");
/* Returns: [[["CH4", "g", 1], ["O2", "g", 2]], [["CO2", "g", 1], ["H2O", "l", 2]]] */

/* Generate LaTeX equation for display */
eqn_latex: chem_reaction_equation_latex("CombustionMethane");
/* Returns: "\\ce{CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)}" */
```

### Nuclide Database Module (`nuclidetable.mac`)

Database containing nuclear data for radioactive isotopes:
- Half-lives for ground and excited states
- Decay modes (alpha, beta-minus, beta-plus, EC, IT, etc.)
- Branching ratios for multiple decay paths

**Note:** This module currently provides the raw data structure `%_NUCLIDE_DATA`. Retrieval functions are planned for future implementation.

**Database Structure:**
```maxima
/* Each entry: ["Nuclide_ID", [Z, N, LevelEnergies, Halflives, HalflifeUnits, DecayModes, BranchingRatios]] */
/* Example: Access tritium data */
assoc("3H", %_NUCLIDE_DATA);
```

### Using Chemical Formulas in Questions

To properly display chemical formulas in your STACK questions, add the following line at the beginning of your **Question text**:

```latex
\(\require{mhchem}\)
```

This enables the `mhchem` LaTeX package for rendering chemical formulas with `\ce{...}` commands. 

**Quick Display Method:**

Use the `chem_display()` function to automatically wrap formulas for proper rendering. Call the function in **Question Variables** and store the result.

```maxima
/* In Question Variables */
acid: rand(chem_weak_acid_array());
acid_display: chem_display(acid);  /* Wraps formula in \ce{...} */
pka_value: chem_acidbase_pKa(acid);
conj_base: chem_acidbase_conjugate_base(acid);
conj_base_display: chem_display(conj_base);
```

```latex
/* In Question Text */
\(\require{mhchem}\)

<p>Calculate the pH of a 0.1 M solution of {@acid_display@}.</p>
<p>Given: pKa = {@pka_value@}</p>
<p>The conjugate base is {@conj_base_display@}.</p>
```

The formulas will be automatically rendered with proper subscripts and superscripts:
- `chem_display("H2SO4")` produces \ce{H2SO4} → displays as H₂SO₄
- `chem_display("NH4+")` produces \ce{NH4+} → displays as NH₄⁺
- `chem_display("HPO4^{2-}")` produces \ce{HPO4^{2-}} → displays as HPO₄²⁻

See the [documentation](ChemLibraryDocumentation.md) for more details.

## Getting Started

### Prerequisites

- Git (for cloning the repository)
- Visual Studio Code (recommended code editor)
- Basic understanding of Maxima/STACK syntax (helpful but not required)

### Installation Guide

#### Windows

1. **Install Git:**
   - Download Git from [git-scm.com](https://git-scm.com/download/win)
   - Run the installer and follow the setup wizard
   - Use default settings unless you have specific preferences

2. **Install Visual Studio Code:**
   - Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/download)
   - Run the installer and follow the installation steps

3. **Clone the repository:**
   - Open Command Prompt or PowerShell
   - Navigate to your desired folder:
     ```cmd
     cd C:\Users\YourUsername\Documents
     ```
   - Clone the repository:
     ```cmd
     git clone https://github.com/your-username/STACK-for-Chemistry.git
     ```

4. **Open in VS Code:**
   - Launch VS Code
   - File → Open Folder → Select the cloned `STACK-for-Chemistry` folder

#### macOS

1. **Install Git:**
   - Open Terminal
   - Install using Homebrew (recommended):
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     brew install git
     ```
   - Alternatively, download from [git-scm.com](https://git-scm.com/download/mac)

2. **Install Visual Studio Code:**
   - Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/download)
   - Drag the application to your Applications folder

3. **Clone the repository:**
   - Open Terminal
   - Navigate to your desired folder:
     ```bash
     cd ~/Documents
     ```
   - Clone the repository:
     ```bash
     git clone https://github.com/your-username/STACK-for-Chemistry.git
     ```

4. **Open in VS Code:**
   - Launch VS Code
   - File → Open Folder → Select the cloned `STACK-for-Chemistry` folder

#### Linux (Ubuntu/Debian)

1. **Install Git:**
   ```bash
   sudo apt update
   sudo apt install git
   ```

2. **Install Visual Studio Code:**
   - Download the .deb package from [code.visualstudio.com](https://code.visualstudio.com/download)
   - Install using:
     ```bash
     sudo dpkg -i code_*.deb
     sudo apt-get install -f
     ```
   - Or install via snap:
     ```bash
     sudo snap install code --classic
     ```

3. **Clone the repository:**
   ```bash
   cd ~/Documents
   git clone https://github.com/your-username/STACK-for-Chemistry.git
   ```

4. **Open in VS Code:**
   ```bash
   cd STACK-for-Chemistry
   code .
   ```

#### Linux (CentOS/RHEL/Fedora)

1. **Install Git:**
   ```bash
   # CentOS/RHEL
   sudo yum install git
   # or for newer versions
   sudo dnf install git
   
   # Fedora
   sudo dnf install git
   ```

2. **Install Visual Studio Code:**
   - Download the .rpm package from [code.visualstudio.com](https://code.visualstudio.com/download)
   - Install using:
     ```bash
     sudo rpm -i code-*.rpm
     ```

3. **Clone and open** (same as Ubuntu instructions above)

### VS Code Extensions (Recommended)

Once you have VS Code installed, consider adding these helpful extensions:

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search and install:
   - **Git History** - View git log and file history
   - **GitLens** - Supercharge Git capabilities
   - **Bracket Pair Colorizer** - Make brackets easier to read
   - **Code Spell Checker** - Spell checking for code comments

## Contributing

We welcome contributions from developers of all skill levels! Here are ways you can help:

- **Add new chemical data**: Extend the periodic table information
- **Add language support**: Translate element names to new languages
- **Improve functions**: Enhance existing chemistry functions
- **Add new functions**: Create functions for chemical calculations
- **Documentation**: Improve code comments and documentation
- **Testing**: Help test functions with different inputs

### Basic Workflow

1. Fork this repository
2. Clone your fork locally
3. Create a new branch for your feature
4. Make your changes
5. Test your changes
6. Commit and push to your fork
7. Create a pull request

## File Structure

- `pse.mac` - Periodic table functions and element data
- `acidbase.mac` - Acid-base chemistry functions and database (standalone)
- `thermodynamictables.mac` - Thermodynamic data and calculation functions
- `reactions.mac` - Chemical reactions database with stoichiometry
- `nuclidetable.mac` - Nuclear data and decay database
- `README.md` - This documentation file
- `ChemLibraryDocumentation.md` - Detailed function documentation

## License

This project is licensed under the GNU General Public License version 2. See the license header in `chemistry.mac` for details.

## Support

If you encounter any issues or have questions:
- Check existing issues on GitHub
- Create a new issue with detailed information
- Include your operating system and any error messages

Happy coding! 🧪⚗️
