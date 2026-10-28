# Self-Replicating Torus Habitat — Design Notes

Back-of-the-envelope design study for a family of self-replicating space habitats: steel tori spun for artificial gravity, built from asteroid materials by a factory in the central hub, inhabited by humans, plants and animals.

All numbers are first-order estimates. Assumptions are listed in each section and collected at the end for later revision. The changelog (section 20) tracks how the design evolved. The parametric model in `habitat_model/` (`plan.md` §1) recomputes the main tables from one assumptions file and ranks the assumptions by impact; `reports/validation.md` lists where it and these notes differ, and `structure_model/` holds the first structural results (`plan.md` §2).

**Guiding principles (adopted):**

1. **Simplest long-lasting design first.** Given how many unknowns remain, prefer designs where *nothing has to keep working* for the habitat to stay safe: no heavy bearings, no perpetual active control, no nested bodies needing station-keeping. (The one bearing, for the despun solar array, is light and slow, and the array still keeps the habitat alive if it locks.)
2. **Bulk materials come from the asteroids.** Every material used in large quantity must be sourced from the asteroids and be common enough to be gathered along with everything else, without becoming a limiting factor (section 10). Only true "vitamins" in small quantities may be imported. **The more common a material or source body, the better.**
3. **Conservative starting points.** Where the right value is unknown, design for the familiar or harder case and adapt later: 1 g, because healthy lower gravity is unknown (lower is better if it proves healthy); **L or LL host asteroids**, the best-studied candidates, though H-type hosts with ~4× the free metal are better (section 10); a **near-Earth location**, knowing the archipelago will spread through the Solar System later (with larger, concentrating solar arrays, or nuclear power if it ever passes the sourcing rule; section 13). **Promising but unproven options** (iron from the silicates by molten-oxide electrolysis, solar concentrators, lower gravity) are noted where they arise but not factored into the preliminary design.

---

## 0. Baseline design

| Item | Choice |
|---|---|
| Form | Co-rotating stack of an even number of tori on one shared hub: a pair, or 6 tori grouped A A B B C C (passively stable up to ~22–25 tori) |
| Size | **900 m / 60 s** or **1.6 km / 80 s** tori, width ratio r/w = 16; **2.5 km / 100 s** as a candidate for mature clusters (section 8, to decide) |
| Gravity | Structure rated for 1 g, run at whatever g proves healthy |
| Location | Near Earth, ~1 AU from the Sun, mining near-Earth asteroids; each cluster built at (and sharing the orbit of) its S-type "mine island"; spreading by seeds, not by moving habitats |
| Orientation | Spin axis perpendicular to the orbital plane, inertially fixed |
| Rotating interfaces | One, light: the despun solar array's bearing at one hub end (unpressurized, ~1 rpm, almost unloaded, power crossing it through a rotary transformer). The stack itself spins as one body; ships dock at the other hub end by matching the spin |
| Structure | Steel hull, cable spokes of high-carbon drawn steel wire, nickel cladding (proposed, to discuss: carbonyl process, tangent-chord spoke net) |
| Shield | ~5.5 m compartmentalised jacket of compacted rock (~11 t/m², mining tailings) carried by each torus, plus ~1 m soil/regolith fill under the floor; a double outer skin (thin meteoroid bumper over an empty ~1–2 m crawl space) for maintenance from inside |
| Atmosphere | 70 kPa, 29% O₂ (sea-level O₂ partial pressure, ~39% less nitrogen) |
| Interior light | Artificial overcast sky (sulfur plasma lamps); tori on staggered days (2 phases 12 h apart for a pair, 3 phases 8 h apart for 6); **seasonal sky** following the host asteroid's orbit, with no seasonal storage |
| Climate | One per habitat (all its valleys alike, connected for migration), set by the solar array's size, the lighting, the orbit's seasons, the water in the air and the night-time cooling. First sites: temperate, North-Atlantic-like, mild wet winters (~6–8 °C) and cool summers (~16–19 °C); temperature set by the coolant loops, independent of light |
| Heat | Coolant loops to radiators along the spokes, between the farm ring and the rim, in the drum between hub and rims; heat leaves through the stack's two open ends and the gaps |
| Power | Despun solar array on a mast at one hub end, always facing the Sun, sized for the valley's sky, the other loads and the farm tiers lit, so that even locked to the spinning stack it keeps the habitat alive and fed; separate free-flying solar array for industry |
| Materials | S-type asteroid (Fe-Ni grains for steel, silicate tailings for the shield) + small C-type asteroid (water, N, C, soil, P, K); M-types and comets optional; all bulk materials from these bodies |
| Interior | A natural narrow valley, anywhere from an arid canyon to a fern gully, its climate set per habitat by the solar array's size, the lighting, the orbit's seasons, the water in the air and the night-time cooling; ≥ 50% wilderness, cliff dwellings behind extra soil |
| Transport | Elevators in the spokes between hub and rim; a one-way antispinward train loop in a tube on the hub-facing side of each torus, joining the elevators; everything between 0 and 1 g |
| Food | Primarily plant-based: a farm ring in each torus's plane at ~0.4 r, three tiers under sulfur lamps and light pipes (potatoes, wheat, soybeans, lentils, berries, flax, greens), the number of tiers lit setting the population; the valley's permaculture and food forest add fruit, nuts, corn, squash and beans; algae, gas-fermented bacterial protein, mushroom + larvae cycle and aquaponics fish as supplements and margins; animal options kept as backups (proposed, to discuss: flooded taro/rice terraces, B12 fermentation) |

| Key numbers, per torus | 900 m / 60 s | 1.6 km / 80 s | 2.5 km / 100 s (candidate) |
|---|---|---|---|
| rpm / rim speed | 1.0 / 94 m/s | 0.75 / 126 m/s | 0.6 / 157 m/s |
| Tube width / floor area | 56 m / 32 ha | 100 m / 100 ha | 156 m / 245 ha |
| Rock shield (after fill credit) | ~11.0 Mt | ~33.5 Mt | ~80 Mt |
| Steel (spokes + hull + frames, excl. hub and factory) | ~1.2 Mt | ~6.0 Mt | ~22 Mt |
| Fill (soil + regolith) | ~0.54 Mt | ~1.7 Mt | ~4.2 Mt |
| Water (soil, O₂, lakes) | ~0.15 Mt | ~0.4 Mt | ~0.9 Mt |
| N₂ | ~8 kt | ~45 kt | ~170 kt |
| **Total** | **~12.8 Mt** | **~41.5 Mt** | **~108 Mt** |
| Mass per m² of floor | ~40 t | ~41 t | ~44 t |
| Mined per torus (S-type, H-like host + C-type) | ~14 + ~5–8 Mt | ~44 + ~27 Mt | ~165 + ~100 Mt |
| Valley lighting, daily average (sulfur lamps; ~15 mol/m²/day on the floor with the light-box ceiling) | ~53 MW | ~166 MW | ~410 MW |
| Farm ring at ~0.4 r: three tiers, crops per tier | ~9 ha | ~29 ha | ~70 ha |
| People fed, 1 / 2 / 3 tiers lit (conservative yields) | ~1,000 / ~2,000 / ~3,050 | ~3,250 / ~6,500 / ~9,750 | ~7,900 / ~15,800 / ~23,700 |
| Floor per person, 1 / 2 / 3 tiers lit | ~310 / ~155 / ~103 m² | ~310 / ~155 / ~103 m² | ~310 / ~155 / ~103 m² |
| Farm lighting, per tier lit | ~32 MW | ~102 MW | ~247 MW |
| Solar needed: valley + other loads, + per tier lit | ~57 + ~32 MW | ~180 + ~102 MW | ~440 + ~247 MW |
| Plain rim solar, for comparison | ~34 MW | ~110 MW | ~270 MW |
| Despun solar array at 1 AU (sized to keep the habitat alive and fed when locked): valley + per tier lit | ~0.27 + ~0.15 km² | ~0.85 + ~0.48 km² | ~2.1 + ~1.16 km² |
| Despun array with three tiers lit | ~0.71 km² | ~2.3 km² | ~5.6 km² |

| Stack of 900 m tori | Pair (A B) | Six (A A B B C C) |
|---|---|---|
| Floor area | 64 ha | 192 ha |
| Mass (excl. shared hub and factory) | ~26 Mt | ~77 Mt |
| Material mined (H-like host) | ~37 Mt | ~110 Mt |
| Stack length (10–40 m clear gaps between the envelopes) | ~160–220 m | ~480–660 m |
| People fed, 1 / 2 / 3 tiers lit | ~2,000 / ~4,000 / ~6,100 | ~6,000 / ~12,000 / ~18,300 |
| Constant valley lighting load (sulfur) | ~105 MW | ~315 MW |
| Farm lighting, per tier lit | ~64 MW | ~190 MW |
| Despun solar array at 1 AU: valley + per tier lit | ~0.53 + ~0.3 km² | ~1.6 + ~0.9 km² |
| Heat to reject with three tiers lit | ~310 MW | ~930 MW |
| Ideal limit of the two open ends (black bodies at ~285 K) | ~1.6 GW | ~1.6 GW |
| Drum maximum, preliminary radiative exchange (ends only; section 13) | ~1.2 GW | ~1.2 GW |

```
  sunlight ↓   (always perpendicular to the axis)

     (A)  (A)  (B)  (B)  (C)  (C)
      |    |    |    |    |    |
 ◀ [dock]══════════ hub ══════════[bearing]━━━━━━━━━━━━━━ ▶ spin axis → ecliptic north
      |    |    |    |    |    |                 └ despun solar array on its mast
     (A)  (A)  (B)  (B)  (C)  (C)                   (edge-on here: it faces the Sun)

  (A)…(C)  tori, tube sections: rock jacket under a double skin (bumper + crawl space);
           rim tunnels A–A, B–B, C–C
  |        spokes: farm rings (three lit tiers) at ~0.4 r, radiators between farm ring and rim
  heat leaves through both open ends ◀ ▶ and the gaps
  (section along the axis, not to scale; A noon, B dawn/dusk, C night, 8 h offsets)
```

The only moving parts left are pumps, elevators, the despun array's slow bearing and the spin itself, which nothing slows down in vacuum.

---

## 1. Rotation and the "1 g" radius/period family

Centripetal acceleration at the floor (outer rim) radius `r` for a rotation period `T`:

```
a = 4π² r / T²
```

Setting `r = (T/2)²` (r in metres, T in seconds) gives:

```
a = 4π² (T²/4) / T² = π² ≈ 9.87 m/s² ≈ 1.006 g
```

So every **even** period gives a perfect-square radius at 1 g.

Rim speed: `v = 2πr/T = πT/2` and `v² = g·r`.

| Period | Radius | rpm | Rim speed |
|---|---|---|---|
| 20 s | 100 m | 3 | 31 m/s |
| 40 s | 400 m | 1.5 | 63 m/s |
| 60 s | 900 m | 1.0 | 94 m/s |
| 80 s | 1.6 km | 0.75 | 126 m/s |
| 100 s | 2.5 km | 0.6 | 157 m/s |
| 120 s | 3.6 km | 0.5 | 188 m/s |
| 140 s | 4.9 km | 0.43 | 220 m/s |
| 160 s | 6.4 km | 0.375 | 251 m/s |
| 180 s | 8.1 km | 0.33 | 283 m/s |
| 200 s | 10 km | 0.3 | 314 m/s |
| 240 s | 14.4 km | 0.25 | 377 m/s |
| 300 s | 22.5 km | 0.2 | 471 m/s |
| 400 s | 40 km | 0.15 | 628 m/s |
| 600 s | 90 km | 0.1 | 942 m/s |

A round 1 km radius gives no round period (≈ 63.2 s).

---

## 2. Habitable floor area

Simplification: the curved floor width ≈ the torus tube width `w`.

```
A_floor = 2π r · w
```

### 2a. Fixed 100 m width (explored first)

`A = 200π r ≈ 628 r` (m²), i.e. `≈ 0.0628 r` ha.

| Period | Radius | r / w | Floor (m²) | Floor (ha) |
|---|---|---|---|---|
| 20 s | 100 m | 1 | 62,800 | 6.3 |
| 40 s | 400 m | 4 | 251,000 | 25 |
| 60 s | 900 m | 9 | 565,000 | 57 |
| 80 s | 1.6 km | 16 | 1,005,000 | ≈ 100 (1 km²) |
| 100 s | 2.5 km | 25 | 1,571,000 | 157 |
| 120 s | 3.6 km | 36 | 2,262,000 | 226 |
| 160 s | 6.4 km | 64 | 4,021,000 | 402 |
| 200 s | 10 km | 100 | 6,283,000 | 628 |
| 300 s | 22.5 km | 225 | 14,137,000 | 1,414 |
| 400 s | 40 km | 400 | 25,133,000 | 2,513 |
| 600 s | 90 km | 900 | 56,549,000 | 5,655 |

With 100 m fixed, `r/w = (T/20)²`. For reference, the Stanford Torus (1.79 km diameter, 130 m tube, 1 rpm) has r/w ≈ 7.

### 2b. Fixed ratio r/w = 16 (adopted design rule)

```
w = r/16
A_floor = 2π r · r/16 = π r² / 8
```

The geometry is self-similar, so the gravity difference across the floor is the same fraction at every size. If the floor spans the lower half of the tube, its edges sit at the tube's equator, a = r/32 closer to the axis, so gravity there is ~3% lower than at the centre line.

The floor areas below are horizontal projections (2πr·w); the curved surface is larger, but the steep parts near the edges become cliffs rather than usable ground.

| Period | Radius | Width | Floor (m²) | Floor (ha) |
|---|---|---|---|---|
| 20 s | 100 m | 6.25 m | 3,930 | 0.39 |
| 40 s | 400 m | 25 m | 62,800 | 6.3 |
| 60 s | 900 m | 56 m | 318,000 | 32 |
| 80 s | 1.6 km | 100 m | 1,005,000 | ≈ 100 |
| 100 s | 2.5 km | 156 m | 2,454,000 | 245 |
| 120 s | 3.6 km | 225 m | 5,089,000 | 509 |
| 140 s | 4.9 km | 306 m | 9,429,000 | 943 |
| 160 s | 6.4 km | 400 m | 16,085,000 | 1,608 |
| 180 s | 8.1 km | 506 m | 25,765,000 | 2,576 |
| 200 s | 10 km | 625 m | 39,270,000 | 3,927 |
| 240 s | 14.4 km | 900 m | 81,430,000 | 8,143 |
| 300 s | 22.5 km | 1.4 km | 198,800,000 | 19,880 |
| 400 s | 40 km | 2.5 km | 628,300,000 | 62,832 |
| 600 s | 90 km | 5.6 km | 3,180,900,000 | 318,086 |

---

## 3. Atmosphere

### 3a. Geometry

The tube has a circular cross-section with diameter = `w`:

```
a (tube radius)  = r/32
R (centre line)  = r − a = 31r/32
V (torus volume) = 2π² R a² ≈ 0.01867 r³
A_hull (surface) = 4π² R a  ≈ 1.195 r²      (≈ 3.04 × floor area)
```

### 3b. Reference: sea level, 80/20 N₂/O₂

```
M   = 0.8·28.01 + 0.2·32.00 = 28.81 g/mol
ρ   = P·M / (R_gas·T) = 101325 · 0.02881 / (8.314 · 288.15) ≈ 1.22 kg/m³
m_air ≈ 0.0228 r³  (kg)
```

By mass the mix is 77.8% N₂ and 22.2% O₂.

| Radius | Volume (m³) | Air mass | N₂ | O₂ |
|---|---|---|---|---|
| 400 m | 1.20 × 10⁶ | 1,460 t | 1,130 t | 323 t |
| 900 m | 1.36 × 10⁷ | 16,600 t | 12,900 t | 3,680 t |
| 1.6 km | 7.65 × 10⁷ | 93,200 t | 72,500 t | 20,700 t |
| 2.5 km | 2.92 × 10⁸ | 0.36 Mt | 0.28 Mt | 0.08 Mt |
| 3.6 km | 8.71 × 10⁸ | 1.06 Mt | 0.83 Mt | 0.24 Mt |
| 10 km | 1.87 × 10¹⁰ | 22.8 Mt | 17.7 Mt | 5.1 Mt |
| 40 km | 1.20 × 10¹² | 1.46 Gt | 1.13 Gt | 0.32 Gt |
| 90 km | 1.36 × 10¹³ | 16.6 Gt | 12.9 Gt | 3.7 Gt |

Air per m² of floor grows as `≈ 0.058 r` kg/m², compared with ~10,300 kg/m² for Earth.

### 3c. Design atmosphere: 70 kPa, 29% O₂ ("Quito")

Keep the O₂ partial pressure at its sea-level value (20.3 kPa under the 80/20 assumption) and remove only nitrogen.

| Total pressure | O₂ fraction | pN₂ | N₂ saved |
|---|---|---|---|
| 101.3 kPa | 20% | 81.1 kPa | — |
| 80 kPa | 25% | 59.7 kPa | −26% |
| **70 kPa** | **29%** | **49.7 kPa** | **−39%** |
| 60 kPa | 34% | 39.7 kPa | −51% |

Why 70 kPa / 29%:

- Lungs and Rubisco respond to partial pressure. People breathe sea-level oxygen (better than in Quito itself, which has ~15 kPa O₂), and plants see Earth-normal O₂.
- Flammability tracks the O₂ fraction. NASA's proposed spacecraft exploration atmosphere was 52.7–58.6 kPa with 30–34% O₂, selected partly with material flammability in view, and tests at those conditions showed materials ignite more easily than in normal air. 29% stays just below that range, but materials still need qualifying for it.
- Hull hoop stress ∝ P, so pressure-containment material drops by ~30%.
- Side effects: water boils at ~90 °C, and convective cooling is slightly weaker.

Resulting masses: O₂ is unchanged, N₂ is ×0.61, so total air is about 30% lighter. N₂ mass ≈ `1.086e-5 r³` t.

---

## 4. Volatiles: nitrogen and water

### Stoichiometry

```
2 NH₃ → N₂ + 3 H₂      1.216 kg NH₃ per kg N₂   (+0.22 kg H₂)
2 H₂O → 2 H₂ + O₂      1.126 kg H₂O per kg O₂   (+0.13 kg H₂)
```

Measured cometary NH₃/H₂O ratios range from ~0.1% to ~1.5% by number, with ~0.5–0.8% typical (Halley ~1.5%, Hale-Bopp ~0.7%, Hyakutake ~0.5%; 67P only ~0.06–0.15% in its coma). By mass the ratio is ~6% lower (NH₃ 17 vs H₂O 18 g/mol). The tables below assume **~1% by mass**, which is optimistic: at a more typical ~0.6%, the ice processed for nitrogen is ~1.7× larger. Some cometary nitrogen may also be locked in ammonium salts on the dust, which coma measurements miss.

Nitrogen is the scarce volatile. Argon is no more available, so it doesn't help.

### Air budget at 70 kPa / 29% O₂

| Radius | N₂ | O₂ | Total air | NH₃ needed | Ice processed (~1% NH₃) |
|---|---|---|---|---|---|
| 900 m | 7.9 kt | 3.7 kt | 11.6 kt | 9.6 kt | ~1.0 Mt |
| 1.6 km | 44,500 t | 20,700 t | 65,200 t | 54,000 t | ~5.8 Mt |
| 2.5 km | 0.17 Mt | 0.08 Mt | 0.25 Mt | 0.21 Mt | ~21 Mt |
| 3.6 km | 0.51 Mt | 0.24 Mt | 0.74 Mt | 0.62 Mt | ~66 Mt |
| 10 km | 10.9 Mt | 5.1 Mt | 15.9 Mt | 13.2 Mt | ~1.4 Gt |
| 22.5 km | 124 Mt | 58 Mt | 181 Mt | 151 Mt | ~16 Gt |
| 40 km | 0.70 Gt | 0.32 Gt | 1.02 Gt | 0.85 Gt | ~90 Gt |
| 90 km | 7.9 Gt | 3.7 Gt | 11.6 Gt | 9.6 Gt | ~1,000 Gt |

Comet 67P has a mass of ~10 Gt (9.98 × 10¹² kg, bulk density ~533 kg/m³), for scale.

Hydrogen by-product is useful as propellant or for reducing oxides.

---

## 5. Structure and radiation shielding

### 5a. Materials from asteroids

| Source | Yields | Processing |
|---|---|---|
| M-type | ~90% Fe, 5–10% Ni, Co, PGMs | native metal, no smelting |
| S-type / ordinary chondrite | 10–20% Fe-Ni grains | crushing, magnetic separation |
| C-type | carbon, hydrated clays, organics, N | thermal processing |

**Proposed (to discuss): steel by the carbonyl (Mond) process.**

- Nickel reacts with CO at ~50–60 °C and near-ambient pressure to form Ni(CO)₄, which decomposes back to metal at ~220–250 °C.
- Iron needs much harsher conditions: Fe(CO)₅ forms industrially at ~5–30 MPa of CO and ~150–200 °C, so the iron line requires pressure vessels. The decomposed product is high-purity "carbonyl iron".
- The result is near-net-shape parts deposited onto moulds, with modest energy use and easy automation.
- Both carbonyls are highly toxic (Ni(CO)₄ much more so), so the plant belongs in the uncrewed factory zone, isolated from the habitat atmosphere.
- CO comes from cometary CO/CO₂, or from carbon plus surplus O₂.
- Design values: working stress σ = 500 MPa (≈1 GPa ultimate, SF 2), ρ = 7,900 kg/m³.

**Alternative (not adopted):** pitch-based carbon fibre composite, σ = 1,000 MPa, ρ = 1,600 kg/m³. The usual PAN precursor contains nitrogen, which is the scarce resource. Stronger, but much harder to automate.

### 5b. Shielding requirement

- Early NASA studies used ~4.5 t/m² for 5 mSv/yr.
- Globus & Strout later recommend 20 mSv/yr for the general population and 6.6 mGy/yr for pregnancies. That needs **~11 t/m² of regolith or crushed rock** (~7 t/m² of water) in deep space.
- **Adopted: a rock jacket** of ~5.5 m of compacted crushed rock (~11 t/m², mining tailings), carried by each torus (section 5e). The first design used two steel hulls with a 7 m water jacket (section 5d, 17.21).
- Shield per m² of floor ≈ `11 × 3.04 ≈ 33 t/m²` before the fill credit, constant at every size because of the fixed ratio.
- **The jacket is compartmentalised** into cells. Under the floor, rock and fill press ~195 kPa on the outer hull, behind the double skin (section 13); at the ceiling, ~30 kPa net presses the ceiling down, so ceiling cells hang from frames tied to the outer hull, or the ceiling is vaulted.

### 5b′. Direction of the radiation: uniform shielding

| | Galactic cosmic rays | Solar particle events |
|---|---|---|
| Typical energy | 100s of MeV – GeV | mostly < 100 MeV |
| Direction | Isotropic | Anisotropic at first (arriving along the spiral interplanetary magnetic field, roughly 45–60° west of the Sun), then spreading |
| Timing | Continuous | Hours to days, occasionally |
| Shielding needed | ~11 t/m² of rock (~7 t/m² of water) for 20 mSv/yr (sets the design) | Far less: spacecraft storm-shelter designs use a few g/cm² (TransHab: ~6 cm water jacket) |

- Cosmic rays set the thickness and come from the whole sky, so the shield is the same in every direction.
- The 11 t/m² shield is far thicker than any solar storm requires, in every direction.
- The spin removes any sunward side anyway: no part of the rim faces the Sun for more than a fraction of a minute, and the faces never do.
- Grazing-angle particles cross more shield than straight-on ones, so uniform thickness is conservative.
- Micrometeoroids are mildly directional (more from the direction of orbital motion), but the double outer skin backed by metres of rock far exceeds what they require (section 13).
- Uniform thickness also means identical jacket cells all the way round: one segment design for the factory.

### 5c. Mass model (adopted: rock jacket, cable spokes)

Cable spokes of drawn steel wire (~1 GPa working stress, a safety factor of ~2 on the strongest bridge wire; section 12) carry the rim's load to the hub (section 12). The tangent-chord net weighs the same as these radial spokes (section 12). A uniform cable of length r holding a rim of mass M needs

```
M_spokes ≈ M · ρv² / (σ − ρv²/2)        (v = rim speed, ρ = 7,900 kg/m³, σ = 1 GPa)
```

~7% of the rim's mass at 900 m, ~13% at 1.6 km, ~22% at 2.5 km and ~32% at 3.6 km; it only diverges near ~26 km (v ≈ 500 m/s). Hull and frames are scaled as r^2.3, fitted to the 900 m and 1.6 km estimates.

