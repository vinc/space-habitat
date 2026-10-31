# Structure: wire, cable net, spin-up and the tube's cross-section

## Wire

Working stress (MPa) by guaranteed strength class of bridge wire and safety factor:

| Safety factor | SF | 1570 MPa class | 1770 MPa class | 1960 MPa class |
|---|---|---|---|---|
| new bridge cables (commonly quoted, unverified) | 2.5 | 628 | 708 | 784 |
| long spans such as Akashi (commonly quoted, unverified) | 2.2 | 714 | 805 | 891 |
| NCHRP 534 action level for existing cables | 2.15 | 730 | 823 | 912 |
| static, well-known spin load (proposed here) | 2 | 785 | 885 | 980 |

The model's 1000 MPa needs a safety factor of 1.96 on the strongest bridge class. Thinner wire is stronger (Bekaert's high-strength threshold, a rough guide):

| Wire diameter | High-strength threshold (MPa) | At SF 2 (MPa) |
|---|---|---|
| 5 mm | 1,460 | 730 |
| 2 mm | 1,910 | 955 |
| 1 mm | 2,250 | 1,120 |
| 0.5 mm | 2,590 | 1,300 |
| 0.3 mm | 2,840 | 1,420 |

Long-term creep of a spoke at 1000 MPa on 1,960 MPa wire (relaxation r = 30 f/fu − 10% after 1,000 h, doubled for the long term, read as creep at constant load):

| Torus | Extra stretch over the spoke's length (m) |
|---|---|
| 400 m | 0.21 |
| 900 m | 0.48 |
| 1.6 km | 0.85 |
| 2.5 km | 1.3 |

## Tangent-chord net (chords tangent at 1.1 × the hub radius, one anchor every 10 m)

Uniform chords keep one area all along, sized at mid-chord where their own spin load adds most; tapered chords at uniform stress need only the end area at their ends.

