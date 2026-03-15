# Chemistry Library Documentation for STACK

## Table of Contents
1. [Installation](#installation)
2. [Module Dependencies](#module-dependencies)
3. [Periodic Table Module](#periodic-table-module)
   - [PSE Data Retrieving Functions](#pse-data-retrieving-functions)
   - [PSE Navigation Functions](#pse-navigation-functions)
   - [Electron Configuration Functions](#electron-configuration-functions)
   - [Molar Mass and Formula Parsing Functions](#molar-mass-and-formula-parsing-functions)
   - [Chemical Formula Display Function](#chemical-formula-display-function)
   - [Available Data Fields](#available-data-fields)
4. [Acid-Base Chemistry Module](#acid-base-chemistry-module)
   - [Acid-Base Data Retrieval Functions](#acid-base-data-retrieval-functions)
   - [Equilibrium Expression Functions](#equilibrium-expression-functions)
   - [Conjugate Acid-Base Functions](#conjugate-acid-base-functions)
   - [Acid-Base Navigation Functions](#acid-base-navigation-functions)
   - [Polyprotic Acid Functions](#polyprotic-acid-functions)
   - [Titration Curve Functions](#titration-curve-functions)
   - [JSXGraph Plot Generation Functions](#jsxgraph-plot-generation-functions)
   - [Available Acids and Bases](#available-acids-and-bases)
5. [Solubility Equilibrium Module](#solubility-equilibrium-module)
   - [Solubility Data Retrieval Functions](#solubility-data-retrieval-functions)
   - [Solubility Equilibrium Expression Functions](#solubility-equilibrium-expression-functions)
   - [Molar Solubility Calculation Functions](#molar-solubility-calculation-functions)
   - [Precipitation Check Functions](#precipitation-check-functions)
   - [Solubility Navigation Functions](#solubility-navigation-functions)
   - [Dissolution Equation Functions](#dissolution-equation-functions)
   - [Available Salts](#available-salts)
   - [Function Reference Table (Solubility)](#function-reference-table-solubility)
6. [Thermodynamic Tables Module](#thermodynamic-tables-module)
   - [Thermodynamic Data Retrieval Functions](#thermodynamic-data-retrieval-functions)
   - [Tag-Based Filtering Functions](#tag-based-filtering-functions)
   - [Thermodynamic Navigation Functions](#thermodynamic-navigation-functions)
   - [Thermodynamic Calculation Functions](#thermodynamic-calculation-functions)
   - [Available Substances](#available-substances)
7. [Chemical Reactions Module](#chemical-reactions-module)
   - [Reaction Data Retrieval Functions](#reaction-data-retrieval-functions)
   - [Available Reactions](#available-reactions)
8. [Nuclide Database Module](#nuclide-database-module)
   - [Data Structure](#data-structure)
   - [Core Data Retrieval Functions](#core-data-retrieval-functions)
   - [Decay Information Functions](#decay-information-functions)
   - [Navigation and Filtering Functions](#navigation-and-filtering-functions)
   - [Utility Functions](#utility-functions)
   - [Practical Examples](#practical-examples)
9. [Usage Examples](#usage-examples)

---

## Installation

### Loading the Library

To use the chemistry library in your STACK question, include the following lines in the **Question variables** section:

```maxima
/* Load periodic table module */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/pse.mac");

/* Load acid-base chemistry module */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/acidbase.mac");

/* Load solubility module */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/solubility.mac");

/* Load thermodynamic tables module */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/thermodynamictables.mac");

/* Load reactions module */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/reactions.mac");

/* Load nuclide database module */
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/nuclidetable.mac");
```

You can load modules independently or together as needed. See [Module Dependencies](#module-dependencies) below for information on which modules depend on others.

### Enabling Chemical Formula Rendering

To properly display chemical formulas in your STACK question, add the following line to the **Question text** (at the beginning, before any chemistry content):

```latex
\(\require{mhchem}\)
```

This enables the `mhchem` LaTeX package, which allows you to use `\ce{...}` commands for chemical formulas.

**Example Question Text:**
```latex
\(\require{mhchem}\)

<p>What is the pKa value of {@acid@} (\ce{ {@acid@} })?</p>
```

**Note:** Without `\(\require{mhchem}\)`, chemical formulas will not render correctly and may show LaTeX errors.

---

## Module Dependencies

Understanding the dependencies between modules is crucial for correct functionality. Here's a breakdown of how the modules relate to each other:

### Independent Modules

These modules have **no dependencies** and can be loaded independently:

1. **Periodic Table Module (`pse.mac`)** — Completely standalone
2. **Acid-Base Chemistry Module (`acidbase.mac`)** — Completely standalone
3. **Solubility Module (`solubility.mac`)** — Completely standalone
4. **Reactions Module (`reactions.mac`)** — Completely standalone
5. **Nuclide Database Module (`nuclidetable.mac`)** — Completely standalone

### Dependent Modules

6. **Thermodynamic Tables Module (`thermodynamictables.mac`)**
   - **Standalone for basic functions**: Works independently for direct thermodynamic data retrieval
   - **Requires `reactions.mac`**: For reaction-based thermodynamic calculations (functions with `_by_name` suffix)

### Loading Order Guidelines

#### Option 1: Load All Modules (Recommended for Full Functionality)

```maxima
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/pse.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/acidbase.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/solubility.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/reactions.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/thermodynamictables.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/nuclidetable.mac");
```

#### Option 2: Thermodynamics with Reactions

```maxima
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/reactions.mac");
stack_include("https://raw.githubusercontent.com/STACK-for-Chemistry/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/thermodynamictables.mac");
```

### Function Dependency Summary

| Function | Required Modules | Notes |
|----------|------------------|-------|
| `chem_data()`, `chem_element()` | `pse.mac` | Periodic table data |
| `chem_electron_config()` | `pse.mac` | Electron configurations |
| `chem_molar_mass()` | `pse.mac` | Molar mass calculations |
| `chem_parse_formula()` | `pse.mac` | Formula parsing |
| `chem_display()` | `pse.mac` | Formula display |
| `chem_acidbase_pKa()`, `chem_acidbase_Ka()` | `acidbase.mac` | Acid-base data |
| `chem_titration_pH()` | `acidbase.mac` | Titration calculations |
| `chem_sol_Ksp()`, `chem_sol_molar_solubility()` | `solubility.mac` | Solubility data |
| `chem_sol_precipitation_check()` | `solubility.mac` | Precipitation checks |
| `chem_thermo_data()` | `thermodynamictables.mac` | Thermodynamic data |
| `chem_reaction_enthalpy()` | `thermodynamictables.mac` | Manual thermo calculations |
| `chem_reaction_data()`, `chem_reaction_equation()` | `reactions.mac` | Reaction data |
| `chem_reaction_enthalpy_by_name()` | `thermodynamictables.mac` + `reactions.mac` | Named reaction thermodynamics |

---

## Periodic Table Module

The periodic table module provides comprehensive data for all 118 elements, including atomic properties, electron configurations, and molar mass calculations.

### PSE Data Retrieving Functions

#### `chem_data(element, dp)`

**Description:** Returns the data field `dp` associated with `element`.

**Parameters:**
- `element` (string): Element symbol (e.g., `"H"`, `"He"`, `"Li"`)
- `dp` (string): Name of the data field (see [Available Data Fields](#available-data-fields))

**Returns:** The value of the requested field, or `false` if not found

**Example:**
```maxima
mass: chem_data("C", "AtomicMass");           /* Returns 12.01 */
name: chem_data("Na", "Name");                /* Returns "Sodium" (or "Natrium" in German) */
en: chem_data("O", "Electronegativity");      /* Returns 3.44 */
period: chem_data("Fe", "Period");            /* Returns 4 */
config: chem_data("N", "ElectronConfiguration"); /* Returns "[He] 2s2 2p3" */
block: chem_data("Cu", "GroupBlock");         /* Returns "Transition metal" */
```

---

#### `chem_data_units(element, dp)`

**Description:** Returns a specific data field with the appropriate unit attached (using STACK's `stackunits` function).

**Parameters:**
- `element` (string): Element symbol
- `dp` (string): Name of the data field

**Returns:** The value with unit (via `stackunits`), or the raw value if no unit is defined

**Example:**
```maxima
mass: chem_data_units("O", "AtomicMass");         /* Returns stackunits(16.00, g*mol^(-1)) */
bp: chem_data_units("H", "BoilingPoint");         /* Returns stackunits(20.28, K) */
radius: chem_data_units("Na", "AtomicRadius");    /* Returns stackunits(227, pm) */
ie: chem_data_units("Li", "IonizationEnergy");    /* Returns stackunits(5.392, J) */
density: chem_data_units("Fe", "Density");        /* Returns stackunits(7.874, g/cm^3) */
```

---

#### `chem_data_all(element)`

**Description:** Returns all available data for an element as an association list of [field, value] pairs.

**Parameters:**
- `element` (string): Element symbol

**Returns:** List of [field, value] pairs

**Example:**
```maxima
all_data: chem_data_all("He");
/* Returns [["AtomicNumber", 2], ["Name", "Helium"], ["Period", 1], ...] */
```

---

#### `chem_element(atomic_num)`

**Description:** Returns the element symbol for a given atomic number.

**Parameters:**
- `atomic_num` (integer): Atomic number (1–118)

**Returns:** Element symbol (string), or `false` if not found

**Example:**
```maxima
symbol: chem_element(6);    /* Returns "C" */
symbol: chem_element(79);   /* Returns "Au" */
symbol: chem_element(1);    /* Returns "H" */
symbol: chem_element(200);  /* Returns false */
```

---

#### `chem_units(dp)`

**Description:** Returns the unit associated with a data field.

**Parameters:**
- `dp` (string): Name of the data field

**Returns:** The unit, or `null` if no unit is defined for the field

**Example:**
```maxima
unit: chem_units("AtomicMass");       /* Returns g*mol^(-1) */
unit: chem_units("MeltingPoint");     /* Returns K */
unit: chem_units("AtomicRadius");     /* Returns pm */
unit: chem_units("Name");             /* Returns null */
```

---

### PSE Navigation Functions

#### `chem_element_array()`

**Description:** Returns an array of all element symbols in the periodic table.

**Parameters:** None

**Returns:** List of all 118 element symbols

**Example:**
```maxima
all_elements: chem_element_array();
/* Returns ["H", "He", "Li", ..., "Og"] */

/* Select a random element */
element: rand(chem_element_array());
```

---

#### `chem_element_array_maingroup()`

**Description:** Returns an array of all main group element symbols (elements with MainGroup > 0).

**Parameters:** None

**Returns:** List of main group element symbols

**Example:**
```maxima
maingroup_elements: chem_element_array_maingroup();
/* Returns ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", ...] */

element: rand(chem_element_array_maingroup());
```

---

#### `chem_element_period(period_num)`

**Description:** Returns all element symbols in a given period.

**Parameters:**
- `period_num` (integer): Period number (1–7)

**Returns:** List of element symbols in that period

**Example:**
```maxima
period_3: chem_element_period(3);
/* Returns ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"] */

element: rand(chem_element_period(2));
```

---

#### `chem_element_group(group_num)`

**Description:** Returns all element symbols in a given IUPAC group.

**Parameters:**
- `group_num` (integer): IUPAC group number (1–18)

**Returns:** List of element symbols in that group

**Example:**
```maxima
group_17: chem_element_group(17);
/* Returns ["F", "Cl", "Br", "I", "At", "Ts"] */
```

---

#### `chem_element_maingroup(maingroup_num)`

**Description:** Returns all element symbols in a given main group (1–8).

**Parameters:**
- `maingroup_num` (integer): Main group number (1–8)

**Returns:** List of element symbols in that main group

**Example:**
```maxima
alkali: chem_element_maingroup(1);
/* Returns ["H", "Li", "Na", "K", "Rb", "Cs", "Fr"] */

halogens: chem_element_maingroup(7);
/* Returns ["F", "Cl", "Br", "I", "At", "Ts"] */

noble_gases: chem_element_maingroup(8);
/* Returns ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"] */
```

---

#### `chem_element_period_group(period_num, group_num)`

**Description:** Returns the element symbol at a specific period and IUPAC group position.

**Parameters:**
- `period_num` (integer): Period number (1–7)
- `group_num` (integer): IUPAC group number (1–18)

**Returns:** Element symbol, or `false` if no element exists at that position

**Example:**
```maxima
element: chem_element_period_group(3, 17);   /* Returns "Cl" */
element: chem_element_period_group(4, 11);   /* Returns "Cu" */
element: chem_element_period_group(1, 5);    /* Returns false */
```

---

#### `chem_element_period_maingroup(period_num, maingroup_num)`

**Description:** Returns the element symbol at a specific period and main group position.

**Parameters:**
- `period_num` (integer): Period number (1–7)
- `maingroup_num` (integer): Main group number (1–8)

**Returns:** Element symbol, or `false` if no element exists at that position

**Example:**
```maxima
element: chem_element_period_maingroup(3, 7);  /* Returns "Cl" */
element: chem_element_period_maingroup(4, 1);  /* Returns "K" */
element: chem_element_period_maingroup(1, 3);  /* Returns false */
```

---

### Electron Configuration Functions

#### `chem_electron_config(element)`

**Description:** Returns the formatted electron configuration for an element, ready for LaTeX display. Orbital letters are wrapped in `\mathrm{}` and electron counts become superscripts.

**Parameters:**
- `element` (string): Element symbol

**Returns:** LaTeX-formatted electron configuration string, or `false` if not found

**Example:**
```maxima
config: chem_electron_config("B");
/* Returns "[\mathrm{He}] 2\mathrm{s}^{2} 2\mathrm{p}^{1}" */

config: chem_electron_config("Fe");
/* Returns "[\mathrm{Ar}] 4\mathrm{s}^{2} 3\mathrm{d}^{6}" */

config: chem_electron_config("Cu");
/* Returns "[\mathrm{Ar}] 4\mathrm{s}^{1} 3\mathrm{d}^{10}" */
```

**Usage in Question Text:**
```latex
<p>The electron configuration of {@element@} is: \({@chem_electron_config(element)@}\)</p>
```

---

#### `chem_electron_config_formatter(config_str)`

**Description:** Formats a raw electron configuration string for LaTeX display. Used internally by `chem_electron_config()`, but can also be used directly with custom configuration strings.

**Parameters:**
- `config_str` (string): Raw electron configuration (e.g., `"[Kr] 5s2 4d10 5p6"`)

**Returns:** LaTeX-formatted string

**Example:**
```maxima
formatted: chem_electron_config_formatter("[Kr] 5s2 4d10 5p6");
/* Returns "[\mathrm{Kr}] 5\mathrm{s}^{2} 4\mathrm{d}^{10} 5\mathrm{p}^{6}" */
```

---

### Molar Mass and Formula Parsing Functions

#### `chem_molar_mass(formula)`

**Description:** Calculates the molar mass of a molecule from its chemical formula string. Returns the result with units (g/mol).

**Parameters:**
- `formula` (string): Chemical formula (e.g., `"H2SO4"`, `"Ca(OH)2"`)

**Returns:** Molar mass with units via `stackunits(value, g*mol^(-1))`, or `false` if an element is not found

**Example:**
```maxima
mass: chem_molar_mass("H2O");       /* Returns stackunits(18.02, g*mol^(-1)) */
mass: chem_molar_mass("H2SO4");     /* Returns stackunits(98.09, g*mol^(-1)) */
mass: chem_molar_mass("NaCl");      /* Returns stackunits(58.44, g*mol^(-1)) */
```

**Note:** This function parses the formula by detecting uppercase letters (element start), optional lowercase letters (second character), and digits (count). It does **not** handle parentheses like `(OH)2` — use the expanded formula `O2H2` instead, or input the element counts directly.

---

#### `chem_parse_formula(formula)`

**Description:** Parses a chemical formula string and returns a list of [element, count] pairs. Removes charge indicators (`+`, `-`, `^`, `{`, `}`) before parsing.

**Parameters:**
- `formula` (string): Chemical formula

**Returns:** List of `[element_symbol, count]` pairs

**Example:**
```maxima
parsed: chem_parse_formula("H2SO4");
/* Returns [["H", 2], ["S", 1], ["O", 4]] */

parsed: chem_parse_formula("NaCl");
/* Returns [["N", 1], ["a", ...]] — Note: works best with simple formulas */

parsed: chem_parse_formula("CO2");
/* Returns [["C", 1], ["O", 2]] */
```

---

#### `chem_string_to_number(str)`

**Description:** Converts a string of digit characters to an integer. Used internally by the formula parser.

**Parameters:**
- `str` (string): String of digits (e.g., `"42"`)

**Returns:** Integer value

**Example:**
```maxima
num: chem_string_to_number("123");   /* Returns 123 */
num: chem_string_to_number("4");     /* Returns 4 */
```

---

### Chemical Formula Display Function

#### `chem_display(substance)`

**Description:** Wraps a chemical formula in `\ce{...}` for LaTeX/mhchem rendering.

**Parameters:**
- `substance` (string): Chemical formula

**Returns:** String formatted as `\ce{formula}`

**Example:**
```maxima
display: chem_display("H2SO4");     /* Returns "\\ce{H2SO4}" */
display: chem_display("Ca^{2+}");   /* Returns "\\ce{Ca^{2+}}" */
```

**Usage in Question Text:**
```maxima
/* In Question Variables */
acid: "H2SO4";
acid_display: chem_display(acid);
```
```latex
/* In Question Text */
\(\require{mhchem}\)
<p>Consider the acid {@acid_display@}.</p>
```

---

### Available Data Fields

The following data fields can be retrieved with `chem_data()` or `chem_data_units()`:

| Field Name | Type | Unit | Description |
|------------|------|------|-------------|
| `AtomicNumber` | Integer | — | Atomic number (1–118) |
| `Name` | String | — | Element name (language-dependent) |
| `Period` | Integer | — | Period number (1–7) |
| `MainGroup` | Integer | — | Main group (1–8, or 0 for transition metals) |
| `GroupNumber` | Integer | — | IUPAC group number (1–18) |
| `AtomicMass` | Float | g/mol | Standard atomic mass |
| `ElectronConfiguration` | String | — | Electron configuration (raw format) |
| `Electronegativity` | Float | — | Pauling electronegativity |
| `AtomicRadius` | Integer | pm | Atomic radius |
| `IonizationEnergy` | Float | J | First ionization energy |
| `ElectronAffinity` | Float | — | Electron affinity |
| `OxidationStates` | String | — | Common oxidation states |
| `StandardState` | String | — | State at standard conditions (Solid/Liquid/Gas) |
| `MeltingPoint` | Float | K | Melting point |
| `BoilingPoint` | Float | K | Boiling point |
| `Density` | Float | g/cm³ | Density |
| `GroupBlock` | String | — | Element category (e.g., "Nonmetal", "Halogen") |
| `YearDiscovered` | Integer/String | — | Year of discovery |

**Note:** Missing numerical data is indicated by the atom `null` rather than a zero.

### Language Support

The library supports multiple languages for element names via the `%_STACK_LANG` variable:
- English (default)
- German (`"de"`)

Element names are automatically translated when using `chem_data(element, "Name")`.

---

## Acid-Base Chemistry Module

The acid-base module provides comprehensive functions for working with acids and bases, including pKa/pKb lookups, conjugate pair determination, equilibrium expressions, titration curve calculation, and JSXGraph plotting.

### Acid-Base Data Retrieval Functions

#### `chem_acidbase_pKa(acid)`

**Description:** Returns the pKa value for a given acid.

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** pKa value (number), or `null` if not found

**Example:**
```maxima
pka: chem_acidbase_pKa("CH3COOH");   /* Returns 4.76 */
pka: chem_acidbase_pKa("HCl");       /* Returns -7.0 */
pka: chem_acidbase_pKa("H3PO4");     /* Returns 2.12 */
pka: chem_acidbase_pKa("H2O");       /* Returns 14 */
```

---

#### `chem_acidbase_pKb(base)`

**Description:** Returns the pKb value for a given base.

**Parameters:**
- `base` (string): Chemical formula of the base

**Returns:** pKb value (number), or `null` if not found

**Example:**
```maxima
pkb: chem_acidbase_pKb("NH3");        /* Returns 4.75 */
pkb: chem_acidbase_pKb("CH3COO-");    /* Returns 9.24 */
pkb: chem_acidbase_pKb("OH-");        /* Returns 0 */
```

---

#### `chem_acidbase_Ka(acid)`

**Description:** Calculates Ka from pKa: Ka = 10^(−pKa).

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** Ka value (number), or `null` if pKa not available

**Example:**
```maxima
ka: chem_acidbase_Ka("CH3COOH");   /* Returns 10^(-4.76) ≈ 1.74e-5 */
ka: chem_acidbase_Ka("HCl");       /* Returns 10^(7) = 1.0e7 */
```

---

#### `chem_acidbase_Kb(base)`

**Description:** Calculates Kb from pKb: Kb = 10^(−pKb).

**Parameters:**
- `base` (string): Chemical formula of the base

**Returns:** Kb value (number), or `null` if pKb not available

**Example:**
```maxima
kb: chem_acidbase_Kb("NH3");        /* Returns 10^(-4.75) ≈ 1.78e-5 */
kb: chem_acidbase_Kb("CH3COO-");    /* Returns 10^(-9.24) ≈ 5.75e-10 */
```

---

#### `chem_acidbase_nH(acid)`

**Description:** Returns the number of acidic protons (nH) for a given acid entry in the database.

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** Integer number of acidic protons, or `null` if not found

**Example:**
```maxima
nh: chem_acidbase_nH("H3PO4");    /* Returns 3 */
nh: chem_acidbase_nH("H2SO4");    /* Returns 2 */
nh: chem_acidbase_nH("HCl");      /* Returns 1 */
nh: chem_acidbase_nH("H2CO3");    /* Returns 2 */
```

---

#### `chem_acidbase_num_protons(acid)`

**Description:** Convenience function that returns the number of protons for an acid (defaults to 1 if not found).

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** Integer number of acidic protons (never returns null, defaults to 1)

**Example:**
```maxima
n: chem_acidbase_num_protons("H3PO4");    /* Returns 3 */
n: chem_acidbase_num_protons("HCl");      /* Returns 1 */
n: chem_acidbase_num_protons("unknown");  /* Returns 1 (default) */
```

---

### Conjugate Acid-Base Functions

#### `chem_acidbase_conjugate_base(acid)`

**Description:** Returns the conjugate base for a given acid from the database.

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** String formula of the conjugate base, or `""` if not found

**Example:**
```maxima
base: chem_acidbase_conjugate_base("H2SO4");      /* Returns "HSO4-" */
base: chem_acidbase_conjugate_base("HSO4-");      /* Returns "SO4^{2-}" */
base: chem_acidbase_conjugate_base("NH4+");       /* Returns "NH3" */
base: chem_acidbase_conjugate_base("CH3COOH");    /* Returns "CH3COO-" */
base: chem_acidbase_conjugate_base("H3PO4");      /* Returns "H2PO4-" */
```

---

#### `chem_acidbase_conjugate_acid(base)`

**Description:** Returns the conjugate acid for a given base from the database.

**Parameters:**
- `base` (string): Chemical formula of the base

**Returns:** String formula of the conjugate acid, or `""` if not found

**Example:**
```maxima
acid: chem_acidbase_conjugate_acid("SO4^{2-}");   /* Returns "HSO4-" */
acid: chem_acidbase_conjugate_acid("NH3");         /* Returns "NH4+" */
acid: chem_acidbase_conjugate_acid("CH3COO-");     /* Returns "CH3COOH" */
acid: chem_acidbase_conjugate_acid("OH-");         /* Returns "H2O" */
```

---

### Equilibrium Expression Functions

#### `chem_acidbase_Ka_expression(acid)`

**Description:** Generates a Ka expression in bracket (concentration) notation as a LaTeX string.

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** LaTeX string of the Ka expression, or `""` if not found

**Example:**
```maxima
expr: chem_acidbase_Ka_expression("CH3COOH");
/* Returns "\\frac{[H^+] \\cdot [CH3COO-]}{[CH3COOH]}" */

expr: chem_acidbase_Ka_expression("NH4+");
/* Returns "\\frac{[H^+] \\cdot [NH3]}{[NH4+]}" */
```

**Usage in Question Text:**
```latex
\(\require{mhchem}\)
<p>\( K_a = {@chem_acidbase_Ka_expression(acid)@} \)</p>
```

---

#### `chem_acidbase_Ka_activity_expression(acid)`

**Description:** Generates a Ka expression in activity notation as a LaTeX string.

**Parameters:**
- `acid` (string): Chemical formula of the acid

**Returns:** LaTeX string using activity notation `a(...)`

**Example:**
```maxima
expr: chem_acidbase_Ka_activity_expression("CH3COOH");
/* Returns "\\frac{a(H^+) \\cdot a(CH3COO-)}{a(CH3COOH)}" */
```

---

#### `chem_acidbase_Kb_expression(base)`

**Description:** Generates a Kb expression in bracket notation as a LaTeX string.

**Parameters:**
- `base` (string): Chemical formula of the base

**Returns:** LaTeX string of the Kb expression, or `""` if not found

**Example:**
```maxima
expr: chem_acidbase_Kb_expression("NH3");
/* Returns "\\frac{[NH4+] \\cdot [OH^-]}{[NH3]}" */
```

---

#### `chem_acidbase_Kb_activity_expression(base)`

**Description:** Generates a Kb expression in activity notation as a LaTeX string.

**Parameters:**
- `base` (string): Chemical formula of the base

**Returns:** LaTeX string using activity notation

**Example:**
```maxima
expr: chem_acidbase_Kb_activity_expression("NH3");
/* Returns "\\frac{a(NH4+) \\cdot a(OH^-)}{a(NH3)}" */
```

---

### Acid-Base Navigation Functions

#### `chem_acid_array()`

**Description:** Returns an array of all acid formulas in the database.

**Returns:** List of acid formula strings

**Example:**
```maxima
acids: chem_acid_array();
/* Returns ["H3O+", "HCl", "HBr", "HI", "H2SO4", ..., "C5H5NH+"] */

acid: rand(chem_acid_array());
```

---

#### `chem_base_array()`

**Description:** Returns an array of all base formulas in the database.

**Returns:** List of base formula strings

**Example:**
```maxima
bases: chem_base_array();
/* Returns ["H2O", "Cl-", "Br-", ..., "C5H5N"] */
```

---

#### `chem_strong_acid_array()`

**Description:** Returns an array of strong acids (pKa < 0).

**Returns:** List of strong acid formulas

**Example:**
```maxima
strong_acids: chem_strong_acid_array();
/* Returns ["HCl", "HBr", "HI", "H2SO4", "HNO3", "HClO4", "HClO3"] */
```

---

#### `chem_weak_acid_array()`

**Description:** Returns an array of weak acids (pKa > 0).

**Returns:** List of weak acid formulas

**Example:**
```maxima
weak_acids: chem_weak_acid_array();
/* Returns ["H2O", "HSO4-", "H3PO4", "H2PO4-", ..., "C5H5NH+"] */
```

---

#### `chem_strong_base_array()`

**Description:** Returns an array of strong bases (pKb ≤ 0).

**Returns:** List of strong base formulas

**Example:**
```maxima
strong_bases: chem_strong_base_array();
/* Returns ["OH-"] */
```

---

#### `chem_weak_base_array()`

**Description:** Returns an array of weak bases (0 < pKb < 14).

**Returns:** List of weak base formulas

**Example:**
```maxima
weak_bases: chem_weak_base_array();
/* Returns ["H2O", "SO4^{2-}", ..., "C5H5N"] */
```

---

#### `chem_acid_array_nH(nH_target)`

**Description:** Returns all acids with a specific number of acidic protons.

**Parameters:**
- `nH_target` (integer): Desired number of acidic protons

**Returns:** List of acid formulas

**Example:**
```maxima
diprotic: chem_acid_array_nH(2);
/* Returns ["H2SO4", "H2PO4-", "H2CO3", "H2S", "H2O2", "H2SiO3", "H2C2O4", ...] */

triprotic: chem_acid_array_nH(3);
/* Returns ["H3PO4", "H3BO3", "H3AsO4"] */
```

---

#### `chem_strong_acid_array_nH(nH_target)`

**Description:** Returns strong acids with a specific number of acidic protons.

**Parameters:**
- `nH_target` (integer): Desired number of acidic protons

**Returns:** List of strong acid formulas

**Example:**
```maxima
strong_diprotic: chem_strong_acid_array_nH(2);
/* Returns ["H2SO4"] */
```

---

#### `chem_weak_acid_array_nH(nH_target)`

**Description:** Returns weak acids with a specific number of acidic protons.

**Parameters:**
- `nH_target` (integer): Desired number of acidic protons

**Returns:** List of weak acid formulas

**Example:**
```maxima
weak_monoprotic: chem_weak_acid_array_nH(1);
/* Returns ["H2O", "HSO4-", "HF", "HNO2", "HCOOH", ..., "C5H5NH+"] */
```

---

#### `chem_acidbase_array()`

**Description:** Legacy function — returns all acid formulas (same as `chem_acid_array()`).

**Returns:** List of all acid formula strings

---

### Polyprotic Acid Functions

#### `chem_acidbase_pKa_list(acid)`

**Description:** Returns all pKa values for a polyprotic acid as a list, following the deprotonation chain through the database.

**Parameters:**
- `acid` (string): Chemical formula of the acid (starting species)

**Returns:** List of pKa values in order of successive deprotonations

**Example:**
```maxima
pkas: chem_acidbase_pKa_list("H3PO4");
/* Returns [2.12, 7.21, 12.32] */

pkas: chem_acidbase_pKa_list("H2CO3");
/* Returns [6.35, 10.33] */

pkas: chem_acidbase_pKa_list("CH3COOH");
/* Returns [4.76] */
```

---

#### `chem_titration_pKa_values(acid)`

**Description:** Alias for `chem_acidbase_pKa_list()` — returns all pKa values for plotting reference lines.

---

### Titration Curve Functions

#### `chem_titration_pH(acid, c_acid, c_base, v_acid, v_base)`

**Description:** Calculates the pH at a given point during the titration of a polyprotic acid with a strong base. Uses alpha fractions and charge balance with a bisection solver.

**Parameters:**
- `acid` (string): Chemical formula of the acid
- `c_acid` (number): Concentration of acid (mol/L)
- `c_base` (number): Concentration of base (mol/L)
- `v_acid` (number): Volume of acid (mL)
- `v_base` (number): Volume of base added (mL)

**Returns:** pH value (float between 0 and 14), or `false` if acid not found

**Example:**
```maxima
ph: chem_titration_pH("CH3COOH", 0.1, 0.1, 25, 0);     /* Initial pH */
ph: chem_titration_pH("CH3COOH", 0.1, 0.1, 25, 12.5);  /* Half-equivalence point */
ph: chem_titration_pH("CH3COOH", 0.1, 0.1, 25, 25);    /* Equivalence point */
```

---

#### `chem_titration_curve_data(acid, c_acid, c_base, v_acid, n_points)`

**Description:** Generates titration curve data with automatic end volume (1.3× final equivalence volume).

**Parameters:**
- `acid` (string): Chemical formula of the acid
- `c_acid` (number): Concentration of acid (mol/L)
- `c_base` (number): Concentration of base (mol/L)
- `v_acid` (number): Volume of acid (mL)
- `n_points` (integer): Number of data points

**Returns:** List of [volume, pH] pairs

**Example:**
```maxima
data: chem_titration_curve_data("CH3COOH", 0.1, 0.1, 25, 100);
/* Returns [[0, 2.88], [0.325, 2.92], ..., [32.5, 12.4]] */
```

---

#### `chem_titration_curve_data_vmax(acid, c_acid, c_base, v_acid, n_points, v_max)`

**Description:** Generates titration curve data with a custom maximum volume. If `v_max ≤ 0`, calculates automatically.

**Parameters:**
- `acid`, `c_acid`, `c_base`, `v_acid`, `n_points`: Same as above
- `v_max` (number): Maximum volume to plot (mL), or ≤ 0 for automatic

**Returns:** List of [volume, pH] pairs

---

#### `chem_titration_xdata(data)`

**Description:** Extracts X-values (volumes) from titration curve data as a Maxima list, rounded to 3 decimal places. Suitable for direct use in JSXGraph.

**Parameters:**
- `data` (list): Titration curve data from `chem_titration_curve_data()`

**Returns:** List of volume values (floats)

---

#### `chem_titration_ydata(data)`

**Description:** Extracts Y-values (pH) from titration curve data as a Maxima list, rounded to 3 decimal places.

**Parameters:**
- `data` (list): Titration curve data from `chem_titration_curve_data()`

**Returns:** List of pH values (floats)

---

#### `chem_titration_jsxgraph_points(data)`

**Description:** Converts titration data to a JSXGraph-compatible JavaScript array string. Values rounded to 3 decimal places.

**Parameters:**
- `data` (list): Titration curve data

**Returns:** JavaScript array string, e.g., `"[[0,2.88],[0.325,2.92],...]"`

---

#### `chem_titration_equiv_volume(c_acid, c_base, v_acid, i)`

**Description:** Returns the i-th equivalence point volume (in mL).

**Parameters:**
- `c_acid` (number): Acid concentration
- `c_base` (number): Base concentration
- `v_acid` (number): Acid volume (mL)
- `i` (integer): Equivalence point index (1, 2, 3, ...)

**Returns:** Volume in mL (float)

**Example:**
```maxima
v_eq1: chem_titration_equiv_volume(0.1, 0.1, 25, 1);  /* Returns 25.0 */
v_eq2: chem_titration_equiv_volume(0.1, 0.1, 25, 2);  /* Returns 50.0 */
```

---

#### `chem_titration_equiv_volumes(acid, c_acid, c_base, v_acid)`

**Description:** Returns a list of all equivalence point volumes for a polyprotic acid.

**Parameters:**
- `acid` (string): Chemical formula of the acid
- `c_acid`, `c_base`, `v_acid`: Concentration and volume parameters

**Returns:** List of equivalence volumes in mL

**Example:**
```maxima
vols: chem_titration_equiv_volumes("H3PO4", 0.1, 0.1, 25);
/* Returns [25.0, 50.0, 75.0] */
```

---

#### `chem_titration_equiv_pH(acid, c_acid, c_base, v_acid, i)`

**Description:** Returns the pH at the i-th equivalence point.

---

#### `chem_titration_half_equiv_pH(acid, c_acid, c_base, v_acid, i)`

**Description:** Returns the pH at the i-th half-equivalence point. At the half-equivalence point, pH ≈ pKa for weak acids.

---

#### `chem_titration_equiv_data(acid, c_acid, c_base, v_acid)`

**Description:** Returns equivalence points as flat lists for easier JSXGraph use.

**Returns:** `[v_list, pH_list]` where both are simple lists

---

#### `chem_titration_plot_data(acid, c_acid, c_base, v_acid, n_points, v_max)`

**Description:** Calculates all data needed for a titration plot in one call.

**Returns:** `[xdata, ydata, v_pushoff, equiv_points, pKa_list]`

**Example:**
```maxima
plot_data: chem_titration_plot_data("H3PO4", 0.1, 0.1, 25, 200, 100);
xdata: plot_data[1];
ydata: plot_data[2];
v_pushoff: plot_data[3];
equiv_points: plot_data[4];
pKa_list: plot_data[5];
```

---

#### `chem_jsxgraph_titration_code(xdata, ydata, v_max, v_pushoff)`

**Description:** Generates complete JSXGraph JavaScript code for a basic titration curve.

**Parameters:**
- `xdata` (list): X-values (volumes)
- `ydata` (list): Y-values (pH)
- `v_max` (number): Maximum x-axis value
- `v_pushoff` (number): Left boundary offset (typically negative)

**Returns:** JavaScript code string

---

#### `chem_jsxgraph_titration_code_full(xdata, ydata, v_max, v_pushoff, equiv_points, pKa_list)`

**Description:** Extended version with equivalence point markers and pKa reference lines.

**Parameters:**
- `xdata`, `ydata`, `v_max`, `v_pushoff`: Same as above
- `equiv_points` (list): List of [volume, pH] pairs for equivalence points
- `pKa_list` (list): List of pKa values for horizontal reference lines

**Returns:** JavaScript code string

---

#### `chem_jsxgraph_titration(acid, c_acid, c_base, v_acid, n_points, v_max)`

**Description:** Convenience function that generates everything from the acid name — returns complete JSXGraph JavaScript code for a full titration plot with equivalence points and pKa lines.

**Parameters:**
- `acid` (string): Chemical formula
- `c_acid`, `c_base` (number): Concentrations (mol/L)
- `v_acid` (number): Volume of acid (mL)
- `n_points` (integer): Number of data points
- `v_max` (number): Maximum volume for x-axis

**Returns:** JavaScript code string

**Example (in Question Variables):**
```maxima
jsxcode: chem_jsxgraph_titration("H3PO4", 0.1, 0.1, 25, 200, 100);
```

**Example (in Question Text):**
```html
[[jsxgraph width="500px" height="400px"]]
{#jsxcode#}
[[/jsxgraph]]
```

---

### Available Acids and Bases

The following substances are available in the acid-base database:

| Acid | pKa | pKb | Conjugate Base | nH |
|------|-----|-----|----------------|-----|
| H3O+ | 0 | 14 | H2O | 1 |
| HCl | −7.0 | 21.0 | Cl- | 1 |
| HBr | −9.0 | 23.0 | Br- | 1 |
| HI | −10.0 | 24.0 | I- | 1 |
| H2SO4 | −2.0 | 16.0 | HSO4- | 2 |
| HNO3 | −1.0 | 15.0 | NO3- | 1 |
| HClO4 | −10.0 | 24.0 | ClO4- | 1 |
| HClO3 | −1.0 | 15.0 | ClO3- | 1 |
| H2O | 14 | 0 | OH- | 1 |
| HSO4- | 1.92 | 12.08 | SO4^{2-} | 1 |
| H3PO4 | 2.12 | 11.88 | H2PO4- | 3 |
| H2PO4- | 7.21 | 6.79 | HPO4^{2-} | 2 |
| HPO4^{2-} | 12.32 | 1.68 | PO4^{3-} | 1 |
| HF | 3.17 | 10.83 | F- | 1 |
| HNO2 | 3.25 | 10.75 | NO2- | 1 |
| HCOOH | 3.75 | 10.25 | HCOO- | 1 |
| C6H5COOH | 4.20 | 9.80 | C6H5COO- | 1 |
| CH3COOH | 4.76 | 9.24 | CH3COO- | 1 |
| H2CO3 | 6.35 | 7.65 | HCO3- | 2 |
| HCO3- | 10.33 | 3.67 | CO3^{2-} | 1 |
| H2S | 7.00 | 7.00 | HS- | 2 |
| HS- | 12.89 | 1.11 | S^{2-} | 1 |
| HClO2 | 1.94 | 12.06 | ClO2- | 1 |
| HClO | 7.53 | 6.47 | ClO- | 1 |
| HBrO | 8.59 | 5.41 | BrO- | 1 |
| HIO | 10.64 | 3.36 | IO- | 1 |
| HCN | 9.21 | 4.79 | CN- | 1 |
| NH4+ | 9.25 | 4.75 | NH3 | 1 |
| H2O2 | 11.62 | 2.38 | HO2- | 2 |
| C6H5OH | 9.95 | 4.05 | C6H5O- | 1 |
| H3BO3 | 9.24 | 4.76 | H2BO3- | 3 |
| H2SiO3 | 9.77 | 4.23 | HSiO3- | 2 |
| HSiO3- | 11.80 | 2.20 | SiO3^{2-} | 1 |
| H2C2O4 | 1.25 | 12.75 | HC2O4- | 2 |
| HC2O4- | 4.27 | 9.73 | C2O4^{2-} | 1 |
| H2SO3 | 1.81 | 12.19 | HSO3- | 2 |
| HSO3- | 6.91 | 7.09 | SO3^{2-} | 1 |
| H3AsO4 | 2.22 | 11.78 | H2AsO4- | 3 |
| H2AsO4- | 6.98 | 7.02 | HAsO4^{2-} | 2 |
| HAsO4^{2-} | 11.50 | 2.50 | AsO4^{3-} | 1 |
| H2CrO4 | 0.74 | 13.26 | HCrO4- | 2 |
| HCrO4- | 6.49 | 7.51 | CrO4^{2-} | 1 |
| CH3NH3+ | 10.64 | 3.36 | CH3NH2 | 1 |
| (CH3)2NH2+ | 10.73 | 3.27 | (CH3)2NH | 1 |
| (CH3)3NH+ | 9.80 | 4.20 | (CH3)3N | 1 |
| C2H5NH3+ | 10.81 | 3.19 | C2H5NH2 | 1 |
| C6H5NH3+ | 4.63 | 9.37 | C6H5NH2 | 1 |
| N2H5+ | 8.07 | 5.93 | N2H4 | 1 |
| HONH3+ | 5.96 | 8.04 | HONH2 | 1 |
| H2NCONH3+ | 0.18 | 13.82 | H2NCONH2 | 1 |
| C5H5NH+ | 5.23 | 8.77 | C5H5N | 1 |

---

## Solubility Equilibrium Module

The solubility equilibrium module provides functions for working with solubility products (Ksp), molar solubility, precipitation reactions, and dissolution equilibria. The database uses a nested association list with the salt as the key.

**Important:** The database stores only `pKsp` values. `Ksp` is always computed as `10^(-pKsp)` to avoid rounding errors from storing both values independently.

### Solubility Data Retrieval Functions

#### `chem_sol_Ksp(salt)`

**Description:** Returns the solubility product Ksp for a given salt, computed from the stored pKsp as `Ksp = 10^(-pKsp)`.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Ksp value (number), or `null` if not found

**Example:**
```maxima
ksp: chem_sol_Ksp("AgCl");       /* Returns 1.77e-10 */
ksp: chem_sol_Ksp("BaSO4");      /* Returns 1.08e-10 */
ksp: chem_sol_Ksp("CaF2");       /* Returns 3.45e-11 */
ksp: chem_sol_Ksp("PbI2");       /* Returns 9.80e-9 */
```

---

#### `chem_sol_pKsp(salt)`

**Description:** Returns the pKsp value (−log₁₀ Ksp) for a given salt.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** pKsp value (number), or `null` if not found

**Example:**
```maxima
pksp: chem_sol_pKsp("AgCl");     /* Returns 9.75 */
pksp: chem_sol_pKsp("BaSO4");    /* Returns 9.97 */
```

---

#### `chem_sol_cation(salt)`

**Description:** Returns the cation formula for a given salt.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Cation formula (string in mhchem format), or `""` if not found

**Example:**
```maxima
cat: chem_sol_cation("AgCl");        /* Returns "Ag^+" */
cat: chem_sol_cation("CaF2");        /* Returns "Ca^{2+}" */
cat: chem_sol_cation("Fe(OH)3");     /* Returns "Fe^{3+}" */
cat: chem_sol_cation("Ag2CrO4");     /* Returns "Ag^+" */
```

---

#### `chem_sol_cation_count(salt)`

**Description:** Returns the stoichiometric coefficient of the cation.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Integer count, or `null` if not found

**Example:**
```maxima
n: chem_sol_cation_count("AgCl");        /* Returns 1 */
n: chem_sol_cation_count("Ag2SO4");      /* Returns 2 */
n: chem_sol_cation_count("Ca3(PO4)2");   /* Returns 3 */
n: chem_sol_cation_count("Ag3PO4");      /* Returns 3 */
```

---

#### `chem_sol_anion(salt)`

**Description:** Returns the anion formula for a given salt.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Anion formula (string in mhchem format), or `""` if not found

**Example:**
```maxima
an: chem_sol_anion("AgCl");           /* Returns "Cl^-" */
an: chem_sol_anion("BaSO4");          /* Returns "SO4^{2-}" */
an: chem_sol_anion("Ca3(PO4)2");      /* Returns "PO4^{3-}" */
an: chem_sol_anion("Mg(OH)2");        /* Returns "OH^-" */
```

---

#### `chem_sol_anion_count(salt)`

**Description:** Returns the stoichiometric coefficient of the anion.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Integer count, or `null` if not found

**Example:**
```maxima
n: chem_sol_anion_count("AgCl");          /* Returns 1 */
n: chem_sol_anion_count("PbCl2");         /* Returns 2 */
n: chem_sol_anion_count("Fe(OH)3");       /* Returns 3 */
n: chem_sol_anion_count("Ca3(PO4)2");     /* Returns 2 */
```

---

#### `chem_sol_ion_counts(salt)`

**Description:** Returns both ion stoichiometric coefficients as a list.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** `[cation_count, anion_count]`, or `null` if not found

**Example:**
```maxima
counts: chem_sol_ion_counts("Ag2CrO4");   /* Returns [2, 1] */
counts: chem_sol_ion_counts("Ca3(PO4)2"); /* Returns [3, 2] */
counts: chem_sol_ion_counts("PbCl2");     /* Returns [1, 2] */
```

---

#### `chem_sol_total_ion_count(salt)`

**Description:** Returns the total number of ions produced per formula unit (cation_count + anion_count).

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Integer total ion count, or `null` if not found

**Example:**
```maxima
n: chem_sol_total_ion_count("AgCl");          /* Returns 2 */
n: chem_sol_total_ion_count("PbCl2");         /* Returns 3 */
n: chem_sol_total_ion_count("Ca3(PO4)2");     /* Returns 5 */
n: chem_sol_total_ion_count("Bi2S3");         /* Returns 5 */
```

---

#### `chem_sol_entry(salt)`

**Description:** Returns the full database entry for a salt as a list.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** `[salt, Ksp, pKsp, cation, cation_count, anion, anion_count]`, or `null` if not found

**Example:**
```maxima
entry: chem_sol_entry("PbCl2");
/* Returns ["PbCl2", 1.70e-5, 4.77, "Pb^{2+}", 1, "Cl^-", 2] */
```

---

### Solubility Equilibrium Expression Functions

#### `chem_sol_Ksp_expression(salt)`

**Description:** Generates a Ksp expression in bracket (concentration) notation as a LaTeX string.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** LaTeX string, or `""` if not found

**Example:**
```maxima
expr: chem_sol_Ksp_expression("AgCl");
/* Returns "[\\ce{Ag^+}] \\cdot [\\ce{Cl^-}]" */

expr: chem_sol_Ksp_expression("PbCl2");
/* Returns "[\\ce{Pb^{2+}}] \\cdot [\\ce{Cl^-}]^2" */

expr: chem_sol_Ksp_expression("Ag2CrO4");
/* Returns "[\\ce{Ag^+}]^2 \\cdot [\\ce{CrO4^{2-}}]" */

expr: chem_sol_Ksp_expression("Ca3(PO4)2");
/* Returns "[\\ce{Ca^{2+}}] \\cdot [\\ce{PO4^{3-}}]" */
```

**Usage in Question Text:**
```latex
\(\require{mhchem}\)
<p>\( K_{\mathrm{sp}} = {@chem_sol_Ksp_expression(salt)@} \)</p>
```

---

#### `chem_sol_Ksp_activity_expression(salt)`

**Description:** Generates the full Ksp expression in activity notation, including the denominator `a(salt)` for pedagogical purposes.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** LaTeX string with fraction including solid activity in denominator

**Example:**
```maxima
expr: chem_sol_Ksp_activity_expression("AgCl");
/* Returns "\\frac{a(\\ce{Ag^+}) \\cdot a(\\ce{Cl^-})}{a(\\ce{AgCl})}" */
```

---

#### `chem_sol_Ksp_activity_expression_simplified(salt)`

**Description:** Generates the simplified Ksp expression in activity notation (denominator a(solid) = 1 is omitted).

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** LaTeX string without denominator

**Example:**
```maxima
expr: chem_sol_Ksp_activity_expression_simplified("PbCl2");
/* Returns "a(\\ce{Pb^{2+}}) \\cdot a(\\ce{Cl^-})^2" */
```

---

#### `chem_sol_solubility_expression(salt)`

**Description:** Generates a LaTeX expression for the molar solubility formula derived from Ksp. For a salt M_p X_q, returns `(Ksp / (p^p · q^q))^{1/(p+q)}` with the denominator computed as a single number.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** LaTeX string, or `""` if not found

**Example:**
```maxima
expr: chem_sol_solubility_expression("AgCl");
/* Returns "\\sqrt{K_{\\mathrm{sp}}}" (1:1 salt, denom=1) */

expr: chem_sol_solubility_expression("PbCl2");
/* Returns "\\left( \\frac{K_{\\mathrm{sp}}}{4} \\right)^{\\frac{1}{3}}" (1:2 salt, denom=1*4=4) */

expr: chem_sol_solubility_expression("Ag2CrO4");
/* Returns "\\left( \\frac{K_{\\mathrm{sp}}}{4} \\right)^{\\frac{1}{3}}" (2:1 salt, denom=4*1=4) */

expr: chem_sol_solubility_expression("Ca3(PO4)2");
/* Returns "\\left( \\frac{K_{\\mathrm{sp}}}{108} \\right)^{\\frac{1}{5}}" (3:2 salt, denom=27*4=108) */
```

**Usage in Question Text:**
```latex
\(\require{mhchem}\)
<p>For \({@salt_display@}\): \({@chem_sol_solubility_expression(salt)@}\)</p>
```

---

### Molar Solubility Calculation Functions

#### `chem_molar_mass(formula)`

**Description:** Calculates the molar mass of a molecule from its chemical formula string. Returns the result with units (g/mol).

**Parameters:**
- `formula` (string): Chemical formula (e.g., `"H2SO4"`, `"Ca(OH)2"`)

**Returns:** Molar mass with units via `stackunits(value, g*mol^(-1))`, or `false` if an element is not found

**Example:**
```maxima
mass: chem_molar_mass("H2O");       /* Returns stackunits(18.02, g*mol^(-1)) */
mass: chem_molar_mass("H2SO4");     /* Returns stackunits(98.09, g*mol^(-1)) */
mass: chem_molar_mass("NaCl");      /* Returns stackunits(58.44, g*mol^(-1)) */
```

**Note:** This function parses the formula by detecting uppercase letters (element start), optional lowercase letters (second character), and digits (count). It does **not** handle parentheses like `(OH)2` — use the expanded formula `O2H2` instead, or input the element counts directly.

---

#### `chem_sol_molar_solubility(salt)`

**Description:** Calculates the molar solubility `s` from Ksp for a salt M_p X_q using the formula:  
`Ksp = (p·s)^p · (q·s)^q` ⟹ `s = (Ksp / (p^p · q^q))^(1/(p+q))`

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** Molar solubility with units via `stackunits(value, mol*L^(-1))`, or `null` if not found

**Example:**
```maxima
s: chem_sol_molar_solubility("AgCl");
/* Returns stackunits(1.33e-5, mol*l^(-1)) */

s: chem_sol_molar_solubility("PbCl2");
/* Returns stackunits(1.62e-2, mol*l^(-1)) */

s: chem_sol_molar_solubility("Ag2CrO4");
/* Returns stackunits(6.54e-5, mol*l^(-1)) */
```

---

#### `chem_sol_molar_solubility_common_ion(salt, c_common, common_ion)`

**Description:** Calculates molar solubility with a common-ion effect using a bisection solver. The common ion already present in solution reduces solubility.

**Parameters:**
- `salt` (string): Chemical formula of the salt
- `c_common` (number): Concentration of the common ion already in solution (mol/L)
- `common_ion` (string): `"cation"` or `"anion"` — which ion is the common ion

**Returns:** Molar solubility with units via `stackunits(value, mol*l^(-1))`, or `null` if not found

**Example:**
```maxima
/* Solubility of AgCl in 0.1 M NaCl solution (common Cl⁻) */
s: chem_sol_molar_solubility_common_ion("AgCl", 0.1, "anion");
/* Returns stackunits(1.77e-9, mol*l^(-1)) */

/* Solubility of PbCl2 in 0.5 M Pb(NO3)2 (common Pb²⁺) */
s: chem_sol_molar_solubility_common_ion("PbCl2", 0.5, "cation");
```

---

### Precipitation Check Functions

#### `chem_sol_ion_product(c_cation, c_anion, salt)`

**Description:** Calculates the ion product Q for a salt given ion concentrations: Q = [cation]^p · [anion]^q.

**Parameters:**
- `c_cation` (number): Cation concentration (mol/L)
- `c_anion` (number): Anion concentration (mol/L)
- `salt` (string): Chemical formula of the salt

**Returns:** Ion product Q (float), or `null` if salt not found

**Example:**
```maxima
Q: chem_sol_ion_product(1e-4, 1e-4, "AgCl");
/* Returns 1e-8 */

Q: chem_sol_ion_product(0.01, 0.02, "PbCl2");
/* Returns 0.01^1 * 0.02^2 = 4e-6 */
```

---

#### `chem_sol_precipitation_check(c_cation, c_anion, salt)`

**Description:** Checks whether precipitation occurs by comparing the ion product Q to Ksp.

**Parameters:**
- `c_cation` (number): Cation concentration (mol/L)
- `c_anion` (number): Anion concentration (mol/L)
- `salt` (string): Chemical formula of the salt

**Returns:** `"precipitates"`, `"saturated"`, or `"unsaturated"` (string), or `null` if salt not found

**Example:**
```maxima
result: chem_sol_precipitation_check(1e-3, 1e-3, "AgCl");
/* Returns "precipitates" (Q = 1e-6 > Ksp = 1.77e-10) */

result: chem_sol_precipitation_check(1e-6, 1e-6, "AgCl");
/* Returns "unsaturated" (Q = 1e-12 < Ksp = 1.77e-10) */
```

---

#### `chem_sol_max_concentration(c_known, salt, ion_type)`

**Description:** Calculates the maximum concentration of one ion before precipitation begins, given the concentration of the other ion.

**Parameters:**
- `c_known` (number): Known ion concentration (mol/L)
- `salt` (string): Chemical formula of the salt
- `ion_type` (string): `"cation"` or `"anion"` — the ion whose max concentration is sought

**Returns:** Maximum concentration in mol/L (float), or `null`

**Example:**
```maxima
/* Max [Ag⁺] before AgCl precipitates in 0.01 M Cl⁻ */
c_max: chem_sol_max_concentration(0.01, "AgCl", "cation");
/* Returns 1.77e-8 */

/* Max [Cl⁻] before AgCl precipitates in 0.001 M Ag⁺ */
c_max: chem_sol_max_concentration(0.001, "AgCl", "anion");
/* Returns 1.77e-7 */
```

---

### Solubility Navigation Functions

#### `chem_sol_array()`

**Description:** Returns an array of all salt names in the database.

**Returns:** List of salt formula strings

**Example:**
```maxima
salts: chem_sol_array();
/* Returns ["AgCl", "AgBr", "AgI", ..., "Ag2SO3"] */

salt: rand(chem_sol_array());
```

---

#### `chem_sol_array_by_cation(cation)`

**Description:** Returns all salts containing a specific cation.

**Parameters:**
- `cation` (string): Cation formula in mhchem format

**Returns:** List of salt formula strings

**Example:**
```maxima
ag_salts: chem_sol_array_by_cation("Ag^+");
/* Returns ["AgCl", "AgBr", "AgI", "AgF", "Ag2SO4", "Ag2CO3", ...] */

pb_salts: chem_sol_array_by_cation("Pb^{2+}");
/* Returns ["PbCl2", "PbBr2", "PbI2", "PbF2", "PbSO4", "PbCO3", ...] */
```

---

#### `chem_sol_array_by_anion(anion)`

**Description:** Returns all salts containing a specific anion.

**Parameters:**
- `anion` (string): Anion formula in mhchem format

**Returns:** List of salt formula strings

**Example:**
```maxima
chlorides: chem_sol_array_by_anion("Cl^-");
/* Returns ["AgCl", "CuCl", "PbCl2", "Hg2Cl2", "TlCl"] */

carbonates: chem_sol_array_by_anion("CO3^{2-}");
/* Returns ["CaCO3", "BaCO3", "SrCO3", ..., "CdCO3"] */
```

---

#### `chem_sol_array_by_cation_count(n)`

**Description:** Returns all salts with a specific cation stoichiometric coefficient.

**Parameters:**
- `n` (integer): Desired cation count

**Returns:** List of salt formula strings

**Example:**
```maxima
salts_2cat: chem_sol_array_by_cation_count(2);
/* Returns ["Ag2SO4", "Ag2CO3", "Cu2S", "Ag2S", "Ag2CrO4", "Ag2C2O4", ...] */

salts_3cat: chem_sol_array_by_cation_count(3);
/* Returns ["Ca3(PO4)2", "Ag3PO4", "Pb3(PO4)2", "Zn3(PO4)2"] */
```

---

#### `chem_sol_array_by_anion_count(n)`

**Description:** Returns all salts with a specific anion stoichiometric coefficient.

**Parameters:**
- `n` (integer): Desired anion count

**Returns:** List of salt formula strings

**Example:**
```maxima
salts_2an: chem_sol_array_by_anion_count(2);
/* Returns ["PbCl2", "PbBr2", "PbI2", "PbF2", "CaF2", ..., "Zn(CN)2"] */

salts_3an: chem_sol_array_by_anion_count(3);
/* Returns ["Fe(OH)3", "Al(OH)3", "Cr(OH)3", "Bi2S3", "Ca3(PO4)2", ...] */
```

---

#### `chem_sol_array_by_total_ions(n)`

**Description:** Returns all salts producing a specific total number of ions per formula unit.

**Parameters:**
- `n` (integer): Desired total ion count (cation_count + anion_count)

**Returns:** List of salt formula strings

**Example:**
```maxima
salts_2: chem_sol_array_by_total_ions(2);
/* Returns all 1:1 salts: ["AgCl", "AgBr", "AgI", "AgF", "CuCl", ...] */

salts_3: chem_sol_array_by_total_ions(3);
/* Returns all 1:2 and 2:1 salts: ["PbCl2", "CaF2", "Ag2SO4", ...] */

salts_5: chem_sol_array_by_total_ions(5);
/* Returns ["Ca3(PO4)2", "Pb3(PO4)2", "Zn3(PO4)2", "Bi2S3"] */
```

---

#### `chem_sol_cation_array()`

**Description:** Returns all unique cations in the database.

**Returns:** List of unique cation formula strings

**Example:**
```maxima
cations: chem_sol_cation_array();
/* Returns ["Ag^+", "Cu^+", "Pb^{2+}", "Ca^{2+}", "Ba^{2+}", ...] */
```

---

#### `chem_sol_anion_array()`

**Description:** Returns all unique anions in the database.

**Returns:** List of unique anion formula strings

**Example:**
```maxima
anions: chem_sol_anion_array();
/* Returns ["Cl^-", "Br^-", "I^-", "F^-", "SO4^{2-}", "CO3^{2-}", ...] */
```

---

#### `chem_sol_array_sorted_Ksp()`

**Description:** Returns all salt names sorted by Ksp in ascending order (least soluble first).

**Returns:** List of salt formula strings

**Example:**
```maxima
sorted: chem_sol_array_sorted_Ksp();
/* Returns ["Bi2S3", "HgS", "Ag2S", "Cu2S", ...] (least soluble first) */
```

---

#### `chem_sol_array_Ksp_range(Ksp_min, Ksp_max)`

**Description:** Returns all salts with Ksp in a specified range [Ksp_min, Ksp_max].

**Parameters:**
- `Ksp_min` (number): Minimum Ksp value
- `Ksp_max` (number): Maximum Ksp value

**Returns:** List of salt formula strings

**Example:**
```maxima
/* Find moderately insoluble salts */
moderate: chem_sol_array_Ksp_range(1e-12, 1e-8);
/* Returns salts with Ksp between 1e-12 and 1e-8 */
```

---

### Dissolution Equation Functions

#### `chem_sol_dissolution_equation(salt)`

**Description:** Generates the dissolution equation as a LaTeX string with `\ce{...}` included, so the question text only needs `\({@...@}\)` without manual `\ce` wrapping.

**Parameters:**
- `salt` (string): Chemical formula of the salt

**Returns:** LaTeX string with `\ce{...}` wrapper, or `""` if not found

**Example:**
```maxima
eq: chem_sol_dissolution_equation("AgCl");
/* Returns "\\ce{AgCl -> Ag^+ + Cl^-}" */

eq: chem_sol_dissolution_equation("PbCl2");
/* Returns "\\ce{PbCl2 -> Pb^{2+} + 2 Cl^-}" */

eq: chem_sol_dissolution_equation("Ag2CrO4");
/* Returns "\\ce{Ag2CrO4 -> 2 Ag^+ + CrO4^{2-}}" */

eq: chem_sol_dissolution_equation("Ca3(PO4)2");
/* Returns "\\ce{Ca3(PO4)2 -> 3 Ca^{2+} + 2 PO4^{3-}}" */
```

**Usage in Question Text:**
```latex
\(\require{mhchem}\)
<p>\({@chem_sol_dissolution_equation(salt)@}\)</p>
```

**Note:** No manual `\ce{...}` wrapping needed — the function output already contains it.

---

### Available Salts

The solubility database contains the following salt categories:

**Halides:** AgCl, AgBr, AgI, AgF, CuCl, PbCl2, PbBr2, PbI2, PbF2, CaF2, BaF2, MgF2, SrF2, Hg2Cl2, Hg2Br2, Hg2I2, TlCl

**Sulfates:** BaSO4, CaSO4, SrSO4, PbSO4, Ag2SO4, Hg2SO4, RaSO4

**Carbonates:** CaCO3, BaCO3, SrCO3, MgCO3, MnCO3, FeCO3, CoCO3, NiCO3, CuCO3, ZnCO3, Ag2CO3, PbCO3, CdCO3

**Hydroxides:** Mg(OH)2, Ca(OH)2, Ba(OH)2, Sr(OH)2, Fe(OH)2, Fe(OH)3, Al(OH)3, Cu(OH)2, Zn(OH)2, Mn(OH)2, Ni(OH)2, Co(OH)2, Cr(OH)3, Pb(OH)2, Cd(OH)2, Sn(OH)2, AgOH

**Sulfides:** CuS, Cu2S, PbS, ZnS, CdS, FeS, NiS, CoS, MnS, Ag2S, HgS, Bi2S3, SnS

**Phosphates:** Ca3(PO4)2, Ag3PO4, FePO4, AlPO4, Pb3(PO4)2, Zn3(PO4)2

**Chromates:** BaCrO4, PbCrO4, Ag2CrO4, SrCrO4, CaCrO4

**Oxalates:** CaC2O4, BaC2O4, SrC2O4, MgC2O4, PbC2O4, Ag2C2O4, FeC2O4

**Iodates:** Ca(IO3)2, Ba(IO3)2, Sr(IO3)2, Pb(IO3)2, AgIO3

**Cyanides:** AgCN, Zn(CN)2, CuCN

**Thiocyanates:** AgSCN, CuSCN

**Miscellaneous:** BaSO3, Ag2S2O3, PbSO3, Ag2SO3

---

### Function Reference Table (Solubility)

| Function | Description | Example |
|----------|-------------|---------|
| `chem_sol_Ksp(salt)` | Get Ksp (computed from pKsp) | `chem_sol_Ksp("AgCl")` → `1.778e-10` |
| `chem_sol_pKsp(salt)` | Get pKsp | `chem_sol_pKsp("AgCl")` → `9.75` |
| `chem_sol_cation(salt)` | Get cation formula | `chem_sol_cation("CaF2")` → `"Ca^{2+}"` |
| `chem_sol_cation_count(salt)` | Get cation coefficient | `chem_sol_cation_count("Ag2SO4")` → `2` |
| `chem_sol_anion(salt)` | Get anion formula | `chem_sol_anion("BaSO4")` → `"SO4^{2-}"` |
| `chem_sol_anion_count(salt)` | Get anion coefficient | `chem_sol_anion_count("PbCl2")` → `2` |
| `chem_sol_ion_counts(salt)` | Get both counts | `chem_sol_ion_counts("Ag2CrO4")` → `[2, 1]` |
| `chem_sol_total_ion_count(salt)` | Get total ion count | `chem_sol_total_ion_count("PbCl2")` → `3` |
| `chem_sol_entry(salt)` | Get full entry | `chem_sol_entry("AgCl")` → `[...]` |
| `chem_sol_molar_solubility(salt)` | Calculate solubility (with units) | `chem_sol_molar_solubility("AgCl")` → `stackunits(1.33e-5, mol*l^(-1))` |
| `chem_sol_molar_solubility_common_ion(...)` | Solubility with common ion (with units) | See above |
| `chem_sol_ion_product(cc, ca, salt)` | Calculate Q | `chem_sol_ion_product(1e-3, 1e-3, "AgCl")` |
| `chem_sol_precipitation_check(cc, ca, salt)` | Check precipitation | Returns `"precipitates"` etc. |
| `chem_sol_max_concentration(c, salt, type)` | Max ion concentration | See above |
| `chem_sol_array()` | All salts | List of all salt names |
| `chem_sol_array_by_cation(cat)` | Salts by cation | `chem_sol_array_by_cation("Ag^+")` |
| `chem_sol_array_by_anion(an)` | Salts by anion | `chem_sol_array_by_anion("Cl^-")` |
| `chem_sol_array_by_cation_count(n)` | Salts by cation count | `chem_sol_array_by_cation_count(2)` |
| `chem_sol_array_by_anion_count(n)` | Salts by anion count | `chem_sol_array_by_anion_count(3)` |
| `chem_sol_array_by_total_ions(n)` | Salts by total ions | `chem_sol_array_by_total_ions(5)` |
| `chem_sol_cation_array()` | All unique cations | List of cation strings |
| `chem_sol_anion_array()` | All unique anions | List of anion strings |
| `chem_sol_array_sorted_Ksp()` | Salts sorted by Ksp | Ascending order |
| `chem_sol_array_Ksp_range(min, max)` | Salts in Ksp range | Filter by Ksp |
| `chem_sol_dissolution_equation(salt)` | Dissolution equation (with `\ce{}`) | `"\\ce{AgCl -> Ag^+ + Cl^-}"` |
| `chem_sol_Ksp_expression(salt)` | Ksp in brackets (with `\ce{}`) | `"[\\ce{Ag^+}] \\cdot [\\ce{Cl^-}]"` |
| `chem_sol_Ksp_activity_expression(salt)` | Full activity expr. (with `\ce{}`) | With `a(\\ce{solid})` denominator |
| `chem_sol_Ksp_activity_expression_simplified(salt)` | Simplified activity (with `\ce{}`) | Without denominator |
| `chem_sol_solubility_expression(salt)` | Solubility formula | `"s = \\sqrt{K_{\\mathrm{sp}}}"` for 1:1 salts |

---

## Thermodynamic Tables Module

The thermodynamic tables module provides access to standard thermodynamic data and functions for calculating reaction thermodynamics. Each substance in the database includes classification tags for flexible filtering.

### Database Structure

Each entry in the thermodynamic database contains:
- **Formula**: Chemical formula (string)
- **ΔHf°**: Standard enthalpy of formation (kJ/mol)
- **S°**: Standard molar entropy (J/(mol·K))
- **ΔGf°**: Standard Gibbs free energy of formation (kJ/mol)
- **Cp°**: Standard molar heat capacity (J/(mol·K))
- **State**: Physical state ("g", "l", "s", or "aq")
- **Tags**: List of classification tags (e.g., ["element", "metal", "inorganic"])

### Available Tags

The following standard tags are used for substance classification:

| Tag | Description |
|-----|-------------|
| `"element"` | Pure elements |
| `"ion"` | Ionic species |
| `"cation"` | Positively charged ions |
| `"anion"` | Negatively charged ions |
| `"molecule"` | Molecular compounds |
| `"salt"` | Ionic salts |
| `"oxide"` | Oxide compounds |
| `"hydroxide"` | Hydroxide compounds |
| `"halogenide"` | Halogen-containing compounds |
| `"chloride"` | Chloride compounds |
| `"bromide"` | Bromide compounds |
| `"iodide"` | Iodide compounds |
| `"fluoride"` | Fluoride compounds |
| `"sulfide"` | Sulfide compounds |
| `"sulfate"` | Sulfate compounds |
| `"carbonate"` | Carbonate compounds |
| `"nitrate"` | Nitrate compounds |
| `"phosphate"` | Phosphate compounds |
| `"acid"` | Acidic substances |
| `"base"` | Basic substances |
| `"organic"` | Organic compounds |
| `"inorganic"` | Inorganic compounds |
| `"hydrocarbon"` | Hydrocarbon compounds |
| `"alcohol"` | Alcohol compounds |
| `"carboxylic_acid"` | Carboxylic acids |
| `"aldehyde"` | Aldehyde compounds |
| `"ketone"` | Ketone compounds |
| `"sugar"` | Sugar compounds |
| `"amine"` | Amine compounds |
| `"metal"` | Metallic elements |
| `"nonmetal"` | Nonmetallic elements |
| `"hydrate"` | Hydrated compounds |

### Thermodynamic Data Retrieval Functions

#### `chem_thermo_data(substance, property, state)`

**Description:** Returns a specific thermodynamic property for a substance in a given state.

**Parameters:**
- `substance` (string): Chemical formula
- `property` (string): "DeltaHf" (ΔHf°), "S" (S°), "DeltaGf" (ΔGf°), "Cp" (Cp°), or "State"
- `state` (string): "g" (gas), "l" (liquid), "s" (solid), or "aq" (aqueous)

**Returns:** Property value or `false` if not found

**Example:**
```maxima
/* Get enthalpy of formation for liquid water */
delta_hf: chem_thermo_data("H2O", "DeltaHf", "l");  /* Returns -285.83 kJ/mol */

/* Get entropy for gaseous CO2 */
entropy: chem_thermo_data("CO2", "S", "g");  /* Returns 213.74 J/(mol·K) */

/* Get Gibbs free energy for solid NaCl */
delta_gf: chem_thermo_data("NaCl", "DeltaGf", "s");  /* Returns -384.14 kJ/mol */
```

---

#### `chem_thermo_data_units(substance, property, state)`

**Description:** Returns a thermodynamic property with appropriate units.

**Parameters:**
- `substance` (string): Chemical formula
- `property` (string): "DeltaHf", "S", "DeltaGf", "Cp", or "State"
- `state` (string): "g", "l", "s", or "aq"

**Returns:** Property value with units using `stackunits()`

**Example:**
```maxima
delta_hf: chem_thermo_data_units("CH4", "DeltaHf", "g");
/* Returns stackunits(-74.81, kJ*mol^(-1)) */

entropy: chem_thermo_data_units("H2O", "S", "l");
/* Returns stackunits(69.91, J*mol^(-1)*K^(-1)) */
```

---

#### `chem_thermo_data_all(substance, state)`

**Description:** Returns all thermodynamic data for a substance in a specific state as an association list.

**Parameters:**
- `substance` (string): Chemical formula
- `state` (string): "g", "l", "s", or "aq"

**Returns:** List of [property, value] pairs, or `false` if not found

**Example:**
```maxima
data: chem_thermo_data_all("H2O", "l");
/* Returns [["DeltaHf", -285.83], ["S", 69.91], ["DeltaGf", -237.13], 
            ["Cp", 75.29], ["State", "l"], ["Tags", ["molecule", "oxide", "inorganic"]]] */
```

---

#### `chem_thermo_data_all_any(substance)`

**Description:** Returns all thermodynamic data for a substance (first match if multiple states exist).

**Parameters:**
- `substance` (string): Chemical formula

**Returns:** List of [property, value] pairs, or `false` if not found

**Example:**
```maxima
data: chem_thermo_data_all_any("NaCl");
/* Returns data for the first matching entry (solid NaCl) */
```

---

#### `chem_thermo_states(substance)`

**Description:** Returns available states for a given substance.

**Parameters:**
- `substance` (string): Chemical formula

**Returns:** List of available states

**Example:**
```maxima
states: chem_thermo_states("H2O");
/* Returns ["l", "g"] */

states: chem_thermo_states("NaCl");
/* Returns ["s", "aq"] */
```

---

### Tag-Based Filtering Functions

#### `chem_thermo_has_tag(entry, tag)`

**Description:** Checks if a database entry has a specific tag.

**Parameters:**
- `entry` (list): A database entry from `%_THERMO_DATA`
- `tag` (string): Tag to check for

**Returns:** `true` if the tag is present, `false` otherwise

**Example:**
```maxima
/* Internal function, typically used by other filtering functions */
```

---

#### `chem_thermo_filter_by_tag(tag)`

**Description:** Returns all database entries that have a specific tag.

**Parameters:**
- `tag` (string): Tag to filter by

**Returns:** List of database entries (each entry is `["Formula", [data...]]`)

**Example:**
```maxima
salts: chem_thermo_filter_by_tag("salt");
/* Returns all entries tagged as "salt" */

metals: chem_thermo_filter_by_tag("metal");
/* Returns all entries tagged as "metal" */
```

---

#### `chem_thermo_filter_by_tags_all(tag_list)`

**Description:** Returns all entries that have ALL specified tags (AND logic).

**Parameters:**
- `tag_list` (list): List of tags that must all be present

**Returns:** List of database entries

**Example:**
```maxima
/* Find all organic acids */
organic_acids: chem_thermo_filter_by_tags_all(["organic", "acid"]);

/* Find all chloride salts */
chloride_salts: chem_thermo_filter_by_tags_all(["salt", "chloride"]);
```

---

#### `chem_thermo_filter_by_tags_any(tag_list)`

**Description:** Returns all entries that have ANY of the specified tags (OR logic).

**Parameters:**
- `tag_list` (list): List of tags where at least one must be present

**Returns:** List of database entries

**Example:**
```maxima
/* Find substances that are either acids or bases */
acid_or_base: chem_thermo_filter_by_tags_any(["acid", "base"]);

/* Find any halogenide */
halogenides: chem_thermo_filter_by_tags_any(["chloride", "bromide", "iodide", "fluoride"]);
```

---

#### `chem_thermo_substances_by_tag(tag)`

**Description:** Returns a list of unique substance formulas with a specific tag.

**Parameters:**
- `tag` (string): Tag to filter by

**Returns:** List of chemical formula strings (unique)

**Example:**
```maxima
salts: chem_thermo_substances_by_tag("salt");
/* Returns ["AlCl3", "BaCO3", "CaCO3", "CaF2", "CaCl2", ...] */

oxides: chem_thermo_substances_by_tag("oxide");
/* Returns ["Al2O3", "BaO", "B2O3", "CO", "CO2", ...] */

hydrocarbons: chem_thermo_substances_by_tag("hydrocarbon");
/* Returns ["CH4", "C2H6", "C2H4", "C2H2", "C3H6", ...] */
```

---

#### `chem_thermo_substances_by_tags_all(tag_list)`

**Description:** Returns unique substance formulas with ALL specified tags.

**Parameters:**
- `tag_list` (list): List of tags that must all be present

**Returns:** List of chemical formula strings (unique)

**Example:**
```maxima
/* Find all organic alcohols */
alcohols: chem_thermo_substances_by_tags_all(["organic", "alcohol"]);
/* Returns ["CH3OH", "C2H5OH", "C6H5OH"] */

/* Find all inorganic chloride salts */
chlorides: chem_thermo_substances_by_tags_all(["salt", "chloride", "inorganic"]);
/* Returns ["AlCl3", "CaCl2", "KCl", "NaCl", ...] */
```

---

#### `chem_thermo_substances_by_tags_any(tag_list)`

**Description:** Returns unique substance formulas with ANY of the specified tags.

**Parameters:**
- `tag_list` (list): List of tags where at least one must be present

**Returns:** List of chemical formula strings (unique)

**Example:**
```maxima
/* Find all aldehydes or ketones */
carbonyl: chem_thermo_substances_by_tags_any(["aldehyde", "ketone"]);
/* Returns ["HCHO", "CH3CHO", "CH3COCH3"] */
```

---

#### `chem_thermo_get_tags(substance)`

**Description:** Returns all tags for a substance (first match if multiple states exist).

**Parameters:**
- `substance` (string): Chemical formula

**Returns:** List of tag strings, or `false` if not found

**Example:**
```maxima
tags: chem_thermo_get_tags("NaCl");
/* Returns ["salt", "halogenide", "chloride", "inorganic"] */

tags: chem_thermo_get_tags("CH3COOH");
/* Returns ["organic", "carboxylic_acid", "acid", "molecule"] */

tags: chem_thermo_get_tags("Fe");
/* Returns ["element", "metal", "inorganic"] */
```

---

#### `chem_thermo_get_tags_state(substance, state)`

**Description:** Returns all tags for a substance in a specific state.

**Parameters:**
- `substance` (string): Chemical formula
- `state` (string): "g", "l", "s", or "aq"

**Returns:** List of tag strings, or `false` if not found

**Example:**
```maxima
tags: chem_thermo_get_tags_state("H2O", "l");
/* Returns ["molecule", "oxide", "inorganic"] */

tags: chem_thermo_get_tags_state("NaCl", "aq");
/* Returns ["salt", "halogenide", "chloride", "inorganic"] */
```

---

#### `chem_thermo_random_by_tags_all(tag_list)`

**Description:** Returns a random substance formula that has ALL specified tags.

**Parameters:**
- `tag_list` (list): List of tags that must all be present

**Returns:** Chemical formula string, or `false` if no matches

**Example:**
```maxima
/* Get a random organic molecule */
random_organic: chem_thermo_random_by_tags_all(["organic", "molecule"]);

/* Get a random inorganic salt */
random_salt: chem_thermo_random_by_tags_all(["salt", "inorganic"]);

/* Get a random metal element */
random_metal: chem_thermo_random_by_tags_all(["element", "metal"]);
```

---

#### `chem_thermo_data_by_tag(tag)`

**Description:** Returns full data for all substances filtered by tag.

**Parameters:**
- `tag` (string): Tag to filter by

**Returns:** List of `[formula, [[property, value], ...]]` pairs

**Example:**
```maxima
acid_data: chem_thermo_data_by_tag("acid");
/* Returns [["HBr", [["DeltaHf", -36.40], ["S", 198.70], ...]], 
            ["HCl", [["DeltaHf", -92.31], ...]], ...] */
```

---

#### `chem_thermo_data_by_tag_state(tag, state)`

**Description:** Returns full data for substances filtered by both tag and state.

**Parameters:**
- `tag` (string): Tag to filter by
- `state` (string): "g", "l", "s", or "aq"

**Returns:** List of `[formula, [[property, value], ...]]` pairs

**Example:**
```maxima
/* Get all gaseous hydrocarbons with their data */
gas_hydrocarbons: chem_thermo_data_by_tag_state("hydrocarbon", "g");

/* Get all aqueous ions with their data */
aq_ions: chem_thermo_data_by_tag_state("ion", "aq");
```

---

### Thermodynamic Navigation Functions

#### `chem_thermo_substance_array()`

**Description:** Returns an array of all unique substance formulas in the database.

**Returns:** List of chemical formula strings

**Example:**
```maxima
all_substances: chem_thermo_substance_array();
/* Returns ["Al", "Al^{3+}", "Al2O3", "Al(OH)3", ...] */

/* Select a random substance */
substance: rand(chem_thermo_substance_array());
```

---

#### `chem_thermo_substance_state_array(state)`

**Description:** Returns an array of all unique substance formulas in a specific state.

**Parameters:**
- `state` (string): "g", "l", "s", or "aq"

**Returns:** List of chemical formula strings

**Example:**
```maxima
gases: chem_thermo_substance_state_array("g");
/* Returns all gaseous substances */

aqueous: chem_thermo_substance_state_array("aq");
/* Returns all aqueous species */
```

---

### Thermodynamic Calculation Functions

#### `chem_reaction_enthalpy(products_list, reactants_list)`

**Description:** Calculates standard reaction enthalpy: ΔH° = Σ(ΔHf°products) − Σ(ΔHf°reactants)

**Parameters:**
- `products_list` (list): List of `[["substance", "state", coefficient], ...]`
- `reactants_list` (list): List of `[["substance", "state", coefficient], ...]`

**Returns:** Reaction enthalpy in kJ/mol (without units)

**Example:**
```maxima
/* Calculate ΔH° for: CH4(g) + 2O2(g) → CO2(g) + 2H2O(l) */
reactants: [["CH4", "g", 1], ["O2", "g", 2]];
products: [["CO2", "g", 1], ["H2O", "l", 2]];
delta_h: chem_reaction_enthalpy(products, reactants);
/* Returns -890.4 kJ/mol */
```

---

#### `chem_reaction_entropy(products_list, reactants_list)`

**Description:** Calculates standard reaction entropy: ΔS° = Σ(S°products) − Σ(S°reactants)

**Returns:** Reaction entropy in J/(mol·K) (without units)

---

#### `chem_reaction_gibbs(products_list, reactants_list)`

**Description:** Calculates standard reaction Gibbs free energy: ΔG° = Σ(ΔGf°products) − Σ(ΔGf°reactants)

**Returns:** Reaction Gibbs free energy with units (kJ/mol)

---

#### `chem_reaction_enthalpy_by_name(reaction_name)`

**Description:** Calculates ΔH° for a reaction by name (requires `reactions.mac`).

---

#### `chem_reaction_entropy_by_name(reaction_name)`

**Description:** Calculates ΔS° for a reaction by name (requires `reactions.mac`).

---

#### `chem_reaction_gibbs_by_name(reaction_name)`

**Description:** Calculates ΔG° for a reaction by name (requires `reactions.mac`).

---

#### `chem_gibbs_from_enthalpy_entropy(delta_h, delta_s, temp)`

**Description:** Calculates ΔG from ΔH and ΔS: ΔG = ΔH − TΔS

**Parameters:**
- `delta_h` (number): Enthalpy in kJ/mol
- `delta_s` (number): Entropy in J/(mol·K)
- `temp` (number): Temperature in K

**Returns:** Gibbs free energy with units (kJ/mol)

---

#### `chem_equilibrium_constant(delta_g, temp)`

**Description:** Calculates equilibrium constant from ΔG°: K = exp(−ΔG°/RT)

**Parameters:**
- `delta_g` (number): Gibbs free energy in kJ/mol
- `temp` (number): Temperature in K

**Returns:** Equilibrium constant K

---

### Function Reference Table (Thermodynamics)

| Function | Description | Example |
|----------|-------------|---------|
| `chem_thermo_data(sub, prop, state)` | Get specific property | `chem_thermo_data("H2O", "DeltaHf", "l")` → `-285.83` |
| `chem_thermo_data_units(sub, prop, state)` | Get property with units | `chem_thermo_data_units("H2O", "S", "l")` |
| `chem_thermo_data_all(sub, state)` | Get all data for substance/state | `chem_thermo_data_all("NaCl", "s")` |
| `chem_thermo_data_all_any(sub)` | Get all data (first match) | `chem_thermo_data_all_any("H2O")` |
| `chem_thermo_states(sub)` | Get available states | `chem_thermo_states("H2O")` → `["l", "g"]` |
| `chem_thermo_substance_array()` | All substances | List of all formulas |
| `chem_thermo_substance_state_array(state)` | Substances by state | `chem_thermo_substance_state_array("g")` |
| `chem_thermo_filter_by_tag(tag)` | Filter entries by tag | `chem_thermo_filter_by_tag("salt")` |
| `chem_thermo_filter_by_tags_all(tags)` | Filter by ALL tags | `chem_thermo_filter_by_tags_all(["organic", "acid"])` |
| `chem_thermo_filter_by_tags_any(tags)` | Filter by ANY tag | `chem_thermo_filter_by_tags_any(["acid", "base"])` |
| `chem_thermo_substances_by_tag(tag)` | Formulas by tag | `chem_thermo_substances_by_tag("oxide")` |
| `chem_thermo_substances_by_tags_all(tags)` | Formulas with ALL tags | `chem_thermo_substances_by_tags_all(["salt", "chloride"])` |
| `chem_thermo_substances_by_tags_any(tags)` | Formulas with ANY tag | `chem_thermo_substances_by_tags_any(["aldehyde", "ketone"])` |
| `chem_thermo_get_tags(sub)` | Get tags for substance | `chem_thermo_get_tags("NaCl")` → `["salt", ...]` |
| `chem_thermo_get_tags_state(sub, state)` | Get tags for substance/state | `chem_thermo_get_tags_state("H2O", "l")` |
| `chem_thermo_random_by_tags_all(tags)` | Random substance with tags | `chem_thermo_random_by_tags_all(["organic"])` |
| `chem_thermo_data_by_tag(tag)` | Full data by tag | `chem_thermo_data_by_tag("acid")` |
| `chem_thermo_data_by_tag_state(tag, state)` | Full data by tag and state | `chem_thermo_data_by_tag_state("ion", "aq")` |
| `chem_reaction_enthalpy(prod, react)` | Calculate ΔH° | See examples above |
| `chem_reaction_entropy(prod, react)` | Calculate ΔS° | See examples above |
| `chem_reaction_gibbs(prod, react)` | Calculate ΔG° | See examples above |
| `chem_gibbs_from_enthalpy_entropy(h, s, T)` | ΔG from ΔH, ΔS | `chem_gibbs_from_enthalpy_entropy(-890, -242, 298)` |
| `chem_equilibrium_constant(g, T)` | K from ΔG° | `chem_equilibrium_constant(-50, 298)` |

### Available Substances

The thermodynamic database includes:
- **Elements**: H2, O2, N2, Cl2, Br2, I2, C (graphite/diamond), S (rhombic), Al, Fe, Cu, Zn, Ag, Na, K, Ca, Mg, etc.
- **Simple Inorganics**: H2O (l, g), CO2, CO, NH3, NO, NO2, N2O, SO2, SO3, H2S, HCN
- **Acids**: HCl, HBr, HI, HF, HNO3, H2SO4, H3PO4, CH3COOH, HCOOH
- **Aqueous Ions**: H+, OH-, Cl-, Br-, I-, F-, Na+, K+, Ca²⁺, Mg²⁺, Fe²⁺, Fe³⁺, Cu²⁺, Ag+, SO₄²⁻, NO₃⁻, CO₃²⁻, NH₄⁺
- **Salts**: NaCl, KCl, CaCl2, MgCl2, AgCl, NaBr, KBr, NaI, CaCO3, MgCO3, Na2SO4, CaSO4, NH4Cl, NH4NO3
- **Oxides**: CaO, MgO, Al2O3, Fe2O3, Fe3O4, FeO, CuO, Cu2O, ZnO, BaO, SiO2
- **Hydroxides**: NaOH, KOH, Ca(OH)2, Mg(OH)2, Al(OH)3, Fe(OH)3
- **Organic Hydrocarbons**: CH4, C2H6, C3H8, C4H10, C5H12, C2H4, C2H2, C3H6, C6H6, C7H8, C8H18
- **Alcohols**: CH3OH, C2H5OH, C6H5OH
- **Carboxylic Acids**: HCOOH, CH3COOH, C6H5COOH
- **Aldehydes/Ketones**: HCHO, CH3CHO, CH3COCH3
- **Sugars**: C6H12O6 (glucose, fructose), C12H22O11 (sucrose)
- **Amines**: CH3NH2, C6H5NH2, NH2CH2COOH (glycine), CO(NH2)2 (urea)

---

## Chemical Reactions Module

The reactions module provides a database of common chemical reactions with complete stoichiometry.

### Reaction Data Retrieval Functions

#### `chem_reaction_data(reaction_name)`

**Description:** Returns complete reaction data for a given reaction.

**Parameters:**
- `reaction_name` (string): Name of the reaction

**Returns:** [reactants_list, products_list] or `false` if not found

**Example:**
```maxima
rxn: chem_reaction_data("CombustionMethane");
/* Returns [[["CH4", "g", 1], ["O2", "g", 2]], [["CO2", "g", 1], ["H2O", "l", 2]]] */
```

---

#### `chem_reaction_reactants(reaction_name)`

**Description:** Returns the reactants for a given reaction.

---

#### `chem_reaction_products(reaction_name)`

**Description:** Returns the products for a given reaction.

---

#### `chem_reaction_equation(reaction_name)`

**Description:** Returns a LaTeX-formatted balanced equation using `\ce{...}`, so the question text only needs `\({@...@}\)` without manual `\ce` wrapping.

**Parameters:**
- `reaction_name` (string): Name of the reaction

**Returns:** LaTeX string with `\ce{...}` wrapper, or `false` if not found

**Example:**
```maxima
eqn: chem_reaction_equation("CombustionMethane");
/* Returns "\\ce{CH4(g) + 2 O2(g) -> CO2(g) + 2 H2O(l)}" */
```

**Usage in Question Text:**
```latex
\(\require{mhchem}\)
<p>\({@chem_reaction_equation("CombustionMethane")@}\)</p>
```

**Note:** No manual `\ce{...}` wrapping needed — the function output already contains it.

---

#### `chem_reaction_array()`

**Description:** Returns an array of all reaction names.

---

#### `chem_reaction_combustion_array()`

**Description:** Returns an array of combustion reaction names.

---

#### `chem_reaction_formation_array()`

**Description:** Returns an array of formation reaction names.

---

#### `chem_reaction_synthesis_array()`

**Description:** Returns an array of synthesis reaction names.

---

#### `chem_reaction_decomposition_array()`

**Description:** Returns an array of decomposition reaction names.

---

### Available Reactions

**Combustion:** CombustionMethane, CombustionEthane, CombustionPropane, CombustionGlucose, CombustionEthanol

**Synthesis:** SynthesisAmmonia, SynthesisWater, SynthesisSO3

**Decomposition:** DecompositionCaCO3, DecompositionH2O

**Formation:** FormationCO2, FormationH2O_l, FormationH2O_g, FormationNH3, FormationCH4

**Neutralization:** NeutralizationHClNaOH, NeutralizationH2SO4NaOH

**Other:** PrecipitationAgCl, OxidationIron, VaporizationWater, FermentationGlucose, PhotosynthesisSimplified

---

## Nuclide Database Module

The nuclide database module provides comprehensive nuclear data from the NNDC NuDat database, including information about radioactive decay, half-lives, and nuclear properties.

### Data Structure

The nuclide database contains the following information for each nuclide:
- **Nuclide ID**: String identifier (e.g., "^{185}Tl")
- **Z**: Atomic number (number of protons)
- **N**: Neutron number
- **Level Energies**: Array of excited state energies in MeV
- **Half-lives**: Array of half-life values
- **Half-life Units**: Array of units
- **Decay Modes**: Nested array of decay modes for each level
- **Branching Ratios**: Nested array of branching ratios (percentages)

### Core Data Retrieval Functions

#### `nucl_data_all(nuclide_id)`
Returns all nuclear data for a given nuclide.

```maxima
nucl_data_all("^{14}C");
/* Returns: [6, 8, [0], [5686], ["y"], [["B-"]], [[100]]] */
```

#### `nucl_data_Z(nuclide_id)`
Returns the atomic number (Z).

#### `nucl_data_N(nuclide_id)`
Returns the neutron number.

#### `nucl_mass_number(nuclide_id)`
Returns the mass number (A = Z + N).

### Decay Information Functions

#### `nucl_halflife(nuclide_id)`
Returns the half-life of the ground state with units.

```maxima
nucl_halflife("^{14}C");     /* Returns: stackunits(5686, "y") */
nucl_halflife("^{210}Po");   /* Returns: stackunits(138.378, "d") */
```

#### `nucl_decay_modes(nuclide_id)`
Returns the decay modes for the ground state.

```maxima
nucl_decay_modes("^{14}C");      /* Returns: ["B-"] */
nucl_decay_modes("^{40}K");      /* Returns: ["B-", "B+"] */
```

#### `nucl_branching_ratios(nuclide_id)`
Returns the branching ratios (in percent) for ground state decay modes.

### Navigation and Filtering Functions

#### `nucl_array()`
Returns an array of all nuclide IDs.

#### `nucl_array_radioactive()`
Returns all radioactive nuclide IDs.

#### `nucl_array_alpha()`
Returns nuclide IDs with pure alpha decay (100%).

#### `nucl_array_betaminus()`
Returns nuclide IDs with pure beta-minus decay.

#### `nucl_array_betaplus()`
Returns nuclide IDs with pure beta-plus decay.

#### `nucl_array_ec()`
Returns nuclide IDs with pure electron capture.

### Utility Functions

#### `nucl_display(nuclide_id)`
Formats a nuclide name for LaTeX display.

```maxima
nucl_display("^{14}C");  /* Returns: "\\ce{^{14}C}" */
```

### Decay Mode Notation

- **A**: Alpha decay (α)
- **B-**: Beta-minus decay (β⁻)
- **B+**: Beta-plus decay (β⁺)
- **EC**: Electron capture
- **IT**: Isomeric transition
- **SF**: Spontaneous fission
- **N**: Neutron emission
- **P**: Proton emission
- **2B-**: Double beta decay
- **B-N**: Beta-delayed neutron emission

### Practical Examples

```maxima
/* Carbon Dating */
halflife_C14: nucl_halflife("^{14}C");
decay_mode: nucl_decay_modes("^{14}C");

/* Random radioactive isotope */
random_isotope: rand(nucl_array_radioactive());
isotope_display: nucl_display(random_isotope);
```

---

## Usage Examples

### Example 1: Random Element Properties
```maxima
element: rand(chem_element_array());
name: chem_data(element, "Name");
z: chem_data(element, "AtomicNumber");
mass: chem_data_units(element, "AtomicMass");
config: chem_electron_config(element);
```

### Example 2: Molar Mass Calculation
```maxima
mass_h2o: chem_molar_mass("H2O");
mass_h2so4: chem_molar_mass("H2SO4");
mass_nacl: chem_molar_mass("NaCl");
```

### Example 3: Acid-Base Pair Problem
```maxima
acid: rand(chem_weak_acid_array());
pka: chem_acidbase_pKa(acid);
ka: chem_acidbase_Ka(acid);
base: chem_acidbase_conjugate_base(acid);
pkb: chem_acidbase_pKb(base);
acid_display: chem_display(acid);
base_display: chem_display(base);
```

```latex
\(\require{mhchem}\)
<p>The acid {@acid_display@} (pKa = {@pka@}) has conjugate base {@base_display@}.</p>
<p>\( K_a = {@chem_acidbase_Ka_expression(acid)@} \)</p>
```

### Example 4: Polyprotic Acid Titration
```maxima
acid: "H3PO4";
pka_list: chem_acidbase_pKa_list(acid);
jsxcode: chem_jsxgraph_titration(acid, 0.1, 0.1, 25, 200, 100);
```

```html
[[jsxgraph width="500px" height="400px"]]
{#jsxcode#}
[[/jsxgraph]]
```

### Example 5: Solubility Problem
```maxima
salt: rand(chem_sol_array_by_anion("Cl^-"));
ksp: chem_sol_Ksp(salt);
s: chem_sol_molar_solubility(salt);
eq: chem_sol_dissolution_equation(salt);
expr: chem_sol_Ksp_expression(salt);
salt_display: chem_display(salt);
```

```latex
\(\require{mhchem}\)
<p>Consider the salt {@salt_display@}.</p>
<p>Dissolution: \({@eq@}\)</p>
<p>\( K_{\mathrm{sp}} = {@expr@} = {@ksp@} \)</p>
<p>The molar solubility is {@s@} mol/L.</p>
```

### Example 6: Precipitation Check
```maxima
salt: "AgCl";
c_ag: 0.001;
c_cl: 0.001;
Q: chem_sol_ion_product(c_ag, c_cl, salt);
ksp: chem_sol_Ksp(salt);
result: chem_sol_precipitation_check(c_ag, c_cl, salt);
```

### Example 7: Common-Ion Effect
```maxima
salt: "CaF2";
s_pure: chem_sol_molar_solubility(salt);
s_common: chem_sol_molar_solubility_common_ion(salt, 0.1, "anion");
/* s_common << s_pure due to F⁻ already in solution */
```

### Example 8: Thermodynamic Calculation for Random Combustion
```maxima
rxn: rand(chem_reaction_combustion_array());
equation: chem_reaction_equation(rxn);
delta_h: chem_reaction_enthalpy_by_name(rxn);
delta_s: chem_reaction_entropy_by_name(rxn);
delta_g: chem_reaction_gibbs_by_name(rxn);
```

### Example 9: Temperature-Dependent Gibbs Energy
```maxima
rxn: "SynthesisAmmonia";
delta_h: chem_reaction_enthalpy_by_name(rxn);
delta_s: chem_reaction_entropy_by_name(rxn);
delta_g_298: chem_gibbs_from_enthalpy_entropy(delta_h, delta_s, 298);
delta_g_500: chem_gibbs_from_enthalpy_entropy(delta_h, delta_s, 500);
k_298: chem_equilibrium_constant(delta_g_298, 298);
k_500: chem_equilibrium_constant(delta_g_500, 500);
```

### Example 10: Nuclear Decay Problem
```maxima
isotope: rand(nucl_array_alpha());
hl: nucl_halflife(isotope);
dm: nucl_decay_modes(isotope);
br: nucl_branching_ratios(isotope);
disp: nucl_display(isotope);
```

```latex
\(\require{mhchem}\)
<p>The isotope {@disp@} has a half-life of {@hl@} and decays via {@dm@}.</p>
```
