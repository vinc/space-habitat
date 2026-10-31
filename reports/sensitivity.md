# Sensitivity (tornado)

One-at-a-time sweep for 2 × 900 m, 1 tier(s) lit, L host at 1 AU. Each cell: change of the output with the input at its low / high end. Ranked by the largest swing on any output. Left out as unknown for this design: Shipping energy per torus, Processing + shipping per torus, Energy-limited generation time.

| Rank | Assumption | Status | Range | Mass per m² of floor (t/m²) | Rock mined per torus (S-type) (Mt) | C-type per torus (Mt) | Despun array at the site (km²) | People per torus | Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) (×) | Processing energy per torus (PJ) |
|---|---|---|---|---|---|---|---|---|---|---|
|  | **Baseline** |  |  | **40.1** | **16.4** | **5.05** | **0.124** | **1,020** | **31.0** | **8.97** |
| 1 | `nitrogen_recovery` | estimate | 0.500–0.900 fraction |  |  | +40% / -22% |  |  |  | +34% / -19% |
| 2 | `bake_mj_kg` | estimate | 1.00–2.00 MJ per kg of C-type |  |  |  |  |  |  | -28% / +28% |
| 3 | `pv_efficiency` | estimate | 0.180–0.280 fraction |  |  |  | +39% / -11% |  |  |  |
| 4 | `metal_wt_L` | sourced | 0.0700–0.110 free metal, wt fraction |  | +29% / -18% |  |  |  |  | +4% / -3% |
| 5 | `crop_light_mol` | estimate | 30.0–45.0 mol/m2/day on the crops |  |  |  | -7% / +10% | -17% / +25% |  |  |
| 6 | `shield_areal_t_m2` | sourced | 9.00–13.0 t/m2 | -19% / +20% | -14% / +14% |  |  |  |  | -2% / +2% |
| 7 | `yield_wheat` | sourced | 0.150–0.400 g/mol |  |  |  |  | -7% / +25% |  |  |
| 8 | `wire_stress_mpa` | estimate | 800–1,200 MPa (working) | +2% / -1% | +19% / -13% |  |  |  |  | +3% / -2% |
| 9 | `radiator_temp_k` | estimate | 275–295 K |  |  |  |  |  | -13% / +15% |  |
| 10 | `hub_factory_metal_frac` | guess | 0.150–0.500 fraction of torus steel |  | -8% / +20% |  |  |  |  | -1% / +3% |
| 11 | `diet_kcal` | estimate | 2,200–2,800 kcal per person per day |  |  |  |  | +14% / -11% |  |  |
| 12 | `hull_frames_ref_mt` | estimate | 0.200–0.450 Mt at the reference radius | -1% / +1% | -9% / +14% |  |  |  |  | -1% / +2% |
| 13 | `lamp_efficacy_umol_j` | estimate | 2.70–3.40 umol/J at the wall, white LEDs (the valley) |  |  |  | +4% / -5% |  | -8% / +11% |  |
| 14 | `farm_planted_frac` | estimate | 0.700–0.850 fraction of each tier |  |  |  | -5% / +3% | -13% / +6% |  |  |
| 15 | `crush_mj_kg` | estimate | 0.0500–0.150 MJ per kg of S-type rock |  |  |  |  |  |  | -6% / +12% |
| 16 | `other_loads_w_m2` | guess | 10.0–25.0 W per m2 of floor |  |  |  | -6% / +12% |  | +6% / -11% |  |
| 17 | `valley_diet_share` | estimate | 0–0.150 fraction of calories |  |  |  |  | -7% / +9% |  |  |
| 18 | `crop_overhead` | estimate | 0.0500–0.200 fraction |  |  |  |  | +5% / -8% |  |  |
| 19 | `yield_potato` | sourced | 0.300–0.600 g/mol |  |  |  |  | -5% / +9% |  |  |
| 20 | `ceiling_delivery` | estimate | 0.750–0.880 fraction |  |  |  | +5% / -1% |  | -10% / +3% |  |
| 21 | `yield_soybean` | estimate | 0.120–0.220 g/mol |  |  |  |  | -5% / +6% |  |  |
| 22 | `farm_lamp_efficacy_umol_j` | estimate | 3.20–4.10 umol/J at the wall, blue + red LEDs (the farm); 0: as the valley's lamps |  |  |  | +5% / -5% |  |  |  |
| 23 | `yield_lentils` | estimate | 0.100–0.220 g/mol |  |  |  |  | -5% / +4% |  |  |
| 24 | `c_nitrogen_wt` | sourced | 0.00230–0.00250 wt fraction |  |  | +4% / -4% |  |  |  | +4% / -3% |
| 25 | `farm_delivery` | estimate | 0.850–0.970 fraction |  |  |  | +5% / -1% |  |  |  |
| 26 | `farm_pressure_kpa` | guess | 30.0–70.0 kPa |  |  | -5% / +0% |  |  |  | -5% / +0% |
| 27 | `yield_flax` | estimate | 0.0500–0.120 g/mol |  |  |  |  | -3% / +3% |  |  |
| 28 | `kcal_wheat` | estimate | 3.40–3.80 kcal/g dry |  |  |  |  | -2% / +2% |  |  |
| 29 | `kcal_potato` | estimate | 3.50–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |
| 30 | `farm_shell_m` | guess | 0.00500–0.0200 m of steel |  | -1% / +1% |  |  |  |  |  |
| 31 | `kcal_soybean` | estimate | 4.20–4.70 kcal/g dry |  |  |  |  | -1% / +1% |  |  |
| 32 | `yield_berries` | estimate | 0.200–0.300 g/mol |  |  |  |  | -1% / +1% |  |  |
| 33 | `rock_density` | estimate | 1.80–2.20 t/m3 | +1% / -1% | +1% / -1% |  |  |  |  |  |
| 34 | `kcal_lentils` | estimate | 3.40–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |
| 35 | `kcal_berries` | estimate | 3.00–3.60 kcal/g dry |  |  |  |  | -1% / +0% |  |  |
| 36 | `yield_greens` | sourced | 0.350–0.740 g/mol |  |  |  |  | -0% / +1% |  |  |
| 37 | `kcal_flax` | estimate | 5.20–5.90 kcal/g dry |  |  |  |  |  |  |  |
| 38 | `kcal_greens` | estimate | 2.50–3.30 kcal/g dry |  |  |  |  |  |  |  |
| 39 | `ballast_frac` | guess | 0.000100–0.00200 share of the rim's mass |  |  |  |  |  |  |  |
| 40 | `crawl_space_m` | estimate | 1.00–2.00 m |  |  |  |  |  |  |  |
| 41 | `hub_radius_per_width` | estimate | 1.00–1.20 hub radius / tube width |  |  |  |  |  |  |  |
| 42 | `soil_water_vol_frac` | estimate | 0.150–0.350 m3 water / m3 soil |  |  |  |  |  |  |  |
| 43 | `rock_per_water_shield` | sourced | 1.40–1.75 t rock / t water |  |  |  |  |  |  |  |
| 44 | `soil_density` | estimate | 1.30–1.80 t/m3 |  |  |  |  |  |  |  |
| 45 | `lake_floor_frac` | guess | 0.0100–0.0500 share of the floor under ponds and streams |  |  |  |  |  |  |  |
| 46 | `regolith_density` | estimate | 1.60–2.00 t/m3 |  |  |  |  |  |  |  |
| 47 | `biomass_water_kg_m2` | estimate | 3.00–30.0 kg per m2 of floor |  |  |  |  |  |  |  |
| 48 | `lake_depth_m` | guess | 0.500–1.50 m, mean depth |  |  |  |  |  |  |  |
| 49 | `farm_growing_kg_m2` | guess | 50.0–200 kg per m2 planted |  |  |  |  |  |  |  |