| Torus | Chord angle at the rim | Net, uniform chords (Mt) | System model spokes (Mt) | Chords vs radial spokes | Saved by tapering | Taper (mid / end area) | Tension per chord end (MN) | Uniform chord area (cm²) | Tapered chord, end area (cm²) | Bow at mid-chord (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| 400 m | 4.3° | 0.0812 | 0.0812 | -0.01% | 0.5% | 1.02 | 50.6 | 513 | 506 | 0.46 |
| 900 m | 4.3° | 0.864 | 0.864 | -0.02% | 1.2% | 1.04 | 104 | 1,080 | 1,040 | 2.3 |
| 1.6 km | 4.3° | 4.85 | 4.85 | -0.04% | 2.2% | 1.06 | 180 | 1,910 | 1,800 | 7.4 |
| 2.5 km | 4.3° | 19.0 | 19.0 | -0.06% | 3.6% | 1.10 | 277 | 3,070 | 2,770 | 18 |

## Building the ring: assembled statics (provisional)

Each chord is one elastic member with a single tension; the rim is cut into rigid segments one tube width long, linked by joints that are *sliding* (shear only: free along the rim, as intended once the ring is closed), *pinned* (tension and shear) or *locked* (also bending). Chords are tension-only: the taut set is iterated both ways until it is exactly the set of stretched chords. Loads at full spin; cable stresses scale with spin². The chords are sized for the finished ring (uniform area).

A stage is **resolved** only if the taut set converges, every segment balances (residual: the worst force or moment imbalance relative to the segment's load) and, after removing the assembly's rigid motion, segment rotations stay below 0.05 rad and displacements below 1% of the radius at the spin rate reported. Otherwise it is left unresolved for a geometrically nonlinear analysis: a mechanism, or displacements too large for the linear geometry. Rotation / displacement are at full spin.

| Torus | Stage | Joints | Status | Chord tensions (MN) | Max chord vs finished | Peak cable stress (MPa) | Max spin fraction within 1 GPa | Max joint tension (MN, share of full hoop) | Max joint moment (GN·m) | Rotation / displacement | Residual |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m | finished ring | sliding | resolved | 99.2–108 | 1.0 | 1,040 | 0.98 | — | — | 0.021 rad / 6.4 m | 3e-09 |
| 900 m | finished ring | locked | resolved | 37.7–37.8 | 0.36 | 386 | 1.0 | 11,900 (63.8%) | 0.072 | 4.7e-07 rad / 1.6 m | 2e-11 |
| 1.6 km | finished ring | sliding | resolved | 179–180 | 1.0 | 1,000 | 1.00 | — | — | 0.0014 rad / 9.0 m | 1e-10 |
| 1.6 km | finished ring | locked | resolved | 90.2–90.5 | 0.50 | 535 | 1.0 | 28,500 (49.7%) | 0.11 | 6.1e-07 rad / 3.8 m | 1e-11 |
| 400 m | two arcs of 119 m (shortest) | locked | resolved | 99.4–99.6 | 2.0 | 1,960 | 0.72 | 34.4 (0.9%) | 2.2 | 3.9e-05 rad / 3.9 m | 7e-06 |
| 400 m | two arcs of 119 m (shortest) | pinned | **unresolved:** no equilibrium (mechanism) |  |  |  |  |  |  | — | 7e-02 |
| 900 m | two arcs of 268 m (shortest) | locked | resolved | 212–213 | 2.0 | 2,010 | 0.71 | 175 (0.9%) | 6.0 | 2.3e-05 rad / 8.9 m | 8e-06 |
| 900 m | two arcs of 268 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 0.52 rad / 27 m | 7e-06 |
| 1.6 km | two arcs of 476 m (shortest) | locked | resolved | 353–354 | 2.0 | 1,910 | 0.72 | 543 (0.9%) | 26 | 3.2e-05 rad / 15 m | 8e-06 |
| 1.6 km | two arcs of 476 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 1.2 rad / 78 m | 8e-06 |
| 2.5 km | two arcs of 743 m (shortest) | locked | resolved | 553–555 | 2.0 | 1,900 | 0.72 | 1,390 (1.0%) | 59 | 2.9e-05 rad / 23 m | 9e-06 |
| 2.5 km | two arcs of 743 m (shortest) | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 0.53 rad / 80 m | 8e-06 |
| 900 m | two arcs of 401 m | locked | resolved | 153–154 | 1.5 | 1,460 | 0.83 | 233 (1.2%) | 68 | 0.0003 rad / 6.4 m | 1e-05 |
| 900 m | two arcs of 401 m | pinned | **unresolved:** no equilibrium (mechanism) |  |  |  |  |  |  | — | 2e-01 |
| 900 m | two arcs of 803 m | locked | resolved | 122–125 | 1.2 | 1,190 | 0.92 | 371 (2.0%) | 220 | 0.0023 rad / 5.6 m | 1e-05 |
| 900 m | two arcs of 803 m | pinned | **unresolved:** outside the small-displacement range |  |  |  |  |  |  | 1.9 rad / 74 m | 1e-05 |

Rigid segments make this a crude model: even resolved stages settle the force balance, not the construction sequence, and the joint moments of the longer locked arcs depend on the segments' real flexibility.

## The baseline: built at rest, spun up finished

A child's stack is assembled at rest (`structure_model/rest.py`): every ring closed, the lattice fitted, the rock and soil in; then spun up slowly with the water last. In the ring's plane, with the geometrically nonlinear model above, the joints sliding along the rim but **bearing on stops**: closed (compression) they act locked, rocking once their moment passes their compression times the tube's radius; open, they slide on a light spring along the rim (~10⁸ N/m, below). The chords are pretensioned to a strain of 5 × 10⁻⁴ as installed, to stay taut through a ±20 K swing of their temperature against the hull's (a guess; α ΔT = 2.4e-04).

### At rest

With no spin load, only the hull resists the chords' pull: the closed ring is squeezed, its joints bear, and most of the installed stretch goes into the hull's shortening (the chords keep only a few % of their finished tension). Allowable compression 150 MPa (half the plate stress, as in the cross-section). Thermal swing: the chords colder (hull's compression) / warmer (the least chord tension). Buckling in the plane: the pretension at which the ring's lowest stiffness vanishes, over the 5 × 10⁻⁴ used (the chords hold it far beyond the free ring's 3EI/r²). Scattered as built (below).

| Torus | Chords (% of finished) | Hull compression (MPa) | Joints' compression (MN) | Cold: hull (MPa) / warm: least chord | Buckling margin |
|---|---|---|---|---|---|
| 900 m | 2.0–3.3% | 74.3 | 499 | 110 / 0.67%, 0 slack | 53.9× |
| 1.6 km | 1.5–2.5% | 81.2 | 1,150 | 120 / 0.57%, 0 slack | — |

### Spinning up: the cables take up tension, the joints open

The spin stepped up from rest to full at 900 m, each step from the last equilibrium. Spin as a share of the final rate; chords as a share of the finished tension; hull stress along the rim (negative: compression) and in bending; joints open and their gap.

| Ring | Spin | Chords (× finished) | Hull along the rim (MPa) | Hull bending (MPa) | Joints open | Gap (cm) | Joints' compression (MN) |
|---|---|---|---|---|---|---|---|
| as drawn | 0 | 0.0267–0.0267 | -74.2 to -74.2 | 0.067 | 0/94 | closed | 498 |
| as drawn | 0.10 | 0.0342–0.0342 | -67.0 to -67.0 | 0.061 | 0/94 | closed | 450 |
| as drawn | 0.17 | 0.0490–0.0490 | -52.7 to -52.7 | 0.048 | 0/94 | closed | 354 |
| as drawn | 0.32 | 0.101–0.101 | -2.44 to -2.44 | 0.0022 | 0/94 | closed | 16.4 |
| as drawn | 0.50 | 0.250–0.251 | 0.632 to 0.632 | 0.0042 | 94/94 | 4.24–4.24 | 0 |
| as drawn | 0.71 | 0.500–0.502 | 1.71 to 1.71 | 0.011 | 94/94 | 11.5–11.5 | 0 |
| as drawn | 1.0 | 1.00–1.01 | 3.88 to 3.88 | 0.026 | 94/94 | 26.0–26.0 | 0 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 0 | 0.0195–0.0333 | -74.3 to -74.1 | 0.88 | 0/94 | closed | 499 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 0.10 | 0.0270–0.0407 | -67.1 to -67.0 | 0.90 | 0/94 | closed | 451 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 0.17 | 0.0421–0.0554 | -52.8 to -52.7 | 1.5 | 0/94 | closed | 355 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 0.32 | 0.0943–0.108 | -2.83 to -2.39 | 3.6 | 0/94 | closed | 19.0 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 0.50 | 0.233–0.265 | 0.373 to 0.923 | 0.60 | 94/94 | 2.53–6.13 | 0 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 0.71 | 0.471–0.532 | 1.15 to 2.39 | 1.2 | 94/94 | 7.78–15.9 | 0 |
| scattered: chords ±2 cm, mass per anchor ±2% (1σ) | 1.0 | 0.942–1.07 | 2.38 to 5.81 | 2.5 | 94/94 | 16.2–38.6 | 0 |

As drawn: the joints open at ~0.32 of the spin; every chord's tension on the way is at most 1.000× its own at full spin; the hull's worst is 74.2 MPa of compression at rest (3.88 MPa along it at full spin), its bending at most 0.067 MPa (0.026 at full spin); finished, the chords at 1.00–1.01× the formula (peak 1.01× the allowable) and the joints open by 26.0–26.0 cm. Scattered: chords ±2 cm, mass per anchor ±2% (1σ): the joints open at ~0.32 of the spin; every chord's tension on the way is at most 1.000× its own at full spin; the hull's worst is 74.3 MPa of compression at rest (5.81 MPa along it at full spin), its bending at most 3.6 MPa (2.5 at full spin); finished, the chords at 0.942–1.07× the formula (peak 1.07× the allowable) and the joints open by 16.2–38.6 cm.

**So nothing exceeds the finished state on the way, except the at-rest pretension:** the hoop's compression in the hull and on the joints' stops, which falls linearly with the spin load and is gone by about a third of the spin, when the joints open together and the chords carry the rim alone, as finished. The scattered ring's finished chords spread by ±~7% (mostly the mass scatter): the finished net's own tolerance, not the spin-up's; it needs the rim's mass placed within ~2% per anchor, or the chords trimmed after spin-up, or a little more safety margin.

**The joints need a spring along the rim.** With joints that only slide, the segments' positions along the rim are barely held: the chords are nearly diametral, so segments sliding in odd harmonics hardly stretch them, and a 2% scatter in the rim's mass slides segments by up to ~1–2 m at a fifth of the spin (and the solution doesn't converge). A spring of ~10⁸ N/m in each joint holds them to the gaps above for a few MPa along the hull; ~10⁷ N/m is too soft to settle, ~10⁹ N/m puts ~30 MPa in the hull. The joints travel ~0.15–0.4 m each by full spin (and ~2 cm more each as the chords creep, ~0.5 m per chord at 900 m: the wire, above).

### The hub's stabilising lines, from rest to full spin

The lines (section on the hub, below) as fixed-length, tension-only lines from the hub's surface to the chords' tangent points, in series with chords whose tension and bow grow with the spin. A chord bows away from the axis by its own spin load over its tension: nothing at rest, the finished bow from where the joints open (its tension grows from its at-rest share, linearly while the joints bear, then with the spin). A line cut to a fixed length is stretched by the chord's free movement outward less what its pull draws the chord in: P = k_s (bow + d0), k_s the line and chord in series at the current tension and spin, d0 the pull-in it is installed with at rest, enough to stay taut (1.5× the swing) under a 10 kt ship docking at 0.1 m/s over 10 s. **So a fixed line holds back the whole bow,** and the lines sized for the finished net (its service preload, a few kN) would be overloaded; sized for it, with their stiffness and pull iterated. Window: the gap around the hub at rest / at full spin with the chords drawn in (finished sizing's, bowed). Margin: the hub's lateral stiffness over its divergence, the least through the spin-up (finished). The lines' pull loads the hub's shell outward all round each net's plane: a ring frame there, at the plate stress.

| Torus | Chords at rest | Finished bow (m) | Fixed lines at the finished sizing: peak / allowable | Line area sized for the bow (mm²) | Line pull at rest / full spin | Window, rest / full (m) | Lateral stiffness, rest / full (MN/m) | Least margin | Docking offset at rest (cm) | Hub's period at rest (s) | Lines' mass (t) | Hub ring frames, per net; both nets |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m | 2.7% | 2.3 | 1.7× | 283 (1.7×) | 265 N / 280 kN | 6.1 / 6.0 (8.4) | 1.8 / 65.5 | 21 (21) | 5.39 | 78.7 | 15.4 (12.7) | 25.2 MN; 506 t |
| 1.6 km | 2.0% | 7.4 | 1.7× | 859 (1.7×) | 149 N / 848 kN | 11 / 11 (18) | 2.4 / 115 | 13 (13) | 3.98 | 153 | 147 (144) | 136 MN; 4,850 t |

**Lines installed snug at rest and sized for the bow (proposed)** keep every line taut and the hub held from rest to full spin, its margin never below the finished one; they cost ~1.7× the finished sizing's area but are shorter (the window narrower by the bow), so only a little more mass, plus a ring frame in the hub at each net. The alternative, lines paid out by the bow as the spin grows (winches, locked at full spin), keeps the finished sizing and window but adds machinery that must work during the spin-up.

### The spin-up's torque

Thrusters on each ring's rim sized to its own inertia; bounded by a fast spin-up, 30 days. Per torus with its hub share and farm ring. Rim: the tangential load over the centrifugal at full spin. Farm ring: its twist at its rim if it is turned by the hub through its radial spokes rather than its own thrusters (at rest / full spin; the spokes resist only by their tension, pretensioned like the chords). Hub: its twist (rad) through 0.2% of the stabilising lines laced (section 11), and the force per laced line against its strength. Lattice: one torus's thrusters 10% off their share, carried across a gap (a braking rim train puts ~40–120 MN·m on a lattice). Water: the spin lost as the water arrives from the axis, made up by thrust.

| Torus | α (rad/s²) | Torque (MN·m) | Thrust (kN) | Rim: tangential / spin load | Farm ring twist at its rim (cm) | Hub twist; laced line force (kN) | Thrust mismatch; lattice force | Water last: spin lost |
|---|---|---|---|---|---|---|---|---|
| 900 m | 4.0e-08 | 399 | 440 | 4e-06 | 24.8 / 0.66 | 3e-05; 3.1 of 169 | 39.8 MN·m; 45.7 kN | 0.5% |
| 1.6 km | 3.0e-08 | 2,960 | 1,840 | 5e-06 | 78.0 / 1.6 | 3e-05; 7.9 of 498 | 295 MN·m; 191 kN | 0.6% |

The spin-up's cost, for the angular momentum of a torus with its hub and farm ring at full spin, delivered at the envelope's outer rim, at the torus's own power (its array, `habitat_model`):

| Torus | Reaction mass | Exhaust (km/s) | Propellant (Mt) | Energy (PJ) | Days at the torus's power |
|---|---|---|---|---|---|
| 900 m | water thrusters | 3.0 | 0.38 | 4.9 | 1,370 |
| 900 m | rock mass driver | 0.50 | 2.3 | 0.57 | 160 |
| 1.6 km | water thrusters | 3.0 | 1.6 | 20 | 1,810 |
| 1.6 km | rock mass driver | 0.50 | 9.5 | 2.4 | 211 |

**The angular acceleration is negligible:** even at the fast rate its loads are millionths of the spin's; a farm ring turned through its radial spokes alone lags ~0.25–0.8 m at its rim at rest (centimetres at full spin), so it gets its own thrusters or simply follows; the laced lines and the lattice carry it with ample margin. What sets the spin-up is energy: water thrusters take years of the torus's own power, host rock thrown by a mass driver at ~0.5 km/s ~5–7 months (proposed; ~6× the reaction mass, of rock mined anyway). The stack at rest has no gyroscopic stiffness, so the thrusters' sideways torques must be balanced or held by the attitude thrusters until the spin builds (not modelled).

### The fill as gravity grows

The rock and soil are placed at rest, in the jacket's cells, whose volume is fixed (5.5 m of jacket, 2 t/m³ finished, ~43% porosity on ~3.5 t/m³ chondrite grains). **Filled loose, a cell holds less rock than the design:** the shield is short of its 11 t/m² everywhere, floor and ceiling included, and settling keeps that mass without restoring it (review of #18). Dose at a sphere's centre behind what is installed, OLTARIS's regolith curve (the design's at 11 t/m²: 14.5 mSv/yr). Loose fill also settles by its porosity as the spin grows: through the jacket's thickness on the floor and ceiling, but at the tube's two sides its cells' columns run along the radius, a cell high (10 m), and a settled cell leaves a slot at its top through the jacket's whole thickness. A slot h high in a wall t thick lets through, unshielded, ~h/4t of the directions seen from the valley at its height, both side walls together twice that: the dose it adds there, against the jacket left around it, is rough. Compacted to its final density as placed, the fill holds the design's mass and settles only by its elastic compression under its own weight at full spin. Top-up: the rock that loose cells lack, per 900 m torus, to be added to every cell.

| Fill placed | Shield installed (t/m²) | Dose behind it (mSv/yr) | Settling strain | Settling through the jacket (cm) | Slot at the sides (cm) | Added at the slots' height (mSv/yr) | Top-up to the design (Mt) |
|---|---|---|---|---|---|---|---|
| loose, 1.6 t/m³ | 8.80 | 37.8 | 20% | 110 | 200 | 77.1 | 2.2 |
| loose, 1.75 t/m³ | 9.62 | 26.7 | 12% | 68.8 | 125 | 49.5 | 1.4 |
| loose, 1.9 t/m³ | 10.4 | 18.6 | 5% | 27.5 | 50.0 | 20.2 | 0.55 |
| compacted at rest, M = 100 MPa | 11.0 | 14.5 | — | 0.30 | 0.99 | 0.40 | — |
| compacted at rest, M = 50.0 MPa | 11.0 | 14.5 | — | 0.60 | 2.0 | 0.80 | — |
| compacted at rest, M = 20.0 MPa | 11.0 | 14.5 | — | 1.5 | 4.9 | 2.0 | — |

**The fill must be compacted as it is placed (proposed).** Loose, the shield is short everywhere (~19–38 mSv/yr behind it, against the design's ~15) and the slots add tens of mSv/yr where they face; making it good would take topping up every cell, not only the sides, with ~0.55–2.2 Mt of rock per 900 m torus, after spin-up and through fill ports. Settling unevenly moves the rim's first moment by ~3.18 cm × its mass even loose, within the ballast's 45 cm, and slows the spin by ~0.07%. The loads the fill puts on its cells grow with the spin to their finished values (the cross-section above).

Not modelled: out of the ring's plane (the ring's buckling sideways, the two nets apart), the joints' stops and springs as hardware, the fill's flow and arching in its cells, the stack's attitude while at rest, the despun array.

## Adding a torus to a spinning stack: geometrically nonlinear

**The baseline is simpler** (previous section): a child is built at rest and spun up finished, so the partial-ring stages below don't arise. What follows is the harder option: a torus added to a living stack, which can't stop, so its arcs are hung at full spin. It checks selected stages of that sequence, not the whole process.

`structure_model/nonlinear.py`, in the ring's plane and the rotating frame: the rim a chain of flexible beams (corotational, one per anchor spacing, E A and E I of the hull and frames as a thin tube of the tube's radius), joined at the segment joints (locked, pinned or sliding: penalty springs); each chord a tension-only cable with its geometric stiffness, pretensioned slightly; the rim's and the chords' centrifugal loads following the parts as they move; the assembly's centre of mass and mean rotation held (it turns about its centre of mass); the spin stepped up with Newton iterations and line search. It reproduces the linear model on the shortest locked arcs (chords ~1.94× their finished tension, joints ~186 MN and ~6 GN·m at full spin) and the finished net (within 1% of the formula). Sequence studies: `structure_model/sequence.py`.

**Joints.** The shortest and longer arcs held at 0.7 of the spin with locked joints, then released step by step, each from the last equilibrium, towards pinned or sliding joints.

| Arcs (× the shortest) | Released to | Locked | Released |
|---|---|---|---|
| 1.00× (271 m) | pinned | 0.93× the allowable, 2.8 GN·m in the joints | held, but rotations 0.70 rad, 39.1 m, chords 1.2× the allowable |
| 1.00× (271 m) | sliding | 0.93× the allowable, 2.8 GN·m in the joints | **no equilibrium** below 1e-06 of the locked moment stiffness |
| 1.50× (411 m) | pinned | 0.76× the allowable, 34 GN·m in the joints | **no equilibrium** below 1e-06 of the locked moment stiffness |
| 1.50× (411 m) | sliding | 0.76× the allowable, 34 GN·m in the joints | **no equilibrium** below 1e-06 of the locked moment stiffness |
| 3.00× (812 m) | pinned | 0.88× the allowable, 27 GN·m in the joints | **no equilibrium** below 1e-06 of the locked moment stiffness |
| 3.00× (812 m) | sliding | 0.88× the allowable, 27 GN·m in the joints | **no equilibrium** below 1e-06 of the locked moment stiffness |

**Flexible arcs, locked, nothing temporary.** The spin each stage reaches with every chord within its allowable, against the linear rigid-segment model's, and the hull's bending.

| Torus | Arcs | Spin limit (chords) | Linear, rigid segments | Chords at full spin (× finished) | Hull bending at full spin (MPa) | At the spin limit (MPa) | Joint tension (MN) | Joint moment (GN·m) |
|---|---|---|---|---|---|---|---|---|
| 900 m | 1.00× | 0.73 | 0.71 | 1.9 | 75.8 | 39.7 | 186 | 5.7 |
| 900 m | 1.50× | 0.80 | 0.83 | 1.6 | 760 | 490 | 222 | 69 |
| 900 m | 3.00× | 0.75 | 0.92 | 1.8 | 592 | 329 | 205 | 56 |
| 1.6 km | 1.00× | 0.72 | — | 2.0 | 5.82 | 3.00 | 573 | 2.0 |
| 1.6 km | 1.50× | 0.79 | — | 1.6 | 1,040 | 652 | 733 | 360 |
| 1.6 km | 3.00× | 0.73 | — | 1.9 | 754 | 400 | 665 | 260 |

With flexible segments, longer arcs don't relieve the chords: the single-laced end zones load theirs to ~1.8× whatever the arc's length, and the arcs bend the hull far past its ~300 MPa plate stress. A torus added to a spinning stack is hung at full spin, so it needs temporary support:

Every chord and line at its peak: tension over area plus its own spin load (a chord's at mid-chord; a radial line's, conservatively, all of it, at its hub end).

| Torus | Arcs | Temporary support | Reached | Peak chord stress (MPa, × allowable) | Peak radial-line stress (MPa, × allowable) | Hull bending (MPa) | Joint tension (MN) | Temporary steel (kt) |
|---|---|---|---|---|---|---|---|---|
| 900 m | 1.50× | none | full spin | 1,550 (1.55×) | — | 760 | 222 | — |
| 900 m | 1.50× | cables doubled at the single-laced anchors | full spin | 857 (0.857×) | — | 693 | 212 | 80 |
| 900 m | 1.50× | radial lines, a chord's area | full spin | 994 (0.994×) | 1,060 (1.06×) | 10.7 | 103 | 37 |
| 900 m | 1.50× | proposed: radial lines 1.15×, end cables 1.05× | full spin | 930 (0.930×) | 985 (0.985×) | 53.8 | 96.1 | 47 |
| 900 m | 3.00× | none | full spin | 1,800 (1.80×) | — | 592 | 205 | — |
| 900 m | 3.00× | cables doubled at the single-laced anchors | full spin | 915 (0.915×) | — | 329 | 198 | 80 |
| 900 m | 3.00× | radial lines, a chord's area | full spin | 1,010 (1.01×) | 1,050 (1.05×) | 23.3 | 108 | 37 |
| 900 m | 3.00× | proposed: radial lines 1.15×, end cables 1.05× | full spin | 1,010 (1.01×) | 991 (0.991×) | 29.2 | 103 | 47 |
| 1.6 km | 1.50× | none | full spin | 1,600 (1.60×) | — | 1,040 | 733 | — |
| 1.6 km | 1.50× | cables doubled at the single-laced anchors | full spin | 890 (0.890×) | — | 984 | 748 | 460 |
| 1.6 km | 1.50× | radial lines, a chord's area | full spin | 996 (0.996×) | 1,060 (1.06×) | 4.97 | 362 | 220 |
| 1.6 km | 1.50× | proposed: radial lines 1.15×, end cables 1.05× | full spin | 931 (0.931×) | 986 (0.986×) | 55.2 | 346 | 270 |
| 1.6 km | 3.00× | none | full spin | 1,880 (1.88×) | — | 754 | 665 | — |
| 1.6 km | 3.00× | cables doubled at the single-laced anchors | full spin | 948 (0.948×) | — | 465 | 691 | 460 |
| 1.6 km | 3.00× | radial lines, a chord's area | full spin | 1,000 (1.00×) | 1,050 (1.05×) | 25.8 | 371 | 220 |
| 1.6 km | 3.00× | proposed: radial lines 1.15×, end cables 1.05× | full spin | 1,010 (1.01×) | 995 (0.995×) | 27.9 | 363 | 270 |

Doubling the cables at the single-laced anchors keeps the chords within their allowable but leaves the hull bending. Temporary radial lines from the hub to those anchors (pulling straight in, nothing along the rim) take the bending away; at a chord's area they are themselves ~5% over at their hub end, thicker they stiffen the ends and bend the hull again. Proposed: lines of 1.15× a chord's area and a 1.05× sleeve on the end-zone cables. The chords are sized to their allowable in the finished net (here at ~1.007× it, from the anchors' discrete positions), so wherever a stage loads them past their finished tension (the mid-arc chords by ~1%) they are past it too at full spin; the worst step is the release after closure (below, ~7%): building at ~0.97 of the spin for it, or a lower safety factor while building, covers it. The hub carries the two arcs' pull across its diameter.

**Growing to closure at full spin** (one opposite pair; two pairs at right angles behave the same, each arc at least the shortest, with twice the lines), with the proposed support:

| Torus | Each arc | Reached | Peak chord stress (MPa, × allowable) | Peak radial-line stress | Spin within every allowable | Hull bending (MPa) | Joint tension (MN, share of hoop) | Joint moment (GN·m) | Pull across the hub (GN) | Radial lines | Their steel (kt) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 900 m | 283 m (10% of a half ring) | full spin | 899 (0.899×) | 958 (0.958×) | 1.00 | 5.74 | 91.0 (0.5%) | 0.35 | 3.0 | 52 | 45 |
| 900 m | 848 m (30% of a half ring) | full spin | 1,010 (1.01×) | 990 (0.990×) | 0.993 | 26.9 | 105 (0.6%) | 2.5 | 3.0 | 52 | 47 |
| 900 m | 1,700 m (60% of a half ring) | full spin | 1,010 (1.01×) | 990 (0.990×) | 0.996 | 33.0 | 108 (0.6%) | 3.1 | 3.0 | 52 | 47 |
| 900 m | 2,690 m (95% of a half ring) | full spin | 1,010 (1.01×) | 990 (0.990×) | 0.996 | 33.3 | 108 (0.6%) | 3.1 | 3.0 | 52 | 47 |
| 1.6 km | 503 m (10% of a half ring) | full spin | 906 (0.906×) | 963 (0.963×) | 1.00 | 1.78 | 291 (0.5%) | 0.50 | 9.5 | 96 | 260 |
| 1.6 km | 1,510 m (30% of a half ring) | full spin | 1,010 (1.01×) | 995 (0.995×) | 0.995 | 25.9 | 366 (0.6%) | 9.2 | 9.4 | 96 | 270 |
| 1.6 km | 3,020 m (60% of a half ring) | full spin | 1,010 (1.01×) | 995 (0.995×) | 0.997 | 32.2 | 373 (0.7%) | 11 | 9.5 | 96 | 270 |

**Closure (900 m, full spin).** Closed with every joint locked, the hull becomes a hoop: ~705 MPa along it, the chords at ~0.75× their finished tension. Made instead with its two closure joints sliding, the ring never becomes a hoop: the hull at ~2.07 MPa along it and ~64.3 MPa in bending, the chords at 0.93–1.1× their finished tension (peak 1.06× the allowable), every anchor now double-laced (the radial lines can go). Then every joint is released to sliding, step by step from the last equilibrium: the finished net, chords at 1.00–1.01× the formula (peak 1.01× the allowable; 1.07× at worst on the way).

## Imbalance: one arc 1% heavier than its partner

The stack spins freely about its centre of mass, so a mismatch moves the spin axis away from the assembly's geometric centre: an estimate of that offset only. The hub and the net move together, so this is not a loss of clearance between them; their relative motion needs the stabilising lines' stiffness (still open). Hub, dock and factory taken as 25% of the torus steel.

| Torus | Shortest arc (Mt) | Axis offset, first pair alone (m) | Axis offset, finished torus if never ballasted (cm) |
|---|---|---|---|
| 400 m | 0.12 | 1.8 | 18 |
| 900 m | 0.56 | 3.6 | 39 |
| 1.6 km | 1.7 | 5.6 | 64 |
| 2.5 km | 4.2 | 7.5 | 92 |

## The hub in the nets: stabilising lines

Each torus has two chord nets, one in each side plane of its tube. In each, the chords pass the hub tangent to a circle 1.1 × its radius, bowed outward by their spin load, leaving a window gap around it. A short line runs from the hub to every chord's tangent point (`structure_model/hub.py`). A chord pulled sideways at its middle resists like a taut string, 2T/L, a little less under its own spin load (shown in brackets); lines and chords act in series, and N lines spread around the window give N k / 2 in any direction of a net's plane, twice that for the torus's two nets. The hub's share is the system model's hub, dock and factory metal (25% of the torus steel). The torus and its hub move relative to each other with their reduced mass μ; off the axis they are pulled apart by μω²x, so the margin is K / μω². In the rotating frame Coriolis couples the two directions of the window's plane: the relative motion has two modes, at |√(K/μ) ∓ ω| (√(K/μ) seen from outside). Lines are preloaded 1.5× their largest swing of tension, in service and while building, and the area, preload, stiffness and loads are iterated until they agree, every line taut and within the wire stress.

### Finished torus

| Torus | Hub share (Mt) | Window gap (m) | Lines | Chord stiffness (kN/m) | Lateral stiffness (MN/m) | Margin K / μω² | Natural frequency / spin: inertial; rotating modes | Tilt stiffness (GN·m/rad) | Axial stiffness (MN/m): radial lines / 10% inclined | Axial natural frequency / spin | Torsional stiffness (GN·m/rad) | Line area (mm²) | Service preload (kN) | Lines' mass (t), + inclined option |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 400 m | 0.032 | 3.2 | 502 | 127 (-1%) | 30.5 | 39 | 6.3; 5.3 and 7.3 | 9.88 | 0.20 / 4.84 | 0.51 / 2.5 | 0.17 | 41.4 | 1.3 | 0.52 (+0.25) |
| 900 m | 0.29 | 8.4 | 1,130 | 117 (-2%) | 64.4 | 21 | 4.5; 3.5 and 5.5 | 72.8 | 0.71 / 11.1 | 0.48 / 1.9 | 3.0 | 169 | 5.3 | 13 (+4.0) |
| 1.6 km | 1.5 | 18 | 2,010 | 115 (-4%) | 113 | 13 | 3.6; 2.6 and 4.6 | 349 | 1.7 / 19.6 | 0.44 / 1.5 | 23 | 498 | 16 | 140 (+32) |
| 2.5 km | 5.5 | 35 | 3,142 | 115 (-7%) | 178 | 8.6 | 2.9; 1.9 and 3.9 | 1,240 | 3.4 / 29.6 | 0.41 / 1.3 | 120 | 1,240 | 38 | 1,100 (+170) |

Radial lines hold the hub along the axis only through their preload: its axial natural frequency is below the spin rate. Running 10% of the lines from the hub's mid-plane out to the side nets, over their full length (the gap and the nets' offset from the mid-plane), holds it ~8–25× more stiffly (second figure; a chord resists sideways pulls out of its plane alike), for the extra line mass shown. Torsion is likewise held by preload only.

### Loads on the hub (finished torus, full spin): offset of the hub from the torus / force in the lines

Hub imbalance: 1% of the hub's mass at its rim. Torus imbalance: a 1% mismatch between two opposite arcs of 4θr, never ballasted. Orbit thrust: 1e-05 m/s² for the torus, pushed through its hub (notes §15). The torus and its hub turn about their common centre of mass.

| Torus | Hub imbalance | Torus imbalance | Orbit thrust |
|---|---|---|---|
| 400 m | 0.71 cm / 0.22 MN | 0.48 cm / 0.15 MN | 0.089 cm / 0.027 MN |
| 900 m | 3.1 cm / 2.0 MN | 2.0 cm / 1.3 MN | 0.21 cm / 0.13 MN |
| 1.6 km | 9.2 cm / 10 MN | 5.7 cm / 6.5 MN | 0.40 cm / 0.45 MN |
| 2.5 km | 22 cm / 40 MN | 13 cm / 23 MN | 0.68 cm / 1.2 MN |

### Building: the first arcs

At 0.71 of the final spin (net_statics), with a 1% mismatch between the arcs of a pair. A pair's chords run between its two arcs, nearly parallel: the lines hold the hub across them, but along them only through the arcs' small spread and the lines' preload. A second pair at right angles holds that direction. The preload is the larger of what gives the stiffness margin and what keeps every line 1.5× above its swing; the stiffness differs by direction, so the modes are solved: without preload a single pair is an asymmetric rotor and the hub's motion grows. Pull-in: how far the preload draws those chords into the window.

| Torus | First stage | Chords per net | Margin without preload | Without preload | Preload (kN) | Swing of tension (kN) | Chord pull-in (m) | Hub offset from the arcs (m) | Force in the lines (MN) |
|---|---|---|---|---|---|---|---|---|---|
| 400 m | one opposite pair | 12 | 0.062 | grows ×e every 0.20 turns | 109 | 72.9 | 0.85 | 4.0 (**more than the gap**) | 2.1 |
| 400 m | two pairs at right angles | 24 | 7.9 | stable | 24.8 | 16.6 | 0.19 | 0.13 | 0.42 |
| 900 m | one opposite pair | 27 | 0.036 | grows ×e every 0.22 turns | 291 | 155 | 2.4 | 9.0 (**more than the gap**) | 17 |
| 900 m | two pairs at right angles | 54 | 4.4 | stable | 102 | 67.7 | 0.85 | 0.58 | 4.0 |
| 1.6 km | one opposite pair | 48 | 0.025 | grows ×e every 0.25 turns | 905 | 275 | 7.6 | 16 | 78 |
| 1.6 km | two pairs at right angles | 96 | 2.9 | stable | 299 | 199 | 2.5 | 1.7 | 22 |
| 2.5 km | one opposite pair | 74 | 0.019 | grows ×e every 0.28 turns | 2,310 | 437 | 19 | 25 | 250 |
| 2.5 km | two pairs at right angles | 148 | 2.1 | stable | 742 | 494 | 6.2 | 4.2 | 86 |

Not modelled: the hub as a beam between tori and the stack's modes (plan §4), the elevator, pipe and power shafts and their compliant joints, docking loads (set by the dock's buffers), and torque through the lines.

## Tube cross-section: hull and frames by finite elements

One metre of tube in the plane of its cross-section (`structure_model/tube_section.py`): the pressure hull and the outer cell wall as membrane skins, the jacket's transverse bulkheads (one every 10 m) smeared into a plane-stress annulus between them, the rock, fill, lakes, air, bumper and steel under spin gravity, 70 kPa on the hull, and the chords' anchors on the outer wall holding the section along the radius. Every part is sized fully stressed at 300 MPa (von Mises at every integration point; half that in compression, blended with tension by the compression's share of the stress state, an allowance for stiffeners), or held at its minimum gauge (1 cm for the skins, 5 mm for bulkheads and cell walls). The skins also carry the hull's lengthwise pressure load and the pillowing of their panels between bulkheads; the hub-facing hull panels pressed in by the rock get stiffeners (vaulted ceiling), or the rock rests on hung cell floors instead (hung). Panels, cell walls and bumper are together in one column. Each anchor is a fitting through the jacket's depth, spreading the chord's pull over the radial line of nodes at its angle and pinned at the chord's attachment on the outer wall (a force, no couple). **Sizing:** *fully stressed* when every part is within 2% of its allowable or at its minimum gauge; *safe* when none is over it but some still have spare capacity after 200 rounds (heavier than needed); *over* when some part still exceeds it (not a design).

### Chords anchored at the tube's two sides (one net in each side plane), vaulted ceiling

| Torus | Load (MN per m of tube) | Hull (Mt) | Outer wall (Mt) | Bulkheads (Mt) | Panels, cell walls, bumper (Mt) | Hull and frames (Mt) | System model, r^2.3 (Mt) | Difference | Steel per torus (with spokes) vs model | Sizing |
|---|---|---|---|---|---|---|---|---|---|---|
| 400 m | 10.1 | 0.015 | 0.022 | 0.0079 | 0.011 | **0.055** | 0.046 | +19% | +7% | fully stressed |
| 900 m | 20.6 | 0.077 | 0.091 | 0.061 | 0.045 | **0.27** | 0.30 | -9% | -2% | fully stressed |
| 1.6 km | 35.7 | 0.32 | 0.29 | 0.38 | 0.14 | **1.1** | 1.1 | +1% | +0% | fully stressed |
| 2.5 km | 56.1 | 1.4 | 0.98 | 1.9 | 0.32 | **4.6** | 3.1 | +45% | +6% | fully stressed |

### Where the chords anchor

Anchors on the hub-facing crest (one net in the torus's mid-plane), at the two sides, or spread over the hub-facing half (anchors that would push are released; the rest share the load). Anchor loads per metre of tube; compression is the largest compressive force in a skin; displacement includes the section's ovalisation.

| Torus | Anchors | Ceiling | Steel (t per m of tube) | Per torus (Mt) | Anchor loads (MN/m) | Max skin compression (MN/m) | Max displacement (m) | Sizing |
|---|---|---|---|---|---|---|---|---|
| 900 m | crest | vaulted | 166 | 0.91 | 180°: 21.7 | 29 | 0.41 | fully stressed |
| 900 m | crest | hung | 177 | 0.97 | 180°: 21.8 | 29 | 0.41 | fully stressed |
| 900 m | sides | vaulted | 50.1 | 0.27 | 90°: 10.3, 270°: 10.3 | 1.3 | 0.076 | fully stressed |
| 900 m | sides | hung | 53.3 | 0.29 | 90°: 10.3, 270°: 10.3 | 2.1 | 0.10 | fully stressed |
| 900 m | fan | vaulted | 49.2 | 0.27 | 90°: 8.70, 120°: 1.03, 150°: 0.228, 180°: 0.692, 210°: 0.228, 240°: 1.03, 270°: 8.70 | 1.4 | 0.11 | fully stressed |
| 900 m | fan | hung | 52.5 | 0.29 | 90°: 9.43, 120°: 0.604, 150°: 0.0888, 180°: 0.418, 210°: 0.0888, 240°: 0.604, 270°: 9.43 | 2.8 | 0.12 | fully stressed |
| 1.6 km | crest | vaulted | 823 | 8.0 | 180°: 42.4 | 96 | 1.1 | safe, up to 4% spare |
| 1.6 km | crest | hung | 856 | 8.3 | 180°: 42.7 | 96 | 1.1 | safe, up to 4% spare |
| 1.6 km | sides | vaulted | 117 | 1.1 | 90°: 17.9, 270°: 17.9 | 4.2 | 0.21 | fully stressed |
| 1.6 km | sides | hung | 123 | 1.2 | 90°: 17.9, 270°: 17.9 | 3.4 | 0.26 | fully stressed |
| 1.6 km | fan | vaulted | 111 | 1.1 | 90°: 17.2, 150°: 0.0272, 180°: 1.26, 210°: 0.0272, 270°: 17.2 | 3.0 | 0.28 | fully stressed |
| 1.6 km | fan | hung | 120 | 1.2 | 90°: 17.5, 180°: 0.734, 270°: 17.5 | 4.8 | 0.32 | fully stressed |
| 2.5 km | crest | vaulted | 3,560 | 54 | 180°: 86.8 | 300 | 2.4 | safe, up to 3% spare |
| 2.5 km | sides | vaulted | 300 | 4.6 | 90°: 28.0, 270°: 28.0 | 10 | 0.59 | fully stressed |
| 2.5 km | fan | vaulted | 281 | 4.3 | 90°: 27.0, 180°: 1.88, 270°: 27.0 | 5.8 | 0.82 | fully stressed |

### Sensitivity at 900 m (sides, vaulted)

| Change | Hull and frames (Mt) | vs base |
|---|---|---|
| `plate_stress_mpa` = 200 | 0.330 | +20% |
| `plate_stress_mpa` = 500 | 0.247 | -10% |
| `skin_min_gauge_m` = 0.005 | 0.221 | -19% |
| `skin_min_gauge_m` = 0.02 | 0.429 | +57% |
| `cell_wall_min_gauge_m` = 0.01 | 0.309 | +13% |
| `bumper_m` = 0.003 | 0.284 | +4% |

Not modelled: buckling of the parts in compression (sized with an allowance only), segment joints and seals, the anchors' local details, and the valley's buildings, light box and ceiling.

