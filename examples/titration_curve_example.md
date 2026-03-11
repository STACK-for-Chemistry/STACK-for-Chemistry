# Titration Curve Example Question

Copy the sections below into the corresponding fields in STACK.

---

## Question Variables

```maxima
/* Load the acid-base module */
stack_include_contrib("https://raw.githubusercontent.com/AlexVCS25/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/acidbase.mac");
stack_include_contrib("https://raw.githubusercontent.com/AlexVCS25/STACK-for-Chemistry/refs/heads/main/Modules/Utilized/pse.mac");

/* Set up the titration parameters */
acid: "CH3COOH";
c_acid: 0.1;
c_base: 0.1;
v_acid: 25.0;

/* Get pKa */
pKa_value: chem_acidbase_pKa(acid);

/* Calculate key points */
v_equiv: chem_titration_equiv_volume(c_acid, c_base, v_acid);
pH_equiv: chem_titration_equiv_pH(acid, c_acid, c_base, v_acid);
pH_half: chem_titration_half_equiv_pH(acid, c_acid, c_base, v_acid);
pH_initial: chem_titration_pH(acid, c_acid, c_base, v_acid, 0);

/* Generate curve data */
curve_data: chem_titration_curve_data(acid, c_acid, c_base, v_acid);
jsxpoints: chem_titration_jsxgraph_points(curve_data);

/* Axis bounds */
x_max: float(v_equiv * 1.6);

/* Display formula */
acid_display: chem_display(acid);

/* Answers */
ta_equiv_vol: v_equiv;
ta_pKa: pKa_value;
```

---

## Question Text

```html
\(\require{mhchem}\)

<p>Die folgende Abbildung zeigt die Titrationskurve von {@v_acid@} mL einer {@c_acid@} M Lösung von {@acid_display@} mit {@c_base@} M NaOH.</p>

[[jsxgraph width="500px" height="400px"]]
var board = JXG.JSXGraph.initBoard(divid, {
    boundingbox: [-2, 15, {#x_max#}+5, -1], 
    axis: true, 
    showCopyright: false
});

/* Add axis labels */
board.create('text', [{#x_max#}/2, -0.7, 'V(NaOH) / mL'], {fontSize: 14});
board.create('text', [-1.5, 7.5, 'pH'], {fontSize: 14, rotate: 90});

/* Titration curve data points */
var points = {#jsxpoints#};

/* Extract x and y data */
var xData = [];
var yData = [];
for (var i = 0; i < points.length; i++) {
    xData.push(points[i][0]);
    yData.push(points[i][1]);
}

/* Draw the curve */
board.create('curve', [xData, yData], {
    strokeColor: 'blue', 
    strokeWidth: 2
});

/* Mark equivalence point */
board.create('point', [{#v_equiv#}, {#pH_equiv#}], {
    name: 'Äquivalenzpunkt', 
    size: 3, 
    color: 'red',
    label: {offset: [10, 10], fontSize: 12}
});

/* Mark half-equivalence point */
board.create('point', [{#v_equiv#}/2, {#pH_half#}], {
    name: 'Halbäquivalenz', 
    size: 3, 
    color: 'green',
    label: {offset: [10, -15], fontSize: 12}
});

/* Dashed line at pKa */
board.create('line', [[0, {#pKa_value#}], [{#x_max#}, {#pKa_value#}]], {
    strokeColor: 'gray', 
    strokeWidth: 1, 
    dash: 2,
    straightFirst: false,
    straightLast: false
});

board.create('text', [{#x_max#}+1, {#pKa_value#}, 'pKa'], {fontSize: 11, color: 'gray'});

[[/jsxgraph]]

<p><strong>Fragen:</strong></p>

<p>1. Wie gross ist das Äquivalenzvolumen (in mL)? [[input:ans1]] [[validation:ans1]]</p>

<p>2. Wie gross ist der pKa-Wert der Säure? (Hinweis: Schauen Sie sich den Halbäquivalenzpunkt an.) [[input:ans2]] [[validation:ans2]]</p>
```

---

## Input: ans1
- **Type:** Numerical
- **Model answer:** `ta_equiv_vol`
- **Box size:** 5

## Input: ans2
- **Type:** Numerical  
- **Model answer:** `ta_pKa`
- **Box size:** 5

---

## Potential Response Tree: prt1 (for ans1)

**Node 1:**
- Answer test: `NumAbsolute`
- SAns: `ans1`
- TAns: `ta_equiv_vol`
- Test options: `0.5`
- True score: 1
- False score: 0

---

## Potential Response Tree: prt2 (for ans2)

**Node 1:**
- Answer test: `NumAbsolute`
- SAns: `ans2`
- TAns: `ta_pKa`
- Test options: `0.1`
- True score: 1
- False score: 0

---

## General Feedback

```html
<p><strong>Lösung:</strong></p>
<ul>
<li>Das Äquivalenzvolumen beträgt {@ta_equiv_vol@} mL.</li>
<li>Der pKa-Wert von {@acid_display@} ist {@ta_pKa@}.</li>
<li>Am Halbäquivalenzpunkt (bei {@v_equiv/2@} mL) gilt: pH = pKa = {@pKa_value@}</li>
</ul>
```

---

## Question Note

```
Acid: {@acid@}, pKa: {@pKa_value@}, V_equiv: {@v_equiv@} mL
```