The jacket has a finite thickness t (~5.5 m) outside the tube of radius a = w/2, so its volume is `2π² R [(a + t)² − a²]`, larger than the thin-shell `4π² R a t` by `1 + t/2a`: ~22% at 400 m, ~10% at 900 m, ~5.5% at 1.6 km. Under the floor's footprint the jacket is thinned by the fill's rock-equivalent (~0.9 m for 1 m of fill: regolith counts 1:1, the soil's water at the rock/water equivalence), on its outer face. Figures from the parametric model (`habitat_model/`).

| Radius | Rock shield (after fill credit) | Fill | Water + air | Hull and frames | Spokes | Total | Per m² of floor |
|---|---|---|---|---|---|---|---|
| 400 m | ~2.4 Mt | 0.11 Mt | 0.02 Mt | 0.05 Mt | 0.08 Mt | ~2.7 Mt | ~42 t |
| 900 m | ~11.0 Mt | 0.54 Mt | 0.14 Mt | 0.30 Mt | 0.87 Mt | ~12.8 Mt | ~40 t |
| 1.6 km | ~33.5 Mt | 1.7 Mt | 0.47 Mt | 1.1 Mt | 4.9 Mt | ~41.5 Mt | ~41 t |
| 2.5 km | ~80 Mt | 4.2 Mt | 1.26 Mt | 3.1 Mt | 19.1 Mt | ~108 Mt | ~44 t |
| 3.6 km | ~165 Mt | 8.6 Mt | 2.9 Mt | 7.3 Mt | 60 Mt | ~243 Mt | ~48 t |

(Water + air: water needed plus N₂ and O₂. The earlier thin-shell figures were ~2.2, 11.9, 40, 105 and 238 Mt, ~36–47 t per m².)

### 5d. First design: water jacket and self-supporting ring (reference)

*Computed for the first design: a 7 m water jacket (7 t/m²) in a ring that carries its load in hoop stress, without cable spokes. Superseded by the rock jacket and cable spokes (section 5e, 17.21); kept for reference.*

```
A_s · σ = (λ_water + λ_air + ρ·A_s) · v²  +  P·π a²

A_s = [ (λ_water + λ_air)·v² + P·π a² ] / (σ − ρ·v²)

with  v² = g·r,
      λ_water = 7000 · 2π a ≈ 1374 r   (kg/m)
      λ_air   ≈ 0.0026 r²              (kg/m)
```

Self-supporting limit (the denominator → 0): `r_max = σ / (ρ g)`, 6.4 km for steel at 500 MPa, 63 km for CFRP at 1,000 MPa.

| Radius | Hull thickness (combined) | Steel | Water | Air | Total |
|---|---|---|---|---|---|
| 400 m | 6 cm | 0.09 Mt | 1.34 Mt | 0.001 Mt | 1.4 Mt |
| 900 m | 15 cm | 1.1 Mt | 6.8 Mt | 0.01 Mt | 7.9 Mt |
| 1.6 km | 30 cm | 7.3 Mt | 21.4 Mt | 0.07 Mt | 29 Mt |
| 2.5 km | 58 cm | 34 Mt | 52 Mt | 0.25 Mt | 87 Mt |
| 3.6 km | 1.2 m | 142 Mt | 108 Mt | 0.74 Mt | 251 Mt |
| 4.9 km | 2.9 m | 667 Mt | 201 Mt | 1.9 Mt | 870 Mt |
| ≥ 6.4 km | — | diverges | — | — | not feasible |

CFRP (1,000 MPa), for comparison: 1.6 km ~22 Mt, 3.6 km ~115 Mt, 10 km ~1.0 Gt, 40 km ~40 Gt, diverging before 90 km. Weaker steel (250 MPa, plain carbonyl iron) took the 900 m ring from 1.1 to 2.7 Mt of steel and the 1.6 km ring from 7.3 to 22 Mt; cable spokes removed that margin problem.

### 5e. Rock shield instead of water (adopted)

Using Globus's equivalence (~11 t/m² of regolith for the protection of 7 t/m² of water), compacted crushed rock at ~2 t/m³, cable spokes at 1 GPa, and the 1 m floor fill credited in both cases (~1.8 t/m² of rock-equivalent under the floor). The rock column uses the jacket's finite thickness (section 5c); the water column is the first design's thin-shell estimate:

| | Rock jacket (11 t/m², adopted) | Water jacket (7 t/m², first design) |
|---|---|---|
| Thickness | ~5.5 m | 7 m |
| Shield mass, 900 m torus | ~11.0 Mt | ~6.5 Mt |
| Spoke steel, 900 m | ~0.87 Mt | ~0.5 Mt |
| **Total, 900 m** | **~12.8 Mt** | **~7.8 Mt** |
| **Total, 1.6 km** | **~41.5 Mt** | **~26 Mt** |
| Mass per m² of floor | ~40–41 t | ~24–26 t |
| Water needed per 900 m torus | ~0.15 Mt (soil, O₂, lakes) | ~6.5 Mt |
| C-type rock baked for volatiles | ~2–5 Mt | ~100 Mt |
| Baking energy | ~5 × 10¹⁵ J (~2 months at 1 GW) | ~1.5 × 10¹⁷ J (~5 years at 1 GW) |
| **Total mass mined and moved per 900 m torus** | **~18–21 Mt** (H or L host) | **~100 Mt** |
| Freezing | None | Risk on exposed surfaces |
| Net load on the ceiling hull | ~30 kPa pressing the ceiling down | ~0 (water weight ≈ air pressure) |
| Load on the outer hull under the floor | ~195 kPa | ~156 kPa |
| Corrosion inside the jacket | Dry | Wet |

**The habitat gets ~50–60% heavier, but ~5× less material is mined and moved per torus, and the energy for volatiles drops ~30×.** Building the jacket and spokes heavier is far cheaper than baking ~100 Mt of clay for its water.

Design consequences:

- **One S-type body supplies metal and shield.** Ordinary-chondrite (S-type) material holds ~10–20% metal grains: ~12 Mt (a rubble pile ~220 m across) gives ~1.2–2.4 Mt of Fe-Ni plus ~10 Mt of silicate tailings, which is the shield. For 1.6 km, ~40 Mt (~340 m) gives ~6 Mt of metal and ~34 Mt of tailings. S-types are the most common near-Earth asteroids.
- **Ceiling.** The water jacket nearly balanced the air pressure at the ceiling; rock doesn't. Ceiling cells hang from frames tied to the outer hull, or the ceiling is vaulted.
- **Ballast.** Jacket water doubled as pumpable ballast; with rock, dedicated (small) ballast tanks are needed.
- **Secondary neutrons.** Rock produces more than water. A thin hydrogen-rich inner layer (moist soil, irrigation water, algae tanks) helps. Hydrated C-type rock with bound water and organics would shield better than lunar regolith per tonne, so 11 t/m² is conservative.
- **Size.** With cable spokes there's no hard divergence like the self-supporting ring's 6.4 km limit. Spoke steel grows with radius (~7% of the rim's mass at 900 m, ~22% at 2.5 km), so the mass per m² of floor rises only slowly (~37 t at 900 m, ~43 t at 2.5 km; section 5c); size is limited by nitrogen and replication speed instead (section 8).
- **Interior space.** The thinner jacket gives ~1.5 m more interior radius for the same outer tube, which matters most for small sizes.
- **Energy no longer sets the generation time.** Crushing and separating ~12 Mt of S-type rock takes ~10¹⁵ J (weeks at 1 GW), and baking the small C-type is similar; logistics and factory throughput become the pacing items.

---

## 6. Soil and regolith fill (1 m under the floor)

| Material | Bulk density | 1 m layer |
|---|---|---|
| Moist agricultural soil (~25% water by volume) | ~1.6 t/m³ | 1.6 t/m² |
| Regolith / mine tailings | ~1.8 t/m³ | 1.8 t/m² |
| Mix 0.5 m + 0.5 m | | ~1.7 t/m² |

Shielding equivalence (Globus: 7 t water ≈ 11 t regolith), so 1 t regolith ≈ 0.64 t water:

| Layer | Mass | Water-equivalent |
|---|---|---|
| 1 m water | 1.0 t/m² | 1.0 t/m² |
| 1 m regolith | 1.8 t/m² | ~1.15 t/m² |
| 1 m moist soil | 1.6 t/m² | ~1.2 t/m² |
| 1 m mix | 1.7 t/m² | ~1.17 t/m² |

A metre of fill shields like ~1.84 t/m² of the rock jacket, so the jacket under the floor shrinks from ~5.5 m to ~4.6 m:

| Radius | Floor | Fill mass | Rock jacket it replaces | Net |
|---|---|---|---|---|
| 400 m | 6.3 ha | 0.11 Mt | 0.12 Mt | ~0 |
| 900 m | 32 ha | 0.54 Mt | 0.59 Mt | −0.05 Mt |
| 1.6 km | 100 ha | 1.7 Mt | 1.85 Mt | −0.15 Mt |
| 2.5 km | 245 ha | 4.2 Mt | 4.5 Mt | −0.3 Mt |
| 3.6 km | 509 ha | 8.7 Mt | 9.4 Mt | −0.7 Mt |

(With the first design's water jacket, the same fill replaced ~0.37 Mt of water at 900 m, ~1.2 Mt at 1.6 km.) The fill presses ~17 kPa on the floor at 1 g. Irrigation water, ponds and lakes count as shielding too.

---

## 7. Water and nitrogen balance

With the rock jacket, water is a small need and **nitrogen sizes the C-type** (section 10):

| Radius | Water needed (soil, O₂, lakes) | + spin-up with water thrusters | N₂ | C-type sized by nitrogen | Water it contains (~6.4%) |
|---|---|---|---|---|---|
| 900 m | ~0.15 Mt | ~0.37 Mt | 8 kt | ~5 Mt | ~0.32 Mt |
| 1.6 km | ~0.4 Mt | ~1.7 Mt | 45 kt | ~27 Mt | ~1.7 Mt |
| 2.5 km | ~0.9 Mt | ~5.5 Mt | 170 kt | ~100 Mt | ~6.5 Mt |

Water is in excess, except at 900 m with water spin-up (the C-type grows to ~8 Mt, or spin-up uses rock in a mass driver, section 15). Spin-up propellant with water thrusters: `m_p ≈ M·v/vₑ`, ~3–5% of the habitat at vₑ ≈ 3 km/s.

### 7b. First design: water jacket (reference)

*Computed for the 7 m water jacket (17.21), when water drove the mining and nitrogen came in excess.*

```
Water needed ≈ shield − fill substitution + soil water + O₂ electrolysis
             ≈ 7.96 r² + 5.7e-6 r³   (t)

Water from the ammonia hunt (ice processed at ~1% NH₃)
             ≈ 1.4e-3 r³             (t)

Break-even: r ≈ 5.7 km   (at 1% NH₃; ≈ 3.4 km at a more typical 0.6%)
```

| Radius | Water needed | Water from NH₃ hunt | Ratio | Balance |
|---|---|---|---|---|
| 400 m | 1.27 Mt | 0.09 Mt | 0.07 | −1.2 Mt |
| 900 m | 6.4 Mt | 1.0 Mt | 0.16 | −5.4 Mt |
| 1.6 km | 20.4 Mt | 5.8 Mt | 0.28 | −14.6 Mt |
| 3.6 km | 103 Mt | 66 Mt | 0.63 | −38 Mt |
| ~5.7 km | | | 1.0 | break-even |
| 10 km | 0.80 Gt | 1.4 Gt | 1.75 | +0.6 Gt |
| 40 km | 13 Gt | 90 Gt | 6.9 | +77 Gt |

---

## 8. Choosing the size

Rock jacket and cable spokes (section 5c):

| Radius | Total per torus | Per m² of floor |
|---|---|---|
| 400 m | ~2.7 Mt | ~42 t |
| 900 m | ~12.8 Mt | ~40 t |
| 1.6 km | ~41.5 Mt | ~41 t |
| 2.5 km | ~108 Mt | ~44 t |
| 3.6 km | ~243 Mt | ~48 t |

**Little economy of scale, and only a slow penalty.** The shield costs ~35 t per m² of floor at most sizes (more at 400 m, where the jacket is thick compared with the tube), and cable spokes keep the structure's share modest up to a few km. What grows with size, per m² of floor, is the air column (∝ r), and with it nitrogen and the C-type; then the steel share, until metal rather than shield rock sizes the S-type. Rotation comfort (< 2 rpm) and gravity gradient (~0.5% over body height at 400 m) are fine at every size here.

**Comparison of the candidate sizes:**

| | 900 m / 60 s | 1.6 km / 80 s | 2.5 km / 100 s (candidate) |
|---|---|---|---|
| rpm, rim speed | 1.0, 94 m/s | 0.75, 126 m/s | 0.6, 157 m/s |
| Coriolis, running at 5 m/s | ±11% of weight | ±8% | ±6% |
| Tube width = valley width and height | 56 m | 100 m | 156 m |
| Floor / wilderness (≥ 50%) | 32 ha / ~16 ha | 100 ha / ~50 ha | 245 ha / ~120 ha |
| Wilderness in a six-stack | ~96 ha | ~300 ha | ~735 ha |
| People fed per torus, 1 / 2 / 3 farm tiers lit (conservative) | ~1,000 / ~2,000 / ~3,050 | ~3,250 / ~6,500 / ~9,750 | ~7,900 / ~15,800 / ~23,700 |
| Farm ring at 0.4 r: ring area / crops per tier (three tiers) | ~11 ha / ~9 ha | ~36 ha / ~29 ha | ~88 ha / ~70 ha |
| Mass per torus / per m² | ~12.8 Mt / ~40 t | ~41.5 Mt / ~41 t | ~108 Mt / ~44 t |
| Steel per torus / per m² | ~1.2 Mt / ~3.7 t | ~6.0 Mt / ~6.0 t | ~22 Mt / ~9 t |
| Air per m² of floor (buffer against drift) | ~37 kg | ~65 kg | ~100 kg |
| Nitrogen per torus / per m² | 8 kt / 25 kg | 45 kt / 45 kg | 170 kt / 70 kg |
| C-type per torus (sized by nitrogen) | ~5 Mt (~200 m) | ~27 Mt (~350 m) | ~100 Mt (~540 m) |
| Tori per Ryugu-sized C-type (~450 Mt) | ~90 | ~17 | ~4.5, less than a six-stack |
| S-type per torus | ~14 Mt, sized by the shield | ~44 Mt, shield and metal nearly balanced | ~165 Mt, sized by the metal (~28 Mt) if H-like; ~2× for an L host, ~4× for LL, unless iron comes from the silicates |
| Lighting (sulfur, daily average): valley + per farm tier lit | ~53 + ~32 MW | ~166 + ~102 MW | ~410 + ~247 MW |
| Despun array at 1 AU (survival sizing): valley + per tier lit | ~0.27 + ~0.15 km² | ~0.85 + ~0.48 km² | ~2.1 + ~1.16 km² |
| Material mined per torus (H-like host) | ~18 Mt (1×) | ~71 Mt (~4×) | ~265 Mt (~15×) |

**2.5 km (candidate, to decide):**
- **Structurally fine.** At 157 m/s the spoke cables' own spin stress is only ~10% of their working stress; spokes take ~22% of the rim's mass, and the mass per m² of floor is only ~8% above 1.6 km.
- **What it buys:** a valley 156 m wide and tall (taller trees, room for real weather), ~120 ha of wilderness per torus and ~735 ha in a six-stack (the most robust biosphere), three times the air per m² of a 900 m torus to buffer the atmosphere against drift (Biosphere 2's problem, section 16), slower spin and weaker Coriolis.
- **What it costs:** nitrogen grows with the air column, ~70 kg per m² of floor, so a torus needs ~100 Mt of C-type and a Ryugu-sized partner supports fewer than one six-stack; the S-type becomes metal-bound (~150–180 Mt per torus, so Itokawa- or Apophis-sized hosts are out, Eros is fine); each generation moves ~15× the material of a 900 m torus, so the archipelago replicates more slowly.
- **Fit:** a later step for mature clusters with a large C-type (or comet) partner, after the 1.6 km stacks. Lower pressure or better nitrogen recovery would ease it. A seed factory builds it on site, like the 1.6 km stacks (its 156 m segments are too wide for a smaller parent's dock).

**Shortlist: 900 m / 60 s and 1.6 km / 80 s, with 2.5 km / 100 s as a candidate (to decide).** 400 m remains possible with thicker steel, less mass, and people sleeping and working in extra-shielded zones. Steel is a poor cosmic-ray shield per tonne (secondary neutrons), so hydrogen-rich layers should protect the living zones.

Replication favours small units: shorter cycles, faster doubling of total floor area, and redundancy.

*(First design, water jacket and self-supporting ring, for reference: 1.4 Mt at 400 m, 7.9 Mt at 900 m, 29 Mt at 1.6 km, 87 Mt at 2.5 km, 251 Mt at 3.6 km, 870 Mt at 4.9 km, i.e. ~23, ~25, ~29, ~36, ~50 and ~93 t per m² of floor; section 5d.)*

---

## 9. Reduced gravity

The radius is kept fixed and the spin slowed: `T(g) = T(1 g) / √g`. Structural load ∝ g; shielding, fill and air are unchanged. Rock jacket and cable spokes; hull and frames are floored at ~30% of their 1 g mass (minimum gauge):

| Radius | g | Period | rpm | Steel | Shield, fill, water, air | Total |
|---|---|---|---|---|---|---|
| 900 m | 1.0 | 60 s | 1.0 | 1.17 Mt | 11.6 Mt | 12.8 Mt |
| | 0.9 | 63 s | 0.95 | 1.05 Mt | 11.6 Mt | 12.7 Mt |
| | 0.3 | 110 s | 0.55 | 0.34 Mt | 11.6 Mt | 12.0 Mt |
| | 0.15 | 155 s | 0.39 | 0.21 Mt | 11.6 Mt | 11.9 Mt |
| 1.6 km | 1.0 | 80 s | 0.75 | 6.0 Mt | 35.5 Mt | 41.5 Mt |
| | 0.9 | 84 s | 0.71 | 5.4 Mt | 35.5 Mt | 40.9 Mt |
| | 0.3 | 146 s | 0.41 | 1.7 Mt | 35.5 Mt | 37.2 Mt |
| | 0.15 | 207 s | 0.29 | 1.0 Mt | 35.5 Mt | 36.5 Mt |
| 2.5 km | 1.0 | 100 s | 0.6 | 22.3 Mt | 85.4 Mt | 107.6 Mt |
| | 0.9 | 105 s | 0.57 | 19.8 Mt | 85.4 Mt | 105.2 Mt |
| | 0.3 | 183 s | 0.33 | 6.1 Mt | 85.4 Mt | 91.5 Mt |
| | 0.15 | 258 s | 0.23 | 3.5 Mt | 85.4 Mt | 88.9 Mt |

The shield dominates, so lower gravity saves little mass: ~6% at 900 m, ~10% at 1.6 km, ~15% at 2.5 km for 0.3 g. The spoke cables' own limit, `r_max ≈ 2σ/(ρg)`, is ~26 km at 1 g.

*(First design, water jacket and self-supporting ring: 1.43 / 1.37 Mt at 400 m for 1 / 0.3 g, 7.9 / 7.1 Mt at 900 m, 28.7 / 23.3 Mt at 1.6 km; its steel limit `σ/(ρg)` was 6.4 km at 1 g, 21 km at 0.3 g.)*

**Strategy (adopted):** design for 1 g and run at whatever g proves healthy. The first habitats become the long-term gravity experiment.

---

## 10. Raw materials and source bodies

### Bill of materials (rock shield, 1 g, steel, 70 kPa, 1 m fill)

| Need | 900 m | 1.6 km | 2.5 km (candidate) |
|---|---|---|---|
| Steel (spokes, hull, frames) | ~1.2 Mt | ~6.0 Mt | ~22 Mt |
| + hub, dock, factory (guess) | ~1.5 Mt total metal | ~7.5 Mt total metal | ~28 Mt total metal |
| Rock for the shield (after fill credit) | ~11.0 Mt | ~33.5 Mt | ~80 Mt |
| Regolith (0.5 m of the fill) | 0.29 Mt | 0.9 Mt | 2.2 Mt |
| Soil (0.5 m of the fill) | 0.25 Mt | 0.8 Mt | 2.0 Mt |
| Water (soil, O₂, lakes) | ~0.15 Mt | ~0.4 Mt | ~0.9 Mt |
| Spin-up propellant (if water thrusters, vₑ ≈ 3 km/s) | ~0.40 Mt | ~1.7 Mt | ~5.6 Mt |
| Nitrogen (as N₂) | 8 kt | 45 kt | 170 kt |
| Carbon | ~15 kt | ~35 kt | ~85 kt |

Sphere diameter from mass: `d = (6 M / (π ρ_bulk))^(1/3)`

### S-type (ordinary chondrite, rubble pile ~2 t/m³) — metal and shield (adopted)

Ordinary-chondrite material holds Fe-Ni metal grains, recovered by crushing and magnetic separation; the silicate tailings become the shield and the regolith fill. **How much metal depends on the class**, and the candidate hosts are not the metal-rich kind:

| Ordinary-chondrite class | Total iron | Free metal | Rock per 900 m torus's ~1.5 Mt of metal | Candidate hosts |
|---|---|---|---|---|
| H (high iron) | ~28 wt% | ~8.4 vol% (~17 wt%) | ~9 Mt (less than the ~11 Mt of shield rock) | none of the candidates |
| L (low iron) | ~22 wt% | ~4.1 vol% (~9 wt%) | ~16 Mt | Didymos (L), Eros (L or LL) |
| LL (low iron, low metal) | ~19 wt% | ~2 vol% (~4–5 wt%) | ~32 Mt | Itokawa, Apophis, Eros (L or LL) |

(Iron and metal by volume from the ordinary-chondrite review cited in the sources; weight percentages converted with metal at ~7.9 t/m³ and grain densities of ~3.6–3.8 t/m³.)

- **The design must work with L or LL hosts; H is better** (principle 3). With an L or LL host, metal rather than shield rock sizes the S-type mining, by ~1.5× (L) to ~3× (LL) at 900 m. Two ways to get the metal (iron from the silicates, below):
  - **On a large host (Eros, Didymos): mine more rock.** Crushing and magnetically separating ~32 Mt of LL rock instead of ~11 Mt takes only ~3 × 10¹⁵ J; the extra ~20 Mt of tailings becomes ballast or spare shield. By far the simplest.
  - **On a small host (Itokawa, Apophis): in the preliminary design, free metal only**, so the host supports fewer tori (Itokawa ~1, Apophis ~1–2) unless metal is brought in from a larger L/LL host or an M-type. Taking the iron out of the silicates (below) would restore them, but it is not factored in yet.
- The sizing table below assumes H-like metal; with an LL host, free metal alone needs ~32 Mt per 900 m torus, ~165 Mt per 1.6 km torus and ~620 Mt per 2.5 km torus.

| | 900 m | 1.6 km | 2.5 km (candidate) |
|---|---|---|---|
| Body mass (H-like metal, ~17 wt%) | ~14 Mt | ~44 Mt | ~165 Mt |
| Diameter | ~235 m | ~350 m | ~540 m |
| Metal used | ~1.5 Mt (of ~2.3 Mt available) | ~7.5 Mt | ~28 Mt |
| Silicate tailings | ~11.3 Mt | ~37 Mt (the shield and regolith need ~34 Mt) | ~136 Mt (the shield and regolith need ~83 Mt) |
| Sized by | the shield | the metal, nearly balanced | the metal |

S-types are the most common near-Earth asteroids, and one body covers both the steel and the shield.

### Iron from the silicates (investigated)

LL rock holds ~19 wt% iron, but only ~4–5 wt% as free metal; most of the rest is iron oxide in olivine and pyroxene (LL silicates are the most iron-rich of the three classes), some in troilite. Ways to reduce it:

| Process | How | Works on olivine? | Inputs vs. the sourcing rule | Status |
|---|---|---|---|---|
| **Hydrogen reduction** | H₂ at 900–1,100 °C, water electrolysed back to H₂ and O₂ | **No:** NASA tests reduced ilmenite completely but olivine and pyroxene only in sparse traces | local | rejected for ordinary chondrites |
| **Molten-oxide electrolysis** (proposed) | the rock melted at ~1,600 °C and electrolysed directly; iron, the easiest oxide to reduce, comes off first as liquid metal, oxygen at the anode | **yes:** the whole melt is the electrolyte | chromium-iron alloy anode (~90% Cr) protected by a chromium-aluminium oxide layer; chromium is in the C-type clays (~13 kt per 900 m torus's C-type); flux from the rock itself | demonstrated at laboratory scale (2013); developed for carbon-free steelmaking on Earth |
| **Molten-salt electro-deoxidation** (FFC process) | solid rock as the cathode in molten calcium chloride at ~950 °C | yes: ~96% of the oxygen removed from lunar regolith simulant in ~50 h | calcium and chlorine local; the anode is the open question | gives a mixed alloy (iron, silicon, aluminium…), not steel, so it needs refining |
| **Carbothermal reduction** | carbon or methane on the melt at ~1,600 °C, carbon recycled from the CO | yes | carbon recycled | studied for lunar oxygen; hot and complex |

- **Molten-oxide electrolysis is the best fit:** one step, liquid iron straight to casting, no chemicals to import, and it runs on the same solar heat and electricity as the rest of the factory.
- **Energy (estimate):** the thermodynamic minimum for iron oxide is ~5 MJ per kg of iron; with losses, ~7–14 MJ of electricity per kg, plus solar-furnace heat to melt ~8–9 kg of rock per kg of iron (~2 MJ per kg of rock, partly recovered from the hot slag). For the ~0.9 Mt of iron an LL-hosted 900 m torus lacks: ~0.6–1.3 × 10¹⁶ J of electricity (~2.5–5 months at 1 GW) plus a similar amount of furnace heat.
- **Oxygen by-product:** ~0.26 Mt per 0.9 Mt of iron, ~70× the oxygen in a 900 m torus's air. Useful as reaction mass, or combined with C-type hydrogen into water.
- **Nickel and cobalt follow the iron:** their oxides are less stable than iron oxide (standard thermodynamics), so they are reduced first and end up in the metal, as in the free metal grains.
- **Status: a likely better option, not factored into the preliminary design.** The numbers that matter aren't public yet: anode life at ~1,600 °C (lab tests ran for hours), energy per tonne and current efficiency at scale. Boston Metal's pilot campaigns made ~10 kg of iron, and its week-long endurance runs fell short of their targets (2023); it commissioned an industrial-scale cell in 2025 and plans a demonstration plant in 2026. NASA has run the same direct electrolysis on molten lunar-regolith simulants near 1,600 °C, producing iron and silicon with oxygen at the anode. The preliminary design uses free metal only (magnetic separation, proven on Earth) and revisits this when industrial data appear.

### M-type (bulk ~5 t/m³, ~80% metal) — optional

An optional metal-rich supplement to the S-type, sized here to supply all the metal:

| | 900 m | 1.6 km | 2.5 km (candidate) |
|---|---|---|---|
| Body mass | ~1.8 Mt | ~9 Mt | ~34 Mt |
| Diameter | ~90 m | ~150 m | ~235 m |
| Tailings | ~0.35 Mt | ~1.8 Mt | ~7 Mt |

The tailings cover the regolith fill.

### C-type (Bennu-like: ~1.2 t/m³) — volatiles and soil base

Bennu samples: ~4.5 wt% carbon, ~0.23–0.25 wt% nitrogen, ammonia-rich. Water is bound in hydrated phyllosilicates: remote sensing gives ~0.71 wt% hydrogen at the surface, equivalent to **~6.4 wt% water**, assumed recoverable by heating.

With the rock shield, the C-type is **sized by nitrogen**, as in the original analysis a decade ago:

| | 900 m | 1.6 km | 2.5 km (candidate) |
|---|---|---|---|
| Nitrogen needed (N₂) | 8 kt | 45 kt | 170 kt |
| C-type mass (~0.24% N, ~70% recovered) | ~5 Mt | ~27 Mt | ~100 Mt |
| Diameter | ~200 m | ~350 m | ~540 m |
| Water contained (6.4%) | ~0.32 Mt (needs ~0.15 Mt + spin-up) | ~1.7 Mt (needs ~0.4 Mt + spin-up) | ~6.5 Mt (needs ~0.9 Mt + spin-up) |
| Carbon contained | ~0.2 Mt | ~1.2 Mt | ~4.5 Mt |

If spin-up uses water thrusters (~0.37 Mt at 900 m, ~1.7 Mt at 1.6 km, ~5.5 Mt at 2.5 km), the 900 m C-type grows to ~8 Mt; at 1.6 km and 2.5 km the nitrogen-sized body roughly covers it.

A C-type also supplies a soil base (clays, organics, P, K, S) and sulfur for the lamps. Its clays carry ~1% nickel and ~0.27% chromium, so making soil means leaching them out, which recovers useful nickel, chromium and cobalt.

*(Water-jacket design, for reference: ~100 Mt of C-type per 900 m torus and ~320 Mt per 1.6 km torus were needed for the shield water.)*

### Comet (67P-like: ~0.5 t/m³, ~30% ice, ~1% NH₃) — optional

Sized by nitrogen, at the optimistic ~1% NH₃ (~1.7× larger at a typical ~0.6%):

| | 900 m | 1.6 km | 2.5 km (candidate) |
|---|---|---|---|
| NH₃ needed | ~10 kt | ~54 kt | ~210 kt |
| Nucleus mass (~30% ice) | ~3 Mt | ~18 Mt | ~69 Mt |
| Diameter | ~230 m | ~410 m | ~640 m |

Logistically hard: most known nuclei are km-scale, and comets have awkward orbits. Comets mattered for the water jacket (ice yields water for a few MJ/kg, 5–10× less energy than baking clays); with the rock shield they are a minor option.

**Adopted: S-type (metal + shield) + small C-type (volatiles, soil); M-types and comets optional.**

### Sourcing rule check

Every bulk material against what one 900 m torus's source bodies contain (~12 Mt S-type, ~5 Mt C-type). C-type figures use Ryugu's measured abundances (close to CI chondrites); S-type figures are ordinary-chondrite values (H for the major elements; the candidate hosts are L or LL, with less metal, nickel and cobalt). Sources and the full list are in the trace-element table below.

| Material | Rough need | Available (S-type / C-type) | Status |
|---|---|---|---|
| Iron (hull, wire, frames) | ~1.4 Mt | ~1.4 Mt as metal grains if H-like, ~0.5 Mt if LL-like (the rest as iron oxide in the silicates) / ~0.9 Mt in oxides and sulfides | ✓ H / ⚠ L, LL: more rock or iron from the silicates |
| Silicate rock (shield, regolith) | ~10.4 Mt | ~10.6 Mt tailings / — | ✓ (sets the S-type's size) |
| Nickel (cladding, Invar) | tens of kt | ~190 kt / ~50 kt | ✓ |
| Water | ~0.15 Mt (+ ~0.37 Mt if water spin-up) | — / ~0.32 Mt | ✓ / ⚠ with water spin-up |
| Nitrogen | 8 kt | — / ~12 kt (~8 kt recovered) | ⚠ sets the C-type's size |
| Carbon (steel, CO, organics) | ~20 kt | — / ~0.2 Mt | ✓ |
| Sulfur (lamps, chemistry) | small | troilite / ~0.27 Mt | ✓ |
| Silicon (glass, quartz, PV) | a few kt | ~2 Mt / ~0.5 Mt | ✓ (purity is a processing problem, not a scarcity) |
| Phosphorus (soil) | ~0.3 kt | ~13 kt / ~5 kt | ✓ |
| Potassium (soil, battery electrolyte) | a few kt | ~10 kt / ~2.7 kt | ✓ (needs leaching) |
| Copper (wiring, motors, magnetrons, waveguides, rotary transformer) | ~0.1–1 kt (guess) | ~1.1 kt / ~0.6 kt (measured: ~86–97 ppm in ordinary chondrites, 126 ppm in Ryugu), dispersed | ✓ if about half is recovered; ⚠ recovery |
| Cobalt + molybdenum (maraging wire) | ~70 kt Co + ~40 kt Mo | ~10 kt Co, ~25 t Mo / ~3 kt Co, ~5 t Mo | ✗ rejected |
| Gallium, indium (LEDs) | not bulk (kg) | ~65 t Ga, ~6–50 kg In / ~50 t Ga, ~0.4 t In, dispersed | contained; recovery makes them vitamins in practice |

Consequences:

- **Spokes use high-carbon drawn (pearlitic) steel wire**, the steel of bridge cables and piano wire: ~1.8–2 GPa ultimate from iron and ~0.8% carbon. Carbonyl iron is naturally sulfur-free, so little manganese is needed.
- **The wire needs refined iron, not the metal grains as mined.** Wire steel tolerates almost no phosphorus (≤ ~0.02%), sulfur (≤ ~0.015%) or nickel (≤ ~0.05% in tire cord; more suppresses the pearlite), while chondritic metal holds ~9% nickel or more, with phosphides and troilite alongside. The carbonyl process (section 14) removes all three: nickel leaves at low pressure, and carbonyl iron is > 99.5% pure. Drawing wire from the separated metal directly is not an option. Maraging steel (~18% Ni, ~9% Co, ~5% Mo) fails the rule because molybdenum is ~1–2 ppm in chondritic material (~30 t per torus's source bodies against ~40 kt needed).
- **Copper is used sparingly:** high-voltage power distribution, aluminium where practical (~0.85% of the C-type, but hard to reduce), iron or steel conductors for low-current runs, copper reserved for motors and magnetrons, careful recycling, and a leaching line for the dispersed copper (the same line that strips nickel and chromium from the soil clays).
- Everything else passes comfortably; the remaining imports are true vitamins (semiconductors, LED materials if chosen).

### Trace elements measured in the explored bodies

Ryugu's samples are the best-measured asteroid material: close to CI chondrites, "more chemically pristine" than any meteorite. Itokawa's samples are LL ordinary chondrite; Apophis's spectra are LL-like, Didymos's L-like, and NEAR found Eros consistent with L or LL chondrites (its surface sulfur depletion likely a space-weathering effect). Bennu's samples are CI-like too. S-type values below are ordinary-chondrite falls (medians of H, L and LL where given; "one H5" marks a single meteorite).

| Element | S-type (ordinary chondrite) | C-type (Ryugu, measured) | Contained in ~12 Mt S + ~5 Mt C | Use and status |
|---|---|---|---|---|
| Copper | 86–97 ppm | 126 ppm | ~1.1 kt + ~0.6 kt | wiring, motors, magnetrons, PV contacts; enough if about half is recovered |
| Nickel | ~1.6% (H; less in L, LL) | 1.19% | ~190 kt + ~59 kt | cladding, Invar, nickel-iron batteries |
| Cobalt | ~0.08% (H) | 582 ppm | ~10 kt + ~3 kt | by-product |
| Chromium | — | 2,681 ppm | — + ~13 kt | heat-resisting steels (receivers, furnaces) |
| Manganese | ~0.23% (H) | 2,489 ppm | ~28 kt + ~12 kt | steelmaking |
| Titanium | ~0.06% (H) | 474 ppm | ~7 kt + ~2.4 kt | not needed in bulk |
| Vanadium | — | 61 ppm | — + ~0.3 kt | alloying |
| Zinc | 46–55 ppm | 346 ppm | ~0.6 kt + ~1.7 kt | coatings |
| Phosphorus | ~0.11% (H) | 1,302 ppm | ~13 kt + ~6.5 kt | soil |
| Potassium | ~0.08% (H) | 522 ppm | ~10 kt + ~2.6 kt | soil, battery electrolyte |
| Sodium | ~0.6% (one H5) | 6,099 ppm | ~74 kt + ~30 kt | soda-lime glass, salts |
| Chlorine | — | 776 ppm | — + ~3.9 kt | silicon purification, chemistry |
| Boron | — | 1.33 ppm | — + ~6.7 t | PV doping (grams a year): available; MgB₂ superconductors (kilotonnes): not |
| Lithium | ~1.3 ppm (one H5) | 1.38 ppm | ~16 t + ~7 t | batteries (nickel-iron preferred) |
| Gallium | 5.1–6.0 ppm | 10 ppm | ~65 t + ~50 t | LEDs (kilograms): contained, recovery is the hard part |
| Germanium | 8–11 ppm | 33 ppm | ~120 t + ~165 t | electronics, infrared optics |
| Selenium | 8–9 ppm | ~20 ppm (CI) | ~100 t + ~100 t | — |
| Molybdenum | ~2 ppm (one H5) | 1.02 ppm | ~25 t + ~5 t | small alloying only; maraging steel fails |
| Tungsten | — | 0.125 ppm | — + ~0.6 t | lamp and magnetron cathodes (kilograms) |
| Tin | 0.33–0.59 ppm | 1.85 ppm | ~4–7 t + ~9 t | solder; a float-glass tin bath is out |
| Silver | 36–66 ppb | 0.195 ppm | ~0.4–0.8 t + ~1 t | PV contacts would need ~0.3 t a year: copper instead |
| Indium | ~0.5–4 ppb | ~78 ppb (CI) | ~6–50 kg + ~0.4 t | LEDs (grams) |
| Platinum, palladium, iridium, gold | — | 0.83, 0.74, 0.48, 0.16 ppm | — + ~4, ~4, ~2.4, ~0.8 t | catalysts (kilograms) |
| Neodymium, lanthanum | — | ~0.47, ~0.24 ppm (CI; Ryugu enriched and variable) | — + ~2.4, ~1.2 t | permanent magnets: tonnes at most, so wound-field machines |

- **Copper is not scarce, just dispersed:** ~1.7 kt per 900 m torus's source bodies, ~7 kt per 1.6 km torus, ~28 kt per 2.5 km torus, against a guessed need of ~0.1–1 kt per 900 m torus. At ~100 ppm it is ~50–100× leaner than terrestrial ore, but the rock is crushed and processed anyway, so recovery is the marginal cost of a leach line (sulfuric acid, electrowinning), the same line that strips nickel and chromium from the soil clays.
- **Most "vitamins" are present in tonnes; extraction, not abundance, makes them vitamins.** Boron for PV doping and the platinum-group catalysts are available outright; tin, silver, tungsten and rare earths only in tonnes, which rules out bulk uses (a float-glass tin bath, silver PV contacts, rare-earth magnets).

---

## 11. Orientation and stability

### Orientation (adopted)

The spin axis points **perpendicular to the orbital plane** (towards the ecliptic pole) and stays inertially fixed.

```
        ↑ spin axis (ecliptic north), same direction all year
        |
   ═══(hub)═══        ← torus seen edge-on
   ☉ →→→ rim          ← sunlight always arrives in the ring's plane
```

- **No precession torque.** The axis never needs to turn as the habitat orbits.
- **Gyroscopic stiffness helps** instead of hurting: it holds the orientation passively, like Earth's axis.
- **Both flat faces are never sunlit.** For a single torus they could carry radiators; in a stack the faces look at each other, so the radiators move onto the spokes (section 13).
- **The rim catches the sunlight.** The spin turns every part of the rim towards the Sun once per rotation, so each rim panel is lit half of every turn and averages ~1/π of full sunlight. With no axial tilt there are no seasons: the exposure is the same all year. The Sun always stays perpendicular to the axis, which is also what lets a despun array on the axis face it with one slow rotation (section 13, Power).
- **No sunward side.** No part of the rim faces the Sun for more than a fraction of a minute at a time, and the faces never do, so shielding and thermal design are uniform around the ring.
- **No despun parts.** Ships dock at the hub axis by matching the slow spin.
- **Spin is essentially free to maintain** in vacuum: small trim thrusters, or water mass moved inside, handle the rest.

### Passive spin stability

A body is only passively stable when spinning about its axis of maximum moment of inertia. Internal dissipation (sloshing lakes, moving people, flexing structure) drains any other spin into a tumble. Explorer 1, spun about its long (minimum-inertia) axis, changed its rotation axis soon after launch because of energy dissipation in its flexible structural elements.

- **Torus:** `I_axis = 2 × I_transverse`, so it is inherently stable.
- **Co-rotating stack of N tori**, radius r, pitch p (the envelope's diameter, tube + rock jacket + crawl space, plus the clear gap between envelopes), rigidly linked, with the spin-axis inertia exceeding the transverse one by a margin m:

```
N² − 1  <  12 (r/p)² · [ 1/(1+m) − 1/2 ]

m = 0     →  N² − 1 < 6 (r/p)²     (limit; stack length ≲ √6 · r ≈ 2.4 r)
m = 10%   →  N² − 1 < 4.9 (r/p)²
m = 20%   →  N² − 1 < 4.0 (r/p)²
```

With a 10 m clear gap, r/p ≈ 11 at 900 m and ≈ 13 at 1.6 km (the jacket doesn't scale with the tube, so the geometry is no longer exactly self-similar):

| | 900 m tori (p ≈ 80 m) | 1.6 km tori (p ≈ 124 m) |
|---|---|---|
| Absolute limit (no margin) | 27 tori | 31 tori |
| 10% margin | 24 tori (12 pairs) | 28 tori (14 pairs) |
| **20% margin** | **22 tori (11 pairs)** | **25 tori (12 pairs)** |
| Stack length at 20% margin | ~1.8 km (≈ 2 r) | ~3.1 km (≈ 2 r) |

Wider gaps lower the count (at 40 m gaps, ~16 tori of 900 m with a 20% margin), still far above the 2 or 6 of the baseline. (An earlier pitch of tube width + gap left no room for the jacket and gave 27 and 29 tori.)

- **Stiffness check (open).** The rule assumes the stack behaves as one rigid body. A long stack joined only by a slender hub has low-frequency bending modes; the hub axle or rim links must keep them well above the spin rate, a requirement that grows quickly with length.
- **Linking neighbours.** Co-rotating neighbours have no relative motion, so they can be linked at the axis and at the rim (tunnels joining the valleys).

---

## 12. Spokes and hub

### Spokes carry the load

The minimum tension-structure mass to hold M at rim speed v is the same for a hoop ring or radial spokes:

```
M_struct ≈ M · v² · ρ / σ
ring self-weight factor:  1 / (1 − ρv²/σ)
spoke taper factor:       exp(ρv² / 2σ)   (1 GPa wire: 1.04 at 900 m, 1.07 at 1.6 km;
                                           500 MPa plate: 1.07 and 1.13)
```

Spokes win in practice:

1. **Wire is stronger than plate.** Drawn high-carbon (pearlitic) steel wire reaches ~1.8–2 GPa from iron and carbon alone, so ~1 GPa working stress halves the load-carrying mass.
   - **Safety factor.** Bridge wire (~5 mm) comes in guaranteed classes of 1,570, 1,770 and 1,960 MPa; Akashi Kaikyō used ~1,770 MPa. 1 GPa is a factor of ~1.96 on the strongest class, at the low end of bridge practice (US guidelines call for action on existing cables below ~2.15; ~2.2–2.5 are the commonly quoted design values for new cables). Thinner wire is stronger (~2.25 GPa at ~1 mm, ~3.2–3.5 GPa for tire cord), so ~1 GPa is a factor of ~2.25 on ~1 mm wire. The spin load is steady and well known, and the spokes are in vacuum (no corrosion, no hydrogen embrittlement), which argue for a lower factor than bridges, which carry traffic and weather. **Adopted range: 800–1,200 MPa working stress; ~1 GPa means a factor of ~2 on bridge wire or thinner wire (proposed, to discuss).**
   - **Creep.** Cold-drawn wire at half its strength relaxes ~5% in 1,000 h and about twice that in the long term; read as creep under constant load, a spoke stretches ~0.2 m (400 m torus), ~0.5 m (900 m), ~0.85 m (1.6 km) and ~1.3 m (2.5 km) over its life. The compliant joints need adjustable lengths of about a metre, or the chords are pre-stretched.
2. **Segment joints only seal and carry shear** once the ring is closed, instead of carrying full hoop tension (~94 m² of steel at 1.6 km). During construction they carry ~1% of it (construction sequence, below).
3. **Incremental growth.** Hang arcs of segments in opposite pairs, each with its own pressure bulkheads, and spin up step by step. No closure support is needed.
4. **Strain compatibility.** A 500 MPa steel ring stretches ~0.25% (~2 m at 900 m, ~4 m at 1.6 km). Spokes pick up load anyway unless made compliant.

| | 900 m | 1.6 km |
|---|---|---|
| Self-supporting ring (plate) | ~1.2 Mt | ~7.4 Mt |
| Cable spokes (1 GPa wire, with taper) | ~0.5 Mt | ~3.1 Mt |
| + hull at minimum gauge (1 cm per hull) | ~0.15 Mt | ~0.5 Mt |
| + load-collecting frames (guess) | ~0.1 Mt | ~0.5 Mt |
| **Spoke-loaded total** | **~0.75 Mt** | **~4 Mt** |
| *With the rock shield (heavier load)* | *~1.1 Mt* | *~5.8 Mt* |

### Large hub (radius slightly above the tube width)

| | 900 m | 1.6 km | 2.5 km (candidate) |
|---|---|---|---|
| Tube width | 56 m | 100 m | 156 m |
| Hub radius | ~60 m | ~110 m | ~170 m |
| Gravity at hub rim | ~0.067 g | ~0.069 g | ~0.068 g |
| Hub rim speed | ~6 m/s | ~9 m/s | ~11 m/s |
| Full hub shield (sphere, 11 t/m² rock) | ~0.5 Mt (+4–5%) | ~1.7 Mt (+4–5%) | ~4 Mt (+4%) |

- Gravity gradient inside the hub: dock and zero-g work at the axis; casting and fluid handling at ~0.07 g on the hub rim.
- The hub rotates with the tori. Nothing is despun except the solar array on its slow bearing at one end (section 13); ships match the spin at the axial dock.
- In a stack, one long hub is shared by all the tori, with the dock at one end of the axis, the despun solar array at the other, and a single factory.
- If the factory runs automated and only crew shelters are shielded, most of the extra 5% shield is avoidable.

### Tangent-chord spoke net (proposed, to discuss)

Straight rim-to-rim chords pass just outside the hub, tangent to a circle slightly larger than its radius, so the chords outline a circular window (string-art pattern):

- **No hub flange needed.** Radial spokes anchored on the hub would load its rim with hoop tension `F_total / 2π`, the same force the self-supporting rim would carry: ~12 m² / 0.08 Mt of steel at 900 m, ~45 m² / 0.5 Mt at 1.6 km.
- **No mass lost.** Each chord is ~4.3° off radial at the rim (`sin θ = c/r ≈ 0.074`, with the tangent circle c at 1.1 × the hub radius, the same angle at every size), so it pulls the rim at only cos θ; but its length per anchor is r cos θ instead of r, so the net weighs the same as radial spokes, within 0.1% (an earlier estimate counted a ~0.2% loss). Tapering the chords to uniform stress saves only ~1% at 900 m, ~2% at 1.6 km and ~4% at 2.5 km: uniform cables are fine.
- **The chords bow outward.** Across a chord the spin load is ω²c, so each chord bows away from the axis by ρω²cL²/2σ: ~2.3 m at 900 m, ~7 m at 1.6 km, ~18 m at 2.5 km. The window grows by as much; the crossings are laid out at the bowed positions.
- **Loads.** With an anchor every 10 m of rim, each chord end carries ~105 MN at 900 m and ~180 MN at 1.6 km; a uniform chord needs ~1,080 cm² (a cable ~37 cm across) and ~1,920 cm², sized at mid-chord where its own spin load adds most.
- **Crossed lacing is built in**, carrying spin-up and docking torque.
- **The hub floats in the net**, held centred by light stabilising lines, with compliant joints on the rigid elevator, pipe and power shafts.
- **The window is the factory's space**: the hole left in the middle of the net is exactly where the factory and dock sit.

### Elevators and rim trains (adopted)

**Rule:** everything that carries people around the habitat stays between 0 and 1 g, never above.

**Elevators** run in the spokes between the hub and the rim:

- Apparent gravity rises from ~0.07 g at the hub to ~0.94 g at the train level.
- Coriolis pushes a moving car sideways: ~0.1 g at 5 m/s (`a = 2ωv`), against one guide rail going down and the other going up.
- A car going down must pick up tangential speed, from ~6 m/s at the hub to ~90 m/s at the rim; the spoke carries that load.

**Rim trains** run in an enclosed tube on the hub-facing side of each torus (R ≈ r − w, ~844 m at 900 m), joining all the elevators so that moving around the ring doesn't mean going up to the hub and back down. A train adds its speed to the spin or subtracts from it:

```
a = (ωR ± v)² / R = ω²R ± 2ωv + v²/R        (+ spinward, − antispinward)
```

For the 900 m torus (ω²R ≈ 0.94 g, ωR ≈ 88 m/s, loop 5.3 km):

| Train speed | Spinward | Antispinward | Half the ring (2.65 km) |
|---|---|---|---|
| 5 m/s (18 km/h) | 1.05 g | 0.84 g | ~9 min |
| 10 m/s (36 km/h) | 1.17 g | 0.74 g | ~4.4 min |
| 20 m/s (72 km/h) | 1.42 g | 0.56 g | ~2.2 min |
| 44 m/s (160 km/h) | 2.1 g | 0.24 g | ~1 min |
| 88 m/s (320 km/h) | 3.8 g | 0 g (at rest in space) | ~30 s |

- **One-way antispinward loop (adopted).** Every trip is lighter, never heavier; one track, no two-way traffic or passing loops; no trip longer than the full loop.
- **Speed ceiling at the rim's own speed** (~88 m/s at 900 m, ~118 m/s at 1.6 km), where riders float. Above it, apparent gravity rises again (full weight at twice that speed), so there is no reason to go faster.
- **Operating speed is a comfort choice.** At ~20–44 m/s riders feel ~0.6–0.25 g and a full loop takes ~2–4.5 min; near the ceiling ~1 min in near-weightlessness, with restrained seats as in the elevators near the hub.
- **Starting and stopping** at ~0.1 g take 20–45 s, so stations need run-up lengths of a few hundred metres at the higher speeds.
- **Larger habitats are gentler:** at 1.6 km the effect per m/s is ~25% weaker, though the loop is 9.4 km long.
- **Shielding:** inside the shield jacket the tube is fully shielded; outside it, trips of a few minutes add negligibly to the annual dose.
- **In a stack**, each torus has its own loop; the elevators connect them through the shared hub, and same-phase neighbours are also joined by rim tunnels.

**Effect on the spin: negligible and reversible.** Angular momentum is conserved, so a train accelerating antispinward speeds the habitat's spin up slightly, and braking returns it exactly. For a 50 t train at 20 m/s on the 900 m torus (I ≈ 6 × 10¹⁵ kg·m²):

| Effect | Size |
|---|---|
| Change in spin rate while running | ~1.3 parts per million |
| Change in the 60 s rotation period | ~80 µs |
| Change in floor gravity | ~3 parts per million |
| Centre-of-mass shift | ~5 mm (absorbed by ballast water) |

Ten trains at once shift the spin by ~1 part in 100,000 while they run. Only mass leaving the habitat (departing ships, thruster exhaust) changes the spin permanently.

### Construction sequence for a child

Ring segments (diameter = tube width < hub radius) leave through the parent's axial dock. The child's hub cannot, so it is built outside from panels.

1. Build the child hub outside from panels.
2. String the chord cable net.
3. Hang arcs of segments (at least ~4θr long, below) in opposite pairs, each sealed behind its own bulkheads.
4. Spin up step by step as mass is added (water thrusters, ~3–4% of the habitat's mass).
5. Close the ring and bring the child's factory online. Factory modules are sized to pass the dock, so the factory is the truly copied core.

**A partial ring in the chord net (structural model, plan §2; provisional):**

- **Arcs, not single segments.** A chord's far end lands 2θr off the point opposite (~134 m at 900 m, ~240 m at 1.6 km). So at each end of two opposite arcs, a zone 2θr long keeps only the chord whose far end lands on the other arc, and every anchor has a chord only if each arc spans at least ~4θr: **~270 m at 900 m** (about five 56 m segments, ~0.56 Mt with rock), ~480 m at 1.6 km, ~740 m at 2.5 km.
- **Spin no faster than ~0.7 of the final rate while the first arcs hang.** In an assembled model (each chord one member with one tension, rigid segments, joints as springs) the chords of the shortest arcs carry twice their finished load, ~2,000 MPa at full spin in cables sized for 1 GPa. Stresses scale with spin², so that stage stays within the allowable below ~0.71 of the final spin rate, at every size; longer arcs ease it (~0.83 at 1.5 × 4θr, ~0.92 at 3 ×, at 900 m), as would temporary extra cables.
- **Joints locked while building, released once closed.** The joints of a partial arc carry tension (~0.9–1% of a full ring's hoop force on the shortest arcs, ~176 MN at 900 m at full spin) and bending (~6 GN·m at 900 m, much more on longer arcs in this rigid-segment model). Joints free along the rim can't hold a partial ring at all. Once the ring is closed, locked joints would make the hull a hoop carrying ~50–64% of the load (strain compatibility, point 4 above), so they must then slide along the rim, as point 2 intends.
- **Imbalance shifts the spin axis, not a bearing.** The partial ring spins freely about its centre of mass, so a mismatch between paired arcs moves the axis away from the assembly's geometric centre: ~3.6 m for a 1% mismatch on the first pair of 900 m arcs. The hub and net move with it; their relative motion, set by the stabilising lines, is still to model. Ballast corrects it as the ring grows.
- **Provisional:** rigid segments, small displacements and no hub; the finite-element model (plan §2) is to settle the joint moments and the sequence.
---

## 13. Light, power and heat

### Artificial overcast sky (adopted)

The sky is a uniform grey-white ceiling, like an overcast day, so the valley looks natural at tree level; it is switched off at night. Mist was dropped as a requirement (it came from the fern-gully image); fog or drizzle may still form on their own (section 18, atmosphere chemistry).

- **Light box (proposed design).** The light pipes run almost side by side across the ceiling in a shallow cavity whose walls and top are coated white with **magnesium oxide** (~95–98% reflective, historically a laboratory white-reflectance standard, and a by-product of the glass line's acid leach). A diffuser hangs about one pipe-width (~0.5–1 m) below the pipes, enough to blend their stripes. Light the diffuser bounces back is reflected down again instead of being absorbed, so ~75–85% of the pipes' light reaches the valley: ceiling losses fall from the ~50% first assumed to **~20–30%** (an estimate, to verify with real prism light pipes and sulfur lamps).
- **Diffuser materials, all local:** rolled patterned glass from the silica line made strongly diffusing (sandblasted, or with fine bubbles), opal glass, or acrylic with scattering particles (C-type carbon).
- **It reads as a real overcast sky.** At ~15 mol/m²/day over a 12 h day the floor gets ~20,000 lux and the ceiling glows at ~7,000 cd/m²: a bright overcast day. A real overcast sky is about three times brighter overhead than near the horizon, so the diffuser is graded brighter along the middle of the ceiling than near the cliffs, and the canyon reads as natural rather than as a lit room.
- **Algae above the ceiling (proposed).** About one pipe in 20–40 shines upward instead, into thin algae trays in the service space above. As a protein base (~35–65 g dry per person per day) algae need ~0.2–0.5 kW of light per person, ~2–6% of the sky's lamps for ~2,000 people (two farm tiers lit), on ~2 m² of trays per person (~0.4 ha and ~200 m³ of water at ~5 cm for 2,000 people). The lamps' waste heat keeps the cultures warm (~30–35 °C for spirulina-type algae), the dedicated pipes can run on the algae's own schedule, and the trays need double walls with a drip catch, since a leak rains into the canyon. A strip this small is too little to serve as the water-rich inner shield layer on the hub-facing side.

Electric power for the sky, as a 24 h average, depends strongly on the lamp efficacy. Light delivered to the floor (before ceiling losses):

| Light level | Daily light integral | Sulfur lamps (~1.4 µmol/J) | LEDs (~3 µmol/J) | 900 m valley (32 ha), sulfur / LED | 1.6 km valley (100 ha), sulfur / LED |
|---|---|---|---|---|---|
| Shade-tolerant forest (a dull overcast summer day) | ~10 mol/m²/day | ~83 W/m² | ~39 W/m² | ~27 / ~12 MW | ~83 / ~39 MW |
| Meadows, gardens, most fruiting plants (a bright overcast day) | ~20 mol/m²/day | ~165 W/m² | ~77 W/m² | ~53 / ~25 MW | ~166 / ~77 MW |

**Ceiling losses and the power sizing.** The habitat is sized at ~53 MW of sulfur lighting per 900 m torus on daily average (~25 MW with LEDs), ~166 MW (~77 MW) at 1.6 km. With the ~50% ceiling losses first assumed, that gave ~10 mol/m²/day; with the light-box ceiling (~25% losses) the same power gives **~15 mol/m²/day**, a level suited to a mixed landscape rather than only shade-tolerant forest.

Dawn, dusk and seasonal day length are schedule settings.

### Lighting schedule and load balancing (adopted)

- **One shared day per torus.** A day line travelling around the ring was rejected (section 17.13): noon and midnight would be only ~2.8 km apart at 900 m, and a bird could fly from day into night in minutes.
- **With a single torus, the load is peaky.** Lights draw ~2× the daily average for 12 hours and nothing at night: the solar supply must cover the daytime peak, or store energy (~240 MWh a day at 900 m, ~8 kt of nickel-iron batteries returning only ~65%), or the factory must absorb a night surplus while the day still runs a deficit.
- **Staggered tori make the total load constant.** In a pair, torus A has its day while B has its night. In a stack of 6, three groups of two run 8 hours apart. At any moment the sum of lighting is constant and equal to the average, so the solar array only needs to match the average, no storage is needed, and the radiator load is steady.
- **Pair rule (adopted).** At most one valley lit at any moment; both may be dark. Summer: 12 h day / 12 h night, one valley always lit, dawns and dusks crossfaded between the two valleys so the total never exceeds one lit valley. Winter: shorter, dimmer days with two dark gaps (24 − 2D hours), used by the hub factory. A pair's day can never exceed 12 h.
- **Six-stack:** the three-phase schedule keeps the total load constant for any day length from 8 to 16 h (an 8-hour block smoothed by ramps of 0 to 8 h), a full Brittany-like range.
- **Day profile.** The profiles must add up to a constant. For three phases, a 12-hour day shaped as **4 h dawn ramp → 4 h full light → 4 h dusk ramp** sums exactly to a constant when shifted by 8 and 16 hours (noon intensity = 3× the daily average). For a pair, any day whose two 12-hour-offset copies sum to a constant works, e.g. 4-hour ramps on either side.
- **Grouped phases: A A B B C C.** Same-phase neighbours share one clock and can be joined by rim tunnels with no light-locks, forming three double valleys (~64 ha each at 900 m). Only two time boundaries remain (A–B and B–C, 8 h each); A and C, 16 h apart, never touch.
- **The 8/8/8 schedule.** At any moment one third of the inhabitants work, one third have free time and one third sleep: the factory, docks and shared facilities run around the clock with nobody on a night shift.
- **Farm rings keep their own schedule** (section 13, farm rings): their zones are staggered so that the farm's load is also constant around the clock, added to the valleys' constant load.
- **Sulfur lamp dimming** has a limited range, so ramps may be made by switching lamp groups rather than a perfectly smooth fade (to check).

**Lamp technology:**

- **LEDs** reach ~3.4 µmol/J (white + red) to ~4.1 µmol/J (blue + red) at the best, but need GaN, indium and rare-earth phosphors, a "vitamin" the factory can't easily make.
  - **Count:** ~100–200 million mid-power LEDs per 900 m torus (dull to bright overcast, with ceiling losses), against ~110,000–220,000 sulfur lamps of ~1 kW.
  - **Scarce material is small:** ~2.5–5 kg of gallium, grams to a few hundred grams of indium, ~100–200 kg of YAG:Ce phosphor. LEDs pass the sourcing rule (section 10); the obstacle is the semiconductor fab, not the mining.
  - **Replacement:** ~50,000 h to 70% output, ~11 years at 12 h/day, so ~10–20 million LEDs replaced every year.
  - Blue + red LEDs avoid the phosphor but give magenta light, not an overcast white sky.
- **Sulfur plasma lamps** are closure-friendly: a quartz bulb holding sulfur and argon, excited by microwaves, with a continuous, mercury-free spectrum, developed for plant growth under NASA contract in the 1990s. Every bulk ingredient is local: sulfur from C-types, quartz from silicates, argon in traces, steel and copper for the microwave source. The cost is efficacy: ~1.3–1.5 µmol/J at the wall plug with small magnetrons, so roughly twice the power of LEDs.

### Sulfur lighting system (adopted direction)

- **Non-rotating bulbs.** Classic sulfur lamps spin the bulb at ~600 rpm with an air jet; without rotation, convection makes a hot spot that melts the bulb within a second or two. A 2002 Fusion Lighting patent keeps the bulb still by adding a trace of cesium bromide and driving it with a circularly polarised microwave field that rotates around the bulb: stable for over 9,000 h at ~350 W with constant colour. Acoustic-resonance confinement is another line of research. Cesium is a vitamin, but ~0.06 mg per bulb (~6 g for 100,000 bulbs).
- **Light pipes are the overcast sky.** Prism light pipes glow evenly along their length; the Smithsonian Air and Space Museum replaced over 100 conventional lamps with 3 sulfur lamps feeding pipes along much of its hall, and runs of tens of metres or more are possible. At the 3-phase noon peak (~500 W of electricity per m² of floor, with losses), a pair of ~6 kW lamps feeding a 40 m pipe covers a strip only ~0.5 m wide, so the pipes sit almost side by side across the ceiling.
- **Lamps outside the valley.** Sources and bulbs sit in a service space above the ceiling, possibly sharing the hub-facing side with the train tube: their waste heat (~70–80% of the input) goes straight into the coolant loops, and maintenance happens without entering the canyon.
- **Large central microwave sources** feeding many electrodeless bulbs through waveguides, instead of one small magnetron per bulb:

| Source | Power | Efficiency | Lifetime |
|---|---|---|---|
| Small magnetron (classic sulfur lamp, 2.45 GHz) | ~1–6 kW | ~70% | ~10,000–20,000 h (system rating) |
| Industrial magnetron, 915 MHz | 100 kW | ~85–86% | ≤ 6,000 h today; R&D aims at 50,000–80,000 h |
| Broadcast klystron (UHF TV) | tens of kW | typically lower than magnetrons | ~60,000 h projected MTBF |

  - **Less hardware to replace:** a 900 m torus at its noon peak (~165 MW) needs ~1,650 sources of 100 kW instead of ~28,000 small lamps (or ~470,000 at 350 W). At today's ~6,000 h that's ~1,200 replacements a year; at 50,000–80,000 h, ~100–150. The farm ring adds ~320 sources per tier lit, running steadily (~1,400 more replacements a year with three tiers at today's lifetimes). The electrodeless bulbs may last almost indefinitely.
  - **Better efficacy:** Fusion's bulbs gave over 2 µmol per joule of microwave power, so behind an 85%-efficient source the system reaches ~1.7–1.8 µmol/J at the wall, ~20–25% less power for the same sky.
  - **Smooth ramps:** magnetron efficiency stays nearly flat from 30% to 100% of rated power, so dawns and dusks can be made by turning sources down, sidestepping the bulbs' limited dimming range.
  - **Sector plants:** waveguide losses limit run lengths, so a plant every few hundred metres along the ring; plants at the boundary between tori on different phases could serve both, cutting installed capacity.
  - **Unknowns:** large bulbs at 915 MHz are plausible but unproven (demonstrations are mostly at 2.45 GHz up to ~6 kW); magnetron and klystron cathodes use tungsten and emissive coatings, trace elements that make long-lived, rebuildable cathodes important.

### Power

- **Plain rims are not enough.** Panels on the rim, lit half of every rotation and averaging ~1/π of full sunlight, give ~34 MW (900 m) or ~110 MW (1.6 km) per torus, against ~57 MW / ~180 MW needed with sulfur lamps for the sky, ceiling losses and other loads, plus ~32 MW / ~102 MW per farm tier lit.
- **Despun solar array on the hub (adopted; replaces the capless solar cylinder, section 17.28).** A flat array on a mast on the spin axis, beyond one end of the stack, its plane containing the axis. Sunlight always arrives perpendicular to the axis, so one rotation about the axis keeps it facing the Sun: relative to the habitat it turns at the spin rate (1 rpm at 900 m, 0.75 rpm at 1.6 km), relative to the stars once a year.
  - **About three times the power per m² of PV:** a sun-facing panel makes ~340 W/m² at 1 AU (25% PV), the spinning cylinder ~108 W/m². Silicon PV is a vitamin, so this also cuts the vitamin by about two thirds.
  - **One light rotating interface:** a slow, almost unloaded bearing. On the axis the array adds no centrifugal load, and sunlight pushes on it with only ~4.6 N per km². A magnetic bearing (iron and copper) avoids lubricants (the usual space lubricant, MoS₂, needs molybdenum, a vitamin). Two bearings, either able to carry the array, and a replaceable drive. Unlike the rejected counter-rotating designs (sections 17.4–17.6), there is no pressurized seal, no traffic and no heavy load.
  - **Power crosses the joint without contact:** a rotary transformer (AC across the gap, ~98–99%, iron and copper), the principle that carries megawatts in brushless generator exciters. Slip rings and roll rings wear; the ISS's solar rotary joint suffered bearing-race damage in 2007.
  - **Survival if it fails.** With cells on both faces, a locked array turns with the stack and still averages 2/π ≈ 64% of its output (1/π with one-sided cells). **It is sized so that, locked, it still delivers the habitat's whole need**, enough to keep it alive and fed through winter: ~1.57× the bare need (for the valley alone, **half the former cylinder's PV area**), with ~1.57× the need while tracking (spare for the factory, brighter gardens or food exports). The farm tiers lit are part of that need (section 13, farm rings). A locked array's output pulses with each turn, so it needs ~30 s of buffering (capacitors, or a small flywheel).
  - **Sizes at 1 AU** (constant sky; section 15 gives the seasonal sizing by orbit): for the valley and other loads ~0.27 km² per 900 m torus (against ~0.55 km² of cylinder) and ~0.85 km² per 1.6 km torus, plus ~0.15 km² / ~0.48 km² per farm tier lit, so ~0.71 km² / ~2.3 km² with three tiers lit. A 900 m pair needs ~0.53 km² for its valleys (for example ~300 m along the axis × ~1.8 km across) and ~1.4 km² with three tiers lit (~800 m × ~1.8 km); a 900 m six-stack ~1.6 km² (~4.3 km² with three tiers); a 1.6 km six-stack ~5 km² (~14 km²). Thin-film panels plus structure at ~3 kg/m² come to ~0.8 kt per 900 m torus for the valley (against ~1.6 kt for the cylinder), ~2.1 kt with three tiers lit.
  - **It scales.** Its size is not tied to the stack's radius and pitch, so it simply grows further from the Sun (per 900 m torus at the survival sizing: ~0.65 km² at Mars and ~2 km² in the belt for the valley, plus ~0.35 / ~1.1 km² per farm tier lit). Only a sun-facing surface can concentrate: local thin-film mirrors can cut the PV area by the concentration ratio, and solar-thermal generators (Stirling or Brayton, ~25–35%) need no PV at all. This is what opens the outer system without nuclear (below).
  - **Placement.** The dock stays at the other end of the hub: ships can't dock at the despun mast without a rotating pressurized joint. The mast extends along the axis beyond the stack's end, so the stack doesn't shade the array. Seen along the axis the array is edge-on, blocking almost none of the radiator vent. Sunlight's push on a single array turns the spin axis by only ~0.002° a year, and since the push rotates with the Sun, it averages out to a tiny yearly wobble; the array's few kilotonnes add almost nothing to the transverse inertia.
  - **Maintenance** happens in microgravity on the array, reachable from the hub. Always facing the Sun, it has no thermal cycling (the cylinder had ~500,000 small swings a year). For major work the bearing is locked and the array keeps producing.
- **Flat PV is the baseline; concentrators are noted as options** for the part of the array above the survival level, mainly further from the Sun. Per ~100 MW of electricity at 1 AU:

| | Flat PV (silicon, adopted) | Mirrors focusing on smaller PV cells (option) | Mirrors + heat engine, solar thermal (option) |
|---|---|---|---|
| Sunlight → electricity | ~18–22% | ~20–25% (cells cooled) | ~18–22% at ~900 K with steel-class parts; ~25–30% at ~1,300 K in silicon carbide |
| Collecting area | ~0.33 km² of cells | ~0.35 km² of mirror + ~0.01 km² of cells at ~30× | ~0.4 km² of mirror, plus ~4–10 ha of radiators at ~400–500 K for the engine's waste heat |
| Materials failing the sourcing rule | very pure silicon, a boron dopant, silver contacts (copper or aluminium possible) | the same, ~30× less | none at ~900 K (steel, iron-nickel-chromium, silicon carbide, copper, aluminium coating; CO₂ or water as working fluid; wound-field generators without rare-earth magnets); hotter alloys need cobalt, molybdenum or tungsten |
| Manufacturing | a semiconductor line | a small semiconductor line plus a mirror line | metalworking: a mirror line, receivers, turbines or Stirling engines, generators, radiators |
| Moving parts | none | none | turbines or pistons and pumps (gas-foil, flexure or magnetic bearings) |
| If the array locks to the stack | ~64% (two-sided cells) | ~0 (must point at the Sun) | ~0 |
| Further from the Sun | cell area grows as distance² | mirror grows, cells stay small | only the mirror grows |

  The despun array suits concentrators: the Sun stays perpendicular to the spin axis, so a dish or trough on the mast stays aimed with the array's single rotation. Because concentrators produce nothing when locked, the survival part stays flat two-sided PV; at Saturn, where flat PV would need ~90× its 1 AU area, survival would have to rest on redundant bearings and drives instead. NASA ran a solar Brayton system up to 2 kW of electricity under a simulated Sun in the 1990s.
- **Industry:** a separate free-flying, non-rotating solar array at the factory or mining site. It has no angular momentum, so following the Sun costs nothing, and it isn't nested around anything, so if it drifts, nothing bad happens.
- **Beamed power (investigated; superseded by the despun array for the habitat).** A non-rotating free-flying array can beam microwaves to the habitat with no despun antenna, as long as the transmitter sits on the spin axis and the receiver is a rectenna disc centred on the axis: the disc then only turns about its own centre, circular polarization makes the dipoles' rotation irrelevant, and a phased array locked on a pilot signal from the rectenna defocuses if it loses it. An off-axis transmitter would need a despun dish or a receiving band around the stack, which faces the beam only part of each turn and loses the gain.
  - After the microwave chain (magnetron ~80–85%, beam capture ~90–95%, rectenna ~80–85%; ~50–60% overall) a sun-facing array still delivers ~1.6–1.9× the cylinder per m² of PV. Lasers (~25–35% overall) give no real gain.
  - **The rectenna is almost a cap:** at ~1 kW/m² of microwaves, ~420 m across for a 900 m pair, ~730 m for a 900 m six-stack and ~1.3 km for a 1.6 km six-stack (~20% of an end opening), across the docking lane and the radiator vent. At 5.8 GHz, transmitter and receiver a few hundred metres across can be up to ~1,000 km apart (~200 km at 915 MHz).
  - Station-keeping is trivial (~4.6 N per km² of array), but the habitat would depend on an actively pointed free-flier. Magnetrons are local; rectenna diodes are semiconductors (a vitamin), with vacuum-tube cyclotron-wave converters (~70–80%) a less mature local alternative.
  - **Superseded** for the habitat by the despun array (~3× the cylinder per m² of PV, ~1–2% losses, no cap-sized receiver, no free-flier to keep in place). Beaming remains a way to bring power from the free-flying industrial array to the hub factory, which tolerates interruptions.
- **Processing energy no longer sets the generation time.** With the rock shield, a 900 m torus needs ~10¹⁵ J to crush and separate ~12 Mt of S-type rock and ~10¹⁶ J to bake ~5–8 Mt of C-type at ~1–2 MJ/kg: ~2–6 months at 1 GW (≈ 1 km² of solar furnace mirror, or ≈ 3 km² of panels at 25%), ~2–5 years at 100 MW. A six-torus stack is ~6× that. Logistics and factory throughput become the pacing items. (The water jacket needed ~1.5 × 10¹⁷ J per torus to bake ~100 Mt of C-type: ~5 years at 1 GW.)
- **Silicon PV is a vitamin** (very pure silicon). Solar-thermal concentrators for the furnaces are easy to make locally.

### Distance from the Sun

Sunlight falls with the square of the distance:

| Orbit | Distance | Sunlight vs. Earth's |
|---|---|---|
| Venus | 0.72 AU | 1.9× |
| **Earth (baseline)** | **1 AU** | **1×** |
| Mars | 1.52 AU | 0.43× |
| Asteroid belt | ~2.7 AU | ~0.14× |

- **Near Earth first (adopted starting point).** Near-Earth asteroids include all the needed types: S-types (the most common), C-types such as Bennu and Ryugu, and some M-types. Staying near 1 AU avoids the belt's ~7× loss of sunlight.
- **Spreading outward needs more collecting area or another power source.** A belt habitat needs ~7× the solar area per torus; the despun array simply grows (its size isn't tied to the stack). Nuclear options were investigated and rejected for now under the sourcing rule (section 17.22).
- **Concentrators on the despun array (now possible, to discuss).** A 900 m torus needs ~230 MW of sunlight for its valley's ~57 MW at 25%, ~620 MW with three farm tiers lit (×1.57 with the survival sizing). Mirror areas below are for the valley; with three tiers lit they are ~2.6× larger. Collecting it further out with sun-tracking thin-film mirrors (~10–20 g/m², aluminium and carbon) on the despun array's mast, focused onto a smaller PV area or a solar-thermal generator:

| Location | Sunlight | Mirror area per torus | Film mass |
|---|---|---|---|
| Asteroid belt (2.7 AU) | 0.14× | ~1.3 km² | ~15–25 t |
| Jupiter (5.2 AU) | 0.037× | ~4.8 km² | ~50–100 t |
| Saturn (9.5 AU) | 0.011× | ~16 km² | ~160–320 t |

  The concentration ratio sets the PV area (~10–100 suns on cooled cells), and a solar-thermal generator (Stirling or Brayton) needs no PV at all. Mounted on the despun mast, the mirrors no longer depend on free-flying craft (the earlier version of this idea used free-flying mirrors focused on the spinning cylinder).

### Farm rings: electric light in three tiers (adopted)

Each torus grows its staple food in a farm ring in its own plane, lit by the same sulfur lamps and light pipes as the valley's sky and powered by the same despun solar array. This replaces the sun-fed rings lit by mirrors around the hub (section 17.29): there are no mirrors, no glass and no flicker, the gaps stay narrow (10–40 m), and the population grows with the array, whose size isn't tied to the stack's geometry.

```
        towards the hub ↑
            ┌────────────────────────────────────┐
  tier 3    │ ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ │ ─┐
            │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │  │ 2.5 m
  tier 2    │ ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ │ ─┤
            │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │  │ 2.5 m      ~8.5 m in all
  tier 1    │ ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ │ ─┤
            │ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │  │ 2.5 m
            └────────────────────────────────────┘ ─┘
            ←── ~0.9 × tube width along the axis (~50 m at 900 m) ──→
        "down" ↓ outward: radiators on the spokes, then the main ring
```
(section through the ring in the torus plane; `≡` light pipes just above the canopy, `▒` crops; floors at ~0.39–0.40 g)

**Layout:**
- **In each torus's own plane, on its own spokes,** at ~0.4 r: ~360 m at 900 m, ~640 m at 1.6 km, ~1,000 m at 2.5 km. The ring stays within the plane's thickness, shares the torus's spokes and elevators (a farm stop on each) and carries its own weight in hoop tension (its rim moves at only ~38 m/s at 900 m), so the spokes only keep it centred. A separate ring in the gap was rejected (section 17.26).
- **Order outward from the axis:** hub → free stretch along the spokes → farm ring → radiators → main ring. No reflected light crosses the inner stretch any more, so it is free, a reserve for more radiators.
- **Three tiers** stacked radially, ~2.5 m floor to floor so that people can walk upright between the crops, ~8.5 m tall in all with floors and services. Width along the axis ~0.9 of the tube width (~50 m at 900 m, ~90 m at 1.6 km, ~140 m at 2.5 km). About 80% of each tier is planted; the rest is aisles, seedlings and processing. Dwarf varieties of wheat and soybean, and potatoes, fit under a 2.5 m tier; tall crops (corn) grow in the valley.
- **All three tiers are built with the torus** (the ring is cheap next to the torus); how many are lit is set by the despun array and decides the population (below).

**Light, air and shielding:**
- **The same lamps as the sky:** non-rotating sulfur bulbs fed by the central microwave sources (section 13, sulfur lighting), with light pipes running just above each tier's canopy. With the pipes close to the crops and white walls around them, ~85% of the lamps' light reaches the leaves (an estimate), against ~75% through the valley's light box.
- **Its own schedule:** each zone runs the day length its crop needs, and the zones are staggered so that the farm's load is constant around the clock, like the tori's days. Wheat, a long-day crop that grows best under long or continuous light, flowers here even in a pair, whose valleys never get more than 12 h days.
- **Its own atmosphere (to decide):** plants need CO₂ and water, not 70 kPa, so a lower pressure lightens the shell; CO₂ enriched to ~1,000 ppm, as in NASA's growth chambers, whose yields the sizing uses. The farm makes most of the habitat's oxygen and takes up its CO₂, exchanged with the valleys' air through ducts in the spokes. Transpired water is condensed as clean water.
- **Light shielding:** crops tolerate deep-space cosmic-ray doses. People working there limit their time, as in any lightly shielded zone, and most routine work can be automated. Only the seed bank needs the full shield.
- **Mass (rough):** a ~1 cm steel shell (~26 ha at 900 m) plus growing systems at ~100 kg per m² planted come to ~50 kt per 900 m torus, ~0.4% of its mass; ~150 kt at 1.6 km.

**Built for the highest density.** The farm ring is built as efficient as possible; it is the biosphere that is high or low density. A habitat that lights fewer tiers simply has fewer people, or exports food. Dark foods (bacteria, mushrooms, larvae, fish) and algae stay as margins on top (section 16).

### Diet and crop yields

**Working diet (proposed):** a simple plant-based staple diet grown on the farm, with the valley's trees and gardens adding the rest. 2,500 kcal per person per day:

| Food | Share | Role |
|---|---|---|
| Potatoes | 33% | the highest yield per mol of light; NASA's chambers grew about twice the field world record |
| Wheat | 28% | flour and bread; preferred over rice: very high yields in NASA's chambers (~3–4× the field world record) and no flooded beds; a little rice for gluten-free needs |
| Soybeans | 15% | protein and oil |
| Lentils | 7% | protein and variety |
| Berries | 5% | fruit and vitamins |
| Flax | 3% | omega-3 oil (ALA); its stems give linen fibre |
| Greens | 2% | lettuce and other leafy vegetables |
| From the valley | 7% | fruit and nut trees, corn, squash and beans in the permaculture and food forest (section 16) |

This gives roughly ~100 g of protein a day. Fat is low at ~11% of the calories: more soybeans or flax, or nuts from the valley, would raise it. Vitamin B12 still comes from fermentation (section 16).

**Yields,** edible dry mass per mol of light reaching the crops. The conservative column sizes the design:

| Crop | Conservative (sizing) | Best demonstrated | Light per person per day, conservative |
|---|---|---|---|
| Potato | 0.37 g/mol | ~0.60 (37.5 g/m²/day of tubers at 725 µmol/m²/s, 12 → 24 h days; Tibbitts et al.) | ~600 mol |
| Wheat | 0.18 | ~0.40 (60 g/m²/day of grain at ~150 mol/m²/day; Bugbee & Salisbury) | ~1,080 mol |
| Soybean | 0.15 | ~0.22 | ~560 mol |
| Lentils | ~0.15 (estimate) | ~0.22 | ~320 mol |
| Berries | ~0.25 | ~0.30 | ~150 mol |
| Flax | ~0.07 (estimate) | ~0.12 | ~190 mol |
| Lettuce, greens | 0.43 | ~0.74 (vertical farms average ~0.55 g/mol of shoot dry mass; Jin et al.) | ~40 mol |
| **Total, with ~10% for seedlings and turnaround** | | | **~3,200 mol** |

NASA's Biomass Production Chamber found edible yields "slightly lower than expected" over many crop cycles, which the conservative column allows for.

**Per person:**

| | Conservative (sizing) | Best demonstrated |
|---|---|---|
| Light on the crops | ~3,200 mol/day | ~1,900 mol/day |
| Crop area at ~36 mol/m²/day (average over crops and day lengths) | ~89 m² | ~52 m² |
| Food per m² of crops | ~26 kcal/day | ~45 kcal/day |
| Electricity, sulfur lamps (~1.4 µmol/J, ~85% delivered; ~350 W per m² of crops) | **~31 kW** | ~18 kW |
| With 915 MHz sources (~1.75 µmol/J) | ~25 kW | ~15 kW |
| With LEDs (~3 µmol/J, a vitamin-dependent option) | ~15 kW | ~8.5 kW |

- **Light per person sets the power,** not the crop area: brighter light on fewer m² needs the same electricity. NASA's estimate of ~40–50 m² of crops for all of one person's food, under brighter light, matches the best-demonstrated column. Biosphere 2, under sunlight through glass, had ~2,500 m² of agriculture for 8 people (~300 m² each) and still grew only ~83% of their diet, with constant hunger in the first year.
- The notes' earlier figure (~45 m² at ~40 mol/m²/day, ~1,800 mol per person) was the best-demonstrated case, and the ~5–10 kW per person quoted earlier was too low: even that case needs ~18 kW with sulfur lamps. With two or more tiers lit, food is the habitat's largest power use.

### People fed, and the power behind them

**People fed per torus, conservative yields** (farm lighting in brackets). The geometry is self-similar, so the floor per person is the same at every size:

| Tiers lit | 400 m (demonstration) | 900 m (32 ha of floor) | 1.6 km (100 ha) | 2.5 km (245 ha) |
|---|---|---|---|---|
| Crops per tier | ~1.8 ha | ~9.0 ha | ~29 ha | ~70 ha |
| 1 | ~200 (~6.3 MW) | ~1,000 (~32 MW) | ~3,250 (~102 MW) | ~7,900 (~247 MW) |
| 2 | ~400 (~13 MW) | ~2,000 (~64 MW) | ~6,500 (~204 MW) | ~15,800 (~495 MW) |
| 3 | ~600 (~19 MW) | ~3,050 (~95 MW) | ~9,750 (~305 MW) | ~23,700 (~742 MW) |

**Floor per person and density.** The overall density counts the whole valley floor, including the ≥ 50% wilderness; people live on the other half, so the settled density is twice as high:

| Tiers lit | Floor per person | Overall density | Settled half | Comparable to (approximate city-wide averages) |
|---|---|---|---|---|
| ~½ | ~700 m² | ~1,400 per km² | ~2,800 per km² | a small town or large village, with most of the farm ring dark or exporting food |
| 1 | ~310 m² | ~3,200 per km² | ~6,400 per km² | settled half like a compact French city (Bordeaux ~5,300, Nantes ~4,900); overall like a suburban town with its parks |
| 2 | ~155 m² | ~6,450 per km² | ~12,900 per km² | settled half like Lyon (~11,000); overall a dense town |
| 3 | ~103 m² | ~9,700 per km² | ~19,400 per km² | settled half close to Paris (~20,000), one of Europe's densest cities |

- **One tier lit** gives a green town: settlements in cliff dwellings, set in a large wild valley. A natural default for early habitats: the most wilderness per person and the smallest array.
- **Two tiers** give a lively town, about the density these notes earlier called "high".
- **Three tiers** reach city density on the settled half, made more livable by the cliff dwellings and the open valley floor. It is the maximum, not a target.
- **In a stack** (900 m): a pair feeds ~2,000 / ~4,000 / ~6,100 people with one, two or three tiers lit, a six-stack ~6,000 / ~12,000 / ~18,300; at 1.6 km a six-stack feeds ~19,500 / ~39,000 / ~58,500.

**Power, array and heat per tier lit.** Each tier lit draws about as much power as half to two thirds of the valley's sky, so lighting all three roughly doubles to triples the habitat's power. In practice the array, not the ring, decides how many tiers are lit:

| Per torus, at 1 AU | 900 m | 1.6 km | 2.5 km |
|---|---|---|---|
| Valley sky + other loads | ~57 MW | ~180 MW | ~440 MW |
| + per farm tier lit | ~32 MW | ~102 MW | ~247 MW |
| Total with 1 / 2 / 3 tiers lit | ~90 / ~122 / ~154 MW | ~282 / ~384 / ~486 MW | ~690 / ~935 / ~1,180 MW |
| Despun array (survival sizing): valley + per tier | ~0.28 + ~0.15 km² | ~0.85 + ~0.48 km² | ~2.1 + ~1.16 km² |
| Despun array with 1 / 2 / 3 tiers lit | ~0.41 / ~0.56 / ~0.71 km² | ~1.3 / ~1.8 / ~2.3 km² | ~3.3 / ~4.4 / ~5.6 km² |
| Radiating surface at ~285 K (two-sided panels: half) | ~16 ha + ~8.5 ha per tier | ~48 + ~27 ha | ~117 + ~66 ha |

- **The survival rule covers the farm:** the array is sized so that, locked to the stack, it still lights the tiers that feed the population, and tracking it gives ~1.57× that, spare for the factory or for exporting food.
- **Seasons:** the farm runs at full output all year, so its share of the array is sized at the host's aphelion (section 15); the perihelion surplus goes to industry. Growing more around perihelion and storing staples (grain, potatoes, dried legumes keep for a year) would save ~30–40% of the farm's array share; noted as an option, not factored in, since it needs brighter light at perihelion on the same tiers (to test).
- **All of the farm's power ends up as heat** in the coolant loops (section 13, heat rejection).

### Glass and the silica line (proposed)

**How much,** per 900 m torus (the farm rings no longer need windows):

| Use | Glass |
|---|---|
| Valley ceiling diffuser (rolled patterned glass, ~4–6 mm, ~32 ha) | ~3–5 kt |
| Light pipes for the valley ceiling (glass version, 2 mm walls) | ~4 kt (or ~0.5 kt as acrylic) |
| Light pipes for the farm ring's three tiers | about as much again |
| Quartz bulbs for the sulfur lamps | small |
| **Total** | **~5–13 kt, ~0.05–0.1% of the torus** |

**Where from.** Window glass is ~72% silica, ~14% soda, ~10% lime, with very little iron. Stony asteroid silicates (olivine, pyroxene) are ~40% silica but rich in magnesium and iron; melted as they are, they crystallise or give dark green glass, so the silica is separated first:

| Ingredient | In ~12 Mt of S-type rock | Needed for ~10 kt of glass |
|---|---|---|
| Silica | ~5 Mt | ~7–10 kt |
| Sodium (as Na₂O) | ~0.1 Mt | ~1.4 kt (soda-lime only) |
| Calcium (as CaO) | ~0.25 Mt | ~1 kt (soda-lime only) |

Only ~12–25 kt of rock is processed for a torus's glass.

**Process:**
1. Start from the tailings after metal separation, already crushed.
2. **Acid leaching** (sulfuric acid from the asteroid's own sulfur) dissolves magnesium, iron and calcium out of olivine and pyroxene, leaving amorphous silica (an established research route on Earth).
3. Wash, dry, calcine: pure silica powder. Iron goes to steel; magnesium and calcium become by-products (refractories, soil, the light box's magnesium oxide coating).
4. **Melt** in a solar furnace: pure silica at ~1,800–2,000 °C gives fused silica (very clear, UV-resistant, heat-shock tolerant), for the lamp bulbs; adding sodium and calcium lowers it to ~1,500 °C for easier forming.
5. **Form by rolling, not floating:** float glass needs a molten tin bath, and tin is ~1.6 ppm in asteroid rock (a vitamin). Rolled patterned glass, the usual greenhouse glass, also diffuses light, as the ceiling needs.
6. Temper with air jets where needed.

Energy is small: melting ~10 kt takes ~2–3 × 10¹³ J, the acid cycle perhaps ~10¹⁴ J, about a day of a 1 GW furnace.

**One silica line, three uses:** the valley's ceiling diffuser, the **quartz bulbs of the sulfur lamps**, and possibly the **light pipes**:

| Light pipe version | How it works | Mass for one 900 m torus's ceiling (the farm tiers need about as much again) |
|---|---|---|
| Glass tube with a reflective lining | thin aluminium coating inside | ~4 kt (2 mm walls) |
| Acrylic prism film | total internal reflection, lower losses over 40 m runs | ~0.5 kt |

(~1,000 km of 25 cm tube per torus ceiling, pipes almost touching.) Both pass the sourcing rule: glass from the silica line, acrylic from carbon, hydrogen and oxygen supplied by the C-type. Acrylic is lighter and better over long runs; glass is simpler chemistry and doesn't age under UV.

**Aluminium coatings.** Aluminium reflects ~90% but is hard to extract from rock; a ~100 nm coating uses only ~0.3 g/m², ~300 kg per km², a vitamin-scale quantity recovered from the leach solution: enough for reflective pipe linings and, if adopted, concentrator mirrors on the despun array. Polished steel or nickel (~55–65%) is a weaker fallback.

### Heat rejection

- **The shield jacket is a near-perfect insulator.** For water, conduction resistance ≈ 7 m / 0.6 W/m·K ≈ 12 m²K/W, so pushing 100 W/m² through it would need a temperature difference of over 1,000 K; compacted crushed rock conducts similarly poorly.
- **Everything that enters the habitat leaves through pumped coolant loops** to the radiators: sky lighting, farm lighting, algae lighting, people, machines.
- **Radiators along the spokes (adopted).** The stack encloses a wide, short drum of empty space between the hub and the rims. Its main openings are the two ends, facing along the axis, and the Sun is always perpendicular to the axis, so no direct sunlight reaches the spokes: inside each torus plane the radiators are shaded by the rim tube, which spans the plane's thickness. Without a solar cylinder the 10–40 m gaps also open the drum sideways, adding vents (~0.2 km² per gap at 900 m, against ~2.2 km² per end); sunlight crossing a gap stays in the gap plane, outside the torus planes. The radiators sit on the stretch between the farm ring and the rim, shaded on both sides by the farm ring and the main ring; the inner stretch, between hub and farm ring, is free as a reserve.
  - A passive loop needs radiators colder than the habitat, say ~285 K (~375 W/m²); warmer radiators would need heat pumps.
  - **Ideal limit:** if the drum were a black-body cavity at the radiators' temperature, heat would leave through the openings as if they were a radiator at that temperature. That is an upper bound, not a design figure: the panels are finite, not perfectly black, and see each other.
  - **Each end face of the stack**, from the axis outward (900 m torus); the dock and the vent sit at different radii, so they don't compete:

| From the axis | What's there | Share of the end opening |
|---|---|---|
| 0–60 m | Hub tip: at one end the dock on the axis (ships approach along the axis, matching the spin); at the other the despun solar array's bearing and mast | ~0.5% |
| Out to ~840 m | Open vent into the drum; the radiators (at ~380–840 m) look straight out through it | ~99% (~2.2 km²) |
| 840–900 m | The end torus's tube | |

  - The despun array, seen along the axis, is edge-on and blocks almost none of its end's vent. At 1.6 km the opening is ~7 km², in the same proportions. (The vent's outer edge is the tori's envelope, rock jacket and crawl space included: ~836 m at 900 m.)

| Stack | Heat to reject (sulfur lamps) | Ideal limit of the two end openings (~285 K) |
|---|---|---|
| 2 × 900 m | ~115 MW, + ~64 MW per farm tier lit (~310 MW with three) | ~1.6 GW (openings ~4.4 km²) |
| 6 × 900 m | ~345 MW, + ~190 MW per tier lit (~930 MW with three) | ~1.6 GW |
| Break-even, 900 m tori | ~29 tori with no farm lit; ~18 / ~13 / ~10–11 with 1 / 2 / 3 tiers lit | ~1.6 GW |
| 1.6 km tori | ~180 MW per torus, + ~102 MW per tier lit | ~5.3 GW (openings ~14 km²): break-even ~29 tori with no farm lit, ~11 with three tiers |

  - The opening area is fixed while heat grows with the number of tori. These break-evens are upper bounds.
  - **Preliminary radiative exchange (`habitat_model/cavity.py`, `reports/thermal.md`).** Rays traced from the panels (emissivity ~0.9, as for AZ-93 white paint) through the drum, with the hub, farm rings and the tori's inner faces insulated (the rock jacket is a near-perfect insulator), so they re-radiate what they receive. Panels also catch each other's radiation, so the drum rejects at most **~75–80% of the ideal limit** (~1.2 GW at 900 m, ~3.9 GW at 1.6 km), and only with panels covering most of the radiator annuli:

| Stack, tiers lit | Heat | Margin, ideal | Margin, ray-traced (ends only / with the side gaps) | Panels needed (one face) |
|---|---|---|---|---|
| 6 × 900 m, 1 tier | ~540 MW | 3.1× | 2.3× / 2.5× | ~100 ha (ideal ~80 ha) |
| 6 × 900 m, 2 tiers | ~730 MW | 2.2× | 1.7× / 1.8× | ~165 ha (ideal ~110 ha) |
| 6 × 900 m, 3 tiers | ~920 MW | 1.8× | 1.3× / 1.4× | ~250 ha (ideal ~140 ha) |
| 6 × 1.6 km, 3 tiers | ~2.9 GW | 1.8× | 1.3× / 1.4× | ~740 ha (ideal ~430 ha) |

  - **So heat limits a stack of 900 m or 1.6 km tori to ~8 with three tiers lit, ~11 with two and ~15 with one** (ends only), against ~10–11, ~13 and ~18 from the ideal limit: still above six, with a thinner margin. The side gaps add only ~5–10% (the 10 m gaps are narrow next to the ~70 m envelopes). Not yet modelled: sunlight through the gaps, the spokes and cables, the envelopes' rounded faces, and a real panel layout (plan §6).
  - **Natural circulation:** spin gravity points outward along the spokes, so warm coolant rises towards the hub and cooled coolant sinks back to the rim. A thermosiphon loop can run without pumps (the driving force weakens near the hub).
  - **Light panels:** at ~285 K a 900 m torus needs ~16 ha of radiating surface for the valley and other loads, plus ~8.5 ha per farm tier lit: ~41 ha with three tiers, ~21 ha of two-sided panels in the ideal case; the ray tracing above puts it nearer ~40 ha of panels per torus in a six-stack (~2 kt at ~5 kg/m²). The stretch between farm ring and rim offers ~2.6 ha per spoke (~460 m × 56 m), so ~16 spokes carry it. The coolant must not freeze in cold panels; ammonia (as on the ISS radiators) needs only small quantities.
  - A shared coolant loop across co-rotating tori keeps the radiator load steady whichever tori are lit.
- **Day and night cooling (adopted direction).** Each torus has its own heat exchangers on the shared radiator loops, so its cooling follows its own day and night. Colder nights cost almost no energy: over a full day the valley gains and loses the same heat either way; a colder night only moves more of it out at night, and in the morning the lamps' waste heat (~70–80% of their power, already in the coolant above the ceiling) can warm the valley instead of going straight to the radiators.
  - **Heat to move:** only the air and the top ~10 cm of soil follow the daily cycle, ~0.15–0.25 MJ per m² per °C. A ~5 °C swing (oceanic coast) means ~0.8–1.3 MJ/m² a night, ~6–9 MW over 12 h for a 900 m torus; a ~15 °C swing (arid canyon) ~2.3–3.8 MJ/m², ~17–28 MW, about the light the valley absorbs by day and well within the radiators' capacity.
  - **A cold ceiling at night,** as the clear night sky cools the ground on Earth: with coolant in the ceiling at ~0 °C over ground at 15 °C, the ground radiates ~75 W/m², ~24 MW over a 900 m valley, with no fans or draughts.
  - **Limits:** passive radiators at ~285 K can't chill coolant much below the valley's temperature; coolant near 0 °C needs colder radiators (about a third more area at 265 K, the spokes have room) or heat pumps. A cold ceiling collects dew or frost, which dims the diffuser and drips: gutters, and humidity managed with it (little issue in a dry habitat). Lakes and wet soil store much more heat and damp the swing, which fits the two looks: a dry canyon swings easily, a wet gully resists.
- **No freezing with the rock jacket.** The water jacket's outer layers would have frozen on surfaces facing deep space (it conducts only ~1–2 W/m² against ~90 W/m² radiated even at 200 K, and water expands ~9% on freezing, bursting sealed cells). Rock doesn't care, which is one of the reasons for adopting it (section 5e). Only water-filled parts (soil, ponds, pipes, ballast tanks) need to stay inside the warm envelope.
- **Industrial radiators** run hotter (~500 K, ~3.5 kW/m² per face, ~15 ha per GW) and stay with the factory or mining site.

### Micrometeoroids and maintenance of the outer surfaces

Space debris is an Earth-orbit problem; at 1 AU, away from the planets, only natural micrometeoroids remain, and they are sparse. Impacts per km² per year (Grün model, ~20 km/s):

| Particle | Impacts per km² per year | Damage |
|---|---|---|
| ≥ 1 ng (~10 µm) | ~10⁸ (~100 per m²) | Slow pitting and fogging of surfaces |
| ≥ 1 µg (~0.1 mm) | ~1.5 × 10⁶ (~1.5 per m²) | Pinholes; a cell loses ~1 mm² |
| ≥ 1 mg (~1 mm) | ~600 | Holes a few mm wide; can crack a cell |
| ≥ 1 g (~1 cm) | ~0.07 (one per ~14 years) | Punches through a panel (~200 kJ) |
| ≥ 1 kg (~10 cm, extrapolated) | ~10⁻⁵ (one per ~100,000 years) | ~50 kg of TNT equivalent |

**Despun solar array:**
- **Impacts are negligible:** the 0.1 mm and 1 mm hits together take out roughly a millionth of the area per year.
- **Panels wear out from radiation and UV.** Always facing the Sun, the array has none of the thermal cycling the spinning cylinder had (~500,000 small swings a year).
- **Replacement:** with ~25–30-year panels, a 900 m torus's ~0.28–0.73 km² (no farm to three tiers lit) needs ~30–80 m² a day, about 7–20 modules of 4 m²; a 900 m six-stack ~40–120 modules a day, steady work for a few robots.
- **Worked in microgravity,** by tethered robots reachable from the hub; for major work the bearing is locked and the array keeps producing.

**Double outer skin on each torus (adopted):**
- **Layout:** a thin outer bumper (~1–3 mm of steel), an empty crawl space of ~1–2 m, then the wall of the rock cells. It is a Whipple shield, as on spacecraft: a meteoroid shatters or vaporizes on the bumper and its spray spreads across the gap before reaching the cell wall. A hole in the bumper leaks nothing, since the space behind it is empty. Covering a whole 900 m torus at ~2 mm of steel takes ~15 kt, ~0.1% of its mass.
- **It takes over the solar cylinder's bumper role,** which the cylinder used to play from ~10–20 m out.
- **Maintenance from inside.** On the floor side, crews work at ~1 g standing on the bumper with the rock cells overhead; that cell wall now carries the jacket's ~110 kPa outward load the single outer skin used to carry, so the structure is the same, with a bumper added outside. On the hub-facing side "down" points towards the rock, so crews stand on the cells with the bumper overhead, at ~0.94 g. The crawl space stays unpressurized: robots or suited crews, patching holes from inside.
- **Heat:** the bumper takes the direct sun and the minute-by-minute temperature swings, and shades the cells behind it.
- **The pressure hull is safe** behind 5.5 m of rock, which stops everything but ~10 kg-class objects arriving once in tens of thousands of years.
- **Rock leaking out is the risk the double skin answers.** On the floor side, centrifugal force presses the rock against the cell wall, so a hole there lets fine crushed rock trickle out; behind an intact bumper it only falls into the crawl space, where it can be swept up, instead of leaving at ~95 m/s. Cells lined with basalt-fibre fabric, or an outer layer of rock sintered into a crust, keep the fines in.
- **On the hub-facing side and the side walls** the rock presses away from the outer skin, so holes don't leak.

**Other sources:** dust from the mine moves at only a few m/s and dirties panels rather than holing them (keep mining tens of km away, and aim mass-driver streams away from the habitat); a host orbit crossing a meteoroid stream raises the flux ~10–100× for a few days a year; anything coming loose leaves at ~95 m/s onto a nearly identical solar orbit, so housekeeping matters.

---

## 14. Nickel

- **Separation is built into the carbonyl process.** Ni(CO)₄ forms at ~50–60 °C near ambient pressure, while Fe(CO)₅ needs several MPa, so a low-pressure stage extracts the nickel and a high-pressure stage the iron, or deposits **nickel cladding over iron parts**: corrosion protection for wet zones such as soil beds, ponds, pipes and ballast tanks (steel + water + 29% O₂ is ideal for rust otherwise). The dry rock jacket needs far less.
- **Maraging steels** (~18% Ni) reach 1.4–2.4 GPa, but also need ~9% cobalt and ~5% molybdenum, which fails the sourcing rule (section 10). The spokes use high-carbon drawn wire instead.
- **Invar** (36% Ni) barely expands with temperature: good for radiators and structures spanning hot-to-cold gradients.
- **Edison nickel-iron batteries** are made from iron, nickel and potash only: nearly indestructible, all-local buffer storage (~30 Wh/kg, ~65% round trip). With staggered days they are only needed for small buffers.
- **By-products:** cobalt, and platinum-group metals as catalysts for electrolysis and ammonia chemistry.

---

## 15. Reproduction, seeds and sites

A single parent habitat builds each child: its hub factory produces the child's hub panels, cable net and ring segments, following the construction sequence in section 12. A child stack is built torus by torus along its shared hub, with the despun solar array enlarged as each torus is added; staggered days only start once there are tori to alternate with. Diversity between habitats comes from exchange across the archipelago (people, seeds, soil, animals, culture and technology), as in the Polynesian model (section 16).

### Build where the bulk is; spread by seeds

Moving a finished habitat costs ~100–300× the energy of building one. Hohmann Δv between circular orbits: 1 AU ↔ Venus orbit ~5.2 km/s, 1 AU ↔ belt (2.7 AU) ~11.0 km/s (same in reverse). With electric propulsion (exhaust ~30 km/s, ~60% efficiency; rock-shield masses, excluding hub, factory and solar array):

| Configuration | Mass | To Venus orbit: energy | Propellant | To the belt: energy | Propellant |
|---|---|---|---|---|---|
| 2 × 900 m | ~26 Mt | ~115 GW·yr | ~4.9 Mt | ~280 GW·yr | ~11 Mt |
| 6 × 900 m | ~77 Mt | ~345 GW·yr | ~14 Mt | ~810 GW·yr | ~34 Mt |
| 2 × 1.6 km | ~83 Mt | ~375 GW·yr | ~16 Mt | ~875 GW·yr | ~37 Mt |
| 6 × 1.6 km | ~250 Mt | ~1,120 GW·yr | ~47 Mt | ~2,650 GW·yr | ~110 Mt |

(1 GW·yr ≈ 3.2 × 10¹⁶ J. A rock-throwing mass driver at ~5 km/s uses less energy but ~1.8× the habitat's mass in reaction rock for Venus, ~8× for the belt. Building a 900 m torus takes ~0.3 GW·yr of processing energy.)

Consequences:

- **Habitats stay where they are built,** sharing the orbit of their S-type asteroid. Circularising a typical near-Earth orbit (a few km/s) would cost ~30 GW·yr per 900 m torus; only small trims (tens to hundreds of m/s, tailings as reaction mass) are affordable.
- **The archipelago spreads by seeds:** factory modules, people, seed bank, soil microbiome and starter wildlife, ~0.1–1 Mt, then a new habitat built from local rock. This is the Polynesian model: canoes carried people, plants and knowledge, not islands.
- **The choice of asteroid is a choice of orbit and climate, for good.** Eccentricity sets the seasons (Itokawa's sunlight swings ~3×, from 1.1× to 0.35×), aphelion sets the size of the solar array, the semi-major axis sets the length of the year, and the orbit sets the close approaches and transfer windows; the C-type partner should be well aligned. S-types are ranked by orbit shape (low e, a near 1 AU) as well as by size and composition.
- **One km-class S-type supplies a whole cluster** (a 1 km rubble pile holds ~1 Gt, enough for ~80 tori of 900 m): the cluster's "mine island".
- **The C-type is refined at its source and only the products are shipped:** ~0.2–0.6 Mt per 900 m torus (nitrogen ~8 kt, carbon/organics ~15–50 kt, water ~0.15 Mt, plus ~0.37 Mt if spin-up uses water thrusters), ~2–5% of the habitat. Soil is made from crushed S-type silicates plus imported organics, nitrogen and microbes. Spin-up reaction mass is better sourced locally (rock in a mass driver) than shipped as water.

**Moving a newly built habitat, before it is inhabited (investigated, rejected).** Test case: circularising a 900 m pair at Itokawa (~25 Mt with hub and factory; ~5 km/s, since steered low thrust needs ≈ 0.7 × orbital speed × eccentricity) and a 1.6 km six-stack at Eros (~245 Mt; ~3.8 km/s).

Solar sail (~7.7 µN/m² at 1 AU, averaged over the orbit and halved for steering, since a sail can never push sunward; film ~10 g/m², aluminium on a carbon-based polymer):

| Habitat | Over 300 years | Over 1,000 years |
|---|---|---|
| 900 m pair at Itokawa | ~5,800 km² (~76 km square), ~60 kt of film | ~1,750 km² (~42 km square), ~18 kt |
| 900 m pair at Apophis (e = 0.19) | ~3,100 km² (~55 km square), ~30 kt | ~920 km² (~30 km square), ~9 kt |
| 1.6 km six-stack at Eros | ~53,000 km² (~230 km square), ~0.5 Mt | ~16,000 km² (~127 km square), ~160 kt |

Thrusters, with propellants the asteroids supply (xenon is a vitamin):

| Thruster, propellant | Exhaust speed | 900 m pair: propellant / energy / time at 10 GW | 1.6 km six-stack: propellant / time at 10 GW |
|---|---|---|---|
| Mass driver, crushed rock | ~4 km/s | ~62 Mt / ~20 GW·yr / ~2 yr | ~390 Mt / ~12 yr |
| Solar thermal rocket, oxygen or water | ~8 km/s | ~22 Mt / ~44 GW·yr / ~4 yr | ~150 Mt / ~30 yr |
| Hall thrusters, magnesium | ~30 km/s | ~4.5 Mt / ~110 GW·yr / ~11 yr | ~33 Mt / ~80 yr |
| Gridded ion | ~50 km/s | ~2.6 Mt / ~150 GW·yr / ~15 yr | ~19 Mt / ~110 yr |

- **Energy:** ~30–200× the ~2 × 10¹⁶ J of processing that builds the pair.
- **Propellant:** Itokawa holds only ~35 Mt in all, so mass drivers and solar-thermal rockets are out. Magnesium (~14% of chondritic rock, already a by-product of the glass line's acid leach) fits the sourcing rule, but ~4.5 Mt means processing ~30 Mt of rock, most of the asteroid.
- **Hardware:** 10 GW at Itokawa's average sunlight is ~50 km² of panels (silicon PV is a vitamin), ~90× the pair's own despun array at 1 AU; ~150–200 kt with the thrusters.
- **A sail** needs no propellant but takes centuries and a film tens of km across. The thrust lies in the orbital plane, perpendicular to the spin axis, so the sail must be a separate spacecraft towing from both hub tips through small swivels; reflective strips pulsed on the spinning stack give far too little force.
- **The thrust itself is easy:** ~10⁻⁵ m/s², and a ring of thrusters around each hub tip, each fired as it swings past the right direction (like the windings of a brushless motor), needs no despun parts.
- **Moving the structure before adding the rock shield** (~3 Mt instead of ~25 Mt) only helps if shield rock is available at the destination, and then building there is simpler.
- **What circularising would buy:** at Itokawa's semi-major axis, a constant ~0.57× sunlight (~1.6× the aphelion level, a year-round sky at ~80% of full with the same array), at the cost of the seasons and of leaving the mine. For the nurseries the leftover asteroid is the same order of mass (Itokawa ~35 Mt, Apophis ~40–60 Mt) and could be moved along; Eros (~6.7 × 10¹⁵ kg) cannot.
- **Conclusion:** habitats are built next to their S-type and adopt its orbit; the archipelago spreads by seeds.

### Candidate bodies (known examples, a feasibility check, not a plan)

| Asteroid | Type | Size | Mass | Orbit (a, e, i) | Sunlight, aphelion → perihelion | Year | 900 m tori supported |
|---|---|---|---|---|---|---|---|
| Itokawa | S, LL-like (samples) | ~330 m | ~35 Mt | 1.32 AU, 0.28, 1.6° | 0.35× → 1.10× | ~1.52 yr | ~1 by free metal (preliminary design); ~3 with iron from the silicates (not yet factored) |
| Apophis | Sq, LL-like (spectra) | ~340–370 m | ~40–60 Mt | today 0.92 AU, 0.19, 3.3°; after 2029 ~1.10 AU, ~0.19 | today 0.83× → 1.8×; after 2029 ~0.55× → 1.2× | ~1.2 yr after 2029 | ~1–2 by free metal (a pair only at the upper mass estimate); ~3–4 with iron from the silicates (not yet factored) |
| Bennu | B (C-complex) | ~490 m | ~73 Mt | 1.13 AU, 0.20, 6.0° | 0.54× → 1.24× | ~1.2 yr | ~15 (N-limited) |
| Ryugu | Cb | ~900 m | ~450 Mt | 1.19 AU, 0.19, 5.9° | 0.50× → 1.09× | ~1.3 yr | ~90 (N-limited) |
| Eros | S, L- or LL-like (NEAR) | ~17 km | ~6.7 × 10¹⁵ kg | 1.46 AU, 0.22, 10.8° | 0.32× → 0.78× | ~1.76 yr | hundreds of thousands |
| Didymos | S, L-like (spectra) | ~780 m | ~0.5 Gt | 1.64 AU, 0.38, 3.4° | 0.19× → 0.98× | ~2.1 yr | ~30 by free metal; ~45 with iron from the silicates |
| Torifune (2001 CC21) | Sq, L-like (spectra; Hayabusa2 flyby 2026) | ~465 m (estimates ~340–490 m), contact binary | ~100 Mt (~2 t/m³ assumed; ~40 Mt at the smallest size) | 1.03 AU, 0.22, 4.8° | 0.63× → 1.54× | ~1.05 yr | ~6 by free metal (~2 at the smallest size); ~9 with iron from the silicates (not yet factored) |

(Per 900 m torus: ~11 Mt of S-type rock for the shield and regolith and ~1.5 Mt of metal, which takes ~16 Mt of L-type or ~32 Mt of LL-type rock by free metal alone; ~5 Mt of C-type. Per 1.6 km torus: ~34 Mt of rock for the shield and regolith and ~7.5 Mt of metal (~83 Mt of L or ~165 Mt of LL rock); ~27 Mt of C-type. Ryugu supports ~17 tori of 1.6 km.)

**Note on Itokawa and Apophis.** With free metal only, a 900 m pair is impossible at Itokawa and uncertain at Apophis (a pair only at the upper end of its mass estimate). They demonstrate the process with **one or two 400 m / 40 s pairs** instead. A 400 m pair needs only ~0.33–0.53 Mt of metal (~7–12 Mt of LL rock) and ~5 Mt of shield rock, so each host has room for about three. **Two pairs demonstrate self-replication:** the second built by the first pair's factory (its 25 m segments pass through a ~27 m hub dock). The 900 m and 1.6 km habitats go to larger L/LL hosts, where mining more rock supplies the metal.

**Note on Torifune (added as a candidate, proposed).** Hayabusa2 flew past it at ~1 km on 5 July 2026 on the way to 1998 KY26; the flyby showed a contact binary, and its data are still arriving.
- **Composition:** ground-based spectra classify it Sq, best matched by L ordinary chondrites (Château-Renard, L6); its older "L-type" label is a spectral class, now superseded, not the L chondrite group. At ~9 wt% free metal, a 900 m torus takes ~16 Mt of its rock, so ~100 Mt supports ~6 tori: a 900 m pair, perhaps three, or many 400 m pairs. If the smallest size estimate (~340 m, ~40 Mt) holds, it is Apophis-class: one pair.
- **The mildest orbit of the candidates:** sunlight swings only ~2.4× (0.63× at aphelion, the brightest winter of any candidate, to 1.54× at perihelion, a hot summer like Apophis's today) over a year of ~1.05 Earth years. The array is the smallest of the candidates (section 15, seasonal sizing), and the biological year is nearly Earth's.
- **It could hold the demonstration and the first 900 m pair at one site,** if its mass is near the upper estimates.
- **Logistics:** easy to reach from Earth's orbit (~4.0 km/s, heliocentric) and from Itokawa (~3.6 km/s, perihelia ~23° apart), but poorly aligned with the known C-types: ~7.6 km/s from Ryugu and ~8.4 from Bennu (perihelia ~150–190° apart), so volatiles cost ~3–4 GW·yr per 0.5 Mt, affordable but a reason to look for a better-aligned C-type. Its period is so close to Earth's that their relative position repeats only every ~22 years, so transfer windows from Earth come in clusters decades apart. It doesn't come close to Earth (minimum orbit distance ~0.08 AU).

### H-type hosts near Earth

- **H-like near-Earth asteroids exist but are the minority.** About two thirds of near-Earth asteroids resemble LL chondrites (Vernazza et al. 2008). Among 47 ordinary-chondrite-like near-Earth asteroids, Dunn et al. (2013) found ~15% H, ~10% L, ~60% LL and ~15% L or LL; the larger MIT-Hawaii survey's model puts S-complex near-Earth objects at ~29% H-like, ~19% L-like and ~51% LL-like.
- **The known H-like ones have poor orbits for a habitat.** Dunn et al. note they mostly have a > 1.8 AU and cluster near the 3:1 resonance with Jupiter. Four of their H-like objects:

| Asteroid | Size | Orbit (a, e, i) | Perihelion → aphelion | Sunlight swing |
|---|---|---|---|---|
| (5587) 1990 SB | ~3.6–4.9 km | 2.40 AU, 0.54, 18° | 1.09 → 3.71 AU | ~0.83× → 0.07× (~11×) |
| (16960) 1998 QS52 | ~3.3–4.1 km | 2.20 AU, 0.86, 17.5° | 0.31 → 4.09 AU | ~10× → 0.06× (~170×) |
| (159857) 2004 LJ1 | ~2.5–3.1 km | 2.26 AU, 0.59, 23° | 0.93 → 3.59 AU | ~1.2× → 0.08× (~15×) |
| (99907) 1989 VA | ~0.55 km | 0.73 AU, 0.59, 29° | 0.30 → 1.16 AU | ~11× → 0.74× (~15×) |

  (The other three in Dunn et al.'s H list, (5626) 1991 FE, (138524) 2000 OJ8 and (143624) 2003 HM16, still need orbit and size lookups.)
- **So H and a mild orbit pull in opposite directions** among known objects: the LL-like population (from the inner main belt's Flora region, through the ν6 resonance) has the habitat-friendly orbits. Km-scale H-like bodies hold tens of Gt, so they would make excellent metal mines, worked from habitats on better orbits, if the Δv is affordable; as hosts, their ~11–170× sunlight swings rule them out.
- **Consequence:** the L/LL candidates stay the working sites, and the design's metal route for them (more rock, or iron from the silicates) is the baseline rather than a fallback. The catalogue search continues for H-like objects with low eccentricity, likely among smaller or newly characterised bodies.

### Phases (adopted as the working scenario)

1. **Demonstration: one or two 400 m / 40 s pairs at Itokawa and Apophis** (note under the candidate table). Per torus: a 25 m valley, ~6.3 ha of floor (~3 ha of wilderness), ~200 people per farm tier lit (~600 with three), ~2.8 Mt, ~11 MW for the valley's sky plus ~6.3 MW per tier, ~0.7 kt of nitrogen. They prove the rock jacket and double skin, cable spokes, the pair rule and despun array, the light-box sky and the tiered farm ring, life support, the factory chain and the first population, and they start the long-term gravity experiment (1.5 rpm; Coriolis at a 5 m/s run ~±16% of weight). A second pair built by the first demonstrates self-replication. The valley is a planted hall rather than a landscape, and its tiny wilderness depends on exchange. Their factories also act as seed factories for the larger habitats, which are built on site (a 900 m torus's 56 m segments don't fit a 400 m pair's dock).
2. **900 m pairs on a larger L/LL host** (Eros as the working case; Didymos possible, with a more eccentric orbit; Torifune possible for a first pair on the mildest orbit, proposed, if its mass is near the upper estimates), metal from mining more rock.
3. **First real islands: 1.6 km six-stacks at Eros, with Ryugu as the C-type partner.** Per six-stack: ~250 Mt of habitat, ~0.5–1 Gt of Eros rock for an L or LL host by free metal (negligible against Eros's mass; an earlier ~240 Mt assumed H-like metal), ~600 ha of floor, ~270 kt of nitrogen from ~160 Mt of Ryugu. **Nitrogen limits the Eros cluster** to ~3 six-stacks per Ryugu; growing beyond needs more C-type partners or a lower atmospheric pressure.

### Supply and seed transfers: Δv check

Rendezvous Δv (departure + arrival burns), two-body heliocentric orbits from published elements, zero-revolution Lambert transfers scanned over departure dates and flight times. "Best phase" ignores where each body is on its orbit (a lower bound for that pair); "dated" uses real positions for departures 2030–2060. The Apophis post-2029 orbit is approximated (a = 1.103 AU, e = 0.189, other angles kept). Script: `asteroid_transfers.py`.

| Transfer | Best phase | Dated, 2030–2060 | Note |
|---|---|---|---|
| Bennu → Itokawa | 8.3 km/s | 8.5 km/s (depart 2048, 540 d) | perihelia almost opposite |
| Bennu → Apophis | 7.4 km/s (post-2029) | 9.2 km/s before the 2029 flyby | |
| Bennu → Eros | 5.8 km/s | 6.2 km/s (depart 2045, 220 d) | |
| **Ryugu → Itokawa** | 6.3 km/s | 6.3 km/s (depart 2033, 350 d) | better than Bennu |
| **Ryugu → Apophis** | 5.5 km/s (post-2029) | — | better than Bennu |
| **Ryugu → Eros** | **4.5 km/s** | **4.7 km/s (depart 2056, 350 d)** | perihelia aligned (~103° vs ~123°) |
| Earth's orbit → Itokawa / Apophis (post-2029) / Ryugu / Bennu / Eros / Torifune | 4.3 / 4.1 / 4.3 / 5.1 / 6.9 / 4.0 km/s | — | heliocentric, Earth's gravity well not included |
| Itokawa → Eros / Apophis → Eros | 7.8 / 7.3 km/s | — | nursery seeds to Eros |
| Ryugu → Torifune / Bennu → Torifune | 7.6 / 8.4 km/s | 7.6 km/s (depart 2051, 340 d) / 8.4 km/s (depart 2030, 420 d) | perihelia ~150–190° apart |
| Itokawa → Torifune / Apophis → Torifune / Torifune → Eros | 3.6 / 5.7 / 8.6 km/s | 3.6 km/s (depart 2037, 290 d) | Itokawa and Torifune have perihelia ~23° apart |

Shipping energy with electric propulsion (~30 km/s exhaust, ~60% efficiency) is `½ (e^{Δv/vₑ} − 1) vₑ² / 0.6` per kg delivered: ~1.2 × 10⁸ J/kg at 4.5 km/s, ~1.75 × 10⁸ at 6.3 km/s, ~2.5 × 10⁸ at 8.5 km/s. For ~0.5 Mt of volatiles per torus: ~2 GW·yr at 4.5 km/s, ~3 GW·yr at 6.3 km/s, ~4 GW·yr at 8.5 km/s; comparable to or above the ~0.3–1.4 GW·yr of processing energy per torus, but affordable.

Findings:

- **Orbit alignment matters as much as size.** Bennu and Itokawa have similar orbit sizes but nearly opposite perihelion directions, so their relative speeds are high. Good partners have similar eccentricity, inclination **and** perihelion longitude: Ryugu–Eros is the best of the known examples.
- **Ryugu is a better supplier than Bennu for all three S-types.** The working scenario becomes Ryugu for the nurseries as well, or a better-aligned C-type found in the catalogue.
- **Seeds from Earth's vicinity are cheaper to reach Eros (~6.9 km/s) than seeds from the nurseries (~7.3–7.8 km/s).** Eros's 10.8° inclination makes it costly from anywhere; seed masses are small, so this matters less than for volatiles.
- **Caveats:** two-body propagation from old epochs over decades, no planetary perturbations, no gravity assists, single-revolution transfers only, impulsive burns. A proper search would use current ephemerides and filter the catalogue for well-aligned S/C pairs.

### Solar sizing by orbit: seasonal sky (adopted)

The habitat adapts to its environment: the sky follows the host asteroid's seasons, with **no seasonal (yearly) energy storage**. The valley's share is sized at aphelion for a sky at half its normal level (constant-sky figures for comparison). The farm runs at full output all year, so its share is sized at aphelion at full output. Area of the despun array per torus, sized so that even locked it keeps the habitat alive and fed (tracking, it gives ~1.57× that power):

| Site | Sunlight at aphelion | 900 m valley, constant / seasonal sky | 900 m, + per farm tier lit | 1.6 km valley, constant / seasonal sky | 1.6 km, + per farm tier lit |
|---|---|---|---|---|---|
| 1 AU (reference) | 1× | 0.27 / 0.14 km² | 0.15 km² | 0.85 / 0.45 km² | 0.48 km² |
| Apophis today | 0.83× | 0.32 / 0.17 km² | 0.18 km² | 1.0 / 0.55 km² | 0.57 km² |
| Apophis after 2029 (approx.) | 0.58× | 0.46 / 0.25 km² | 0.26 km² | 1.5 / 0.8 km² | 0.82 km² |
| Itokawa | 0.35× | 0.76 / 0.41 km² | 0.42 km² | 2.4 / 1.3 km² | 1.37 km² |
| Eros | 0.32× | 0.84 / 0.46 km² | 0.47 km² | 2.65 / 1.45 km² | 1.51 km² |
| Torifune | 0.63× | 0.42 / 0.23 km² | 0.23 km² | 1.35 / 0.71 km² | 0.76 km² |

For example, a 900 m pair at Eros needs ~1.9 km² with one tier lit per torus and ~3.8 km² with three; a 1.6 km six-stack at Eros with two tiers lit needs ~27 km². With the seasonal sky halving the valley's share, food becomes the largest part of the array.

Further reductions: the 915 MHz microwave sources (~20–25% less power), concentrating mirrors on the array, and a seasonal harvest with stored staples (~30–40% less array for the farm; an option, section 13). **Perihelion is the industrial season:** at Itokawa the array produces ~3× its winter output at perihelion, ~2.5× at Eros.

### Climate and winter light

- **Temperate, North-Atlantic-like on the first sites:** winter mean ~6–8 °C with occasional light frost (useful for plants that need chilling), summer ~16–19 °C; the rock jacket and soil give ocean-like thermal mass. Drizzle fits the overcast sky if the air is kept humid.
- **Winter light without storage (900 m pair at Itokawa,** seasonal-sky array; the table is the survival case with the array locked, ~55 MW available for the lit valley in midwinter against ~110 MW in summer; the farm's share of the array is separate and keeps its tiers at full output):

| Winter day length | Light per valley (sulfur, ~1.4 µmol/J) | With 915 MHz sources (~1.75 µmol/J) | Dark gaps for the factory | Same midwinter day length on Earth |
|---|---|---|---|---|
| 12 h | ~7.5 mol/m²/day | ~9.3 | none | Equator |
| 10 h | ~6.3 | ~7.8 | 4 h | ~30°N |
| **8.5 h** | **~5.3** | **~6.6** | **7 h** | **~48°N (Brittany, Paris)** |
| 7 h | ~4.4 | ~5.4 | 10 h | ~56°N |
| 6 h | ~3.8 | ~4.7 | 12 h | ~60°N |

  (With the light-box ceiling, ~25% losses. Summer reference: ~15 mol/m²/day over a 12 h day. Tracking normally, the array gives ~1.57× these figures, ~8.3 mol/m²/day at 8.5 h days with sulfur lamps.) The 8.5 h option is a little brighter than a cloudy north-western European December (~2–5 mol/m²/day outdoors); the schedule can dim it.
- **Pairs: Atlantic winters, equinox-length summers.** A pair's day never exceeds 12 h, so long-day plants (flowering only above ~13–14 h) won't flower in its valleys; day-neutral and short-day species are fine. (The farm ring sets its own day lengths, so long-day crops such as wheat grow there.) **Six-stacks allow 8–16 h days**, the natural home for long-day species: another reason to exchange species between habitats.
- **Year length:** ~1.05 years (Torifune), ~1.2 (Apophis after 2029, Bennu), ~1.5 (Itokawa), ~1.76 (Eros). Species keyed to day length and temperature follow the longer cycle; tightly timed annual plants and insects may behave unexpectedly. Following the asteroid's year keeps sky and sunlight in step.
- **Future tropical habitats:** an S-type on a near-circular orbit between Earth and Venus would give strong, steady sunlight and little seasonality, a tropical island group with its own species pool.

### Trade between inner and outer habitats

- **Inward,** light is plentiful but asteroids are scarce and volatile-poor: Atens (cross Earth's orbit), Atiras (23 known in 2020, ~8 km-sized S-types expected), one Vatira (2020 AV₂, ~1.5 km, olivine-rich), no vulcanoids. Inner bodies drift in from the main belt and survive ~10–20 Myr. Mercury is the exception: metal-rich, volatile-rich surface, water ice under organic-rich dark material in polar craters, but a 4.25 km/s escape velocity, deep in the Sun's well, ~6.7× sunlight.
- **Outward,** volatiles are plentiful but light is scarce.
- Inner habitats could export energy-intensive products (refined metals, wire, solar film, manufactured parts) and import small amounts of nitrogen and carbon; outer habitats export volatiles. Near Earth both are in reach, another argument for starting there.


## 16. Vision

- **Directed panspermia by habitat**, not by planet. Earth is already a space habitat, only very large ("Spaceship Earth"). The aim is to replicate it in miniature, like islands, carrying as much nature as possible. Interplanetary or interstellar travel may come later.
- **Polynesian model.** An archipelago of habitats exchanging people, plants, animals, culture and technology. A "canoe plants" seed kit for each founding.
  - Larger habitats = **high islands**: species-rich reservoirs.
  - Many small and medium tori = **atolls**: numerous and quick to found.
  - Together they form one metapopulation, countering genetic loss on small islands.
- **Interior: a natural narrow valley** under an overcast sky. At least **half of the floor is wilderness.**
  - **Its climate is set by four dials:** the size of the solar array (how much light and warmth the habitat can afford), the lighting (level and day length), the seasonality of the host orbit, and the amount of water in the atmosphere (humidity, rain, streams).
  - **The same valley can look like an arid canyon or a fern gully:** dry air, a brighter sky, little water and wide day/night swings give a canyon; humid air, a dimmer sky, running water and small swings give a gully. **One climate per habitat,** shared by all its valleys so that species move between them as one population; diversity comes from the archipelago, where each habitat or cluster can have its own climate and species pool.
  - The tube cross-section makes the walls steepen into cliffs.
  - Humans live and work in cliff dwellings behind extra soil, which doubles as the extra-shielded sleep and work zones.
  - Recreation happens in the wilderness.
  - Dense habitats look park-like; sparse ones cluster humans in villages to leave room for wild animals.
- **Island biogeography.** About 16 ha (900 m), 50 ha (1.6 km) or 120 ha (2.5 km) of wilderness per torus supports forest, streams, insects, birds, amphibians and small mammals. Connected valleys count as one area: a six-stack holds ~96 ha (900 m), ~300 ha (1.6 km) or ~735 ha (2.5 km). A six-stack of 1.6 km can hold a few dozen deer, still a small population that depends on exchanges between habitats. Exchange between habitats is essential.
- **Biosphere selection (adopted principles):**
  - **One climate and one ecosystem per habitat,** not per valley: even the largest valley is too small for two ecosystems, and six connected valleys make a stronger biosphere than six separate smaller ones.
  - **Valleys are connected for migration.** Same-phase neighbours are already joined by rim tunnels into double valleys (section 13). Across a phase boundary (8 h apart in a six-stack, 12 h in a pair) a tunnel leads from day into night: no obstacle for rodents, foxes, martens, bats and walking insects, harder for birds and deer, so the tunnels are wide, planted at their mouths, with light grading from one valley's sky to the other's. Little movement is needed: a common rule of thumb in conservation genetics is about one migrant per generation between subpopulations, which people can supplement by moving seeds, insects and the odd animal, as between habitats.
  - **No attempt to replicate a precise Earth biome:** it won't be the same. Choose super-common, adaptable generalists that have already proven they thrive in other biomes on Earth, and describe the forest at genus level (fir, pine, oak, alder, cherry), since what spans regions is often two close species rather than one.
  - **Species that cope with both temperate and tropical-highland day lengths,** showing they don't depend on long summer days: examples are Douglas fir (native from the Mexican highlands to British Columbia, widely planted in Europe, New Zealand and Chile) and American hornbeam (eastern North America to the Central American highlands). Alders are a bonus: they fix nitrogen, helping turn crushed rock into soil.
  - **The day/night temperature swing is a habitat-wide climate dial** (section 13, heat rejection): a few °C for a humid, oceanic habitat, 15 °C or more for an arid one. Species are chosen to match their habitat's swing; the first, North-Atlantic-like habitats keep it small (~4–8 °C), so they avoid trees that need a large day/night differential.
  - **No migratory species;** resident animals with flexible breeding.
  - **Animals: the same principle, super-common and adaptable,** many already living alongside humans: deer (e.g. white-tailed deer), rats, mice, sparrows, pigeons, squirrels, opossums, foxes, bats, corvids, blackbirds.
  - **Deer only in the larger habitats** (Eros six-stacks), none in the nursery pairs. With no room for wolves or lynx (a pack ranges over a few hundred km², a lynx over ~100 km² or more), deer numbers are controlled by hunters or contraceptives.
  - **Small predators fit:** owls, foxes and martens, which will help control the rodent population that will inevitably follow humans.
  - **Good colonisers can be invasive,** so the mix is balanced to keep one species from taking over.
  - **Test on Earth first:** growth chambers running 1.2–1.8-year cycles for candidate species before they travel.
- **The habitat as organism**, with a fractal analogy: cells → humans → villages → habitats → archipelago. It feeds on photons and asteroid and comet materials, and sometimes reproduces. Individuals keep their individuality, as within a village, a state or a corporation.
- **An AI mind as steward and homeostasis.** Small closed ecosystems drift fast: in Biosphere 2 (1.27 ha), O₂ fell from ~21% to ~14% in about 16 months, as soil microbes respired the compost-rich soil and the concrete absorbed the CO₂. The 900 m torus holds only ~36 kg of air per m² of floor, against Earth's 10,300. The habitat is closely monitored by a central computer, an AI acting as its mind. How that mind is built and how it relates to the inhabitants' governance is not yet discussed (section 18).
- **Food, primarily plant-based**, with backups: when all is well the habitat eats plants; in an emergency it has other options. Options are judged by how efficient and useful they are, not excluded for not being vegan.
  - **Algae** in tanks (under the floor or in the cliff zones, where they double as the hydrogen-rich inner layer of the rock shield, or in trays above the ceiling lit by dedicated upward light pipes, section 13), lit artificially:
    - light budget ~2–3.5 kW per person (~106 W of food energy at 3–5% light-to-biomass);
    - microalgae are protein-rich and contain ~4–6% nucleic acids by dry weight (3–8% across algae); with the UN Protein Advisory Group guidance of ~2 g/day of nucleic acids from novel protein sources (2.6 g cited in some studies), safe intake is roughly **35–65 g dry/day**: a protein and micronutrient base, not bulk calories, unless starch- or oil-rich strains are used or the biomass is processed to remove nucleic acids.
  - **Starchy calories from water (proposed, to discuss):** taro in flooded terraces (Hawaiian loʻi), rice, lotus root, water chestnut. Flooded terraces on the lower canyon walls add shielding mass too.
  - **Small permaculture areas** supplement the diet: with the food forest, ~7% of the working diet (fruit and nut trees, corn, squash and beans).
  - **Food forest and edible wilderness (low-density biospheres, with few farm tiers lit):** a food forest next to the permaculture. Near the villages, trees that give good timber or fruit and nuts are favoured (chestnut and walnut, for example, give both), and the rest of the wilderness stays edible as a backup (oaks, pines, cherries and hazels give acorns, pine nuts, fruit and hazelnuts; acorns need leaching to remove their tannins).
  - **Farm rings, the staple diet:** three tiers in each torus's plane at ~0.4 r under sulfur lamps (section 13): potatoes, wheat, soybeans, lentils, berries, flax and greens, ~93% of a 2,500 kcal working diet. Each tier lit feeds ~1,000 people per 900 m torus conservatively (~3,250 at 1.6 km, ~7,900 at 2.5 km), for ~31 kW of electricity per person; a habitat lights as many tiers as its array allows, and a low-density one exports food:
    - at ~0.4 g (cheaper structure);
    - plants orient fine in low g;
    - crops tolerate deep-space cosmic-ray doses, so the rings can be lightly shielded;
    - only the seed bank needs the full shield.
  - **Vitamin B12 (proposed, to discuss)** from a bacterial fermentation line: spirulina's B12 is mostly pseudovitamin B12, inactive in humans.
  - **Gas-fermented bacteria (no light):** electricity splits water, and hydrogen-oxidising bacteria grow on the hydrogen, CO₂, oxygen and nitrogen. Solar Foods (Solein) puts electricity-to-calories at **~20%**, against ~0.4–0.6% for crops under sulfur lamps (~18–31 kW of electricity per person, section 13) and ~1–1.5% for algae, so ~0.5 kW per person for the same ~106 W of food energy, ~35–60× less than crops. A 2021 PNAS study (Leger et al.) found solar-powered microbial protein needs ~10% of the land per kg of protein that soybeans do. It consumes the habitat's CO₂ and its inputs pass the sourcing rule. Caveats: nucleic-acid-rich biomass needs processing to remove them (as for mycoprotein); mostly protein (~15% of a diet's energy), so the big gain needs microbial calories (fats, sugars from CO₂ routes, under research); hydrogen plus oxygen is explosive, so the reactors belong in the factory zone.
  - **Mushroom + larvae cycle (no light, no extra energy):** mushrooms (e.g. oyster, ~0.5–1.5 kg fresh per kg of dry substrate, ~20–30% protein dry) grow on inedible crop residue (stems, leaves, prunings, straw); black soldier fly larvae turn the spent substrate, compost and food waste into protein and fat (~13–15% of the waste becomes larvae, ~48% protein and ~28% fat dry; waste dry mass cut ~70%). Their frass returns to the soil after composting (heavy metals can accumulate, to watch with asteroid-derived soil).
  - **Aquaponics with fish (very low light):** fish in tanks in the cliff zones or the hub, fed on larvae and other low-grade protein (~1.5–2 kg of feed per kg of fish); their water fertilises crops. Any species works in the dark.
  - **Ranking by efficiency and usefulness:**

| Option | Energy efficiency | Usefulness |
|---|---|---|
| Gas-fermented bacteria | ~20% electricity → calories, no light | Bulk protein, consumes CO₂ |
| Larvae on waste | No extra energy | Protein and fat from what would otherwise be lost; frass for soil |
| Mushrooms on residue | No extra energy | Food and flavour from inedible plant parts |
| Fish in low-light tanks | ~1.5–2 kg of feed per kg of fish | High-quality protein and fats from larvae and low-grade protein; fertilises crops |
| Lit crops and algae | ~0.4–0.6% (crops) to ~1–1.5% (algae) electricity → calories | The only route to a complete diet (starches, fats, vitamins, fibre), plus oxygen and the landscape |

  - **Animals are efficient when they eat what people can't** (larvae on waste, fish on larvae); feeding fish on protein people could eat directly is usually a loss unless it adds nutrients or variety.
  - **Emergency food sources:** fish and larvae from the two cycles, and, if needed, all of the habitat's birds and animals (for example the rats that will inevitably follow humans, pigeons, or deer in the larger habitats). They add resilience if crops or reactors have a bad season.
  - **Energy flows of the food model:** (1) electricity → lamps → crops and algae → people (~0.4–1.5%); (2) crop residue → mushrooms → people, and residue and waste → larvae → fish or frass → soil; (3) electricity → hydrogen → bacteria → protein → people (~20%), consuming the habitat's CO₂. With crops at ~31 kW per person, the share of calories from route 3 largely sets how many more people a habitat could feed for the same power.

---

## 17. Considered and rejected

Kept here to document the research path and the reasoning behind each decision.

### 17.1 Stanford-style mirrors and windows

- **Idea:** let sunlight in through chevron mirror baffles that cosmic rays can't follow.
- **Rejected:** windows and light paths complicate the shield, and the artificial overcast sky (section 13) gives the desired uniform light, spectrum and night cycle. It also removes any need to point the axis at the Sun.

### 17.2 Larger tori (beyond 2.5 km)

- **Idea:** bigger habitats for more land per unit.
- **First rejected above 1.6 km** with the water jacket and self-supporting ring: no economy of scale, the steel limit at 6.4 km, per-m² mass rising steeply above ~2.5 km.
- **Revised with the rock jacket and cable spokes:** 2.5 km / 100 s is a candidate (section 8). **Beyond it, rejected for now:** the mass per m² keeps rising (~47 t at 3.6 km), nitrogen per m² grows with the air column (~100 kg per m² of floor at 3.6 km), the C-type and S-type per torus grow faster than the floor, and small units replicate faster. CFRP extends the range but is much harder to automate, and its usual precursor needs nitrogen.

### 17.3 Rotating cylinders (O'Neill style)

- **Idea:** the whole inner wall is floor, so shielding is used more efficiently.

Model: floor `2πrL`, caps `2πr²` (shielded, not floor), hull `t = (P + m·g)·r / (σ − ρ g r)` (2.39 t/m² at 900 m, 4.86 t/m² at 1.6 km), air `0.852 kg/m³ · π r² L`.

**900 m radius**

| Shape | L/r | Floor | Total | t/m² floor | N₂ kg/m² |
|---|---|---|---|---|---|
| Torus | — | 32 ha | 8.2 Mt | 25.7 | 25 |
| Cylinder, L = 450 m | 0.5 | 254 ha | 75 Mt | 29.3 | 261 |
| Cylinder, L = 900 m | 1 | 509 ha | 102 Mt | 20.0 | 261 |
| Cylinder, L = 1.8 km | 2 | 1,018 ha | 155 Mt | 15.3 | 261 |
| Cylinder, L = 7.2 km | 8 | 4,072 ha | 478 Mt | 11.7 | 261 |

**1.6 km radius**

| Shape | L/r | Floor | Total | t/m² floor | N₂ kg/m² |
|---|---|---|---|---|---|
| Torus | — | 100 ha | 29.6 Mt | 29.5 | 44 |
| Cylinder, L = 800 m | 0.5 | 804 ha | 299 Mt | 37.2 | 465 |
| Cylinder, L = 1.6 km | 1 | 1,608 ha | 407 Mt | 25.3 | 465 |
| Cylinder, L = 3.2 km | 2 | 3,217 ha | 623 Mt | 19.4 | 465 |
| Cylinder, L = 12.8 km | 8 | 12,868 ha | 1,921 Mt | 14.9 | 465 |

Passive stability for a shell with caps of equal areal mass:

```
I_axis > I_transverse  ⇔  x³ + 3x² − 6x − 3 < 0,  x = L/r  ⇒  L < ~1.67 r
```

- **Rejected:** ~10× the nitrogen per m² of floor, 12–14× the mass per generation, and only ~20–25% mass saving within the stability limit. Longer cylinders need active nutation control forever, whatever the orientation (section 17.7).

### 17.4 Sun-pointing axis with a counter-rotating pair and a non-rotating spine

- **Idea:** point the spin axis at the Sun, with a solar-panel sunshield on the sunward end and radiators on the dark end. Two counter-rotating tori cancel the net angular momentum so the stack can precess once a year cheaply.

| | 900 m | 1.6 km |
|---|---|---|
| Single-torus angular momentum | ~7 × 10¹⁴ N·m·s | ~6 × 10¹⁵ N·m·s |
| Torque to precess once a year | ~1.4 × 10⁸ N·m | ~1.2 × 10⁹ N·m |
| Couple carried by a 10 m radius axle | wall ~1 mm | wall ~8 mm |
| Bearing force (bearings 100 m apart) | ~1.4 MN | ~12 MN |
| Spin-up energy, both tori (motor in the joint) | ~7 × 10¹³ J | ~5 × 10¹⁴ J |
| Full-disk sunshield power (25% PV) | ~1 GW | ~3 GW |

Explored details: magnetic or hydrostatic bearings; propellant-free spin-up by torquing the tori against each other; transfers through the axis (~0.2 m/s relative speed at 1 m); rotary unions for fluids; gigawatt power kept off rotating joints; dock on the spine; balancing by ballast water; torque-limiting breakaway against seizure.

- **Rejected:** depends for centuries on heavy rotating bearings under continuous load, with a catastrophic seizure failure mode. The requirement that created it, sun-pointing, disappears with the artificial sky and the ecliptic-normal orientation (section 11).

### 17.5 Non-rotating annular shield can around the pair

- **Idea:** with a non-rotating spine and sunshield available anyway, enclose the tori in a stationary shell carrying the shield. The spinning structure then carries only soil, air and itself.

| | 900 m pair | 1.6 km pair |
|---|---|---|
| Shield on the tori (cable spokes) | ~15.5 Mt | ~52 Mt |
| Non-rotating water can (total) | ~16.7 Mt | ~49 Mt |
| Can shield area vs. two torus hulls | 1.18× | 1.08× |
| Spinning steel per torus, in can | ~0.1 Mt | ~0.7 Mt |

Attractive side effects: the shield can be tailings (~11 t/m²) or ice blocks; mass per m² stays flat with size; the shell can be built first as a shielded construction "egg".

Precedent: the 1975 Stanford Torus design also used a non-rotating shield, 1.7 m of raw lunar soil making up ~95% of its total mass.

Costs: spoke slot through the inner wall, rims passing the stationary wall at ~100 m/s with metres of clearance, algae layer displaced, and a torus breakup threatening the can.

- **Rejected:** relied on the rejected spine. A free-floating nested shell without contact needs perpetual active station-keeping, with a collision as the failure mode.

### 17.6 Counter-rotating stacks inside a shielded cylinder

- **Idea:** an even number of tori alternating spin direction (A B A B) in a non-rotating can. Net angular momentum is zero (no instability at any length), the spine moment never exceeds one torus's couple, and the end caps are shared.

| Tori in stack | 900 m: t/m² floor | 1.6 km: t/m² floor |
|---|---|---|
| 2 | 26.2 | 24.5 |
| 4 | 21.6 | 20.4 |
| 8 | 19.3 | 18.4 |
| 16 | 18.2 | 17.4 |
| ∞ | 17.0 | 16.3 |

Same nitrogen per m² as a single torus; radiators could wrap the can's shaded sides.

- **Rejected:** needs a bearing between every pair of counter-rotating neighbours, a long spine, and ~190 m/s relative rim speed across small vacuum gaps.

### 17.7 Long co-rotating stacks and long cylinders with active control

- **Idea:** with the axis perpendicular to the orbit, no precession torque is needed, so only nutation damping (thrusters, ballast pumping) is required.
- **Rejected:** spinning about the minimum-inertia axis is unstable with any internal dissipation (Explorer 1). Control is cheap but mandatory forever; a long enough control failure means a tumbling habitat. Short co-rotating stacks (≤ ~1.5–2 r) are kept as an option because they are passively stable.

### 17.8 Radial spokes anchored on a hub flange

- **Rejected in favour of tangent-chord spokes:** the flange would carry the full rim hoop force around the factory (section 12).

### 17.9 Self-supporting ring with non-structural elevator spokes

- **Rejected:** rigid elevator spokes pick up load anyway through strain mismatch, every segment joint becomes a critical tension splice, and plate steel is weaker than wire.

### 17.10 Two-parent reproduction

- **Idea:** two counter-rotating pairs each produce one torus of the child pair, like sexual reproduction.
- **Dropped** together with the counter-rotating architecture (section 17.4).

### 17.11 Comets as the main volatile source

- **Demoted to optional:** a Bennu-class C-type supplies water, nitrogen, carbon and soil for the baseline sizes, and is easier to reach and handle than a comet nucleus. With the rock shield, little water is needed at all.

### 17.12 Sea-level 80/20 atmosphere

- **Superseded** by 70 kPa / 29% O₂: same oxygen for lungs and plants, 39% less nitrogen, 30% less pressure load.

### 17.13 Travelling day around the ring

- **Idea:** light half of the ring at a time, brightest at a "noon point" that moves around the ring once a day, giving a constant lighting load from a single torus.
- **Rejected:** at 900 m noon and midnight are only ~2.8 km apart and dusk to full dark spans a few hundred metres; a bird at 10 m/s would fly from noon into night in ~5 minutes (under 10 at 1.6 km), and other animals would be similarly confused. On Earth the terminator moves at ~1,670 km/h at the equator. It would only suit habitats far larger than these. (Side effects noted at the time: a travelling warm zone would create gentle weather, and the ring would have time zones, ~1 hour per ~240 m at 900 m.)

### 17.14 Single torus with one shared day, balanced by storage or night-shift industry

- **Idea:** keep a single torus; size solar for the daytime peak, store ~240 MWh a day (900 m) in nickel-iron batteries, or run the hub factory at night on the surplus.
- **Superseded** by staggered tori (section 13): the night-shift factory absorbs the surplus but cannot cover the daytime deficit, and storage needs a larger solar supply to cover its ~35% losses. With staggered tori the factory can run steadily instead.

### 17.15 Radiators on the faces, then radiator fins

- **Idea:** radiators on the two permanently shaded faces of each torus; in a stack, annular fins in each gap plane sticking out ~25–50 m beyond the solar cylinder, edge-on to the Sun.
- **Superseded** by radiators along the spokes: in a stack the faces look at each other, and the fins are unnecessary once the shaded drum between hub and rims is used as a radiator cavity.

### 17.16 Maraging steel spokes

- **Rejected** under the sourcing rule: ~9% cobalt and ~5% molybdenum per tonne of wire, and molybdenum is ~1 ppm in chondritic material. Replaced by high-carbon drawn wire (section 10).

### 17.17 Solar panels on spokes extending beyond the rim

- **Idea (original design):** spokes pass through the rim and continue outward carrying solar panels.
- **Superseded** by the capless solar cylinder: panels on spokes would have to rotate to avoid shading each other, and centrifugal load grows with radius. A continuous cylinder just beyond the rims never self-shades and needs no articulation. (The cylinder was itself superseded by the despun solar array, section 17.28.)

### 17.18 Alternating phases A B C A B C

- **Superseded** by A A B B C C: grouping same-phase neighbours lets them share rim tunnels without light-locks and leaves only two 8-hour time boundaries instead of five.

### 17.19 Spinward or two-way rim trains

- **Rejected:** spinward trains make riders heavier (1.17 g at 10 m/s, 1.42 g at 20 m/s on the 900 m torus), breaking the 0–1 g rule, and two-way traffic needs two tracks or passing loops. The one-way antispinward loop keeps every trip at or below floor gravity.

### 17.20 Small rotating-bulb sulfur lamps

- **Superseded** by non-rotating bulbs fed from large central microwave sources: one motor, air jet and small magnetron per lamp would mean tens of thousands of moving, wearing parts per torus.

### 17.21 Water jacket shield

- **Idea:** two steel hulls with a 7 m compartmentalised water jacket (7 t/m²), the first design (reference figures in sections 5d and 7b).
- **Superseded** by the rock jacket (section 5e). The water had to come from baking ~100 Mt of C-type rock per 900 m torus (~1.5 × 10¹⁷ J, ~5 years at 1 GW), the jacket could freeze and burst on surfaces facing space, and it kept the steel wet. The rock jacket makes the habitat ~50% heavier but cuts the material mined ~6× and the processing energy ~30×, uses the most common asteroid type, and is ~1.5 m thinner. What the water did better: it balanced the air pressure at the ceiling, doubled as pumpable ballast, and produced fewer secondary neutrons.

### 17.22 Nuclear power: fission, RTGs, fusion

Investigated for the outer system, where sunlight is weak; **rejected for now because the critical materials don't meet the local-availability rule.**

- **Fission.** Operation is not the obstacle: naval reactors have run reliably for decades at the right scale (~150–200 MW thermal ≈ the ~60 MW of electricity a 900 m torus needs), and fission has flown in space (SNAP-10A in 1965, Soviet reactor satellites, NASA's Kilopower test in 2018) at kilowatt scale. Waste heat is rejected at ~600–900 K on small radiators (~5,000 m² for ~120 MW at ~800 K), not by the habitat's radiators. A reactor stopping is not immediately dangerous: a 900 m torus holds ~3.7 kt of O₂, about a decade of breathing for a thousand people, though plants need light within weeks. **The obstacle is fuel:** ~75 kg fissioned per torus per year (~2–3 t per 30 years), but thorium is only ~0.03 ppm in asteroid rock, so extracting it costs about as much energy as it yields unless the thorium-bearing phosphate grains can be concentrated cheaply. Fuel would come from the Moon's KREEP terrains (~300× richer) or Earth, tying the lineage to a planetary fuel supply chain (enrichment, fabrication, reprocessing).
- **RTGs.** Far too weak for habitat power: ~23 W of electricity per kg of PuO₂ (MMRTG: ~110 W from 4.8 kg), so ~2,600 t of PuO₂ per 900 m torus, against world production of plutonium-238 on the order of kilograms per year. **Kept as an option for kilowatt-scale emergency power** (AI mind, sensors, communications, critical controls), which fits the "nothing has to keep working" principle.
- **Fusion.** The fuel is perfect: a full D–D burn gives ~3.5 × 10¹¹ J per gram of deuterium, ~10 GJ per kg of ordinary water (~0.035 g D per kg; comet water ~2–3× more), so ~0.5 kt of water a year per torus. **But the machine fails the rule:** tungsten (~0.09 ppm in CI chondrites), beryllium (~0.02 ppm), niobium (~0.25 ppm) and tin (~1.6 ppm) for superconducting magnets, lithium (~1.5 ppm) for D–T breeding blankets, rare earths for REBCO tape. ITER's coils use several hundred tonnes of Nb₃Sn/NbTi strand, i.e. ~100 t of niobium per reactor, hundreds of megatonnes of rock. M-types concentrate platinum-group metals, not W or Nb; MgB₂ and proton–boron fusion need boron (~0.8 ppm). First walls and divertors also need replacing within years. And no net-power reactor exists yet.
- **Mirror images:** fission has a mostly local machine and imported fuel; fusion has local fuel and imported critical hardware (hundreds of tonnes per reactor, recurring). These elements are found concentrated only on differentiated bodies (Earth, the Moon's KREEP regions, probably Mars).

### 17.23 Moving finished habitats

- **Rejected:** moving a pair or six-stack between orbits costs ~100–2,500 GW·yr, ~100–300× the energy to build the same habitats at the destination (section 15). Moving a newly built habitat before it is inhabited was checked too: a solar sail takes centuries with a film tens of km across; ~10 GW of solar-electric propulsion moves a 900 m pair in ~10–15 years, but costs ~30–200× the building energy and most of a small host asteroid's magnesium (section 15). The archipelago spreads by seeds.

### 17.24 Constant sky with seasonal energy storage

- **Rejected:** the habitat adapts to its orbit. The sky follows the host asteroid's seasons, sized without yearly storage; only daily scheduling (dark gaps used by the factory) balances supply and demand.

### 17.25 Bennu as the volatile supplier for the nurseries

- **Superseded** by Ryugu (or a better-aligned C-type): Bennu → Itokawa needs ~8.3–8.5 km/s and Bennu → Apophis ~7.4 km/s, against ~6.3 and ~5.5 km/s from Ryugu.

### 17.26 Farm ring as a separate ring in the gap

- **Idea:** the farm ring sits in the gap between two tori, on its own spokes, with sunlight entering the gap beside it.
- **Rejected:** it blocks part of the gap it collects light through, needs its own spokes, hub link and elevators, and its width is limited by the gap. In the torus's own plane (adopted), it shares spokes and elevators and the gaps stay narrow.

### 17.27 Magnetic shielding (an artificial magnetosphere)

- **Idea:** a superconducting magnetic field, or a plasma-inflated mini-magnetosphere, deflects charged particles instead of rock stopping them.
- **Findings:**
  - ESA's SR2S project (2013–2015) designed superconducting toroids around a crew module, with an MgB₂-in-titanium conductor, and built a test coil. Earlier simplified studies had promised nearly a tenfold dose cut, but they overlooked the secondary particles (neutrons and others) produced in the magnet structure; the best layout "could provide a factor two" reduction of cosmic-ray dose, for ~50 t of magnet.
  - A 2016 comparison of ESA, NASA NIAC and SR2S designs found the field contributed only ~8–50% of the total dose reduction, passive mass doing the rest; the best case needed ~23 T·m of bending power and ~140 t, and protected only ~75% of incoming directions.
  - Plasma mini-magnetospheres can deflect the solar wind and lower-energy solar storm particles, not cosmic rays at billions of electron volts.
  - Cosmic-ray protons curl with a radius of ~3.3 m × rigidity (GV) ÷ field (T), so turning them away takes ~10–30 T·m all around the habitat. Scaled to a 900 m torus (rough estimate), a ~0.1 T field shell ~200 m thick needs very roughly ~10 kt of superconductor and stores ~10¹² J.
- **Rejected:** at best a factor of ~2 against cosmic rays, so most of the rock is still needed; every practical superconductor needs vitamins (boron, niobium, or yttrium, barium and silver); an active cryogenic system storing that much energy goes against simplicity and long life. Earth's own protection from cosmic rays at sea level comes mostly from its air (~10 t/m², close to the rock jacket's 11 t/m²); its magnetic field mainly turns away the solar wind and lower-energy particles. A light field against solar storms may suit the ships carrying seeds and people between habitats.

### 17.28 Capless solar cylinder around the stack

- **Idea (adopted until 26 Oct 2026):** the solar bands of neighbouring tori join into one cylinder around the stack, at or slightly beyond the rims, spinning with it. It never self-shades, needs no articulation, and its area per torus is `2π R · p` (R = cylinder radius, p = pitch):

| Gap between tori | 900 m pitch | Cylinder radius needed (sulfur, ~60 MW per torus) |
|---|---|---|
| 10 m | 66 m | ~1.3 km (≈ 1.45 r) |
| 25 m | 81 m | ~1.1 km (≈ 1.2 r) |
| 40 m | 96 m | ~0.9 km (at the rims) |

  At 1.6 km the pattern was the same (~2.4 km radius at 10 m gaps, at the rims with ~70 m gaps). At 1.3 km the cylinder moved at ~136 m/s, so a steel hoop carried its own spin at ~150 MPa; thin-film panels plus structure at ~3 kg/m² came to ~1.6 kt per torus. It also served as the tori's meteoroid bumper and as a floor catching anything falling outward, worked from inside at ~1–1.75 g.
- **Superseded** by the despun solar array (section 13, Power):
  - spinning, it averages only ~1/π of full sunlight per m², so it needs ~3× the PV of a sun-facing array, and PV silicon is a vitamin;
  - its area is tied to the stack's radius and pitch, so further from the Sun it has to grow outward to impractical radii, and it can never concentrate sunlight;
  - its panels go through ~500,000 small temperature swings a year;
  - its bumper role moves to a double outer skin on each torus (section 13, micrometeoroids); the cost is one light, slow bearing, with the array sized to keep the habitat alive even when locked to the stack.

### 17.29 Sun-fed farm rings lit by mirrors around the hub

- **Idea (the adopted direction until 26 Oct 2026):** the farm ring in each torus's plane at ~0.4 r, a single level under a glass ceiling and glass sides, lit by sunlight reflected from mirrors built around the hub: a funnel beyond each end of the stack and, in option A, a slightly barrel-shaped double cone in each gap. The crops needed no electricity.
- **Superseded** by the electric farm ring in three tiers (section 13):
  - **it couldn't grow with the population:** one level under glass, fed by mirrors whose size was tied to the hub and the gaps. Feeding a high-density biosphere took long end funnels (~350 m at 900 m, option B, with the far rings of a six-stack lit at a slant through the nearer tori, ray tracing still to do) or 100 m gaps (option A, limiting a stack to ~11 tori);
  - **many parts to keep working:** glass ceilings and sides carrying the farm's pressure, shutters for the night, a background light floor for the anti-sun half of each turn, light flickering every ~30 s;
  - **an axial sunlight relay** was considered to scale it (sunlight collected sunward and sent along the axis to the rings): too complex, and it would have limited how many tori a stack could feed;
  - **the despun array scales,** so the same lamps and light pipes as the valley are now the simpler route, at ~32 MW per tier lit per 900 m torus.
- **What it did better:** no electricity for food, and ~2.7× brighter per m² than the valley. The research on minute-scale flicker showed that a dim background light makes it workable for many crops. The figures are kept below for reference.

**Layout** (side view, axis vertical, not to scale; `[]` main ring, `====` radiators, `[F]` farm ring, `-----` clear light path along the spokes, `#` hub, `\ /` mirrors, whose real tilts are only a few degrees):

```
sunlight -->              \   #   /                 end funnel
sunlight -->               \  #  /
sunlight -->    []====[F]-----#-----[F]====[]       torus A
sunlight -->               /  #  \                  gap double cone
sunlight -->               \  #  /                  (option A only)
sunlight -->    []====[F]-----#-----[F]====[]       torus B
sunlight -->               /  #  \
sunlight -->              /   #   \                 end funnel
```

**Hub mirrors.**

**Location and shape.** Surfaces of revolution on the axis, built as extensions of the hub: a **funnel** beyond each end of the stack, opening away from it, and (option A below) a **double cone** in each gap, bulging at mid-gap, whose upper half lights the torus above and lower half the torus below. The funnels' hollow centres keep the axial approach clear; the docks move to the tip of the hub extensions.

**The real tilts are small.** A horizontal ray hitting a 45° mirror goes straight along the axis, into the next torus's hub region. To reach a ring ceiling at 0.4 r the surfaces must be nearly parallel to the axis, tilting more where the target is farther off, so the profile is gently curved:

| Mirror | Tilt from the axis | Shape |
|---|---|---|
| Gap cone at ~60 m radius (900 m) | ~3° near the torus plane to ~7° at mid-gap | bulges ~4–5 m over each 50 m half: a slightly barrel-shaped cylinder |
| Gap cone at ~140 m radius | ~4° to ~10° | bulges ~6 m |
| End funnel, ~2 gaps long | ~3° near the torus to ~18° at the far end | flares ~35 m (60 → ~95 m radius at 900 m) |

The geometry is self-similar, so the tilts are the same at 1.6 km.

**How much light they collect.**
- **The silhouette counts:** the Sun sees a mirror as a band 2 × R × L (outer radius × length). Whether the mirror touches the hub doesn't matter, but the space between the hub and a mirror set farther out stays empty, since light reflected from near the torus plane leaves almost horizontally.
- Every part of the mirror faces the Sun for half of each turn, so it is built all the way round.
- **Delivery:** ~60% of the caught light reaches the crops (mirror ~90%, glass ~90%, aiming and spill ~75%). Sunlight carries ~2.04 µmol of photosynthetic light per joule.

| Configuration (900 m, 100 m gaps) | Light per farm ring | Share of the high-density need |
|---|---|---|
| Gap cone at hub radius (60 m): ~16 MW caught per gap | ~1.7 × 10⁶ mol/day per gap | |
| Pair: half a hub-radius gap cone + an end section 1 gap long | ~2.6 × 10⁶ | ~65% |
| Pair: end funnel ~2 gaps long (60 → 95 m) alone | ~4.5 × 10⁶ | **~110%** |
| Six-stack inner ring: gap cones at hub radius | ~1.7 × 10⁶ | ~43% |
| Six-stack inner ring: gap cones out to ~140 m (~0.16 r) | ~4 × 10⁶ | **~100%** |

1.6 km is self-similar if its gaps scale with r (~180 m): hub ~110 m, inner-gap cones to ~260 m.

**Gap mirrors no longer cost PV.** While the habitat had a capless solar cylinder, sunlight could reach a gap's mirrors only through an annular slot in it, and that strip would otherwise have been PV: the gap cones caught only 2 R_m w of the 2 R_cyl w of sunlight crossing a slot, returning ~50–55% of what the same strip gave as PV and lamps, and the slots pushed the cylinder out to ~1.75 r. With the despun array (section 13, Power) there is no cylinder: the gaps are open to sunlight and both options are free. The end funnels were always free.

**Two ways to feed the farm rings:**

| | A. Gap cones + end funnels (as drawn) | B. End funnels only |
|---|---|---|
| Gaps | ~100 m | 10–40 m |
| Pair | works | each ring fed by its own end funnel (~110%) |
| Six-stack | inner rings fed by ~140 m gap cones | each end funnel feeds three rings: its far part lights the end ring through the glass side facing the end; its root lights rings 2 and 3 through their ceilings, ~25–60° from vertical, across the clear inner stretch of the nearer tori |
| Six-stack end funnels | ~2 gaps long | ~350 m long, flaring from ~60 to ~200 m (900 m); ~620 m long to ~360 m (1.6 km); the profile curves outward, so its mouth is a little wider than a straight cone's |
| Stack limit (20% margin) | ~11 tori | ~18–29 tori |
| Trade-offs | simpler optics (each ring lit from its neighbouring gaps at small angles); a longer stack and fewer tori | a shorter stack and more tori; far rings lit at slant through the nearer tori; ray tracing and glass losses at slanted incidence to check |

**Size and weight.** Mirror area ≈ 2π R̄ L (the tilts are small); facets plus frame ~1–4 kg/m²:

| Stack | Mirror area | Mass | Aluminium coating |
|---|---|---|---|
| 900 m pair, end funnels only | ~0.2 km² | ~0.2–0.8 kt | ~60 kg |
| 900 m pair, with a gap cone (A) | ~0.24 km² | ~0.2–1 kt | ~70 kg |
| 900 m six-stack, A (5 cones to ~140 m + 2 funnels) | ~0.64 km² | ~0.6–2.6 kt | ~190 kg |
| 900 m six-stack, B (2 funnels of ~350 m) | ~0.56 km² | ~0.6–2.2 kt | ~170 kg |
| 1.6 km stacks | ~3.2–3.4× the 900 m figures | | |

Negligible next to the stacks (~23–70 Mt at 900 m), and for spin stability (all of it near the axis). The end funnels hide only ~1–5% of the end openings that vent the radiator drum.

**How they are built (proposed):**
1. **Facets** ~1–2 m across: thin rolled steel sheet (~0.1–0.5 mm) from the S-type's iron-nickel, polished flat or gently curved; or rolled glass from the silica line, coated on the back (heavier, ~5–8 kg/m², with the coating protected behind the glass).
2. **Coating:** ~100 nm of aluminium by vacuum evaporation, using space's free vacuum, then a thin silica overcoat from the same line: the standard "protected aluminium" mirror, ~85–90% reflectance. The aluminium comes from the glass line's leach solution (section 13, glass and the silica line).
3. **Frame:** a steel truss on the hub extensions, light because gravity there is ~0–0.2 g. Facets are replaceable from the hub.
4. **Fixed facets** are the simple baseline. Steerable facets (small motors) could aim light away from shuttered zones, recovering up to ~1/3 of it with three zones, at the cost of moving parts.
5. **Built by the hub factory** as the hub is extended, next to the dock; maintenance at near 0 g.
6. **Wear:** micrometeoroid pitting and UV slowly lower reflectance; facets are recycled and recoated over decades.

**Farm ring light vs. the valley's sulfur sky** (900 m torus, 1.6 km in brackets):

| | Valley, 32 ha [100 ha] | Farm ring, ~10 ha [~34 ha] of crops |
|---|---|---|
| Light per m² | ~15 mol/m²/day with the light-box ceiling (~10–20 by zone) | ~40 mol/m²/day |
| Total light | ~4.8 × 10⁶ mol/day [~1.5 × 10⁷] | ~4 × 10⁶ mol/day [~1.35 × 10⁷] |
| Compared with the valley | 1 | ~0.85× the whole valley's light |
| Electricity | ~55 MW [~166 MW], ceiling losses included | none; from sulfur lamps the same light would need ~33 MW right over the crops, ~44 MW behind the light-box ceiling [~110 / ~150 MW] |
| Sunlight delivered | | ~23 MW [~77 MW] |

So the farm ring receives almost as much photosynthetic light as the whole valley, ~2.7× brighter per m², without electricity: in effect it nearly doubles each torus's light for growing.

**Operation:**
- **Flicker.** Each spot of the ring receives reflected light while it is on the sunward side, about half of each turn (~30 s on, ~30 s off). The mirrors reflect back towards the Sun, so the anti-sun half gets no direct light: its background floor of ~10–15% (below) must come from scattering in the ring (diffusing glass, pale walls) or a low lamp floor.
- **Night by shading.** Opaque shutters on the glass close for the night part of each day; a stuck shutter means a few days of continuous light for one zone, not a hazard. The ring is split into zones on staggered schedules (e.g. three zones 8 h apart with 16 h days, two always lit).
- **Free day length per zone:** long 16 h days for long-day crops (wheat, spinach, many grasses) that won't flower in a pair's valley; shaded zones cool at night like a field, set per zone independently of the valleys' small oceanic swings.
- **Heat.** Each ring absorbs ~23 MW [~77 MW], rejected through the coolant loops along with the valley's ~60 MW [~180 MW]: ~22 ha [~69 ha] of radiating surface per torus, ~11 ha [~34 ha] of two-sided panels. The spoke stretch between farm ring and rim (~460 m × 56 m [~830 m × 100 m], ~2.6 [~8.3] ha per spoke) holds that on ~4–5 spokes. The panels face along the axis, shaded on both sides by the farm ring's floor and the main ring, and must not stick out into the gaps. A six-stack of 900 m tori then rejects ~0.5 GW against the drum's ~1.6 GW. Most of the sunlight crossing a gap leaves through the far side; only the caught part and some scattered light add heat.
- **Pressure.** Large glass areas at 70 kPa carry big loads; a farm ring at lower pressure (plants need CO₂ and water, not 70 kPa) makes the glass much lighter.
- **Stability.** Option A's 100 m gaps give a pitch of ~156 m, limiting a stack to ~11 tori with a 20% margin, still above 6; option B keeps the 10–40 m gaps.
- **Radiation.** Crops tolerate the higher dose under glass; people working there limit their time, as in any lightly shielded zone.

**Plants under minute-scale light fluctuations:**

- **Fully on/off every minute hurts badly.** Light switched every 1 minute between 200 and 0 µmol/m²/s (same daily light as a constant 100) severely reduced growth: shorter plants, fewer and smaller leaves, less biomass, pale and wilted leaves.
- **A dim background fixes most of it.** With 1-minute switching between 175 and 25, or 125 and 75, shoot biomass was not significantly affected; a floor of ~25 µmol/m²/s lets plants smooth out rapid changes. Photosynthesis takes minutes to "warm up" (enzyme activation, stomata), so a minute of full darkness wastes much of the next light minute; varieties that restart quickly lose less.
- **Real nights are still needed:** light flashing all day and night reads as continuous light, since even brief light at night counts as daytime for day-length sensing.
- **On the spinning habitat** a rim or ring spot faces the Sun for about half of each 60 s turn (~30 s on, ~30 s off); a floor of ~10–15% of the peak and proper nights should make it workable for many crops, to be tested on candidate crops.

**Glass for the farm ring** (900 m torus: ring at ~360 m radius, 50 m wide, glass ceiling and two 20 m high glass sides):

| | Value |
|---|---|
| Glass area | ~200,000 m² (ceiling ~113,000 + sides ~90,000); ~520,000 m² at 1.6 km |
| Pane thickness | ~10–20 mm (small ~0.5 m panes in a steel grid; thinner at lower farm pressure) |
| Glass mass | ~5–10 kt (~13–26 kt at 1.6 km) |
| Steel frames (rough) | a similar order |
| Compared with the torus (~11.9 Mt) | ~0.04–0.09% |

A flat pane carrying 70 kPa across a 1 m span would need ~3–4.5 cm; small panes, tempered glass, pillowed or curved panels and a lower farm-ring pressure bring it to ~1–2 cm. A six-stack with six farm rings needs only tens of kilotonnes.

---

## 18. Open questions

Status of the gaps identified so far:

| Topic | Status |
|---|---|
| Iron for L and LL hosts | Preliminary design: free metal only (magnetic separation), mining more rock on large hosts. Molten-oxide electrolysis noted as a likely better option, not factored: anode life, energy and current efficiency at scale not yet public (industrial cell 2025, demonstration plant planned 2026). Itokawa and Apophis resolved by building 400 m demonstration pairs instead of 900 m pairs (section 15) |
| Size | 900 m and 1.6 km shortlisted. **To decide:** 2.5 km / 100 s as a later candidate (section 8): structurally fine, limited by nitrogen (~100 Mt of C-type per torus) and slower replication |
| Despun solar array | Adopted (section 13); ~2.6× larger with three farm tiers lit than for the valley alone. **Open:** bearing and drive redundancy, magnetic bearing design, a rotary transformer at 100 MW–GW scale, buffering the locked array's pulsing output, a second dock now that one hub end carries the array, concentrators for the outer system |
| Heat rejection | Architecture chosen (coolant loops, radiators on the spokes between farm ring and rim, venting through the open ends and gaps, thermosiphon). Ideal limit treated as an upper bound; a preliminary radiative exchange model (section 13) gives ~75–80% of it, so with three farm tiers lit heat limits a stack of 900 m tori to ~8 (~11 with two), still above six. **Open:** sunlight through the gaps, spokes and cables, real panel layout, loop sizing (plan §6, brought forward) |
| Energy / replication time | With the rock shield, processing energy is ~2–6 months per 900 m torus at 1 GW; shipping the refined volatiles adds ~2.5× that from Ryugu to Eros (~21 PJ against ~8 PJ per 900 m torus, parametric model); **open:** logistics and factory throughput, now the pacing items |
| Population vs. power | Chosen: electric farm rings of three tiers (section 13). Food under sulfur lamps costs ~31 kW of electricity per person with conservative yields (~18 kW at the best demonstrated), so each tier lit (~1,000 people per 900 m torus) needs ~32 MW and ~0.15 km² of array at 1 AU: the array, not the ring, sets the population. **Open:** yields of the chosen crops under sulfur light at ~0.4 g; 915 MHz sources (~20% less power); the share of microbial food (gas-fermented bacteria, ~0.5 kW per person, ~35–60× less than crops, but mostly protein) |
| Nitrogen | C-type sized by nitrogen again (~5 Mt per 900 m torus, ~27 Mt per 1.6 km torus at ~70% recovery); **open:** recovery from organics and ammonium salts |
| Soil from C-type clays | **Open:** leaching nickel, chromium and salts (recovering the metals), microbial start-up |
| Rock jacket details | **Open:** hung or vaulted ceiling cells (~30 kPa net load), ballast tanks, hydrogen-rich inner layer against secondary neutrons, compaction method |
| Light delivery | Chosen (artificial overcast sky, sulfur lamps, light pipes in a light box: magnesium oxide coating, graded diffuser; in the farm, light pipes just above each tier's crops). **Open:** measured light-pipe and diffuser efficiency with sulfur lamps (~75% delivered assumed in the valley, ~85% in the farm), diffuser material |
| Habitat power balance | Architecture chosen (staggered tori, despun solar array at one hub end, sized so a locked array keeps the habitat alive; tracking it gives ~1.57× that, spare for the factory, brighter gardens or food exports; the farm tiers lit are part of the need, their share sized at aphelion, with a seasonal harvest and stored staples noted as an option); beamed power kept as a way to feed the hub factory from the industrial array (section 13) |
| Lamps | Direction chosen (non-rotating sulfur bulbs, light pipes, central 915 MHz sources); **open:** bulbs at kW scale and 915 MHz, source lifetime, waveguide losses and plant spacing, cathode materials |
| Jacket thermal control | Resolved by the rock jacket; only water-filled parts must stay inside the warm envelope |
| Spokes and cable net | Wire, net and spin-up checked (section 12): ~1 GPa is a safety factor of ~2 on 1,960 MPa bridge wire or more on thinner wire, from carbonyl-refined iron; the chord net weighs the same as radial spokes; a partial ring is hung in arcs of ≥ ~4θr, spinning at ≤ ~0.7 of the final rate (its chords carry twice their finished load), with joints locked while building (~1% of the hoop force, plus bending) and released after closure (provisional). **To decide:** the safety factor. **Open:** finite-element model of a tube segment (checking the r^2.3 hull and frames), the hub's stabilising lines, wire drawn from refined asteroid iron (Earth test) |
| Stack stiffness | **Open:** bending modes of the shared hub and rim links must stay well above the spin rate |
| Farm rings | Chosen (section 13): electric, three tiers ~2.5 m apart in each torus's plane at ~0.4 r, the same sulfur lamps and light pipes as the valley, built for the highest density, tiers lit as the array allows; radiators between farm ring and rim. The sun-fed ring with hub mirrors is superseded (17.29). **Open:** crop trials (yields, dwarf varieties, ~0.4 g), the farm's atmosphere (pressure, CO₂, gas exchange with the valleys), shielding against workers' dose, light-pipe layout and heat at 2.5 m tier spacing, automation |
| Diet | Working diet proposed (section 13): ~93% from the farm, ~7% from the valley, ~100 g of protein a day. **Open:** fat only ~11% of calories (more soybeans, flax or nuts), vitamin B12 by fermentation, variety and acceptance, crop trials for lentils and flax under lamps |
| Glass | Needed for the ceiling diffuser, the lamps' quartz bulbs and possibly the light pipes (the farm rings no longer need windows). **Open:** acid-leach silica process from chondritic silicates, rolled-glass forming, aluminium recovery for pipe linings |
| Copper | **Open:** extraction line for dispersed copper, high-voltage distribution, aluminium or iron conductors |
| Attitude | Solved by the ecliptic-normal orientation |
| Self-replication closure | **Open:** which parts are vitamins (semiconductors, PV, motors, bearings, seals, sensors); trace elements are now sourced (section 10): copper, boron and platinum-group metals are contained in useful amounts, tin, silver, tungsten and rare earths only in tonnes; iron from the silicates for L and LL hosts; bootstrap of the first habitat |
| Location and logistics | Working scenario: demonstration 400 m pairs at Itokawa and Apophis (one or two, the second showing self-replication), 900 m pairs and 1.6 km six-stacks on larger L/LL hosts (Eros), Ryugu as C-type partner; Torifune added as a candidate with the mildest orbit (proposed); habitats built in their S-type's orbit, C-types refined at source (section 15). **Open:** a catalogue search with current ephemerides for well-aligned S/C pairs (similar e, i and perihelion longitude), ranking S-types by orbit shape (low e, a near 1 AU) since the habitat keeps that orbit for good, and by metal class (H-like hosts have ~4× the free metal of LL-like ones; the current candidates are L or LL, and the known H-like near-Earth asteroids have very eccentric orbits, section 15), multi-revolution and low-thrust transfers, gravity assists |
| Nitrogen at Eros | **Open:** Ryugu supports ~3 six-stacks of 1.6 km; more C-type partners or a lower atmospheric pressure needed beyond |
| Biological year and photoperiod | **Open:** effects of 1.2–1.8-year years (Torifune's ~1.05-year year nearly avoids the question) on annual plants and insects; long-day species limited to six-stacks |
| Power beyond the inner system | Nuclear investigated and rejected for now under the sourcing rule (section 17.22); **open:** thin-film concentrator mirrors (belt to Saturn), RTGs for emergency power |
| Atmosphere chemistry | **Open:** CO₂ (plants want ≳ 40 Pa), humidity, condensation and rain under a 56–100 m ceiling, trace contaminants |
| Corrosion | Largely addressed (dry rock jacket, nickel cladding in wet zones) |
| Dynamics | **Open:** ballast balancing with dedicated tanks, settling of the rock fill during spin-up, docking loads |
| Failure modes | Micrometeoroids assessed (section 13: negligible for the panels, the rock jacket protects the pressure hull, rock leaking through the outer skin is the main risk, answered by the double skin with a crawl space). **Open:** punctures, fire at 29% O₂, compartmentalising the canyon, evacuation to sister habitats |
| Ecology closure | **Open:** species lists, soil microbiome, pollinators, phosphorus cycle, food webs, minimum viable populations |
| People | Set by the farm tiers lit: conservatively ~1,000 / ~2,000 / ~3,050 per 900 m torus with 1 / 2 / 3 tiers (~3,250 / ~6,500 / ~9,750 at 1.6 km, ~7,900 / ~15,800 / ~23,700 at 2.5 km), ~310 / ~155 / ~103 m² of floor per person. **Open:** founding group size, child development under partial g, governance |
| The habitat's AI mind | **Not yet discussed:** its architecture (one central computer, or layered and distributed control as one possible option), what it regulates, and its relationship to the inhabitants' governance |
| Coriolis comfort | Noted: at 900 m, running at 5 m/s spinward or antispinward changes apparent weight by ~±10%; shapes paths and waterways |

---

## 19. Assumptions to revisit

These are the inputs of the parametric model (`habitat_model/assumptions.toml`), each with a range, source and status. Ranked by impact over representative designs (`reports/sensitivity.md`), the ones that move the results most are the electric propulsion's exhaust speed and the water shipped (through the lake-water guess), C-type nitrogen recovery and baking energy, PV efficiency, free metal in the host rock, the shield's areal density and light on the crops.

- 80/20 N₂/O₂ reference; 70 kPa / 29% O₂ design atmosphere.
- Cometary NH₃ at ~1% of ice by mass (optimistic; ~0.5–0.8% by number is typical); Bennu-like C-type with ~6.4 wt% recoverable water and ~0.24 wt% N.
- Shielding at ~11 t/m² of compacted crushed rock (~2 t/m³), equivalent to 7 t/m² of water, for 20 mSv/yr (deep space, no magnetosphere).
- Mass model (section 5c): uniform cable spokes at ~1 GPa working stress carrying the rim; hull and frames scaled as r^2.3 from the 900 m and 1.6 km estimates; S-type metal ~12–18%; 2.5 km figures extrapolated.
- S-type body: ordinary-chondrite-like, rubble pile ~2 t/m³; ~12–18% recoverable metal assumed in the sizing tables (H-like), ~9 wt% for L and ~4–5 wt% for LL hosts (section 10); C-type nitrogen recovery ~70%.
- Near-Earth location (~1 AU), as a conservative starting point like 1 g.
- Steel plate at 500 MPa working stress (SF 2), ρ = 7,900 kg/m³; wire at ~1 GPa working stress (range 800–1,200 MPa: a safety factor of ~2 on 1,960 MPa bridge wire, more on thinner wire; section 12); CFRP at 1,000 MPa, ρ = 1,600 kg/m³.
- Circular tube cross-section with diameter = floor width; thin-shell approximations (poor for 400–900 m with a 5.5–7 m jacket).
- Hub, dock and factory mass as rough guesses.
- Soil 1.6 t/m³, regolith 1.8 t/m³, fill 1 m.
- Rotation comfort < 2 rpm; g tolerance unknown (0.15–1 g).
- Spin-up exhaust velocity ~3 km/s for water thrusters.
- Lamps ~1.4 µmol/J (sulfur plasma) or ~3 µmol/J (LED); ~25% of emitted light lost in the light-box ceiling (first assumed ~50%); ~85% of the light reaches the crops in the farm tiers; PV at 25% efficiency on the sun-facing despun array (the former spinning cylinder averaged ~1/π of full sunlight); a locked two-sided array averages 2/π; radiators at ~285 K for passive loops.
- Other habitat loads (life support, algae, hub) ~5 MW per 900 m torus, ~15 MW per 1.6 km torus (guess).
- Population set by the farm tiers lit: a 2,500 kcal working diet, ~93% from the farm; conservative edible yields per mol of light (potato 0.37, wheat 0.18, soybean and lentils 0.15, berries 0.25, flax 0.07, lettuce 0.43 g/mol), plus ~10% for seedlings and turnaround; ~36 mol/m²/day on average on the crops; ~80% of each tier planted; so ~1,000 people per tier lit per 900 m torus.
- Ryugu's measured abundances (close to CI) for the C-type; ordinary-chondrite falls for the S-type (H values for the major elements); iron-meteorite composition for the M-type.
- C-type processing energy ~1–2 MJ/kg.

---

## 20. Changelog

How the design evolved, newest first. Entries before 22 October 2026 come from earlier sessions: they are in order, but undated.

**28 October 2026**
- **Independent review of the system model** (GitHub issue #1), addressed:
  - **The rock jacket and crawl space are now outside the tube in the geometry.** The earlier pitch (tube width + gap) left the neighbouring jackets overlapping. Pitch is now the envelope's diameter plus a clear gap: ~80 m at 900 m, ~124 m at 1.6 km. Passive stability allows ~22 tori of 900 m (~25 of 1.6 km) with a 20% margin, not ~27 (~29); a six-stack of 900 m tori is ~480–660 m long (sections 0, 11).
  - **The jacket has a finite thickness:** ~10% more shield rock at 900 m than the thin-shell estimate, ~5.5% at 1.6 km, ~22% at 400 m. A 900 m torus is ~12.8 Mt (~40 t per m² of floor), a 1.6 km torus ~41.5 Mt, a 2.5 km torus ~108 Mt (sections 0, 5c, 5e, 8, 9, 10, 15). The fill's shielding credit now follows the actual fill.
  - **Heat:** the end openings' capacity is an ideal limit. A preliminary radiative exchange model gives ~75–80% of it: ~1.3× margin for a 900 m six-stack with three tiers lit (not 1.8×), ~250 ha of panels (not ~125 ha), and a heat limit of ~8 tori with three tiers lit, ~11 with two (section 13). Thermal work moves ahead of the second tier in `plan.md`.
  - **Model accounting:** unknown Δv no longer counts as zero shipping energy; shipping, total energy and generation time join the sensitivity ranking, over five representative designs, which puts the propulsion's exhaust speed and the (guessed) lake water first; the trace-element budget now compares demand with recoverable supply.
  - **Validation headline corrected:** after the corrections, 189 of 197 checked figures are within 5% (192 within their configured tolerances). The earlier "191 of 197 within 5%" counted relaxed tolerances as 5%.
  - **Eros mining corrected** (section 15): a 1.6 km six-stack takes ~0.5–1 Gt of L or LL rock by free metal, not ~240 Mt.
- **Parametric system model** (`habitat_model/`, `plan.md` §1): reproduced 185 of 197 checked figures within 5%, and the rest were rounding. Corrected here where the notes were more than ~5% off, mainly the 900 m valley's sky and other loads (~53 + ~5 MW, ~57 MW in all, not ~60), so the 900 m arrays are ~4–6% smaller (~0.27 km² for the valley at 1 AU, ~0.71 km² with three tiers lit; section 15's 900 m columns) and the heat break-even with no farm lit is ~29 tori, not ~27. Also noted: the water need doesn't scale with the floor (section 7), and section 5c's "water + air" counts the soil's water and the water electrolysed for O₂ twice (~0.05 Mt at 900 m).
- **Validation plan re-ordered** by the model's sensitivity ranking: structure, radiation transport, stack dynamics, second tier, heat rejection; C-type nitrogen recovery and baking energy, the top two inputs, become Earth tests.
- **Wire and safety factor** (section 12; `structure_model/`): ~1 GPa working stress is a factor of ~2 on the strongest bridge wire, at the low end of bridge practice, or ~2.25 on ~1 mm wire; range 800–1,200 MPa. The factor of safety is to decide. Spokes creep ~0.5–1.3 m over their life.
- **Wire needs carbonyl-refined iron** (section 10): wire steel tolerates almost no nickel, phosphorus or sulfur, and chondritic metal has ~9%+ nickel.
- **Tangent-chord net corrected** (section 12): no ~0.2% loss, it weighs the same as radial spokes; tapering saves only 1–4%; chords bow 2–18 m outward.
- **Construction sequence corrected** (section 12): arcs of at least ~4θr (~270 m at 900 m) hung in opposite pairs, not single segments; their joints carry ~1% of a full ring's hoop force until the ring closes.
- **Review of the structural model** (pull request #2): an assembled equilibrium model (one tension per chord) replaces the anchor-by-anchor estimate. The chords of the first arcs carry twice their finished load, so construction must spin at ≤ ~0.7 of the final rate; joints must be locked while building and released after closure; uniform chords need ~3% (900 m) to ~11% (2.5 km) more area than the tapered end area quoted before; the arc mismatch moves the spin axis, which says nothing yet about hub-to-net clearance. All provisional until the finite-element model.

**27 October 2026**
- **Torifune (2001 CC21) added as a candidate host** (section 15): Sq-type, L-chondrite-like, ~465 m (~100 Mt if the larger size estimates hold), visited by Hayabusa2 on 5 July 2026. It has the mildest orbit of the candidates (0.63–1.54× sunlight, a ~1.05-year year), room for ~6 tori of 900 m by free metal, and is cheap to reach from Earth and Itokawa, but poorly aligned with Ryugu and Bennu. Added to the candidate, transfer and seasonal-sizing tables; possible site for a first 900 m pair (proposed).

**26 October 2026**
- **Farm rings now electric, in three tiers** (section 13): the same sulfur lamps and light pipes as the valley, powered by the despun array; tiers ~2.5 m apart, ~8.5 m tall in all, ~80% planted, each zone on its own day length, with a lower-pressure, CO₂-enriched atmosphere of its own (to decide). No mirrors, glass, shutters or flicker; the gaps stay at 10–40 m. The sun-fed ring with hub mirrors, and an axial sunlight relay considered to scale it, move to 17.29, with the mirror figures and the flicker research.
- **Working diet and crop yields** (section 13): potatoes, wheat (preferred over rice), soybeans, lentils, berries, flax and greens give ~93% of 2,500 kcal, the valley ~7%; conservative and best-demonstrated yields per mol of light from NASA's growth chambers and vertical farms.
- **Population set by the farm tiers lit,** replacing the high- and low-density figures: conservatively ~1,000 people per tier per 900 m torus (~3,250 at 1.6 km, ~7,900 at 2.5 km, ~200 at 400 m), so ~310 / ~155 / ~103 m² of floor per person with 1 / 2 / 3 tiers lit, compared with real towns and cities. The earlier "high density" (~7,000 per km²) falls between two and three tiers, the "low density" at about half a tier.
- **Corrected: food costs ~31 kW of electricity per person** with conservative yields (~18 kW at the best demonstrated), not ~5–10 kW. The earlier crop figure (~45 m² at ~40 mol/m²/day) matched the best-demonstrated yields. Gas-fermented bacteria's advantage over crops grows to ~35–60×.
- **Despun array and radiators grow with the tiers lit** (sections 0, 8, 13, 15, 18): per 900 m torus at 1 AU, ~0.28 km² for the valley plus ~0.15 km² per tier lit, the farm's share sized at aphelion; with three tiers lit, heat limits a stack to ~10–11 tori, still above six.
- **3D model updated:** tiered farm rings with one to three tiers lit, the hub mirrors and light paths removed, and stats for people fed, power, array size and heat.
- **Glass:** the farm rings no longer need windows; the silica line makes the ceiling diffuser, the lamps' quartz bulbs and possibly the light pipes (section 13). Without the end funnel mirrors, the end faces vent ~99% of their area.
- **Itokawa and Apophis become demonstration sites** (section 15): one or two 400 m / 40 s pairs instead of 900 m pairs, which free metal alone can't supply there; a second pair built by the first demonstrates self-replication. 900 m pairs and 1.6 km six-stacks move to larger L/LL hosts (Eros as the working case). The candidate table still counts 900 m tori, with a note below it.
- **Unproven options kept out of the preliminary design** (principle 3): molten-oxide electrolysis is noted as a likely better option for iron from the silicates but not factored in, since its anode life, energy and efficiency at scale aren't public yet. The preliminary design uses free metal only, so Itokawa supplies about one torus and Apophis a pair only at the upper end of its mass; how to supply a nursery pair at Itokawa is an open decision.
- **Host metal class as a design rule** (principle 3): the design must work with L or LL hosts, the best-studied candidates; H-type hosts are better, as lower gravity would be. **H-like near-Earth asteroids researched** (section 15): ~15–29% of ordinary-chondrite-like ones, and the known examples have very eccentric orbits (~11–170× sunlight swings), so the L/LL candidates stay. **Iron from the silicates researched** (section 10): hydrogen reduction doesn't work on olivine; molten-oxide electrolysis is proposed for small hosts, simply mining more rock for large ones.
- **Trace elements sourced** (section 10): measured abundances for Ryugu and ordinary chondrites replace the guesses. Copper is ~1.7 kt per 900 m torus's source bodies, enough if about half is recovered; boron, gallium and platinum-group metals are contained in tonnes; tin, silver, tungsten and rare earths only in tonnes. Corrected: molybdenum in the C-type is ~5 t, not ~5 kg.
- **Metal content by host class** (section 10, candidate bodies): the candidate S-types are L or LL, with ~9 wt% and ~4–5 wt% free metal instead of the ~12–18% assumed. With these hosts metal, not shield rock, sizes the mining, unless iron is also extracted from the silicates; Itokawa supports ~1 torus by free metal (~3 with iron from the silicates).
- **Flat PV kept for the despun array; concentrators noted as options** (section 13, Power): mirrors on smaller cells, or mirrors with a heat engine, compared by efficiency, materials, manufacturing and behaviour when locked.
- **2.5 km / 100 s torus added as a candidate** next to 900 m and 1.6 km (sections 0, 3, 4, 5c, 6–10, 12; decision table in section 8): structurally fine with cable spokes (~43 t per m² of floor), with a 156 m valley and a much larger connected wilderness, but limited by nitrogen (~100 Mt of C-type per torus) and slower replication. 17.2 revised: rejected only beyond 2.5 km.
- **Main text and tables now use the rock jacket and cable spokes**; the first design's water-jacket and self-supporting-ring figures moved to reference subsections (5d, 7b) and footnotes (sections 6, 8, 9). A new mass model (5c) covers 400 m to 3.6 km; the 900 m and 1.6 km totals are now quoted as ~11.9 Mt and ~40 Mt (same estimate, the components summed).
- **One climate per habitat** (section 16): all valleys alike and connected for migration through rim tunnels, including across day/night boundaries; diversity comes from the archipelago.
- **Day and night cooling** (section 13, heat rejection): each torus's cooling follows its own day and night; a cold ceiling at night makes the day/night swing a habitat-wide climate dial, small for a humid habitat, large for an arid one.
- **Vision restated as a natural narrow valley** (section 16), anywhere from an arid canyon to a fern gully, its climate set by the solar array's size, the lighting, the orbit's seasons and the water in the air. The fern gully is no longer the reference: light levels are now labelled by landscape (shade-tolerant forest, meadows and gardens), and mist is no longer a requirement.
- **Light-box ceiling** (section 13, artificial overcast sky): light pipes in a cavity coated white with magnesium oxide (a by-product of the glass line) above a graded diffuser, so the sky reads as a real overcast day; ceiling losses ~20–30% instead of ~50%, so the same ~55 MW per 900 m torus now gives ~15 mol/m²/day instead of ~10. Winter-light and farm-ring comparison tables updated.
- **Algae trays above the ceiling** (proposed), lit by about one light pipe in 20–40 shining upward.
- **Despun solar array replaces the capless solar cylinder** (section 13, Power; 17.28): ~3× the power per m² of PV, a size not tied to the stack so it scales further from the Sun, and sunlight concentration becomes possible. One light, slow bearing at one hub end, with power crossing it through a rotary transformer; sized so that, locked to the stack, it still keeps the habitat alive. The dock stays at the other end. Farm-ring mirror option A no longer costs PV through slots. The 3D model now shows the array (with a toggle to lock it to the stack) instead of the cylinder.
- **Double outer skin on each torus** (section 13, micrometeoroids): a thin bumper over an empty crawl space takes over the cylinder's meteoroid-bumper role, with maintenance from inside.
- **Micrometeoroids and maintenance assessed** (section 13): impacts are negligible for panels; rock leaking through the outer skin is the main risk.
- **Magnetic shielding rejected** (17.27): at best a factor ~2 against cosmic rays, superconductors fail the sourcing rule.
- **Beamed power investigated** (section 13, Power): a rectenna on the axis needs no despun antenna, but is almost a cap. Superseded the same day by the despun array; kept as a way to power the hub factory from the industrial array. End-face layout recorded (dock on the axis, vent around it).
- **Moving a newly built habitat checked** (section 15; 17.23): solar sails take centuries, solar-electric thrusters ~10–15 years at 10 GW for a 900 m pair but ~30–200× the building energy. Habitats are built next to their S-type and adopt its orbit; S-types are ranked by orbit shape.

**22–23 October 2026**
- **Interactive 3D model** of the stack published.
- **Hub mirrors** for the farm rings (section 13, now 17.29): end funnels, and in option A double cones in the gaps; tilts, size, mass and construction; option B (end funnels only) added; farm-ring light compared with the valley's sulfur sky.
- **Farm rings moved into each torus's own plane** at ~0.4 r, on its spokes, sized for the high-density biosphere (crop area per person from NASA and Biosphere 2); radiators between farm ring and rim. The ring in the gap is rejected (17.26).
- **Food forest and edible wilderness** for low-density biospheres (section 16).

**Earlier sessions** (newest first)
- Sun-fed farm rings first proposed in widened gaps between tori; glass from S-type silicates and one silica line; plants under minute-scale light fluctuations.
- Food primarily plant-based, with backups ranked by efficiency and usefulness: gas-fermented bacteria, mushrooms and larvae, aquaponics fish, any of the habitat's animals in an emergency.
- Biosphere selection: super-common adaptable generalists at genus level, one ecosystem per valley, no migratory species, small day/night temperature swings; deer only in the larger habitats.
- Sites and seeds: habitats built in their S-type's orbit and spreading by seeds; nursery pairs of 900 m at Itokawa and Apophis, six-stacks of 1.6 km at Eros with Ryugu; Bennu superseded as supplier (17.25); moving finished habitats rejected on energy (17.23).
- Seasonal sky following the host orbit, no yearly storage (17.24); North-Atlantic-like climate; pair lighting rule (never both valleys lit).
- Nuclear power rejected for now under the sourcing rule (17.22); near-Earth location adopted as a conservative starting point.
- Rock shield from S-type tailings adopted instead of the water jacket (17.21).
- Sulfur plasma lighting: non-rotating bulbs, light pipes, central 915 MHz sources (17.20).
- Elevators in the spokes and a one-way antispinward rim train (17.19).
- Six-stack grouped A A B B C C with an 8/8/8 schedule (17.18).
- Capless solar cylinder around the stack (17.17, itself superseded in 17.28); radiators along the spokes in the shaded drum (17.15).
- Co-rotating pairs with staggered days; one shared day per torus (17.13, 17.14).
- Sourcing rule: every massively used material from common asteroid sources.
- Orientation: spin axis perpendicular to the orbital plane, no despun parts; sun-pointing counter-rotating pairs, a non-rotating shield can, counter-rotating stacks and long actively controlled stacks rejected (17.4–17.7); two-parent reproduction dropped (17.10).
- Artificial overcast sky instead of Stanford-style mirrors and windows (17.1).
- Vision: directed panspermia by habitat, a Polynesian-style archipelago, a canyon with at least half wilderness, the habitat as an organism with an AI mind.
- Large hub (radius slightly above the tube width) with factory and dock; structural cable spokes (17.8, 17.9).
- Materials: S-type for metal and shield, C-type for volatiles; comets optional (17.11); steel structure; uses of nickel.
- Sizes: 400 m, 900 m and 1.6 km compared, reduced gravity considered; rotating cylinders (17.3) and larger tori (17.2) rejected.
- Atmosphere: 70 kPa with 29% O₂ instead of sea-level 80/20 (17.12), since nitrogen is the bottleneck.
- Geometry: the 1 g family r = (T/2)²; a fixed 100 m width replaced by the ratio r/w = 16.

---

## Sources

### Radiation shielding

- Globus & Strout, *Orbital Space Settlement Radiation Shielding*, NSS Space Settlement Journal (2017) — 20 mSv/yr limit, deep-space shielding mass (§5b): https://NSS.org/wp-content/uploads/2018/01/NSS-JOURNAL-Orbital-Space-Settlement-Radiation-Shielding.pdf
- NSS summary of the above: https://nss.org/?p=5526
- Globus, *A Radically Easier Path to Space Settlement* — 7 t/m² water, 11 t/m² regolith (§5b, §6): https://NSS.org/wp-content/uploads/RadicallyEasier.pdf
- SR2S (Space Radiation Superconductive Shield), final report summary, CORDIS — toroid designs, MgB₂ conductor, factor-two cosmic-ray dose reduction, ~50 t (§17.27): https://cordis.europa.eu/project/id/313224/reporting/es
- Comparison of active magnetic shielding designs (ESA, NASA NIAC, SR2S), Frontiers in Oncology (2016) — field's share of the dose reduction, bending power and mass (§17.27): https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2016.00097/pdf
- Bamford et al., plasma mini-magnetospheres for crew protection (University of Strathclyde repository) (§17.27): https://strathprints.strath.ac.uk/56454/
- Atwell & Badhwar, *A Shielding Model for an Inflatable Vehicle, TransHab, and the Associated Astronaut Space Radiation Risk Assessment* (COSPAR, 2000) — storm-shelter water jacket (§5b′): https://ntrs.nasa.gov/api/citations/20100033236/downloads/20100033236.pdf

### Atmosphere

- NASA study of material ignition in the spacecraft exploration atmosphere (52.7–58.6 kPa, 30–34% O₂) (§3c): https://ntrs.nasa.gov/api/citations/20080013149/downloads/20080013149.pdf

### Volatiles and source bodies

- Lodders, *Solar System Abundances of the Elements* (2010) — CI chondrite element abundances for the sourcing rule (§10): https://arxiv.org/pdf/1010.2746
- Comet NH₃/H₂O compilation including 67P (A&A 2015, table 4) (§4): https://www.aanda.org/articles/aa/full_html/2015/11/aa26450-15/T4.html
- Altwegg, Balsiger & Fuselier, *Cometary Chemistry and the Origin of Icy Solar System Bodies: the View After Rosetta* (ARA&A 2019) — NH₃ ~0.8% of water, nitrogen deficiency, ammonium salts (§4): https://arxiv.org/pdf/1908.04046
- Pätzold et al., *A homogeneous nucleus for comet 67P/Churyumov–Gerasimenko from its gravity field*, Nature 530 (2016) — mass and density (§4, §10): https://sci.esa.int/web/rosetta/-/57310-patzold-et-al-2015
- Glavin et al., *Abundant ammonia and nitrogen-rich soluble organic matter in samples from asteroid (101955) Bennu*, Nature Astronomy (2025) (§10): https://link.springer.com/article/10.1038/s41550-024-02472-9
- Review of asteroid sample-return science — Bennu C and N content (§10): https://arxiv.org/pdf/2604.22182
- Praet et al., *Hydrogen abundance estimation and distribution on (101955) Bennu*, Icarus 363 (2021) — 0.71 wt% H (§10): https://experts.arizona.edu/en/publications/hydrogen-abundance-estimation-and-distribution-on-101955-bennu/
- Lauretta et al., *Asteroid (101955) Bennu in the Laboratory: Properties of the Sample Collected by OSIRIS-REx* (2024) — phyllosilicates, carbonates, magnetite (§10): https://mdsoar.org/items/ebbe95b1-f869-4af4-9e48-06a8416e59d6/full

### Composition of the explored bodies

- Lodders, *Solar System Abundances of the Elements* (2010), Table 2 — CI chondrite abundances (§10): https://arxiv.org/pdf/1010.2746
- Yokoyama et al., *The Elemental Abundances of Ryugu: Assessment of Chemical Heterogeneities and the Nugget Effect* (2024) — Ryugu bulk abundances vs. CI (§10): https://arxiv.org/pdf/2405.04500
- Yokoyama et al., *Samples returned from the asteroid Ryugu are similar to Ivuna-type carbonaceous meteorites*, Science (2022) — Ryugu ≈ CI, "more chemically pristine" (§10): https://faculty.epss.ucla.edu/~eyoung/reprints/Yokoyama_2022.pdf
- Schaefer & Fegley, *Volatile element chemistry during metamorphism of ordinary chondritic material* — trace elements in H, L and LL falls (Cu, Zn, Ga, Ge, Sn, Ag, In, Se, Te) (§10): https://arxiv.org/pdf/0801.1099
- Arpu Kuilpu H5 chondrite characterization (2024) — one H5's bulk composition and H-chondrite averages after Wasson & Kallemeyn (1988) (§10): https://arxiv.org/pdf/2409.10382
- *The Formation and Evolution of Ordinary Chondrite Parent Bodies* (review) — total iron and metal by volume for H, L, LL; Itokawa LL-like (§10): https://arxiv.org/pdf/1611.08734
- JAXA, Hayabusa sample results (2011) — Itokawa particles match thermally metamorphosed LL chondrites (§10): https://global.jaxa.jp/press/2011/08/20110826_hayabusa_e.html
- Mikouchi et al., *Mineralogy and crystallography of some Itokawa particles*, Earth, Planets and Space (2014) — equilibrated LL (§10): https://earth-planets-space.springeropen.com/articles/10.1186/1880-5981-66-82
- Reddy et al., *Surface Composition of (99942) Apophis* (2018) — Sq-type, LL ordinary chondrite (§10): https://arxiv.org/pdf/1803.05375
- Trombka et al., NEAR X-ray spectrometer results, Science 289 (2000) — Eros chondritic, sulfur-depleted surface (§10): https://experts.arizona.edu/en/publications/the-elemental-composition-of-asteroid-433-eros-results-of-the-nea/
- Peplowski et al., *Hydrogen and major element concentrations on 433 Eros*, Meteoritics & Planetary Science (2015) — L- or LL-chondrite-like (§10): https://karmaka.de/?p=4008
- Zhai et al., *The meteorite analogs of (65803) Didymos*, A&A (2026) — L ordinary chondrite (§10): https://karmaka.de/?p=41745

### Host classes and iron extraction

- Vernazza et al., *Compositional differences between meteorites and near-Earth asteroids*, Nature 454 (2008) — ~2/3 of near-Earth asteroids LL-like (§15): https://news.mit.edu/2008/meteorites-0813
- Dunn et al., *Mineralogies and source regions of near-Earth asteroids*, Icarus 222 (2013) — 15% H, 10% L, 60% LL; named H-like objects (§15): https://www.boulder.swri.edu/~bottke/Reprints/Dunn_2013_Icarus_222_273_Mineral_Source_Regions_NEAs.pdf
- Binzel et al., *Compositional distributions and evolutionary processes for the near-Earth object population* (MITHNEOS, 2019) — S-complex ~29% H, ~19% L, ~51% LL (§15): https://arxiv.org/pdf/2004.05090
- Bourdelle de Micas et al., *Spectral and photometric characterization of (98943) Torifune in preparation for the Hayabusa2# spacecraft flyby*, A&A 693, L19 (2025) — Sq-type, L-chondrite analogue, ~465 m (§15): https://www.aanda.org/10.1051/0004-6361/202452498
- NEOWISE data and thermophysical modelling of (98943) Torifune (2025) — size estimates ~340–490 m, albedo, 5.02 h rotation (§15): https://arxiv.org/html/2512.08181v1
- (98943) Torifune — orbital elements (JPL, via Wikipedia), contact binary seen by Hayabusa2 (§15): https://en.wikipedia.org/wiki/98943_Torifune
- Hayabusa-2 close-up images of asteroid Torifune, Sci.News (2026) — flyby on 5 July 2026 (§15): https://www.sci.news/space/hayabusa-2-close-up-images-asteroid-torifune-14902.html
- (5587) 1990 SB, (16960) 1998 QS52, (159857) 2004 LJ1, (99907) 1989 VA — sizes and orbits (§15): https://en.wikipedia.org/wiki/(5587)_1990_SB, https://en.wikipedia.org/wiki/(16960)_1998_QS52, https://en.wikipedia.org/wiki/(159857)_2004_LJ1, https://en.wikipedia.org/wiki/(99907)_1989_VA
- Hydrogen reduction of lunar basalt, olivine, pyroxene and ilmenite (NASA, 1993) — olivine and pyroxene barely reduced (§10): https://ntrs.nasa.gov/api/citations/19930009598/downloads/19930009598.pdf
- Allanore, Yin & Sadoway, chromium-based anode for molten oxide electrolysis, Nature (2013), as reported by Physics Today and Chemistry World (§10): https://physicstoday.aip.org/news/leaner-greener-iron-and-steel, https://chemistryworld.com/news/greener-cleaner-steel-/6155.article
- Boston Metal, industrial-scale molten-oxide electrolysis cell commissioned (2025), demonstration plant planned for 2026 (§10): https://www.globenewswire.com/news-release/2025/03/12/3041404/0/en/Boston-Metal-Commissions-Industrial-Scale-Cell-in-Crucial-Green-Steel-Milestone.html
- Boston Metal, DOE peer review (2023) — pilot campaigns, endurance runs short of targets (§10): https://www1.eere.energy.gov/iedo/downloads/2023/peer_review/Boston%20Metal_Lambotte_IEDO_Iron-and-Steel_Carbon%20Free%20Iron%20for%20a%20Sustainable%20Future.pdf
- NASA, molten regolith electrolysis of lunar simulant near 1,600 °C (2011) (§10): https://ntrs.nasa.gov/citations/20110008535
- ESA, oxygen and metal from lunar regolith simulant by the FFC process (2019) — ~96% of oxygen at 950 °C in 50 h (§10): https://www.esa.int/ESA_Multimedia/Images/2019/10/Oxygen_and_metal_from_lunar_regolith

### Metallurgy

- Mond process — Ni(CO)₄ formation at 50–60 °C, decomposition at 220–250 °C (§5a, §14): https://en.wikipedia.org/wiki/Mond_process
- Iron pentacarbonyl — industrial formation at 5–30 MPa and 150–200 °C, carbonyl iron, toxicity (§5a, §14): https://en.wikipedia.org/wiki/Iron_pentacarbonyl
- Carbonyl iron powder patent — reduced grades > 99.5% Fe, < 0.1% C, < 0.01% N (§10): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6309620
- The full list for the wire (strength classes, safety factors, impurity limits, relaxation) is in `structure_model/README.md`; the main ones:
  - Tokyo Rope, suspension-bridge wire catalogue — 1,570 / 1,770 / 1,960 MPa classes (§12): https://www.tokyorope.co.jp/english/product/catalog/pdf/scs.pdf
  - JSCE (1995) — Akashi Kaikyō wire at 180 kgf/mm² (§12): https://www.jstage.jst.go.jp/article/jscej1984/1995/528/1995_528_57/_article/-char/en
  - Ohio DOT (2013), cable strength evaluation — NCHRP 534 action level of 2.15 (§12): https://ftp.dot.state.oh.us/PUB/Districts/D02/Programmatic/September%202025/LUC-116431%20%20LUC-2-18.62%20NSTM%20Inspection%20and%20Load%20Rating/2013%20Cable%20Strength%20Evaluation%20Report.pdf
  - Kobelco Technology Review No. 30 — tire cord and saw wire up to ~4 GPa (§12): https://www.kobelco.co.jp/english/ktr/pdf/ktr_30/062-065.pdf
  - US 4,854,032 (Bekaert) — strength rising as wire gets thinner (§12): https://patents.google.com/patent/US4854032
  - The influence of phosphorus and sulphur on the deformability of high-carbon wire (§10): https://wirenet.org/product/the-influence-of-phosphorus-and-sulphur-contents-on-the-plastic-deformability-of-high-carbon-steel-wire/
  - Periodica Polytechnica (BME) — relaxation of cold-drawn wire (§12): https://pp.bme.hu/ci/article/download/4056/3161/7814

### Micrometeoroids

- Drolshagen & Sandra, Grün interplanetary meteoroid flux model (International Meteor Conference 2015) — fluxes at 1 AU, ~20 km/s impacts (§13): https://www.imo.net/imcs/imc2015/2015-24-drolshagensandra-final.pdf

### Dynamics

- Explorer 1 — change of spin axis from internal energy dissipation (§11): https://solarspell-dls.sfis.asu.edu/mea/wikipedia/wp/e/Explorer_1.htm

### Power

- NASA TM-107252, Solar Dynamic Ground Test Demonstration (1990s) — solar Brayton system tested up to 2 kW of electricity (§13): https://ntrs.nasa.gov/citations/19960047096

### Light

- Maclennan et al. (Fusion Systems), *Efficient, full-spectrum, long-lived, non-toxic microwave lamp for plant growth* (1994, NASA contract NAS10-11987) — sulfur lamp efficacy (§13): https://ntrs.nasa.gov/citations/19960011712
- Kusuma, Pattison & Bugbee, *From physics to fixtures to food: current and potential LED efficacy*, Horticulture Research (2020) — 3.4–4.1 µmol/J (§13): https://digitalcommons.usu.edu/psc_facpub/983
- Don Klipstein, sulfur lamp notes — bulb rotation, Smithsonian light-pipe installation, lifetimes (§13): https://donklipstein.com/sulfbulb.html
- US 6,476,557 B1, *Non-rotating electrodeless lamp containing molecular fill* (Fusion Lighting, 2002) — cesium bromide, circularly polarised field, 9,000 h (§13): https://patents.google.com/patent/US6476557
- *On the plasma confinement by acoustic resonance* — alternative to bulb rotation (§13): https://www.researchgate.net/publication/319343991_On_the_plasma_confinement_by_acoustic_resonance_An_innovation_for_electrodeless_high-pressure_discharge_lamps
- Stellant Systems CWM-100kW magnetron data sheet — 915 MHz, 85–86% efficiency (§13): https://stellantsystems.com/wp-content/uploads/2023/10/Magnetron_CWM-100kW_sellsheet_MAY2023.pdf
- High-efficiency magnetrons for accelerators (Snowmass 2022) — ≤ 6,000 h today, 50,000–80,000 h goal, flat efficiency 30–100% (§13): https://www.slac.stanford.edu/econf/C210711/papers/2203.07888.pdf
- NASA Spinoff, CPI MDC klystron for UHF-TV — ~60,000 h projected MTBF (§13): https://spinoff.nasa.gov/node/9980

### Ecology and food

- Biosphere 2 oxygen decline (1.27 ha, 21% → ~14% O₂ in ~16 months; soil respiration, concrete carbonation) (§16): https://www.earthmagazine.org/article/benchmarks-september-26-1991-crew-sealed-inside-biosphere-2/
- Microalgae nucleic acid content (Spirulina maxima ~4–6% dry weight) (§16): https://microbiologyjournal.org/download/75982
- *Food Safety on Utilization of Solar-dried Thai Spirulina* — Protein Advisory Group nucleic acid intake guidance (§16): https://li01.tci-thaijo.org/index.php/anres/article/view/240492
- Spirulina pseudovitamin B12 (citing Watanabe et al. 1999, J. Agric. Food Chem.; Watanabe 2007, Exp. Biol. Med.) (§16): https://en.wikipedia.org/wiki/Spirulina_(dietary_supplement)

### Sites and orbits

- Orbital elements and physical data (Wikipedia infoboxes), used by `asteroid_transfers.py` (§15): [101955 Bennu](https://en.wikipedia.org/wiki/101955_Bennu), [99942 Apophis](https://en.wikipedia.org/wiki/99942_Apophis), [25143 Itokawa](https://en.wikipedia.org/wiki/25143_Itokawa), [162173 Ryugu](https://en.wikipedia.org/wiki/162173_Ryugu), [433 Eros](https://en.wikipedia.org/wiki/433_Eros)
- NASA, Apophis facts — S-type, ~340 m, orbit enlarged after 2029 (§15): https://science.nasa.gov/solar-system/asteroids/apophis-facts
- ESA, Earth's gravity will alter Apophis's orbit during the 2029 flyby (§15): https://www.esa.int/ESA_Multimedia/Images/2021/03/Earth_s_gravity_will_alter_Apophis_orbit_during_2029_flyby
- Orbital evolution of Atira asteroids (MNRAS 2022) — 23 known in 2020, ~8 km-sized S-types expected, ~10–20 Myr lifetimes (§15): https://academic.oup.com/mnras/article/517/4/5921/6815743
- Physical characterization of 2020 AV₂, the first Vatira (§15): https://arxiv.org/html/2006.08304
- MESSENGER finds new evidence for water ice at Mercury's poles (JHU APL) (§15): https://www.jhuapl.edu/news/news-releases/121129-messenger-finds-new-evidence-water-ice-mercurys-poles

### Food

- *Supplemental Food Production With Plants: A Review of NASA Research*, Frontiers in Astronomy and Space Sciences (2021) — ~40–50 m² of crops per person under high light, ~35–40 m² with insects (§13): https://www.frontiersin.org/journals/astronomy-and-space-sciences/articles/10.3389/fspas.2021.734343/full
- Biosphere 2 — ~2,500 m² of agriculture for 8 people, ~83% of the diet (§13): https://en.wikipedia.org/wiki/Biosphere_2
- Wheeler et al., *NASA's Biomass Production Chamber: a testbed for bioregenerative life support studies*, Advances in Space Research 18 (1996) — wheat, soybean, lettuce and potato cycles; edible yields slightly below expectations (§13): https://ntrs.nasa.gov/citations/20040089951
- Wheeler, *NASA Plant Research for Life Support in Space* (2017) — wheat ~3–4× and potato ~2× the field world records; ~40–50 m² of crops for all of one person's food (§13): https://ntrs.nasa.gov/api/citations/20170005429/downloads/20170005429.pdf
- Wheeler, *Growing Food for Space and Earth: NASA's Contributions to Vertical Agriculture* (ASHS, 2015) — crop yield vs. light (§13): https://simoc.space/wp-content/uploads/2018/09/NASA%E2%80%99s-Contributions-to-Vertical-Agriculture-WHEELER-2015.pdf
- Tibbitts, Cao & Wheeler, *Growth of potatoes for CELSS*, NASA CR-177646 (1994) — 37.5 g/m²/day of tuber dry mass at 725 µmol/m²/s, 12 → 24 h days (§13): https://ntrs.nasa.gov/citations/19950005536
- Bugbee & Salisbury, *Exploring the Limits of Crop Productivity: Photosynthetic Efficiency in High Irradiance Environments*, Plant Physiology 88 (1988) — 60 g/m²/day of grain at up to 150 mol/m²/day (§13): https://repository.exst.jaxa.jp/dspace/handle/a-is/299693
- Bugbee, *The components of crop productivity: measuring and modeling plant metabolism*, ASGSB Bulletin 8 (1995) — 0.4–0.7 g of biomass per mol of photons (§13): https://ntrs.nasa.gov/citations/20040090014
- Jin, Formiga Lopez, Heuvelink & Marcelis, *Light use efficiency of lettuce cultivation in vertical farms compared with greenhouse and field*, Food and Energy Security 12 (2023) — ~0.55 g/mol of shoot dry mass on average in vertical farms (§13): https://doaj.org/article/1564564058f648ecb4f5a4e1577c7a79
- Solar Foods, Solein energy use — ~20% electricity-to-calories (§16): https://solarfoods.com/?p=15256
- Solar-powered microbes to feed the world? (ScienceDaily, on Leger et al., PNAS 2021) — ~10% of soybean land per kg of protein (§16): https://ScienceDaily.com/releases/2021/07/210730104303.htm
- Black soldier fly larvae bioconversion of kitchen waste (§16): https://pmc.ncbi.nlm.nih.gov/articles/PMC11765844
- Blue oyster mushroom yield and nutrition on different substrates (§16): https://phytojournal.com/archives/2019.v8.i6.10257/evaluation-of-different-substrates-for-growth-yield-and-nutritive-value-of-ltemgthypsizygus-ulmariusltemgt-blue-oyster-mushroom

### Plants and light fluctuations

- Plant growth under fluctuating light: only extreme amplitudes reduce biomass (Frontiers in Plant Science, 2025) (§17.29): https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2025.1500197/xml
- Rapid photosynthetic induction after short dark periods mitigates growth reduction in lettuce exposed to frequent light–dark cycles (§17.29): https://pubmed.ncbi.nlm.nih.gov/41982517/

### Reference designs

- Stanford Torus (1975 NASA/Stanford summer study; Johnson & Holbrow, *Space Settlements: A Design Study*, 1977) — dimensions, non-rotating soil shield, mirrors (§2a, §17.1, §17.5): https://en.wikipedia.org/wiki/Stanford_torus

### Background works (cited by name, not checked online)

- R. Buckminster Fuller, *Operating Manual for Spaceship Earth* (1969) — "Spaceship Earth" (§16).
- F. H. C. Crick & L. E. Orgel, *Directed Panspermia*, Icarus 19 (1973) (§16).
- G. K. O'Neill, *The High Frontier: Human Colonies in Space* (1977) — rotating cylinders (§17.3).
- R. H. MacArthur & E. O. Wilson, *The Theory of Island Biogeography* (1967) (§16).

### Still unsourced (first-principles estimates or general knowledge)

Rotation, floor area, gas laws, stoichiometry, hoop-stress and spoke models, tangent-chord net and partial-ring loads, spin stability condition, radiator and conduction estimates, Coriolis effect: derived here from standard physics. Not yet backed by a specific source: steel plate strength, the design safety factors of new bridge cables (~2.2–2.5, commonly quoted), maraging steel composition, LED die and phosphor quantities, LED lifetime, ceiling light losses, nickel-iron battery performance, M-type metal fraction and density, soil and regolith densities, rim speed comfort limit (< 2 rpm), light requirements of shade and meadow plants, overcast-sky brightness and its overhead-to-horizon ratio, magnesium oxide reflectance, light-box efficiency, C-type processing energy (~1–2 MJ/kg), solar particle event arrival direction, Bennu's size and mass, taro and loʻi practice, mirror delivery efficiency and facet mass (17.29), protected-aluminium reflectance, city population densities, edible yields per mol for soybean, lentils, berries and flax (estimates), food energy per gram of the crops, the working diet's protein and fat, the farm's light delivery (~85%), tier spacing and ring mass.
