# Torus habitat: validation plan

Check the design's load-bearing assumptions with models before going deeper. The parametric system model comes first: it recomputes the design notes' numbers from one set of assumptions and ranks them by how much they matter. That ranking sets the priorities for the detailed models.

**Order:** 1 → 2, 3 and 5 in parallel → 4 (needs the structural stiffness from 3) → 6. Section 7 lists what only Earth tests can settle.

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
- [x] **Materials and mining:** metal needed vs host class (H / L / LL free metal, optional iron from the silicates), shield rock from tailings, rock mined per torus; C-type sized by nitrogen (0.24 wt%, 70% recovery); trace-element budget (Cu, B, Sn…) per torus vs source bodies
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
- [ ] Rank the assumptions, then re-order sections 2–6 accordingly

### 1.5 Outputs
- [x] Markdown report that regenerates the §0 tables (so the notes' tables can come from the model)
- [x] JSON export for the 3D model's stats panel

**Status:** implemented in `habitat_model/` (see its README); reports in `reports/`. 185 of 197 checked figures within 5%, the rest rounding in the notes (`reports/validation.md`); ranking in `reports/sensitivity.md`, re-ordering sections 2–6 still to decide.

**Done when:** every key table in the notes is reproduced or corrected, and the assumptions are ranked by impact.

---

## 2. Radiation transport (the shield is ~85% of the mass)

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

## 3. Structure

- [ ] Finite-element model of one tube segment (CalculiX, FEniCS or sfepy):
  - rock cells and double skin
  - floor fill and hung ceiling cells
  - loads: 1 g spin and 70 kPa of air
- [ ] Cable net: chord geometry, tension distribution, taper, compliant joints
- [ ] Spin-up sequence: a partial ring with segments hung in opposite pairs, and the asymmetric loads on the way
- [ ] Hub held in the net by stabilising lines
- [ ] Wire from asteroid iron-nickel: literature on drawn pearlitic wire with nickel, cobalt, phosphorus and sulfur; achievable strength, creep and fatigue
- [ ] Output: steel per torus at 400 m / 900 m / 1.6 km / 2.5 km vs the r^2.3 estimate; stiffness for model 4

**Changes the design if:** the steel per torus differs from the r^2.3 estimate by more than ~30%, or ~1 GPa working stress isn't reachable with asteroid iron.

---

## 4. Stack dynamics

- [ ] Rigid stack with energy dissipation: margin vs number of tori and gaps
- [ ] Flexible stack: hub as a beam, tori as rings on cable nets; lowest bending modes vs spin rate for a pair and a six-stack
- [ ] Disturbances: docking, rim trains, ballast transfers, friction in the despun array's bearing, sunlight pressure on the array
- [ ] Tools: Python (scipy) multibody model, or modal analysis using model 3's stiffness
- [ ] Output: ratio of lowest mode to spin rate, damping needed, maximum tori

**Changes the design if:** a six-stack needs active control to stay stable, which would break the "nothing has to keep working" principle.

---

## 5. Heat rejection

- [ ] Monte Carlo ray tracing of the drum between hub and rims: radiators on the spokes, end openings, gap vents, shading by the farm rings and main rings
- [ ] Check that no direct sunlight reaches the radiators (Sun perpendicular to the axis, including through the gaps)
- [ ] Coolant loops: thermosiphon sizing along the spokes, fluids (ammonia, water), pressure drops
- [ ] Valley thermal model: day/night swing with the cold ceiling, wet vs dry valley
- [ ] Output: capacity vs stack length with 0–3 farm tiers lit, radiator area per torus

**Changes the design if:** the end openings carry much less than ~1.6 GW for a 900 m stack, or six-stacks with two or three tiers lit don't fit.

---

## 6. Second tier

- [ ] **Light-box and farm optics:** ray trace of the magnesium-oxide cavity, diffuser and light pipes. Check the ~75% (valley) and ~85% (farm) delivery, and the light uniformity at 2.5 m tier spacing
- [ ] **Closed atmosphere and ecology:** compartment model (ODEs) of O₂, CO₂, N₂, water and soil carbon across farm, valley, soil, people and algae
  - validate by replaying Biosphere 2 (O₂ from ~21% to ~14% in ~16 months)
  - failure scenarios: a farm tier dark, a soil respiration burst, a leak
  - output: buffer and control needs
- [ ] **Replication logistics:** stock-and-flow or discrete-event model of mining, factory throughput, shipping and imported vitamins per generation. Output: doubling time, and the share of each child habitat that is made locally

---

## 7. Earth tests (models can't settle these)

- [ ] Growth-chamber trials of the working diet under sulfur lamps (CO₂ ~1,000 ppm, 2.5 m tiers), especially lentils and flax, whose yields are estimates
- [ ] Non-rotating sulfur bulb at kW scale, fed by a 915 MHz source
- [ ] Wire drawing from meteoritic iron-nickel or a simulant
- [ ] Magnetic separation of free metal from L and LL chondrite material (meteorites or simulant)
- [ ] Partial-gravity health data (spaceflight, centrifuge studies)
- [ ] Growth chambers on 1.05–1.8-year cycles for candidate species
