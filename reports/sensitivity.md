# Sensitivity (tornado)

One-at-a-time sweep for 6 × 900 m, 2 tier(s) lit, L host at Eros. Each cell: change of the output with the input at its low / high end. Ranked by the largest swing on any output.

| Rank | Assumption | Status | Range | Mass per m² of floor (t/m²) | Rock mined per torus (S-type) (Mt) | C-type per torus (Mt) | Despun array at the site (km²) | People per torus | Ideal heat margin (end-aperture limit / stack heat) (×) | Processing energy per torus (PJ) | Shipping energy per torus (PJ) | Processing + shipping per torus (PJ) | Energy-limited generation time (yr) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  | **Baseline** |  |  | **40.3** | **16.5** | **5.05** | **1.39** | **2,030** | **4.76** | **8.97** | **20.9** | **29.8** | **5.67** |
| 1 | `ep_exhaust_km_s` | estimate | 20.0–50.0 km/s |  |  |  |  |  |  |  | -31% / +61% | -21% / +43% | -21% / +43% |
| 2 | `lake_water_t_m2` | guess | 0.100–0.500 t per m2 of floor | -0% / +1% |  |  |  |  |  |  | -29% / +48% | -20% / +34% | -20% / +34% |
| 3 | `nitrogen_recovery` | estimate | 0.500–0.900 fraction |  |  | +40% / -22% |  |  |  | +34% / -19% |  | +10% / -6% | +10% / -6% |
| 4 | `bake_mj_kg` | estimate | 1.00–2.00 MJ per kg of C-type |  |  |  |  |  |  | -28% / +28% |  | -8% / +8% | -8% / +8% |
| 5 | `pv_efficiency` | estimate | 0.180–0.280 fraction |  |  |  | +39% / -11% |  |  |  |  |  |  |
| 6 | `metal_wt_L` | sourced | 0.0700–0.110 free metal, wt fraction |  | +29% / -18% |  |  |  |  | +4% / -3% |  | +1% / -1% | +1% / -1% |
| 7 | `crop_light_mol` | estimate | 30.0–45.0 mol/m2/day on the crops |  |  |  | -11% / +17% | -17% / +25% |  |  |  |  |  |
| 8 | `shield_areal_t_m2` | sourced | 9.00–13.0 t/m2 | -19% / +19% | -14% / +14% |  |  |  |  | -2% / +2% |  | -1% / +1% | -1% / +1% |
| 9 | `ep_efficiency` | estimate | 0.500–0.700 fraction |  |  |  |  |  |  |  | +20% / -14% | +14% / -10% | +14% / -10% |
| 10 | `yield_wheat` | sourced | 0.150–0.400 g/mol |  |  |  |  | -7% / +25% |  |  |  |  |  |
| 11 | `wire_stress_mpa` | estimate | 800–1,200 MPa (working) | +2% / -1% | +19% / -13% |  |  |  |  | +3% / -2% |  | +1% / -1% | +1% / -1% |
| 12 | `radiator_temp_k` | estimate | 275–295 K |  |  |  |  |  | -13% / +15% |  |  |  |  |
| 13 | `hub_factory_metal_frac` | guess | 0.150–0.500 fraction of torus steel |  | -8% / +20% |  |  |  |  | -1% / +3% |  | -0% / +1% | -0% / +1% |
| 14 | `diet_kcal` | estimate | 2,200–2,800 kcal per person per day |  |  |  |  | +14% / -11% |  |  |  |  |  |
| 15 | `hull_frames_ref_mt` | estimate | 0.200–0.450 Mt at the reference radius | -1% / +1% | -9% / +14% |  |  |  |  | -1% / +2% |  | -0% / +1% | -0% / +1% |
| 16 | `soil_water_vol_frac` | estimate | 0.150–0.350 m3 water / m3 soil |  |  |  |  |  |  |  | -10% / +10% | -7% / +7% | -7% / +7% |
| 17 | `organics_shipped_t_m2` | guess | 0.0500–0.150 t per m2 of floor |  |  |  |  |  |  |  | -10% / +10% | -7% / +7% | -7% / +7% |
| 18 | `farm_planted_frac` | estimate | 0.700–0.850 fraction of each tier |  |  |  | -8% / +4% | -13% / +6% |  |  |  |  |  |
| 19 | `ceiling_delivery` | estimate | 0.650–0.800 fraction |  |  |  | +4% / -2% |  | -12% / +6% |  |  |  |  |
| 20 | `crush_mj_kg` | estimate | 0.0500–0.150 MJ per kg of S-type rock |  |  |  |  |  |  | -6% / +12% |  | -2% / +4% | -2% / +4% |
| 21 | `valley_diet_share` | estimate | 0–0.150 fraction of calories |  |  |  |  | -7% / +9% |  |  |  |  |  |
| 22 | `lamp_efficacy_umol_j` | sourced | 1.30–1.50 umol/J at the wall |  |  |  | +7% / -6% |  | -7% / +7% |  |  |  |  |
| 23 | `crop_overhead` | estimate | 0.0500–0.200 fraction |  |  |  |  | +5% / -8% |  |  |  |  |  |
| 24 | `yield_potato` | sourced | 0.300–0.600 g/mol |  |  |  |  | -5% / +9% |  |  |  |  |  |
| 25 | `farm_delivery` | estimate | 0.750–0.900 fraction |  |  |  | +9% / -4% |  |  |  |  |  |  |
| 26 | `yield_soybean` | estimate | 0.120–0.220 g/mol |  |  |  |  | -5% / +6% |  |  |  |  |  |
| 27 | `yield_lentils` | estimate | 0.100–0.220 g/mol |  |  |  |  | -5% / +4% |  |  |  |  |  |
| 28 | `c_nitrogen_wt` | sourced | 0.00230–0.00250 wt fraction |  |  | +4% / -4% |  |  |  | +4% / -3% |  | +1% / -1% | +1% / -1% |
| 29 | `other_loads_w_m2` | guess | 10.0–25.0 W per m2 of floor |  |  |  | -2% / +3% |  | +3% / -5% |  |  |  |  |
| 30 | `farm_pressure_kpa` | guess | 30.0–70.0 kPa |  |  | -5% / +0% |  |  |  | -5% / +0% |  | -2% / +0% | -2% / +0% |
| 31 | `yield_flax` | estimate | 0.0500–0.120 g/mol |  |  |  |  | -3% / +3% |  |  |  |  |  |
| 32 | `kcal_wheat` | estimate | 3.40–3.80 kcal/g dry |  |  |  |  | -2% / +2% |  |  |  |  |  |
| 33 | `kcal_potato` | estimate | 3.50–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 34 | `farm_shell_m` | guess | 0.00500–0.0200 m of steel |  | -1% / +1% |  |  |  |  |  |  |  |  |
| 35 | `kcal_soybean` | estimate | 4.20–4.70 kcal/g dry |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 36 | `yield_berries` | estimate | 0.200–0.300 g/mol |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 37 | `rock_density` | estimate | 1.80–2.20 t/m3 | +1% / -1% | +1% / -1% |  |  |  |  |  |  |  |  |
| 38 | `kcal_lentils` | estimate | 3.40–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 39 | `kcal_berries` | estimate | 3.00–3.60 kcal/g dry |  |  |  |  | -1% / +0% |  |  |  |  |  |
| 40 | `yield_greens` | sourced | 0.350–0.740 g/mol |  |  |  |  | -0% / +1% |  |  |  |  |  |
| 41 | `kcal_flax` | estimate | 5.20–5.90 kcal/g dry |  |  |  |  |  |  |  |  |  |  |
| 42 | `kcal_greens` | estimate | 2.50–3.30 kcal/g dry |  |  |  |  |  |  |  |  |  |  |
| 43 | `crawl_space_m` | estimate | 1.00–2.00 m |  |  |  |  |  |  |  |  |  |  |
| 44 | `hub_radius_per_width` | estimate | 1.00–1.20 hub radius / tube width |  |  |  |  |  |  |  |  |  |  |
| 45 | `rock_per_water_shield` | sourced | 1.40–1.75 t rock / t water |  |  |  |  |  |  |  |  |  |  |
| 46 | `soil_density` | estimate | 1.30–1.80 t/m3 |  |  |  |  |  |  |  |  |  |  |
| 47 | `regolith_density` | estimate | 1.60–2.00 t/m3 |  |  |  |  |  |  |  |  |  |  |
| 48 | `farm_growing_kg_m2` | guess | 50.0–200 kg per m2 planted |  |  |  |  |  |  |  |  |  |  |