# Combined ranking

Each input's largest swing on any output, over representative designs (sizes, host classes and sites; `sensitivity.REPRESENTATIVE`), with the output and design where it occurs.

| Rank | Assumption | Status | Largest effect on | Low / high | Design |
|---|---|---|---|---|---|
| 1 | `ep_exhaust_km_s` | estimate | Shipping energy per torus | -31% / +61% | 900 m six-stack, L host, Eros |
| 2 | `nitrogen_recovery` | estimate | C-type per torus | +40% / -22% | 900 m six-stack, L host, Eros |
| 3 | `bake_mj_kg` | estimate | Processing energy per torus | -31% / +31% | 2.5 km pair, H host, Eros |
| 4 | `pv_efficiency` | estimate | Despun array at the site | +39% / -11% | 900 m six-stack, L host, Eros |
| 5 | `ballast_frac` | guess | Shipping energy per torus | -10% / +39% | 400 m pair, LL host, Itokawa |
| 6 | `metal_wt_LL` | sourced | Rock mined per torus (S-type) | +29% / -18% | 400 m pair, LL host, Itokawa |
| 7 | `metal_wt_L` | sourced | Rock mined per torus (S-type) | +29% / -18% | 900 m six-stack, L host, Eros |
| 8 | `shield_areal_t_m2` | sourced | Mass per m² of floor | -21% / +22% | 400 m pair, LL host, Itokawa |
| 9 | `crop_light_mol` | estimate | People per torus | -17% / +25% | 1.6 km six-stack, LL host, Eros |
| 10 | `wire_stress_mpa` | estimate | Rock mined per torus (S-type) | +24% / -15% | 2.5 km pair, H host, Eros |
| 11 | `crush_mj_kg` | estimate | Processing energy per torus | -12% / +23% | 400 m pair, LL host, Itokawa |
| 12 | `ep_efficiency` | estimate | Shipping energy per torus | +20% / -14% | 900 m six-stack, L host, Eros |
| 13 | `yield_wheat` | sourced | People per torus | -7% / +25% | 900 m six-stack, L host, Eros |
| 14 | `organics_shipped_t_m2` | guess | Shipping energy per torus | -16% / +16% | 400 m pair, LL host, Itokawa |
| 15 | `soil_water_vol_frac` | estimate | Shipping energy per torus | -16% / +16% | 400 m pair, LL host, Itokawa |
| 16 | `hull_frames_ref_mt` | estimate | Rock mined per torus (S-type) | -12% / +18% | 400 m pair, LL host, Itokawa |
| 17 | `radiator_temp_k` | estimate | Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) | -13% / +15% | 1.6 km six-stack, LL host, Eros |
| 18 | `hub_factory_metal_frac` | guess | Rock mined per torus (S-type) | -8% / +20% | 2.5 km pair, H host, Eros |
| 19 | `diet_kcal` | estimate | People per torus | +14% / -11% | 900 m six-stack, L host, Eros |
| 20 | `metal_wt_H` | sourced | Rock mined per torus (S-type) | +13% / -11% | 2.5 km pair, H host, Eros |
| 21 | `lamp_efficacy_umol_j` | estimate | Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) | -8% / +11% | 1.6 km six-stack, LL host, Eros |
| 22 | `farm_planted_frac` | estimate | People per torus | -13% / +6% | 900 m six-stack, L host, Eros |
| 23 | `other_loads_w_m2` | guess | Despun array at the site | -6% / +12% | 2.5 km pair, H host, Eros |
| 24 | `valley_diet_share` | estimate | People per torus | -7% / +9% | 900 m six-stack, L host, Eros |
| 25 | `farm_lamp_efficacy_umol_j` | estimate | Despun array at the site | +7% / -7% | 900 m six-stack, L host, Eros |
| 26 | `crop_overhead` | estimate | People per torus | +5% / -8% | 900 m six-stack, L host, Eros |
| 27 | `yield_potato` | sourced | People per torus | -5% / +9% | 900 m six-stack, L host, Eros |
| 28 | `ceiling_delivery` | estimate | Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) | -10% / +3% | 2.5 km pair, H host, Eros |
| 29 | `lake_floor_frac` | guess | Shipping energy per torus | -3% / +10% | 400 m pair, LL host, Itokawa |
| 30 | `hull_frames_exponent` | estimate | Rock mined per torus (S-type) | +6% / -5% | 400 m pair, LL host, Itokawa |
| 31 | `farm_pressure_kpa` | guess | C-type per torus | -11% / +0% | 400 m pair, LL host, Itokawa |
| 32 | `yield_soybean` | estimate | People per torus | -5% / +6% | 1.6 km six-stack, LL host, Eros |
| 33 | `yield_lentils` | estimate | People per torus | -5% / +4% | 1.6 km six-stack, LL host, Eros |
| 34 | `biomass_water_kg_m2` | estimate | Shipping energy per torus | -2% / +6% | 400 m pair, LL host, Itokawa |
| 35 | `c_nitrogen_wt` | sourced | C-type per torus | +4% / -4% | 400 m pair, LL host, Itokawa |
| 36 | `farm_delivery` | estimate | Despun array at the site | +7% / -1% | 900 m six-stack, L host, Eros |
| 37 | `lake_depth_m` | guess | Shipping energy per torus | -3% / +3% | 400 m pair, LL host, Itokawa |
| 38 | `yield_flax` | estimate | People per torus | -3% / +3% | 2.5 km pair, H host, Eros |
| 39 | `farm_shell_m` | guess | Rock mined per torus (S-type) | -2% / +3% | 400 m pair, LL host, Itokawa |
| 40 | `kcal_wheat` | estimate | People per torus | -2% / +2% | 900 m six-stack, L host, Eros |
| 41 | `rock_density` | estimate | Mass per m² of floor | +2% / -1% | 400 m pair, LL host, Itokawa |
| 42 | `kcal_potato` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 43 | `kcal_soybean` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 44 | `yield_berries` | estimate | People per torus | -1% / +1% | 2.5 km pair, H host, Eros |
| 45 | `kcal_lentils` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 46 | `kcal_berries` | estimate | People per torus | -1% / +0% | 900 m six-stack, L host, Eros |
| 47 | `yield_greens` | sourced | People per torus | -0% / +1% | 900 m six-stack, L host, Eros |
| 48 | `kcal_flax` | estimate | People per torus | -0% / +0% | 900 m six-stack, L host, Eros |
| 49 | `crawl_space_m` | estimate | Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) | +0% / -0% | 400 m pair, LL host, Itokawa |
| 50 | `kcal_greens` | estimate | People per torus | -0% / +0% | 1.6 km six-stack, LL host, Eros |
| 51 | `soil_density` | estimate | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 52 | `hub_radius_per_width` | estimate | Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) | +0% / -0% | 400 m pair, LL host, Itokawa |
| 53 | `regolith_density` | estimate | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 54 | `rock_per_water_shield` | sourced | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 55 | `farm_growing_kg_m2` | guess | Rock mined per torus (S-type) | -0% / +0% | 2.5 km pair, H host, Eros |

