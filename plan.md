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
  - check: ~3,200 mol, ~89 m², ~12 kW per person with LEDs (~31 kW with the sulfur lamps first sized); ~1,000 / 3,250 / 7,900 people per tier lit
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

**Status:** implemented in `habitat_model/` (see its README); reports in `reports/`. 190 of 193 checked figures within 5% (192 within their configured tolerance) after correcting the notes (`reports/validation.md`); this shows the model reproduces the notes, not that the design is physically validated. Ranking in `reports/sensitivity.md`; sections 2–7 re-ordered by it.

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

- [ ] Tool: Geant4 (via GRAS or MULASSIS) run locally, or NASA's OLTARIS / HZETRN (not available here; OLTARIS's published results used instead, below; a run in the tube's own geometry is still needed)
- [x] Stand-in transport model (`radiation_model/`, `reports/radiation.md`): straight-ahead transport along each ray (protons, neutrons, helium, three heavier groups and charged pions; slowing down, nuclear collisions, leading and cascade nucleons, evaporation neutrons, knocked-out light ions, fragments), two-group diffusion of the slow neutrons, directions summed at a sphere's centre or in the tube; checked against proton ranges, cross sections, the nucleon attenuation length in air, and OLTARIS (Globus & Strout 2017, Table 2; Janhunen 2020): it agrees for water and polyethylene but falls too fast in rock, so the sizing uses OLTARIS's regolith curve
- [x] Shield composition: L and LL chondritic tailings after metal removal (within ~2% of lunar regolith per tonne), CI-like clays, water and polyethylene; water or polyethylene inner layers
- [x] Environment: galactic cosmic rays at a deep solar minimum (force-field modulation of an interstellar spectrum, in place of Badhwar–O'Neill); the August 1972 solar particle event (King's fit)
- [x] Geometry: sphere centre, slab (OLTARIS: about half the sphere's dose at the wall), the tube's cross-section with the floor fill and a cliff dwelling (straight ahead it overstates the gain; the hub-facing side and the stack's shading left out)
- [x] Outputs:
  - dose vs areal density 0–20 t/m²: OLTARIS's ~10.3 t/m² of regolith for 20 mSv/yr at a sphere's centre stands; near the walls half that dose
  - share from secondary neutrons: about two thirds deep in rock
  - dose saved per t/m² of hydrogen-rich layer: ~2 mSv/yr per t/m² of water over rock (model); OLTARIS: water and boron-10 inside save ~1.3 t/m² (Janhunen)
- [ ] Decide the shield thickness for 20 mSv/yr and feed it back into model 1: **proposed 10 t/m²** (~12 mSv/yr near the walls, ~−10% mass per torus); the system model keeps 11 t/m² until a run in the tube's own geometry confirms the factor near the walls

**Status:** the 11 t/m² jacket gives ~15 mSv/yr at a sphere's centre and ~7 near the walls (OLTARIS's curves), so ~10 t/m² would do where people live; a run in the tube's geometry should confirm it before the design changes.

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

**Why fifth:** once shipping is counted, its inputs top the combined ranking (`reports/sensitivity.md`): the electric propulsion's exhaust speed (−31% / +61% on shipping energy). The water shipped ranked second while the lakes were fitted (0.25 t/m²); with small ponds instead (plan §5, below) it drops out of the top ranks, but the ballast's share, a guess, now ranks ~5th (+39% on shipping energy at its high end). With the notes' Δv, shipping volatiles from Ryugu to Eros takes ~1.3× the energy of crushing and baking. C-type nitrogen recovery and baking energy, also near the top, are Earth tests (section 8).

- [x] Stock-and-flow model of a generation (`logistics_model/flows.py`): the rates a parent's lines must sustain for a given generation (rock mined, metal, rock placed, C-type baked, cargo per window, power), what a child is made of by source, and the cluster's growth until its C-type runs out
  - found: at 10-year generations a 900 m torus's child takes ~9 kt of S-type and ~400 t of metal a day, ~2% of Earth's largest mines and steelworks; ~99.2% of it comes from the host, ~0.8% from the C-type, ~0.0004% are vitamins (the array's silicon made at the host, notes §13); Ryugu's nitrogen caps a 900 m cluster after ~55 years of doubling (1.6 km six-stacks after ~14)
  - open: factory throughput against its own mass (how fast a factory copies itself), people, seed transfers to new sites, failures and spares
- [x] Water budget per torus with a breakdown (soil, ponds, O₂, ballast, vegetation; spin-up as an option), replacing the lake-water guess (`logistics_model/water.py`, system model): ~0.066 / 0.22 / 0.56 Mt at 900 m / 1.6 km / 2.5 km, soil moisture about 60% of it, ballast (2 e M for an unbalanced e M at the rim) about a fifth; the lakes become small ponds and streams (~2% of the floor, ~1 m deep), water access for the biosphere rather than a feature
  - investigated: ship only the water's hydrogen, as methane, with the oxygen from the silicates by molten-oxide electrolysis. Charged for the electrolysis and furnace heat the baseline doesn't otherwise run, it only just beats shipping water with electric thrusters and loses with mass drivers; it pays only on a host that electrolyses its silicates for iron anyway. Methane stays useful as a storable fuel (methalox)
- [x] Transfer Δv from current ephemerides for the chosen S/C pairs; propulsion options
  - done: a Lambert solver (`logistics_model/transfers.py`) on JPL's current elements reproduces the notes' best-phase Δv within ~0.1 km/s; dated windows (`windows.py`) on JPL Horizons' ephemerides for 2027–2077 (`ephemeris.py`, stored in `logistics_model/data/`) confirm the notes' dated values within ~0.1 km/s (Ryugu → Eros 4.66 km/s in 2031, best 4.52 in 2061), with usable windows on average every ~2–7 years but clustered, gaps up to ~20 years (Ryugu → Eros, 2036–2056) setting the stock to hold; propulsion options by energy and propellant (`propulsion.py`)
  - found: the electricity per kg delivered is lowest at vₑ ≈ Δv / 1.59 (~3 km/s): mass-driver freighters using the C-type's baked residue need ~3.7× less than electric thrusters at 30 km/s (proposed)
  - found: a catalogue search (`catalogue.py`, 365 dark or C-complex near-Earth asteroids) finds better partners than Ryugu: 1999 XX262 for Eros (~3.6 km/s phase-free, ~1.5 km) and 2001 WT1 for Itokawa and Torifune (~3.9 / ~2.8 km/s); 1999 XX262 is already a B/Ch type in published spectra (SsODNet); next its 3 µm band (water, ammonium), and a spectrum of 2001 WT1
  - open: low-thrust and multi-revolution trajectories, gravity assists, a dated shipping schedule (stock against off-window departures and their Δv), the freighters' mass and power, ranking S-type hosts by orbit and metal class

**Changes the design if:** shipping dominates the generation time enough to favour a different C-type partner, local water, or a different propulsion.

**Status:** with small ponds, shipping is ~1.3× the processing energy; mass-driver freighters (proposed) cut it ~3.7×, so a generation's energy floor goes from ~1.5 to ~0.9 years for a 900 m pair at 1 GW per stack (~19 → ~13 years for a 1.6 km six-stack). Shipping only the hydrogen doesn't pay unless the host electrolyses its silicates anyway. Dated windows confirm the transfers; usable ones cluster, with gaps of up to ~20 years to stock through; better-aligned C-types than Ryugu exist (1999 XX262 for Eros, 2001 WT1 for Itokawa and Torifune), pending spectra. Ryugu's nitrogen, not shipping, sets the cluster's horizon (`reports/logistics.md`).

---

## 6. Heat rejection

**Why sixth:** a preliminary radiative exchange model now exists (below). With the farm rings in their own section, the tori's drum carries only the valleys' heat: traced together as one scene, a 900 m six-stack with three tiers lit keeps ~5.2× margin in the drum and ~5.0× in the farm section at once with LEDs (~2.4× / ~2.5× with sulfur lamps; ~1.3× with the farm rings in the tori's planes). With LEDs, heat no longer limits the stack (40 tori or more cooled; with sulfur lamps ~16–18, just below stability's ~22).

- [x] Preliminary radiative exchange (`habitat_model/cavity.py`, `reports/thermal.md`): finite two-sided panels with emissivity ~0.9, insulated hub, farm rings and envelopes, escape through the ends and optionally the side gaps; per section (the tori's drum, the open farm section), then the whole stack traced as one scene, with both sections' panel coverages swept together; the farm radiators' reach swept on its own
- [x] Farm section's radiators: reach, layout, and how much of the drum's farm end they may shade (`thermal_model/layout.py`, `reports/heat_rejection.md`)
  - found: outboard of the farm rings (the baseline) the heat flows against spin gravity, so the loops need pumps; inboard (passive) the rings enclose the radiators: with LEDs they cool a six-stack's whole farm (~1.3× with three tiers lit; ~0.5–0.75× with sulfur lamps). Baseline: outboard pumped, with the inboard passive set as fallback; inboard alone now possible
  - found: reach ~0.45–0.5 r for 1.5× (six-stack, three tiers lit; ~0.75 r with sulfur lamps); at most ~9 + ~11 ha of panels per 900 m torus at 1.5× (~27 + ~42 with sulfur lamps)
- [ ] Full Monte Carlo ray tracing of the drum between hub and rims: radiators on the spokes, end openings, gap vents, shading by the farm rings and main rings
  - done: end openings, gap vents, farm rings and their radiators, the whole stack as one scene (`habitat_model/cavity.py`); open: the spokes and cables, the envelopes' rounded inner faces
- [x] Check that no direct sunlight reaches the radiators (`thermal_model/sunlight.py`): none on the drum's panels below ~1.5° of axis tilt (the tori shade them, ends and gaps alike); the open farm section takes ~0.8% of its heat per degree at 1 AU, so the axis needs holding to a degree or two
- [x] Coolant loops (`thermal_model/coolant.py`): single-phase water, passive in the main section (~0.35 m pipes, ~0.6 m/s, ~0.55 kt per 900 m torus), pumped in the farm section (~0.3% of its heat); two-phase ammonia can't boil at the rim under its own liquid column (~1.9 MPa at 900 m) without throttling
- [x] Valley thermal model (`thermal_model/valley.py`): left to itself the valley swings ~2–4 K (baseline, wet) to ~4–11 K (dry canyon) over a 12 h day; wider swings need scheduled cooling
- [x] Output: capacity vs stack length with 0–3 farm tiers lit (40 tori or more at any tiers lit with LEDs, 900 m and 1.6 km alike; ~24 / 18 / 18 / 16 with sulfur lamps), radiator area per torus

**Changes the design if:** the end openings carry much less than ~1.6 GW for a 900 m stack, or six-stacks with two or three tiers lit don't fit.

**Status:** six-stacks with three tiers lit fit easily with LEDs (~5.0–5.2× in both sections), the farm radiators reaching ~0.5 r or more; the valleys' loops are passive, the farm's pumped with a passive fallback that now carries every tier (`reports/heat_rejection.md`). Open: the spokes and the envelopes' faces in the ray tracing, freezing at low load, hardware.

---

## 7. Second tier

**Why seventh:** the farm inputs set the population (light on the crops −17% / +25% on people per torus, wheat yield −7% / +25%) and the light delivery moves the array by under 10%; the closed atmosphere is a control question rather than a sizing one.

- [x] **Light-box and farm optics:** ray trace of the magnesium-oxide cavity, diffuser and light pipes (`optics_model/`, `reports/optics.md`): the pipes as ray classes along their length with a graded extractor, the light box and a farm tier traced across the pipes (diffuse rays, exact for long pipes)
  - the light box passes ~82% of the pipes' light to the floor (~75–85% estimated); the diffuser blends the stripes ~0.5 m below the pipes; a farm tier puts ~93% on the crops, within ~15% across a bed with the pipes ~0.6 m above the canopy at 2.5 m tier spacing
  - with the lamps' coupling into the pipes (~85%) and the pipes' own losses (~72% out of a 40 m pipe), both guesses, ~50% (valley) and ~57% (farm) of the lamps' light arrives with the pipes laid out for the power that needs, against ~75% / ~85% assumed: ~50% more lighting power and array, ~2–3× the radiator panels for 1.5×; the sizing is left unchanged until measured (plan §8)
- [x] **Closed atmosphere and ecology:** compartment model (`ecology_model/`, `reports/atmosphere.md`) of O₂, CO₂, N₂ and carbon across the farm, the valley's air and woodland, the soil (fast and slow pools), the people and leaks; the farm's air quasi-steady through the hub ducts
  - Biosphere 2 replayed (approximate, recalled figures): its O₂ loss takes ~1.2 µmol/m²/s of excess soil respiration, the CO₂ going into the concrete; the same in a torus shows as CO₂ within ~8 months
  - failure scenarios: one / two / all farm tiers dark reach the CO₂ limit in ~110 / ~36 / ~22 days (900 m), a soil burst is absorbed by the CO₂-fertilised crops, a 10 cm hole loses 10% of the air in ~19 days
  - buffer and control needs: the air holds ~5 years of O₂; a ~1 MW CO₂-to-O₂ recovery plant per 900 m torus holds the whole farm going dark (proposed); a new torus's imported organics need ~8 MW at first unless composted first (~1.4 MW, proposed)
  - open: water and humidity, trace gases, the nitrogen cycle, daily swings, the controls' failures; the algae (not yet in the model)

**Status:** done. The closed atmosphere holds with a modest recovery plant; the startup soil is the hard case. The light box and the farm tiers deliver what the notes expected of them, but the light pipes' own losses, left out of the sizing, could cost ~50% more lighting power; ~1 kW sulfur lamps straight in the light box (no pipes, fed by 915 MHz sector plants) avoid them, at ~81% / ~89% delivered and ~130 MW per 900 m torus (`optics_model/architectures.py`). LEDs (white in the valley, blue + red in the farm) take ~66 MW and ~79 ha of array (ageing allowed for), ~430 t less PV silicon per torus; their materials are under 1% of the source bodies' content, indium for the red the tightest (`optics_model/leds.py`). Adopted, with a semiconductor works in every factory making the array, the LEDs and their drivers (notes §13); sulfur lamps in the box are the fallback. The system model is now sized for the LEDs (~3.0 / ~3.6 µmol/J at the fixtures' output, ~85% of it over their life, ~90% / ~100% delivered).

---

## 8. Earth tests (models can't settle these)

- [ ] **C-type baking (top of the ranking):** nitrogen recovery and energy per kg from CI-like meteorite or simulant. Recovery (50–90%) moves the C-type per torus by −22% to +40%; baking energy (1–2 MJ/kg) moves the processing energy by ±28%. Lab data, not a model, settles both.
- [ ] Growth-chamber trials of the working diet under blue + red LEDs (CO₂ ~1,000 ppm, 2.5 m tiers), especially lentils and flax, whose yields are estimates
- [ ] (Fallback only) non-rotating sulfur bulb at kW scale, fed by a 915 MHz source
- [ ] LED materials from asteroid simulant: gallium and indium recovered from a chondrite leach liquor, YAG:Ce from its rare earths, a GaN film grown from the recovered gallium
- [ ] LED strips behind a diffuser in a magnesium-oxide light box (the fixtures' efficiency and albedo are estimates); for the fallback, a ~1 kW sulfur lamp in a reflector behind a diffuser (its luminaire efficiency moves the power ~−5% / +10%); a lamp on a prism light pipe only if pipes come back (coupling, loss per metre, extractor: ±5–8 points each, `reports/optics.md`)
- [ ] Wire drawing from carbonyl-refined meteoritic iron, and from the as-separated metal for comparison (the wire's strength sets the spoke mass, section 2)
- [ ] Magnetic separation of free metal from L and LL chondrite material (meteorites or simulant)
- [ ] Partial-gravity health data (spaceflight, centrifuge studies)
- [ ] Growth chambers on 1.05–1.8-year cycles for candidate species

