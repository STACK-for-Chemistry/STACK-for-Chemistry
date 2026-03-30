/* Explanation of variables and functions used
   - all_reactions: list of all reaction names via chem_reaction_array()
   - rxn: a randomly selected reaction name
   - rxn_data: full raw entry via chem_reaction_data(rxn)
   - rxn_reactants: reactants list via chem_reaction_reactants(rxn)
   - rxn_products: products list via chem_reaction_products(rxn)
   - rxn_eq: LaTeX equation string via chem_reaction_equation(rxn)

   Navigation / filter arrays:
   - combustion_rxns: via chem_reaction_combustion_array()
   - formation_rxns: via chem_reaction_formation_array()
   - synthesis_rxns: via chem_reaction_synthesis_array()
   - decomp_rxns: via chem_reaction_decomposition_array()

   Species-count filter:
   - rxns_2r_1p: reactions with 2 reactants and 1 product via chem_reaction_filter_by_species(2,1)
   - rxns_1r_2p: reactions with 1 reactant and 2 products via chem_reaction_filter_by_species(1,2)
   - rxns_2r_2p: reactions with 2 reactants and 2 products via chem_reaction_filter_by_species(2,2)
   - rxns_1r_1p: reactions with 1 reactant and 1 product via chem_reaction_filter_by_species(1,1)

   Known-reaction cross-checks (fixed names, not random):
   - eq_synthesis_water: equation for SynthesisWater (2 H2 + O2 -> 2 H2O)
   - eq_combustion_methane: equation for CombustionMethane
   - eq_decomp_caco3: equation for DecompositionCaCO3
   - n_reactants_synth: number of reactants in SynthesisWater (expect 2)
   - n_products_synth: number of products in SynthesisWater (expect 1)
   - synth_water_in_2r1p: whether SynthesisWater appears in rxns_2r_1p

   Functions exercised from reactions.mac:
   - chem_reaction_array()
   - chem_reaction_data()
   - chem_reaction_reactants()
   - chem_reaction_products()
   - chem_reaction_equation()
   - chem_reaction_combustion_array()
   - chem_reaction_formation_array()
   - chem_reaction_synthesis_array()
   - chem_reaction_decomposition_array()
   - chem_reaction_filter_by_species()
*/

---

## Question variables (paste into STACK "Question variables" field):

```
stack_include("https://raw.githubusercontent.com/AlexVCS25/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/reactions.mac");

/* --- All reactions --- */
all_reactions: chem_reaction_array();

/* --- Pick a random reaction --- */
rxn: rand(all_reactions);

/* --- Core accessors on the random reaction --- */
rxn_data:      chem_reaction_data(rxn);
rxn_reactants: chem_reaction_reactants(rxn);
rxn_products:  chem_reaction_products(rxn);
rxn_eq:        chem_reaction_equation(rxn);

/* --- Navigation arrays --- */
combustion_rxns: chem_reaction_combustion_array();
formation_rxns:  chem_reaction_formation_array();
synthesis_rxns:  chem_reaction_synthesis_array();
decomp_rxns:     chem_reaction_decomposition_array();

/* --- Species-count filter --- */
rxns_2r_1p: chem_reaction_filter_by_species(2, 1);
rxns_1r_2p: chem_reaction_filter_by_species(1, 2);
rxns_2r_2p: chem_reaction_filter_by_species(2, 2);
rxns_1r_1p: chem_reaction_filter_by_species(1, 1);

/* --- Known-reaction cross-checks --- */
eq_synthesis_water:    chem_reaction_equation("SynthesisWater");
eq_combustion_methane: chem_reaction_equation("CombustionMethane");
eq_decomp_caco3:       chem_reaction_equation("DecompositionCaCO3");

n_reactants_synth: length(chem_reaction_reactants("SynthesisWater"));
n_products_synth:  length(chem_reaction_products("SynthesisWater"));

synth_water_in_2r1p: member("SynthesisWater", rxns_2r_1p);

/* Dummy answer */
ta1: 10;
```

---

## Question text (paste into STACK "Question text" field):

```
\(\require{mhchem}\)

This page checks every function in reactions.mac. All values are computed automatically — no student input is needed beyond the dummy answer at the bottom.

--- chem_reaction_array() ---

Total reactions in the database: {@length(all_reactions)@}

--- Random reaction: {@rxn@} ---

Raw data entry: {@rxn_data@}

Reactants list: {@rxn_reactants@}

Products list: {@rxn_products@}

Formatted equation: \({@rxn_eq@}\)

--- Navigation arrays ---

Combustion reactions: {@combustion_rxns@}

Formation reactions: {@formation_rxns@}

Synthesis reactions: {@synthesis_rxns@}

Decomposition reactions: {@decomp_rxns@}

--- chem_reaction_filter_by_species ---

Reactions with 2 reactants and 1 product: {@rxns_2r_1p@}

Reactions with 1 reactant and 2 products: {@rxns_1r_2p@}

Reactions with 2 reactants and 2 products: {@rxns_2r_2p@}

Reactions with 1 reactant and 1 product: {@rxns_1r_1p@}

--- Known-reaction cross-checks ---

SynthesisWater equation (expect 2 H2 + O2 -> 2 H2O): \({@eq_synthesis_water@}\)

Number of reactant species in SynthesisWater (expect 2): {@n_reactants_synth@}

Number of product species in SynthesisWater (expect 1): {@n_products_synth@}

SynthesisWater appears in the 2-reactant / 1-product list (expect true): {@synth_water_in_2r1p@}

CombustionMethane equation (expect CH4 + 2 O2 -> CO2 + 2 H2O): \({@eq_combustion_methane@}\)

DecompositionCaCO3 equation (expect CaCO3 -> CaO + CO2): \({@eq_decomp_caco3@}\)

--- Dummy answer (ignore) ---

[[input:ans1]] [[validation:ans1]]
```