# Combined ranking

Each input's largest swing on any output, over representative designs (sizes, host classes and sites; `sensitivity.REPRESENTATIVE`), with the output and design where it occurs.

| Rank | Assumption | Status | Largest effect on | Low / high | Design |
|---|---|---|---|---|---|
| 1 | `ep_exhaust_km_s` | estimate | Shipping energy per torus | -31% / +61% | 1.6 km six-stack, LL host, Eros |
| 2 | `lake_water_t_m2` | guess | Shipping energy per torus | -30% / +51% | 400 m pair, LL host, Itokawa |
| 3 | `nitrogen_recovery` | estimate | C-type per torus | +40% / -22% | 900 m six-stack, L host, Eros |
| 4 | `bake_mj_kg` | estimate | Processing energy per torus | -31% / +31% | 2.5 km pair, H host, Eros |
| 5 | `pv_efficiency` | estimate | Despun array at the site | +39% / -11% | 2.5 km pair, H host, Eros |
| 6 | `metal_wt_LL` | sourced | Rock mined per torus (S-type) | +29% / -18% | 400 m pair, LL host, Itokawa |
| 7 | `metal_wt_L` | sourced | Rock mined per torus (S-type) | +29% / -18% | 900 m six-stack, L host, Eros |
| 8 | `shield_areal_t_m2` | sourced | Mass per m² of floor | -20% / +22% | 400 m pair, LL host, Itokawa |
| 9 | `crop_light_mol` | estimate | People per torus | -17% / +25% | 1.6 km six-stack, LL host, Eros |
| 10 | `wire_stress_mpa` | estimate | Rock mined per torus (S-type) | +24% / -15% | 2.5 km pair, H host, Eros |
| 11 | `crush_mj_kg` | estimate | Processing energy per torus | -12% / +23% | 400 m pair, LL host, Itokawa |
| 12 | `ep_efficiency` | estimate | Shipping energy per torus | +20% / -14% | 400 m pair, LL host, Itokawa |
| 13 | `yield_wheat` | sourced | People per torus | -7% / +25% | 900 m six-stack, L host, Eros |
| 14 | `hull_frames_ref_mt` | estimate | Rock mined per torus (S-type) | -12% / +18% | 400 m pair, LL host, Itokawa |
| 15 | `radiator_temp_k` | estimate | Ideal heat margin (end-aperture limit / stack heat) | -13% / +15% | 900 m six-stack, L host, Eros |
| 16 | `hub_factory_metal_frac` | guess | Rock mined per torus (S-type) | -8% / +20% | 2.5 km pair, H host, Eros |
| 17 | `diet_kcal` | estimate | People per torus | +14% / -11% | 900 m six-stack, L host, Eros |
| 18 | `metal_wt_H` | sourced | Rock mined per torus (S-type) | +13% / -11% | 2.5 km pair, H host, Eros |
| 19 | `soil_water_vol_frac` | estimate | Shipping energy per torus | -10% / +10% | 400 m pair, LL host, Itokawa |
| 20 | `organics_shipped_t_m2` | guess | Shipping energy per torus | -10% / +10% | 400 m pair, LL host, Itokawa |
| 21 | `farm_planted_frac` | estimate | People per torus | -13% / +6% | 900 m six-stack, L host, Eros |
| 22 | `ceiling_delivery` | estimate | Ideal heat margin (end-aperture limit / stack heat) | -12% / +6% | 1.6 km six-stack, LL host, Eros |
| 23 | `valley_diet_share` | estimate | People per torus | -7% / +9% | 900 m six-stack, L host, Eros |
| 24 | `lamp_efficacy_umol_j` | sourced | Despun array at the site | +7% / -6% | 900 m six-stack, L host, Eros |
| 25 | `crop_overhead` | estimate | People per torus | +5% / -8% | 900 m six-stack, L host, Eros |
| 26 | `yield_potato` | sourced | People per torus | -5% / +9% | 900 m six-stack, L host, Eros |
| 27 | `farm_delivery` | estimate | Despun array at the site | +9% / -4% | 1.6 km six-stack, LL host, Eros |
| 28 | `hull_frames_exponent` | estimate | Rock mined per torus (S-type) | +6% / -5% | 400 m pair, LL host, Itokawa |
| 29 | `farm_pressure_kpa` | guess | C-type per torus | -11% / +0% | 400 m pair, LL host, Itokawa |
| 30 | `yield_soybean` | estimate | People per torus | -5% / +6% | 1.6 km six-stack, LL host, Eros |
| 31 | `yield_lentils` | estimate | People per torus | -5% / +4% | 1.6 km six-stack, LL host, Eros |
| 32 | `c_nitrogen_wt` | sourced | C-type per torus | +4% / -4% | 400 m pair, LL host, Itokawa |
| 33 | `other_loads_w_m2` | guess | Ideal heat margin (end-aperture limit / stack heat) | +3% / -5% | 900 m pair, L host, Torifune |
| 34 | `yield_flax` | estimate | People per torus | -3% / +3% | 2.5 km pair, H host, Eros |
| 35 | `farm_shell_m` | guess | Rock mined per torus (S-type) | -1% / +3% | 400 m pair, LL host, Itokawa |
| 36 | `kcal_wheat` | estimate | People per torus | -2% / +2% | 900 m six-stack, L host, Eros |
| 37 | `rock_density` | estimate | Mass per m² of floor | +2% / -1% | 400 m pair, LL host, Itokawa |
| 38 | `kcal_potato` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 39 | `kcal_soybean` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 40 | `yield_berries` | estimate | People per torus | -1% / +1% | 2.5 km pair, H host, Eros |
| 41 | `kcal_lentils` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 42 | `kcal_berries` | estimate | People per torus | -1% / +0% | 900 m six-stack, L host, Eros |
| 43 | `yield_greens` | sourced | People per torus | -0% / +1% | 900 m six-stack, L host, Eros |
| 44 | `kcal_flax` | estimate | People per torus | -0% / +0% | 900 m six-stack, L host, Eros |
| 45 | `crawl_space_m` | estimate | Ideal heat margin (end-aperture limit / stack heat) | +0% / -0% | 400 m pair, LL host, Itokawa |
| 46 | `kcal_greens` | estimate | People per torus | -0% / +0% | 1.6 km six-stack, LL host, Eros |
| 47 | `soil_density` | estimate | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 48 | `hub_radius_per_width` | estimate | Ideal heat margin (end-aperture limit / stack heat) | +0% / -0% | 400 m pair, LL host, Itokawa |
| 49 | `regolith_density` | estimate | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 50 | `rock_per_water_shield` | sourced | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 51 | `farm_growing_kg_m2` | guess | Rock mined per torus (S-type) | -0% / +0% | 2.5 km pair, H host, Eros |

# Monte Carlo (2000 samples)

Each input drawn independently from a triangular distribution (low, value, high). The spread shows what the chosen ranges imply; it is not a physical confidence interval.

| Output | Unit | 5th percentile | Median | 95th percentile |
|---|---|---|---|---|
| Mass per m² of floor | t/m² | 35.1 | 40.3 | 45.8 |
| Rock mined per torus (S-type) | Mt | 13.9 | 17.4 | 22.0 |
| C-type per torus | Mt | 4.13 | 4.97 | 6.22 |
| Despun array at the site | km² | 1.28 | 1.51 | 1.87 |
| People per torus |  | 1,830 | 2,320 | 2,940 |
| Ideal heat margin (end-aperture limit / stack heat) | × | 4.05 | 4.61 | 5.22 |
| Processing energy per torus | PJ | 7.07 | 9.17 | 11.8 |
| Shipping energy per torus | PJ | 16.0 | 23.8 | 36.1 |
| Processing + shipping per torus | PJ | 24.9 | 33.3 | 45.2 |
| Energy-limited generation time | yr | 4.73 | 6.34 | 8.60 |
