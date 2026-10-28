# Validation against the notes

197 figures from notes.md checked; 185 within tolerance (5% unless noted), 12 known mismatches, 0 unexplained.

## Mismatches

| § | Figure | Notes | Model | Diff | Why |
|---|---|---|---|---|---|
| §5c | Hull and frames, 400 m | 0.0500 Mt | 0.0465 Mt | -7.1% | the notes round 0.047 Mt to 0.05 |
| §7 | Water needed (soil, O₂, lakes), 900 m | 0.150 Mt | 0.123 Mt | -17.7% | the notes give no breakdown of the water; their per-m² figure falls with size (0.47 -> 0.40 -> 0.37 t/m²) for no stated reason, while the model's soil and lake water scale with the floor; the lake term is fitted at 1.6 km |
| §7 | Water needed (soil, O₂, lakes), 2.5 km | 0.900 Mt | 1.01 Mt | +12.1% | the notes give no breakdown of the water; their per-m² figure falls with size (0.47 -> 0.40 -> 0.37 t/m²) for no stated reason, while the model's soil and lake water scale with the floor; the lake term is fitted at 1.6 km |
| §7 | C-type sized by nitrogen, 900 m | 5.00 Mt | 4.71 Mt | -5.8% | the notes round 4.7 Mt up to ~5 |
| §10 | C-type water contained, 900 m | 0.320 Mt | 0.302 Mt | -5.8% | follows the rounded ~5 Mt of C-type |
| §10 | S-type, H host, 1.6 km | 40.0 Mt | 42.5 Mt | +6.2% | metal-bound at 17 wt% free metal (the notes use ~18% there) |
| §13 | Array at 1 AU, valley, 900 m | 0.280 km² | 0.265 km² | -5.4% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, constant sky, Itokawa | 0.800 km² | 0.756 km² | -5.5% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, constant sky, Eros | 0.900 km² | 0.840 km² | -6.6% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, constant sky, Apophis | 0.340 km² | 0.317 km² | -6.6% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, seasonal sky, Eros | 0.480 km² | 0.455 km² | -5.2% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, seasonal sky, Torifune | 0.240 km² | 0.226 km² | -5.6% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §13 | Break-even, 900 m, no farm lit | 27.0 tori | 29.0 tori | +7.5% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, constant sky, Torifune | 0.440 km² | 0.418 km² | -5.0% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, seasonal sky, 1 AU | 0.150 km² | 0.143 km² | -4.4% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |
| §15 | Array, 900 m valley, seasonal sky, Itokawa | 0.430 km² | 0.409 km² | -4.8% | the notes round the 900 m valley + other loads up to ~60 MW (~55 MW of sky + ~5 MW); the same formulas give ~57 MW (52.6 + 4.8), so the arrays sized from it are ~4-5% smaller |

## All checks

