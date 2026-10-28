# Sensitivity (tornado)

One-at-a-time sweep for 6 × 900 m, 2 tier(s) lit, L host at Eros. Each cell: change of the output with the input at its low / high end. Ranked by the largest swing on any output.

| Rank | Assumption | Status | Range | Mass per m² of floor (t/m²) | Rock mined per torus (S-type) (Mt) | C-type per torus (Mt) | Despun array at the site (km²) | People per torus | Heat margin (capacity / stack heat) (×) | Processing energy per torus (PJ) |
|---|---|---|---|---|---|---|---|---|---|---|
|  | **Baseline** |  |  | **37.1** | **15.3** | **4.71** | **1.39** | **2,030** | **2.28** | **8.37** |
| 1 | `nitrogen_recovery` | estimate | 0.500–0.900 fraction |  |  | +40% / -22% |  |  |  | +34% / -19% |
| 2 | `bake_mj_kg` | estimate | 1.00–2.00 MJ per kg of C-type |  |  |  |  |  |  | -28% / +28% |
| 3 | `pv_efficiency` | estimate | 0.180–0.280 fraction |  |  |  | +39% / -11% |  |  |  |
| 4 | `metal_wt_L` | sourced | 0.0700–0.110 free metal, wt fraction |  | +29% / -18% |  |  |  |  | +4% / -3% |
| 5 | `wire_stress_mpa` | estimate | 700–1,200 MPa (working) | +3% / -1% | +33% / -12% |  |  |  |  | +5% / -2% |
| 6 | `crop_light_mol` | estimate | 30.0–45.0 mol/m2/day on the crops |  |  |  | -11% / +17% | -17% / +25% | +10% / -12% |  |
| 7 | `shield_areal_t_m2` | sourced | 9.00–13.0 t/m2 | -18% / +18% | -13% / +13% |  |  |  |  | -2% / +2% |
| 8 | `yield_wheat` | sourced | 0.150–0.400 g/mol |  |  |  |  | -7% / +25% |  |  |
| 9 | `radiator_temp_k` | estimate | 275–295 K |  |  |  |  |  | -13% / +15% |  |
| 10 | `hub_factory_metal_frac` | guess | 0.150–0.500 fraction of torus steel |  | -8% / +20% |  |  |  |  | -1% / +3% |
| 11 | `hull_frames_ref_mt` | estimate | 0.200–0.450 Mt at the reference radius | -1% / +1% | -10% / +15% |  |  |  |  | -2% / +2% |
| 12 | `diet_kcal` | estimate | 2,200–2,800 kcal per person per day |  |  |  |  | +14% / -11% |  |  |
| 13 | `farm_planted_frac` | estimate | 0.700–0.850 fraction of each tier |  |  |  | -8% / +4% | -13% / +6% | +7% / -3% |  |
| 14 | `crush_mj_kg` | estimate | 0.0500–0.150 MJ per kg of S-type rock |  |  |  |  |  |  | -6% / +12% |
| 15 | `valley_diet_share` | estimate | 0–0.150 fraction of calories |  |  |  |  | -7% / +9% |  |  |
| 16 | `lamp_efficacy_umol_j` | sourced | 1.30–1.50 umol/J at the wall |  |  |  | +7% / -6% |  | -7% / +7% |  |
| 17 | `crop_overhead` | estimate | 0.0500–0.200 fraction |  |  |  |  | +5% / -8% |  |  |
| 18 | `yield_potato` | sourced | 0.300–0.600 g/mol |  |  |  |  | -5% / +9% |  |  |
| 19 | `farm_delivery` | estimate | 0.750–0.900 fraction |  |  |  | +9% / -4% |  | -7% / +3% |  |
| 20 | `yield_soybean` | estimate | 0.120–0.220 g/mol |  |  |  |  | -5% / +6% |  |  |
| 21 | `ceiling_delivery` | estimate | 0.650–0.800 fraction |  |  |  | +4% / -2% |  | -6% / +3% |  |
| 22 | `yield_lentils` | estimate | 0.100–0.220 g/mol |  |  |  |  | -5% / +4% |  |  |
| 23 | `c_nitrogen_wt` | sourced | 0.00230–0.00250 wt fraction |  |  | +4% / -4% |  |  |  | +4% / -3% |
| 24 | `yield_flax` | estimate | 0.0500–0.120 g/mol |  |  |  |  | -3% / +3% |  |  |
| 25 | `other_loads_w_m2` | guess | 10.0–25.0 W per m2 of floor |  |  |  | -2% / +3% |  | +1% / -3% |  |
| 26 | `kcal_wheat` | estimate | 3.40–3.80 kcal/g dry |  |  |  |  | -2% / +2% |  |  |
| 27 | `kcal_potato` | estimate | 3.50–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |
| 28 | `kcal_soybean` | estimate | 4.20–4.70 kcal/g dry |  |  |  |  | -1% / +1% |  |  |
| 29 | `yield_berries` | estimate | 0.200–0.300 g/mol |  |  |  |  | -1% / +1% |  |  |
| 30 | `kcal_lentils` | estimate | 3.40–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |
| 31 | `rock_per_water_shield` | sourced | 1.40–1.75 t rock / t water | +1% / -1% |  |  |  |  |  |  |
| 32 | `lake_water_t_m2` | guess | 0.100–0.500 t per m2 of floor | -0% / +1% | -0% / +1% |  |  |  |  |  |
| 33 | `kcal_berries` | estimate | 3.00–3.60 kcal/g dry |  |  |  |  | -1% / +0% |  |  |
| 34 | `fill_water_equiv_t_m2` | estimate | 1.05–1.25 t/m2 water-equivalent | +1% / -0% |  |  |  |  |  |  |
| 35 | `yield_greens` | sourced | 0.350–0.740 g/mol |  |  |  |  | -0% / +1% |  |  |
| 36 | `kcal_flax` | estimate | 5.20–5.90 kcal/g dry |  |  |  |  |  |  |  |
| 37 | `soil_density` | estimate | 1.30–1.80 t/m3 |  |  |  |  |  |  |  |
| 38 | `regolith_density` | estimate | 1.60–2.00 t/m3 |  |  |  |  |  |  |  |
| 39 | `kcal_greens` | estimate | 2.50–3.30 kcal/g dry |  |  |  |  |  |  |  |
| 40 | `hub_radius_per_width` | estimate | 1.00–1.20 hub radius / tube width |  |  |  |  |  |  |  |

# Monte Carlo (2000 samples, triangular over every range)

| Output | Unit | 5th percentile | Median | 95th percentile |
|---|---|---|---|---|
| Mass per m² of floor | t/m² | 32.8 | 37.3 | 41.7 |
| Rock mined per torus (S-type) | Mt | 13.0 | 16.6 | 21.6 |
| C-type per torus | Mt | 3.93 | 4.74 | 5.90 |
| Despun array at the site | km² | 1.28 | 1.52 | 1.88 |
| People per torus |  | 1,830 | 2,310 | 2,910 |
| Heat margin (capacity / stack heat) | × | 1.94 | 2.22 | 2.55 |
| Processing energy per torus | PJ | 6.67 | 8.68 | 11.2 |
