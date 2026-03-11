/* Explanation of variables and functions used
   - all_salts: list of all salt strings from chem_sol_array()
   - salt: a randomly selected salt
   - salt_display: chem_display(salt)

   - Ksp: solubility product via chem_sol_Ksp(salt)
   - pKsp: pKsp via chem_sol_pKsp(salt)
   - cation: cation string via chem_sol_cation(salt)
   - cation_count: stoichiometric coefficient of cation via chem_sol_cation_count(salt)
   - anion: anion string via chem_sol_anion(salt)
   - anion_count: stoichiometric coefficient of anion via chem_sol_anion_count(salt)
   - ion_counts: [cation_count, anion_count] via chem_sol_ion_counts(salt)
   - full_entry: [salt, Ksp, pKsp, cation, n_cat, anion, n_an] via chem_sol_entry(salt)

   - s_molar: molar solubility via chem_sol_molar_solubility(salt)

   - salt2: a second random salt for common-ion test
   - s_common: molar solubility with common-ion effect via chem_sol_molar_solubility_common_ion()

   - diss_eq: dissolution equation string via chem_sol_dissolution_equation(salt)
   - Ksp_expr: Ksp bracket expression via chem_sol_Ksp_expression(salt)
   - Ksp_act: Ksp activity expression (full) via chem_sol_Ksp_activity_expression(salt)
   - Ksp_act_s: Ksp activity expression (simplified) via chem_sol_Ksp_activity_expression_simplified(salt)
   - sol_expr: solubility expression via chem_sol_solubility_expression(salt)

   - Q_test: ion product via chem_sol_ion_product()
   - precip_check: precipitation check result via chem_sol_precipitation_check()
   - c_max: max concentration via chem_sol_max_concentration()

   - salts_by_cation: list of salts sharing a cation via chem_sol_array_by_cation()
   - salts_by_anion: list of salts sharing an anion via chem_sol_array_by_anion()
   - all_cations: unique cation list via chem_sol_cation_array()
   - all_anions: unique anion list via chem_sol_anion_array()
   - sorted_salts: salts sorted by Ksp ascending via chem_sol_array_sorted_Ksp()
   - range_salts: salts with Ksp in a given range via chem_sol_array_Ksp_range()

   - salts_1cat: salts with 1 cation via chem_sol_array_by_cation_count(1)
   - salts_2cat: salts with 2 cations via chem_sol_array_by_cation_count(2)
   - salts_3cat: salts with 3 cations via chem_sol_array_by_cation_count(3)
   - salts_1an: salts with 1 anion via chem_sol_array_by_anion_count(1)
   - salts_2an: salts with 2 anions via chem_sol_array_by_anion_count(2)
   - salts_3an: salts with 3 anions via chem_sol_array_by_anion_count(3)
   - salts_2ions: salts producing 2 total ions via chem_sol_array_by_total_ions(2)
   - salts_3ions: salts producing 3 total ions via chem_sol_array_by_total_ions(3)
   - salts_5ions: salts producing 5 total ions via chem_sol_array_by_total_ions(5)
   - total_ions: total ion count for a salt via chem_sol_total_ion_count(salt)

   Display variables:
   - salt_display, salt2_display, cation_display, anion_display

   Functions exercised from solubility.mac and pse.mac:
   - chem_sol_array(), chem_sol_Ksp(), chem_sol_pKsp()
   - chem_sol_cation(), chem_sol_cation_count(), chem_sol_anion(), chem_sol_anion_count()
   - chem_sol_ion_counts(), chem_sol_entry()
   - chem_sol_molar_solubility(), chem_sol_molar_solubility_common_ion()
   - chem_sol_dissolution_equation()
   - chem_sol_Ksp_expression(), chem_sol_Ksp_activity_expression(), chem_sol_Ksp_activity_expression_simplified()
   - chem_sol_ion_product(), chem_sol_precipitation_check(), chem_sol_max_concentration()
   - chem_sol_array_by_cation(), chem_sol_array_by_anion()
   - chem_sol_cation_array(), chem_sol_anion_array()
   - chem_sol_array_sorted_Ksp(), chem_sol_array_Ksp_range()
   - chem_sol_array_by_cation_count(), chem_sol_array_by_anion_count(), chem_sol_array_by_total_ions()
   - chem_sol_total_ion_count()
   - chem_molar_mass() (from pse.mac)
   - chem_display()
*/

---

## Question variables (paste into STACK "Question variables" field):