| § | Figure | Notes | Model | Diff |  |
|---|---|---|---|---|---|
| §1 | Rotation, 900 m | 1.00 rpm | 1.00 rpm | +0.0% | ✓ |
| §1 | Rotation, 1.6 km | 0.750 rpm | 0.750 rpm | +0.0% | ✓ |
| §1 | Rotation, 2.5 km | 0.600 rpm | 0.600 rpm | +0.0% | ✓ |
| §1 | Rim speed, 900 m | 94.0 m/s | 94.2 m/s | +0.3% | ✓ |
| §1 | Rim speed, 1.6 km | 126 m/s | 126 m/s | -0.3% | ✓ |
| §1 | Rim speed, 2.5 km | 157 m/s | 157 m/s | +0.1% | ✓ |
| §2b | Floor, 400 m | 6.30 ha | 6.28 ha | -0.3% | ✓ |
| §2b | Floor, 900 m | 32.0 ha | 31.8 ha | -0.6% | ✓ |
| §2b | Floor, 1.6 km | 100 ha | 101 ha | +0.5% | ✓ |
| §2b | Floor, 2.5 km | 245 ha | 245 ha | +0.2% | ✓ |
| §3a | Torus volume, 400 m | 1,200,000 m³ | 1,200,000 m³ | -0.4% | ✓ |
| §3a | Torus volume, 900 m | 13,600,000 m³ | 13,600,000 m³ | +0.1% | ✓ |
| §3a | Torus volume, 1.6 km | 76,500,000 m³ | 76,500,000 m³ | -0.0% | ✓ |
| §3a | Torus volume, 2.5 km | 292,000,000 m³ | 292,000,000 m³ | -0.1% | ✓ |
| §12 | Hub radius, 900 m | 60.0 m | 60.8 m | +1.3% | ✓ |
| §12 | Hub radius, 1.6 km | 110 m | 108 m | -1.8% | ✓ |
| §12 | Hub radius, 2.5 km | 170 m | 169 m | -0.7% | ✓ |
| §4 | N₂, 900 m | 7.90 kt | 7.92 kt | +0.2% | ✓ |
| §4 | N₂, 1.6 km | 44.5 kt | 44.5 kt | -0.0% | ✓ |
| §4 | N₂, 2.5 km | 170 kt | 170 kt | -0.2% | ✓ |
| §4 | O₂, 900 m | 3.70 kt | 3.68 kt | -0.4% | ✓ |
| §4 | O₂, 1.6 km | 20.7 kt | 20.7 kt | +0.0% | ✓ |
| §4 | O₂, 2.5 km | 80.0 kt | 79.0 kt | -1.3% | ✓ |
| §5c | Rock shield after fill credit, 400 m | 2.00 Mt | 1.99 Mt | -0.6% | ✓ |
| §5c | Rock shield after fill credit, 900 m | 10.1 Mt | 10.1 Mt | -0.4% | ✓ |
| §5c | Rock shield after fill credit, 1.6 km | 31.9 Mt | 31.8 Mt | -0.3% | ✓ |
| §5c | Rock shield after fill credit, 2.5 km | 78.0 Mt | 77.7 Mt | -0.4% | ✓ |
| §5c | Rock shield after fill credit, 3.6 km | 162 Mt | 161 Mt | -0.6% | ✓ |
| §5c | Fill, 400 m | 0.110 Mt | 0.107 Mt | -2.9% | ✓ |
| §5c | Fill, 900 m | 0.540 Mt | 0.541 Mt | +0.1% | ✓ |
| §5c | Fill, 1.6 km | 1.70 Mt | 1.71 Mt | +0.5% | ✓ |
| §5c | Fill, 2.5 km | 4.20 Mt | 4.17 Mt | -0.7% | ✓ |
| §5c | Fill, 3.6 km | 8.60 Mt | 8.65 Mt | +0.6% | ✓ |
| §5c | Hull and frames, 400 m | 0.0500 Mt | 0.0465 Mt | -7.1% | ✗ |
| §5c | Hull and frames, 900 m | 0.300 Mt | 0.300 Mt | +0.0% | ✓ |
| §5c | Hull and frames, 1.6 km | 1.10 Mt | 1.13 Mt | +2.4% | ✓ |
| §5c | Hull and frames, 2.5 km | 3.10 Mt | 3.15 Mt | +1.5% | ✓ |
| §5c | Hull and frames, 3.6 km | 7.00 Mt | 7.28 Mt | +3.9% | ✓ |
| §5c | Spokes, 400 m | 0.0700 Mt | 0.0684 Mt | -2.3% | ✓ |
| §5c | Spokes, 900 m | 0.800 Mt | 0.800 Mt | -0.0% | ✓ |
| §5c | Spokes, 1.6 km | 4.70 Mt | 4.65 Mt | -1.0% | ✓ |
| §5c | Spokes, 2.5 km | 18.5 Mt | 18.5 Mt | +0.2% | ✓ |
| §5c | Spokes, 3.6 km | 58.0 Mt | 58.4 Mt | +0.8% | ✓ |
| §5c | Total per torus, 400 m | 2.20 Mt | 2.23 Mt | +1.2% | ✓ |
| §5c | Total per torus, 900 m | 11.9 Mt | 11.8 Mt | -0.9% | ✓ |
| §5c | Total per torus, 1.6 km | 40.0 Mt | 39.6 Mt | -1.0% | ✓ |
| §5c | Total per torus, 2.5 km | 105 Mt | 104 Mt | -0.6% | ✓ |
| §5c | Total per torus, 3.6 km | 238 Mt | 237 Mt | -0.3% | ✓ |
| §5c | Mass per m² of floor, 400 m | 36.0 t | 35.4 t | -1.6% | ✓ |
| §5c | Mass per m² of floor, 900 m | 37.0 t | 37.1 t | +0.2% | ✓ |
| §5c | Mass per m² of floor, 1.6 km | 40.0 t | 39.4 t | -1.5% | ✓ |
| §5c | Mass per m² of floor, 2.5 km | 43.0 t | 42.5 t | -1.1% | ✓ |
| §5c | Mass per m² of floor, 3.6 km | 47.0 t | 46.6 t | -0.8% | ✓ |
| §8 | Steel per torus, 900 m | 1.10 Mt | 1.10 Mt | -0.0% | ✓ |
| §8 | Steel per torus, 1.6 km | 5.80 Mt | 5.78 Mt | -0.4% | ✓ |
| §8 | Steel per torus, 2.5 km | 22.0 Mt | 21.7 Mt | -1.4% | ✓ |
| §9 | Steel at 0.3 g, 900 m | 0.320 Mt | 0.319 Mt | -0.2% | ✓ |
| §9 | Steel at 0.3 g, 1.6 km | 1.60 Mt | 1.64 Mt | +2.6% | ✓ |
| §9 | Steel at 0.3 g, 2.5 km | 6.00 Mt | 5.98 Mt | -0.3% | ✓ |
| §9 | Total at 0.3 g, 900 m | 11.1 Mt | 11.0 Mt | -0.8% | ✓ |
| §9 | Total at 0.3 g, 1.6 km | 35.7 Mt | 35.5 Mt | -0.6% | ✓ |
| §9 | Total at 0.3 g, 2.5 km | 89.2 Mt | 88.7 Mt | -0.6% | ✓ |
| §9 | Period at 0.3 g, 900 m | 110 s | 110 s | -0.4% | ✓ |
| §9 | Period at 0.3 g, 1.6 km | 146 s | 146 s | +0.0% | ✓ |
| §9 | Period at 0.3 g, 2.5 km | 183 s | 183 s | -0.2% | ✓ |
| §7 | Water needed (soil, O₂, lakes), 900 m | 0.150 Mt | 0.123 Mt | -17.7% | ✗ |
| §7 | Water needed (soil, O₂, lakes), 1.6 km | 0.400 Mt | 0.400 Mt | +0.1% | ✓ |
| §7 | Water needed (soil, O₂, lakes), 2.5 km | 0.900 Mt | 1.01 Mt | +12.1% | ✗ |
| §7 | Spin-up propellant (water, 3 km/s), 900 m | 0.370 Mt | 0.371 Mt | +0.2% | ✓ |
| §7 | Spin-up propellant (water, 3 km/s), 1.6 km | 1.70 Mt | 1.66 Mt | -2.4% | ✓ |
| §7 | Spin-up propellant (water, 3 km/s), 2.5 km | 5.50 Mt | 5.46 Mt | -0.6% | ✓ |
| §7 | C-type sized by nitrogen, 900 m | 5.00 Mt | 4.71 Mt | -5.8% | ✗ |
| §7 | C-type sized by nitrogen, 1.6 km | 27.0 Mt | 26.5 Mt | -1.9% | ✓ |
| §7 | C-type sized by nitrogen, 2.5 km | 100 Mt | 101 Mt | +1.0% | ✓ |
| §7 | C-type with water spin-up, 900 m | 8.00 Mt | 7.72 Mt | -3.5% | ✓ |
| §10 | C-type water contained, 900 m | 0.320 Mt | 0.302 Mt | -5.8% | ✗ |
| §10 | C-type water contained, 1.6 km | 1.70 Mt | 1.69 Mt | -0.3% | ✓ |
| §10 | C-type water contained, 2.5 km | 6.50 Mt | 6.46 Mt | -0.6% | ✓ |
| §10 | C-type diameter, 900 m | 200 m | 196 m | -2.1% | ✓ |
| §10 | C-type diameter, 1.6 km | 350 m | 348 m | -0.6% | ✓ |
| §10 | C-type diameter, 2.5 km | 540 m | 544 m | +0.7% | ✓ |
| §10 | Total metal (with hub, dock, factory), 900 m | 1.40 Mt | 1.37 Mt | -1.8% | ✓ |
| §10 | Total metal (with hub, dock, factory), 1.6 km | 7.30 Mt | 7.22 Mt | -1.1% | ✓ |
| §10 | Total metal (with hub, dock, factory), 2.5 km | 27.0 Mt | 27.1 Mt | +0.4% | ✓ |
| §10 | Regolith (0.5 m), 900 m | 0.290 Mt | 0.286 Mt | -1.3% | ✓ |
| §10 | Regolith (0.5 m), 1.6 km | 0.900 Mt | 0.905 Mt | +0.5% | ✓ |
| §10 | Regolith (0.5 m), 2.5 km | 2.20 Mt | 2.21 Mt | +0.4% | ✓ |
| §10 | Soil (0.5 m), 900 m | 0.250 Mt | 0.254 Mt | +1.8% | ✓ |
| §10 | Soil (0.5 m), 1.6 km | 0.800 Mt | 0.804 Mt | +0.5% | ✓ |
| §10 | Soil (0.5 m), 2.5 km | 2.00 Mt | 1.96 Mt | -1.8% | ✓ |
| §10 | S-type, H host, 900 m | 12.0 Mt | 12.5 Mt | +3.9% | ✓ |
| §10 | S-type, H host, 1.6 km | 40.0 Mt | 42.5 Mt | +6.2% | ✗ |
| §10 | S-type, H host, 2.5 km | 165 Mt | 159 Mt | -3.4% | ✓ |
| §10 | S-type, LL host, 900 m | 32.0 Mt | 30.5 Mt | -4.5% | ✓ |
| §10 | S-type, LL host, 1.6 km | 165 Mt | 161 Mt | -2.7% | ✓ |
| §10 | S-type, LL host, 2.5 km | 600 Mt | 602 Mt | +0.4% | ✓ |
| §10 | S-type, L host, 900 m | 16.0 Mt | 15.3 Mt | -4.5% | ✓ |
| §10 | S-type diameter, H host, 900 m | 225 m | 228 m | +1.5% | ✓ |
| §13 | Valley lighting, 900 m | 55.0 MW | 52.6 MW | -4.4% | ✓ |
| §13 | Valley lighting, 1.6 km | 166 MW | 166 MW | +0.1% | ✓ |
| §13 | Valley lighting, 2.5 km | 410 MW | 406 MW | -1.0% | ✓ |
| §13 | Valley + other loads, 900 m | 60.0 MW | 57.4 MW | -4.4% | ✓ |
| §13 | Valley + other loads, 1.6 km | 180 MW | 181 MW | +0.7% | ✓ |
| §13 | Valley + other loads, 2.5 km | 440 MW | 443 MW | +0.6% | ✓ |
| §13 | Farm lighting per tier, 400 m | 6.30 MW | 6.34 MW | +0.6% | ✓ |
| §13 | Farm lighting per tier, 900 m | 32.0 MW | 32.1 MW | +0.2% | ✓ |
| §13 | Farm lighting per tier, 1.6 km | 102 MW | 101 MW | -0.6% | ✓ |
| §13 | Farm lighting per tier, 2.5 km | 247 MW | 247 MW | +0.2% | ✓ |
| §13 | Plain rim solar, 900 m | 34.0 MW | 34.5 MW | +1.3% | ✓ |
| §13 | Plain rim solar, 1.6 km | 110 MW | 109 MW | -1.0% | ✓ |
| §13 | Plain rim solar, 2.5 km | 270 MW | 266 MW | -1.5% | ✓ |
| §13 | Array at 1 AU, valley, 900 m | 0.280 km² | 0.265 km² | -5.4% | ✗ |
| §13 | Array at 1 AU, valley, 1.6 km | 0.850 km² | 0.837 km² | -1.5% | ✓ |
| §13 | Array at 1 AU, valley, 2.5 km | 2.10 km² | 2.04 km² | -2.7% | ✓ |
| §13 | Array at 1 AU, per tier, 900 m | 0.150 km² | 0.148 km² | -1.3% | ✓ |
| §13 | Array at 1 AU, per tier, 1.6 km | 0.480 km² | 0.468 km² | -2.5% | ✓ |
| §13 | Array at 1 AU, per tier, 2.5 km | 1.16 km² | 1.14 km² | -1.5% | ✓ |
| §13 | Array at 1 AU, three tiers, 900 m | 0.730 km² | 0.709 km² | -2.9% | ✓ |
| §13 | Array at 1 AU, three tiers, 1.6 km | 2.30 km² | 2.24 km² | -2.6% | ✓ |
| §13 | Array at 1 AU, three tiers, 2.5 km | 5.60 km² | 5.47 km² | -2.3% | ✓ |
| §8 | Farm ring area per tier, 900 m | 11.0 ha | 11.5 ha | +4.1% | ✓ |
| §8 | Farm ring area per tier, 1.6 km | 36.0 ha | 36.2 ha | +0.5% | ✓ |
| §8 | Farm ring area per tier, 2.5 km | 88.0 ha | 88.4 ha | +0.4% | ✓ |
| §13 | Crops per tier, 400 m | 1.80 ha | 1.81 ha | +0.5% | ✓ |
| §13 | Crops per tier, 900 m | 9.00 ha | 9.16 ha | +1.8% | ✓ |
| §13 | Crops per tier, 1.6 km | 29.0 ha | 29.0 ha | -0.2% | ✓ |
| §13 | Crops per tier, 2.5 km | 70.0 ha | 70.7 ha | +1.0% | ✓ |
| §13 | Light per person | 3,200 mol/day | 3,240 mol/day | +1.3% | ✓ |
| §13 | Crop area per person | 89.0 m² | 90.1 m² | +1.2% | ✓ |
| §13 | Food per m² of crops | 26.0 kcal/day | 25.8 kcal/day | -0.7% | ✓ |
| §13 | Electricity per person | 31.0 kW | 31.5 kW | +1.7% | ✓ |
| §13 | People per tier lit, 400 m | 200  | 201  | +0.5% | ✓ |
| §13 | People per tier lit, 900 m | 1,000  | 1,020  | +1.7% | ✓ |
| §13 | People per tier lit, 1.6 km | 3,250  | 3,220  | -1.1% | ✓ |
| §13 | People per tier lit, 2.5 km | 7,900  | 7,850  | -0.6% | ✓ |
| §13 | People, three tiers lit, 900 m | 3,050  | 3,050  | +0.1% | ✓ |
| §13 | People, three tiers lit, 1.6 km | 9,750  | 9,650  | -1.1% | ✓ |
| §13 | People, three tiers lit, 2.5 km | 23,700  | 23,500  | -0.6% | ✓ |
| §13 | Floor per person, one tier, 900 m | 310 m² | 313 m² | +0.9% | ✓ |
| §13 | Floor per person, one tier, 1.6 km | 310 m² | 313 m² | +0.9% | ✓ |
| §13 | Floor per person, one tier, 2.5 km | 310 m² | 313 m² | +0.9% | ✓ |
| §13 | Farm ring mass, 900 m | 50.0 kt | 48.6 kt | -2.8% | ✓ |
| §13 | Farm ring mass, 1.6 km | 150 kt | 149 kt | -0.4% | ✓ |
| §13 | Radiating surface, valley, 900 m | 16.0 ha | 15.3 ha | -4.2% | ✓ |
| §13 | Radiating surface, valley, 1.6 km | 48.0 ha | 48.5 ha | +1.0% | ✓ |
| §13 | Radiating surface, valley, 2.5 km | 117 ha | 118 ha | +1.1% | ✓ |
| §13 | Radiating surface per tier, 900 m | 8.50 ha | 8.57 ha | +0.9% | ✓ |
| §13 | Radiating surface per tier, 1.6 km | 27.0 ha | 27.1 ha | +0.4% | ✓ |
| §13 | Radiating surface per tier, 2.5 km | 66.0 ha | 66.2 ha | +0.2% | ✓ |
| §13 | End openings (both), 900 m | 4.40 km² | 4.45 km² | +1.1% | ✓ |
| §13 | End openings (both), 1.6 km | 14.0 km² | 14.1 km² | +0.5% | ✓ |
| §13 | Capacity of the end openings, 900 m | 1.60 GW | 1.66 GW | +4.0% | ✓ |
| §13 | Capacity of the end openings, 1.6 km | 5.30 GW | 5.26 GW | -0.7% | ✓ |
| §13 | Break-even, 900 m, no farm lit | 27.0 tori | 29.0 tori | +7.5% | ✓ |
| §13 | Break-even, 900 m, 1 tiers lit | 18.0 tori | 18.6 tori | +3.4% | ✓ |
| §13 | Break-even, 900 m, 2 tiers lit | 13.0 tori | 13.7 tori | +5.4% | ✓ |
| §13 | Break-even, 900 m, 3 tiers lit | 10.5 tori | 10.8 tori | +3.2% | ✓ |
| §13 | Break-even, 1.6 km, no farm lit | 29.0 tori | 29.0 tori | +0.1% | ✓ |
| §13 | Break-even, 1.6 km, three tiers lit | 11.0 tori | 10.8 tori | -1.5% | ✓ |
| §13 | Heat, 900 m pair, three tiers lit | 310 MW | 307 MW | -0.9% | ✓ |
| §13 | Heat, 900 m six-stack, three tiers lit | 930 MW | 922 MW | -0.9% | ✓ |
| §13 | Array mass, 900 m, valley | 0.800 kt | 0.794 kt | -0.7% | ✓ |
| §13 | Radiator panel mass, 900 m, three tiers | 1.00 kt | 1.03 kt | +2.6% | ✓ |
| §11 | Max tori, 0.9 km, 10 m gaps, 0% margin | 33.0 tori | 33.0 tori | +0.0% | ✓ |
| §11 | Max tori, 0.9 km, 10 m gaps, 10% margin | 30.0 tori | 30.0 tori | +0.0% | ✓ |
| §11 | Max tori, 0.9 km, 10 m gaps, 20% margin | 27.0 tori | 27.0 tori | +0.0% | ✓ |
| §11 | Max tori, 1.6 km, 10 m gaps, 0% margin | 35.0 tori | 35.0 tori | +0.0% | ✓ |
| §11 | Max tori, 1.6 km, 10 m gaps, 10% margin | 32.0 tori | 32.0 tori | +0.0% | ✓ |
| §11 | Max tori, 1.6 km, 10 m gaps, 20% margin | 29.0 tori | 29.0 tori | +0.0% | ✓ |
| §11 | Max tori, 0.9 km, 40 m gaps, 20% margin | 18.0 tori | 18.0 tori | +0.0% | ✓ |
| §11 | Stack length at the limit, 900 m | 1,800 m | 1,790 m | -0.6% | ✓ |
| §0 | Six-stack length, 10 m gaps | 400 m | 398 m | -0.6% | ✓ |
| §0 | Six-stack length, 40 m gaps | 580 m | 578 m | -0.4% | ✓ |
| §15 | Array, 900 m valley, constant sky, Itokawa | 0.800 km² | 0.756 km² | -5.5% | ✗ |
| §15 | Array, 900 m valley, constant sky, Eros | 0.900 km² | 0.840 km² | -6.6% | ✗ |
| §15 | Array, 900 m valley, constant sky, Torifune | 0.440 km² | 0.418 km² | -5.0% | ✓ |
| §15 | Array, 900 m valley, constant sky, Apophis | 0.340 km² | 0.317 km² | -6.6% | ✗ |
| §15 | Array, 900 m valley, seasonal sky, 1 AU | 0.150 km² | 0.143 km² | -4.4% | ✓ |
| §15 | Array, 900 m valley, seasonal sky, Itokawa | 0.430 km² | 0.409 km² | -4.8% | ✓ |
| §15 | Array, 900 m valley, seasonal sky, Eros | 0.480 km² | 0.455 km² | -5.2% | ✗ |
| §15 | Array, 900 m valley, seasonal sky, Torifune | 0.240 km² | 0.226 km² | -5.6% | ✗ |
| §15 | Array, 900 m, per tier, Itokawa | 0.430 km² | 0.423 km² | -1.7% | ✓ |
| §15 | Array, 900 m, per tier, Eros | 0.470 km² | 0.470 km² | -0.0% | ✓ |
| §15 | Array, 900 m, per tier, Torifune | 0.240 km² | 0.234 km² | -2.6% | ✓ |
| §15 | Array, 900 m, per tier, Apophis 2029 | 0.260 km² | 0.255 km² | -2.0% | ✓ |
| §15 | Array, 1.6 km valley, seasonal sky, Eros | 1.45 km² | 1.44 km² | -0.8% | ✓ |
| §15 | Array, 1.6 km, per tier, Eros | 1.51 km² | 1.48 km² | -1.7% | ✓ |
| §15 | 900 m tori supported by Itokawa | 1.00 tori | 1.15 tori | +14.6% | ✓ |
| §15 | 900 m tori supported by Didymos | 30.0 tori | 32.7 tori | +9.1% | ✓ |
| §15 | 900 m tori supported by Torifune | 6.00 tori | 6.55 tori | +9.1% | ✓ |
| §15 | 900 m tori supported by Ryugu | 90.0 tori | 95.5 tori | +6.1% | ✓ |
| §15 | 900 m tori supported by Bennu | 15.0 tori | 15.5 tori | +3.3% | ✓ |
| §15 | 1.6 km tori supported by Ryugu | 17.0 tori | 17.0 tori | -0.0% | ✓ |
| §15 | Processing energy, 900 m | 0.300 GW·yr | 0.258 GW·yr | -14.1% | ✓ |
| §15 | Shipping energy at 4.5 km/s | 120,000,000 J/kg | 121,000,000 J/kg | +1.1% | ✓ |
| §15 | Shipping energy at 6.3 km/s | 175,000,000 J/kg | 175,000,000 J/kg | +0.1% | ✓ |
| §15 | Shipping energy at 8.5 km/s | 250,000,000 J/kg | 246,000,000 J/kg | -1.7% | ✓ |
