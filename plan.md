# Torus habitat: validation plan

Check the design's load-bearing assumptions with models before going deeper. The parametric system model comes first: it recomputes the design notes' numbers from one set of assumptions and ranks them by how much they matter. That ranking sets the priorities for the detailed models.

**Order** (set by the combined sensitivity ranking of model 1 over representative designs, `reports/sensitivity.md`, revised after the review in issue #1): 1 → 2 and 3 in parallel, with a preliminary thermal check done alongside → 4 (needs the structural stiffness from 2) → 5 → 6 → 7. Section 8 lists what only Earth tests can settle; C-type nitrogen recovery and baking energy, near the top of the ranking, are among them.

**Simplicity rule:** where parts of the design can be separated, model them separately and check how each affects the whole as a final step. So the stack has two sections (proposed, 28 Oct 2026): the main section (the tori) and a farm section (one farm ring per torus, on its own spokes) on the same hub, each modelled on its own, then put together.

---

## 1. Parametric system model (Python, first)

**Goal:** one model replaces the hand calculations spread across the notes, reproduces their key tables, and shows which assumptions move the results.

### 1.1 Setup
- [x] Small package `habitat_model/`, plain Python + numpy, run from the command line, e.g. `python -m habitat_model --size 900 --stack six --tiers 2 --host L --site Eros`
- [x] One assumptions file (TOML or a dataclass), one entry per input: value, unit, low/high range, source (section of the notes or reference), status (sourced / estimate / guess)
- [x] Seed it from section 19 of the notes (assumptions to revisit) and the "Still unsourced" list
- [x] Modules: `geometry`, `mass`, `materials`, `power`, `food`, `heat`, `stability`, `replication`, `report`

### 1.2 Modules, each checked against the notes
- [x] **Geometry:** r = (T/2)², w = r/16, floor, tube surface, air volume, hub radius, gaps, pitch, stack length, farm ring area per tier (0.4 r, 0.9 w, 80% planted)
  - check: §0 key numbers (floor 32 / 100 / 245 ha), §2
- [x] **Mass:** rock shield (11 t/m², minus fill credit), double skin, hull and frames (r^2.3), cable spokes `M·ρv²/(σ − ρv²/2)`, fill, water, N₂, farm ring, array, radiators
  - check: §5c table (~2.2 / 11.9 / 40 / 105 / 238 Mt; t per m² of floor)
- [x] **Materials and mining:** metal needed vs host class (H / L / LL free metal, optional iron from the silicates), shield rock from tailings, rock mined per torus; C-type sized by nitrogen (0.24 wt%, 70% recovery); trace-element budget (Cu, B, Sn…) per torus vs source bodies: contained, recoverable, demand and surplus (`--trace`)
  - check: §8 mined per torus, §10 bill of materials and trace table, §15 "tori supported" per candidate host
- [x] **Power and light:** valley lighting (light per m² of floor per day, lamp efficacy, ceiling losses), farm per tier lit, other loads, despun array with the survival sizing (×1.57), seasonal sizing by orbit (aphelion, half sky for the valley, full farm), concentrator option
  - check: §0 and §13 power tables, §15 seasonal sizing table
- [x] **Food:** diet table → mol per person → crop area and kW → people per tier lit, floor per person and density
  - check: ~3,200 mol, ~89 m², ~31 kW per person; ~1,000 / 3,250 / 7,900 people per tier lit
- [x] **Heat:** total heat per torus and stack, radiator area at ~285 K, end-opening capacity, break-even number of tori
  - check: §13 heat table (~27 / 18 / 13 / 10–11 tori)
- [x] **Stability (rigid body):** spin-axis vs transverse inertia of the stack, maximum tori with a 20% margin, for given gaps
  - check: ~26–28 tori in §0
- [x] **Processing and replication:** crushing and baking energy, shipping energy from Δv (`asteroid_transfers.py`), generation time at a given power
  - check: §13 processing energy, §15 shipping energy

### 1.3 Validation
- [x] Unit tests on the formulas (1 g family, spoke taper, radiator law, food chain)
- [x] Reproduce each key table of the notes within ~5%; list every mismatch and fix the model or the notes

### 1.4 Sensitivity
- [x] One-at-a-time sweep of each input over its range, giving a ranked (tornado) table for these outputs:
  - mass per m² of floor
  - rock mined per torus
  - C-type per torus
  - array area
  - people per torus
  - heat margin
  - processing energy
- [x] Optional: Monte Carlo over all ranges for the spread of the key outputs
- [x] Rank the assumptions, then re-order sections 2–6 accordingly
- [ ] Source the trace-element demands and recoveries (mostly guesses taken from the notes; Cr, Sn, Mo and Zn not yet estimated)

### 1.5 Outputs
- [x] Markdown report that regenerates the §0 tables (so the notes' tables can come from the model)
- [x] JSON export for the 3D model's stats panel

**Status:** implemented in `habitat_model/` (see its README); reports in `reports/`. 189 of 197 checked figures within 5% (192 within their configured tolerance) after correcting the notes (`reports/validation.md`); this shows the model reproduces the notes, not that the design is physically validated. Ranking in `reports/sensitivity.md`; sections 2–7 re-ordered by it.

**Review (issue #1), addressed:** the tube's rock jacket and crawl space are now in the geometry (pitch, gaps, end openings, stability) and the jacket has a finite thickness; the fill credit follows the actual fill; the heat capacity is labelled an ideal limit, with a preliminary radiative exchange model alongside; an unknown Δv stays unknown; shipping, total energy and generation time are in the sensitivity outputs, ranked over several designs; the trace budget compares demand with recoverable supply; the validation headline separates the literal 5% from the configured tolerances.

**Done when:** every key table in the notes is reproduced or corrected, and the assumptions are ranked by impact.

---

## 2. Structure

**Why second:** under way. The steel inputs move the S-type rock mined per torus by up to ~+20% (wire stress, hull and frames, hub and factory metal), the jacket's geometry sets the pitch, mass and stack limits, and the stack dynamics need its stiffness.

**Status:** the wire, the cable net and the spin-up are done in `structure_model/` (findings and sources in its README, report in `reports/structure.md`). ~1 GPa is reachable at a safety factor of ~2 on bridge wire, or with thinner wire; the range is narrowed to 800–1,200 MPa (10th in the combined ranking). The rim loads were updated for the jacket's finite thickness (review, issue #1). The tube's cross-section is now modelled by finite elements (`structure_model/tube_section.py`): with the chords anchored at the tube's two sides, the hull and frames are within −8% / +1% of the r^2.3 estimate at 900 m / 1.6 km, +46% at 2.5 km, so the steel per torus moves by under 10%. The hub's stabilising lines are next.

- [x] Finite-element model of the tube's cross-section (numpy: plane-stress bulkheads between membrane skins, fully stressed sizing; `structure_model/tube_section.py`):
  - rock cells and double skin, floor fill, vaulted or hung ceiling cells; loads: 1 g spin and 70 kPa of air
  - found: anchor the chords at the tube's sides (two nets per torus); on the crest the section bends, 3–12× the steel; vaulted and hung ceilings within ~7%
  - open: buckling of the hub-facing half (in compression; sized with an allowance only), the anchors' local details, a 3D shell model of a segment with its joints
- [x] Cable net: chord geometry, tension distribution, taper, compliant joints
- [ ] Spin-up sequence: a partial ring with segments hung in opposite pairs, and the asymmetric loads on the way (provisional)
  - done: assembled statics with one tension per chord, rigid segments and joint springs (`structure_model/net_statics.py`): arcs must span ≥ ~4θr (~270 m at 900 m); their chords carry 2× the finished load, so spin ≤ ~0.71 of the final rate; joints locked while building (~1% of the hoop force, plus bending), released after closure
  - checks: tension-only law for every chord, segment balance, and small displacements at the reported spin; stages failing them (pinned joints, some sliding cases) are left unresolved
  - open: a geometrically nonlinear, prestressed analysis for those, flexible segments (the joint moments of longer arcs), the hub and its stabilising lines, the actual sequence
- [x] Hub held in the nets by stabilising lines (`structure_model/hub.py`): two-body statics and modes (Coriolis) of a torus and its share of the hub in the rotating frame, chords as taut strings, lines in series, sizing iterated with every line taut
  - found: the lines beat the spin's pull on torus and hub ~21× at 900 m (~9× at 2.5 km); in the rotating frame their relative motion has two modes at ~3.5× and ~5.5× the spin (Coriolis); loads move the hub by cm; ~13 t of lines per torus
  - found: hang the first arcs as two pairs at right angles (a single pair can't hold the hub along its chords: without preload it is an unstable rotor); ~10% of the lines inclined to the side nets for axial hold (radial lines alone hold it below the spin rate)
  - open: torque and docking loads through the lines, the elevator and pipe shafts' compliant joints
- [x] Wire from asteroid iron-nickel: literature on drawn pearlitic wire with nickel, cobalt, phosphorus and sulfur; achievable strength, creep and fatigue
  - found: the wire needs carbonyl-refined iron (chondritic metal holds ~9%+ Ni, P and S nearby); fatigue left to the stack dynamics (§4)
- [ ] Output: steel per torus at 400 m / 900 m / 1.6 km / 2.5 km vs the r^2.3 estimate (done for hull and frames: +19% / −8% / +1% / +46%; −2% to +7% with the spokes); stiffness for model 4 (stack dynamics; done for the nets: lateral, tilt, axial and torsion per torus, `reports/structure.md`)

**Changes the design if:** the steel per torus differs from the r^2.3 estimate by more than ~30%, or ~1 GPa working stress isn't reachable with asteroid iron.

---

## 3. Radiation transport (the shield is ~85% of the mass)

**Why third:** 9–13 t/m² of shield moves the mass per m² of floor by about −20% / +22%, at every size.

- [ ] Tool: Geant4 (via GRAS or MULASSIS) run locally, or NASA's OLTARIS / HZETRN
- [ ] Shield composition: L and LL chondritic tailings after metal removal (~2 t/m³), CI-like clays for comparison, water or polyethylene inner layers
- [ ] Environment: galactic cosmic rays at solar minimum (Badhwar–O'Neill model); a worst-case solar particle event (e.g. August 1972, October 1989)
- [ ] Geometry: flat slab first, then the tube cross-section with floor fill, cliff dwellings and the hub-facing side
- [ ] Outputs:
  - effective dose vs areal density (0–20 t/m²)
  - share from secondary neutrons
  - dose saved per t/m² of hydrogen-rich layer
- [ ] Decide the shield thickness for 20 mSv/yr and feed it back into model 1

**Changes the design if:** the dose at ~11 t/m² is off by more than ~20%, either way.

---

## 4. Stack dynamics

**Why fourth:** not in the sweep (the system model treats the stack as rigid), but it decides whether the "nothing has to keep working" principle holds; it needs the stiffness from model 2. The farm section nearly doubles the hub's length (~480 → ~900 m for a 900 m six-stack), which lowers its bending modes.

- [x] Rigid and flexible stack with energy dissipation (`dynamics_model/`): whirl modes in the inertial frame (gyroscopic), the criterion that every forward whirl beats the spin (the maximum-axis rule for a rigid stack), checked by a damped solve
  - found: the nets alone hold a torus on the shared axis at only ~half its centrifugal pull: a stack is not passively stable (six-stack ~0.16 of the spin); rim links between neighbouring tori and a trace of radial ties from the hub fix it (proposed)
  - found: long stacks are then set by the hub's bending with the farm section at its end: ~18 tori of 900 m, ~14–17 of 1.6 km with the hub's mass budget as its wall (rigid rule: 22, 25); a six-stack needs a few mm to ~1 cm of wall
- [x] Flexible stack: hub as a beam, tori as rings on cable nets (their stiffness per torus from plan §2, `structure_model/hub.py`); lowest forward whirl vs spin rate for a pair and a six-stack, and vs stack length
- [ ] Disturbances: docking, rim trains, ballast transfers, friction in the despun array's bearing, sunlight pressure on the array
- [ ] Tools: Python (scipy) multibody model, or modal analysis using model 2's stiffness
- [ ] Output: ratio of lowest mode to spin rate and maximum tori (done, `reports/dynamics.md`); damping needed and the disturbances' response still open
- [ ] Rim links and radial ties: design, preload, how they're built in the construction sequence; the hub's shear and joints; axial and torsional modes

**Changes the design if:** a six-stack needs active control to stay stable, which would break the "nothing has to keep working" principle.

**Status:** no active control is needed, but the nets alone don't hold the tori on the shared axis: rim links between neighbouring tori (and a trace of radial ties) are added to the design (proposed), and the hub's wall sets the longest stack (`reports/dynamics.md`).

---

## 5. Replication logistics

**Why fifth:** once shipping is counted, its inputs top the combined ranking (`reports/sensitivity.md`): the electric propulsion's exhaust speed (−31% / +61% on shipping energy) and the water shipped, set by the lake water per m² of floor, a guess (−30% / +51%). With the notes' Δv, shipping volatiles from Ryugu to Eros takes ~2.5× the energy of crushing and baking. C-type nitrogen recovery and baking energy, also near the top, are Earth tests (section 8).

- [ ] Stock-and-flow or discrete-event model of mining, factory throughput, shipping and imported vitamins per generation. Output: doubling time, and the share of each child habitat that is made locally
- [ ] Water budget per torus with a breakdown (soil, lakes, O₂, ballast, spin-up), replacing the lake-water guess; which water is shipped and which is made locally
- [ ] Transfer Δv from current ephemerides for the chosen S/C pairs (the system model uses the notes' table), and propulsion options (exhaust speed, efficiency, propellant source)

**Changes the design if:** shipping dominates the generation time enough to favour a different C-type partner, local water, or a different propulsion.

---

## 6. Heat rejection

**Why sixth:** a preliminary radiative exchange model now exists (below). With the farm rings in their own section, the tori's drum carries only the valleys' heat: traced together as one scene, a 900 m six-stack with three tiers lit keeps ~2.4× margin in the drum and ~2.5× in the farm section at once (it was ~1.3× with the farm rings in the tori's planes). Heat limits the stack to ~16–18 tori of 900 m, just below stability (~22), and depends most on the farm radiators' reach, a guess: at 0.6 r three tiers lit leave no margin.

- [x] Preliminary radiative exchange (`habitat_model/cavity.py`, `reports/thermal.md`): finite two-sided panels with emissivity ~0.9, insulated hub, farm rings and envelopes, escape through the ends and optionally the side gaps; per section (the tori's drum, the open farm section), then the whole stack traced as one scene, with both sections' panel coverages swept together; the farm radiators' reach swept on its own
- [ ] Farm section's radiators: reach (~1 r assumed; 0.6 r leaves no margin with three tiers lit), layout, and how much of the drum's farm end they may shade
- [ ] Full Monte Carlo ray tracing of the drum between hub and rims: radiators on the spokes, end openings, gap vents, shading by the farm rings and main rings
- [ ] Check that no direct sunlight reaches the radiators (Sun perpendicular to the axis, including through the gaps)
- [ ] Coolant loops: thermosiphon sizing along the spokes, fluids (ammonia, water), pressure drops
- [ ] Valley thermal model: day/night swing with the cold ceiling, wet vs dry valley
- [ ] Output: capacity vs stack length with 0–3 farm tiers lit, radiator area per torus

**Changes the design if:** the end openings carry much less than ~1.6 GW for a 900 m stack, or six-stacks with two or three tiers lit don't fit.

---

## 7. Second tier

**Why seventh:** the farm inputs set the population (light on the crops −17% / +25% on people per torus, wheat yield −7% / +25%) and the light delivery moves the array by under 10%; the closed atmosphere is a control question rather than a sizing one.

- [ ] **Light-box and farm optics:** ray trace of the magnesium-oxide cavity, diffuser and light pipes. Check the ~75% (valley) and ~85% (farm) delivery, and the light uniformity at 2.5 m tier spacing
- [ ] **Closed atmosphere and ecology:** compartment model (ODEs) of O₂, CO₂, N₂, water and soil carbon across farm, valley, soil, people and algae
  - validate by replaying Biosphere 2 (O₂ from ~21% to ~14% in ~16 months)
  - failure scenarios: a farm tier dark, a soil respiration burst, a leak
  - output: buffer and control needs

---

## 8. Earth tests (models can't settle these)

- [ ] **C-type baking (top of the ranking):** nitrogen recovery and energy per kg from CI-like meteorite or simulant. Recovery (50–90%) moves the C-type per torus by −22% to +40%; baking energy (1–2 MJ/kg) moves the processing energy by ±28%. Lab data, not a model, settles both.
- [ ] Growth-chamber trials of the working diet under sulfur lamps (CO₂ ~1,000 ppm, 2.5 m tiers), especially lentils and flax, whose yields are estimates
- [ ] Non-rotating sulfur bulb at kW scale, fed by a 915 MHz source
- [ ] Wire drawing from carbonyl-refined meteoritic iron, and from the as-separated metal for comparison (the wire's strength sets the spoke mass, section 2)
- [ ] Magnetic separation of free metal from L and LL chondrite material (meteorites or simulant)
- [ ] Partial-gravity health data (spaceflight, centrifuge studies)
- [ ] Growth chambers on 1.05–1.8-year cycles for candidate species