```
stack_include("https://raw.githubusercontent.com/AlexVCS25/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/pse.mac");
stack_include("https://raw.githubusercontent.com/AlexVCS25/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/solubility.mac");

stack_unit_si_declare(true);
stackfltfmt:"~f";

/* Pick a random salt */
all_salts: chem_sol_array();
salt: rand(all_salts);

/* Basic accessors */
Ksp: chem_sol_Ksp(salt);
pKsp: chem_sol_pKsp(salt);
cation: chem_sol_cation(salt);
cation_count: chem_sol_cation_count(salt);
anion: chem_sol_anion(salt);
anion_count: chem_sol_anion_count(salt);
ion_counts: chem_sol_ion_counts(salt);
full_entry: chem_sol_entry(salt);

/* Molar solubility */
s_molar: chem_sol_molar_solubility(salt);

/* Second salt for common-ion test */
salts_by_cation: chem_sol_array_by_cation(cation);
salt2: if is(length(salts_by_cation) > 1) then rand(delete(salt, salts_by_cation)) else salt;
s_common: chem_sol_molar_solubility_common_ion(salt, 0.01, "cation");

/* Dissolution equation and Ksp expressions */
diss_eq: chem_sol_dissolution_equation(salt);
Ksp_expr: chem_sol_Ksp_expression(salt);
Ksp_act: chem_sol_Ksp_activity_expression(salt);
Ksp_act_s: chem_sol_Ksp_activity_expression_simplified(salt);
sol_expr: chem_sol_solubility_expression(salt);

/* Precipitation check (use arbitrary concentrations) */
Q_test: chem_sol_ion_product(0.001, 0.001, salt);
precip_check: chem_sol_precipitation_check(0.001, 0.001, salt);
c_max: chem_sol_max_concentration(0.01, salt, "cation");

/* Navigation / filtering */
salts_by_anion: chem_sol_array_by_anion(anion);
all_cations: chem_sol_cation_array();
all_anions: chem_sol_anion_array();
sorted_salts: chem_sol_array_sorted_Ksp();
sorted_salts_5: makelist(sorted_salts[i], i, 1, min(5, length(sorted_salts)));
range_salts: chem_sol_array_Ksp_range(1.0e-12, 1.0e-6);

/* Ion count navigation */
salts_1cat: chem_sol_array_by_cation_count(1);
salts_2cat: chem_sol_array_by_cation_count(2);
salts_3cat: chem_sol_array_by_cation_count(3);
salts_1an: chem_sol_array_by_anion_count(1);
salts_2an: chem_sol_array_by_anion_count(2);
salts_3an: chem_sol_array_by_anion_count(3);
salts_2ions: chem_sol_array_by_total_ions(2);
salts_3ions: chem_sol_array_by_total_ions(3);
salts_5ions: chem_sol_array_by_total_ions(5);
total_ions: chem_sol_total_ion_count(salt);

/* Display variables */
salt_display: chem_display(salt);
salt2_display: chem_display(salt2);
cation_display: chem_display(cation);
anion_display: chem_display(anion);

/* Dummy answer */
ta1: 10;
```

---

## Question text (paste into STACK "Question text" field):

```
\(\require{mhchem}\)

<b>Basic accessors:</b>

This is a randomly selected salt: \({@salt_display@}\) with a \(K_{\mathrm{sp}}\) of {@Ksp@} and a \(\mathrm{p}K_{\mathrm{sp}}\) of {@pKsp@}.

Its cation is \({@cation_display@}\) (coefficient: {@cation_count@}) and its anion is \({@anion_display@}\) (coefficient: {@anion_count@}).

Ion counts [cation, anion]: {@ion_counts@}

Full database entry: {@full_entry@}

<b>Molar solubility:</b>

The molar solubility of \({@salt_display@}\) in pure water is {@s_molar@}.

With a common-ion concentration of 0.01 mol/L (cation), the molar solubility is {@s_common@}.

<b>Dissolution equation and \(K_{\mathrm{sp}}\) expressions:</b>

Dissolution equation: \({@diss_eq@}\)

\(K_{\mathrm{sp}}\) bracket expression: \(K_{\mathrm{sp}} = {@Ksp_expr@}\)

\(K_{\mathrm{sp}}\) activity expression (full): \(K_{\mathrm{sp}} = {@Ksp_act@}\)

\(K_{\mathrm{sp}}\) activity expression (simplified): \(K_{\mathrm{sp}} = {@Ksp_act_s@}\)

Solubility expression: \({@sol_expr@}\)

<b>Precipitation check:</b>

For c<sub>cation</sub> = c<sub>anion</sub> = 0.001 mol/L the ion product Q is {@Q_test@}. Result: {@precip_check@}.

The maximum cation concentration at c<sub>anion</sub> = 0.01 mol/L is {@c_max@} mol/L.

<b>Navigation functions:</b>

Salts with the same cation (\({@cation_display@}\)): {@salts_by_cation@}

Salts with the same anion (\({@anion_display@}\)): {@salts_by_anion@}

All cations in the database: {@all_cations@}

All anions in the database: {@all_anions@}

First 5 salts sorted by \(K_{\mathrm{sp}}\) (ascending): {@sorted_salts_5@}

Salts with \(K_{\mathrm{sp}}\) in [10<sup>−12</sup>, 10<sup>−6</sup>]: {@range_salts@}

<b>Ion count navigation:</b>

Total ions for \({@salt_display@}\): {@total_ions@}

Salts with 1 cation: {@salts_1cat@}

Salts with 2 cations: {@salts_2cat@}

Salts with 3 cations: {@salts_3cat@}

Salts with 1 anion: {@salts_1an@}

Salts with 2 anions: {@salts_2an@}

Salts with 3 anions: {@salts_3an@}

Salts producing 2 total ions: {@salts_2ions@}

Salts producing 3 total ions: {@salts_3ions@}

Salts producing 5 total ions: {@salts_5ions@}

<b>Second salt (same cation):</b>

\({@salt2_display@}\)

<b>Molar mass:</b>

\({@salt_display@}\) has a molar mass of {@chem_molar_mass(salt)@}.

<b>Your answer:</b>

[[input:ans1]] [[validation:ans1]]
```