# Monte Carlo (2000 samples)

Each input drawn independently from a triangular distribution (low, value, high). The spread shows what the chosen ranges imply; it is not a physical confidence interval.

| Output | Unit | 5th percentile | Median | 95th percentile |
|---|---|---|---|---|
| Mass per m² of floor | t/m² | 34.9 | 40.1 | 45.6 |
| Rock mined per torus (S-type) | Mt | 13.8 | 17.4 | 22.1 |
| C-type per torus | Mt | 4.14 | 4.95 | 6.15 |
| Despun array at the site | km² | 0.115 | 0.134 | 0.165 |
| People per torus |  | 913 | 1,160 | 1,460 |
| Main section's ideal heat margin (drum end apertures / valley heat; farm section excluded) | × | 26.1 | 29.8 | 34.2 |
| Processing energy per torus | PJ | 7.01 | 9.14 | 11.9 |

# Farm radiators' reach: `farm_radiator_outer_frac` across its range

The farm radiators' outer radius (guess, 0.60–1.4 of the floor radius) sets the farm section's panel area and how much of the drum's farm end it shades. The one-at-a-time sweep and the Monte Carlo can't see it (they use `evaluate`, which ray traces nothing, and their heat metric is the main drum's ideal margin, which leaves the farm section out), so it is swept here with the farm section alone and the assembled stack.

| Stack, tiers lit | Reach (× floor radius) | Farm alone | Assembled farm margin | Assembled main margin | Assembled coverage main / farm | Cools both? |
|---|---|---|---|---|---|---|
| 900 m six, 2 tiers | 0.60 | 5.2 | 4.0 | 4.9 | 20% / 100% | yes |
| 900 m six, 2 tiers | 0.80 | 10.0 | 6.5 | 6.3 | 75% / 75% | yes |
| 900 m six, 2 tiers | 1.0 (default) | 16 | 6.2 | 6.3 | 50% / 20% | yes |
| 900 m six, 2 tiers | 1.2 | 22 | 6.3 | 6.3 | 35% / 10% | yes |
| 900 m six, 2 tiers | 1.4 | 30 | 9.3 | 6.9 | 50% / 10% | yes |
| 900 m six, 3 tiers | 0.60 | 3.5 | 2.9 | 3.1 | 10% / 100% | yes |
| 900 m six, 3 tiers | 0.80 | 6.6 | 4.7 | 5.5 | 35% / 100% | yes |
| 900 m six, 3 tiers | 1.0 (default) | 11 | 5.6 | 5.7 | 100% / 35% | yes |
| 900 m six, 3 tiers | 1.2 | 15 | 6.8 | 6.2 | 100% / 20% | yes |
| 900 m six, 3 tiers | 1.4 | 20 | 6.2 | 6.9 | 75% / 10% | yes |
