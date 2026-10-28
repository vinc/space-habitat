# Sensitivity (tornado)

One-at-a-time sweep for 6 × 900 m, 2 tier(s) lit, L host at Eros. Each cell: change of the output with the input at its low / high end. Ranked by the largest swing on any output.

| Rank | Assumption | Status | Range | Mass per m² of floor (t/m²) | Rock mined per torus (S-type) (Mt) | C-type per torus (Mt) | Despun array at the site (km²) | People per torus | Ideal heat margin (end-aperture limit / stack heat) (×) | Processing energy per torus (PJ) | Shipping energy per torus (PJ) | Processing + shipping per torus (PJ) | Energy-limited generation time (yr) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  | **Baseline** |  |  | **40.3** | **16.2** | **4.71** | **1.39** | **2,030** | **2.25** | **8.45** | **20.8** | **29.2** | **5.55** |
| 1 | `ep_exhaust_km_s` | estimate | 20.0–50.0 km/s |  |  |  |  |  |  |  | -31% / +61% | -22% / +44% | -22% / +44% |
| 2 | `lake_water_t_m2` | guess | 0.100–0.500 t per m2 of floor | -0% / +1% |  |  |  |  |  |  | -29% / +49% | -21% / +35% | -21% / +35% |
| 3 | `nitrogen_recovery` | estimate | 0.500–0.900 fraction |  |  | +40% / -22% |  |  |  | +33% / -19% |  | +10% / -5% | +10% / -5% |
| 4 | `bake_mj_kg` | estimate | 1.00–2.00 MJ per kg of C-type |  |  |  |  |  |  | -28% / +28% |  | -8% / +8% | -8% / +8% |
| 5 | `pv_efficiency` | estimate | 0.180–0.280 fraction |  |  |  | +39% / -11% |  |  |  |  |  |  |
| 6 | `metal_wt_L` | sourced | 0.0700–0.110 free metal, wt fraction |  | +29% / -18% |  |  |  |  | +5% / -3% |  | +1% / -1% | +1% / -1% |
| 7 | `crop_light_mol` | estimate | 30.0–45.0 mol/m2/day on the crops |  |  |  | -11% / +17% | -17% / +25% | +10% / -12% |  |  |  |  |
| 8 | `shield_areal_t_m2` | sourced | 9.00–13.0 t/m2 | -19% / +19% | -14% / +14% |  |  |  |  | -2% / +2% |  | -1% / +1% | -1% / +1% |
| 9 | `ep_efficiency` | estimate | 0.500–0.700 fraction |  |  |  |  |  |  |  | +20% / -14% | +14% / -10% | +14% / -10% |
| 10 | `wire_stress_mpa` | estimate | 800–1,200 MPa (working) | +2% / -1% | +19% / -13% |  |  |  |  | +3% / -2% |  | +1% / -1% | +1% / -1% |
| 11 | `yield_wheat` | sourced | 0.150–0.400 g/mol |  |  |  |  | -7% / +25% |  |  |  |  |  |
| 12 | `radiator_temp_k` | estimate | 275–295 K |  |  |  |  |  | -13% / +15% |  |  |  |  |
| 13 | `hub_factory_metal_frac` | guess | 0.150–0.500 fraction of torus steel |  | -8% / +20% |  |  |  |  | -1% / +3% |  | -0% / +1% | -0% / +1% |
| 14 | `diet_kcal` | estimate | 2,200–2,800 kcal per person per day |  |  |  |  | +14% / -11% |  |  |  |  |  |
| 15 | `hull_frames_ref_mt` | estimate | 0.200–0.450 Mt at the reference radius | -1% / +1% | -9% / +14% |  |  |  |  | -1% / +2% |  | -0% / +1% | -0% / +1% |
| 16 | `soil_water_vol_frac` | estimate | 0.150–0.350 m3 water / m3 soil |  |  |  |  |  |  |  | -10% / +10% | -7% / +7% | -7% / +7% |
| 17 | `organics_shipped_t_m2` | guess | 0.0500–0.150 t per m2 of floor |  |  |  |  |  |  |  | -10% / +10% | -7% / +7% | -7% / +7% |
| 18 | `crush_mj_kg` | estimate | 0.0500–0.150 MJ per kg of S-type rock |  |  |  |  |  |  | -7% / +12% |  | -2% / +4% | -2% / +4% |
| 19 | `farm_planted_frac` | estimate | 0.700–0.850 fraction of each tier |  |  |  | -8% / +4% | -13% / +6% | +7% / -3% |  |  |  |  |
| 20 | `valley_diet_share` | estimate | 0–0.150 fraction of calories |  |  |  |  | -7% / +9% |  |  |  |  |  |
| 21 | `lamp_efficacy_umol_j` | sourced | 1.30–1.50 umol/J at the wall |  |  |  | +7% / -6% |  | -7% / +7% |  |  |  |  |
| 22 | `crop_overhead` | estimate | 0.0500–0.200 fraction |  |  |  |  | +5% / -8% |  |  |  |  |  |
| 23 | `yield_potato` | sourced | 0.300–0.600 g/mol |  |  |  |  | -5% / +9% |  |  |  |  |  |
| 24 | `farm_delivery` | estimate | 0.750–0.900 fraction |  |  |  | +9% / -4% |  | -7% / +3% |  |  |  |  |
| 25 | `yield_soybean` | estimate | 0.120–0.220 g/mol |  |  |  |  | -5% / +6% |  |  |  |  |  |
| 26 | `ceiling_delivery` | estimate | 0.650–0.800 fraction |  |  |  | +4% / -2% |  | -6% / +3% |  |  |  |  |
| 27 | `yield_lentils` | estimate | 0.100–0.220 g/mol |  |  |  |  | -5% / +4% |  |  |  |  |  |
| 28 | `c_nitrogen_wt` | sourced | 0.00230–0.00250 wt fraction |  |  | +4% / -4% |  |  |  | +4% / -3% |  | +1% / -1% | +1% / -1% |
| 29 | `yield_flax` | estimate | 0.0500–0.120 g/mol |  |  |  |  | -3% / +3% |  |  |  |  |  |
| 30 | `other_loads_w_m2` | guess | 10.0–25.0 W per m2 of floor |  |  |  | -2% / +3% |  | +1% / -3% |  |  |  |  |
| 31 | `kcal_wheat` | estimate | 3.40–3.80 kcal/g dry |  |  |  |  | -2% / +2% |  |  |  |  |  |
| 32 | `kcal_potato` | estimate | 3.50–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 33 | `kcal_soybean` | estimate | 4.20–4.70 kcal/g dry |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 34 | `yield_berries` | estimate | 0.200–0.300 g/mol |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 35 | `rock_density` | estimate | 1.80–2.20 t/m3 | +1% / -1% | +1% / -1% |  |  |  |  |  |  |  |  |
| 36 | `kcal_lentils` | estimate | 3.40–3.90 kcal/g dry |  |  |  |  | -1% / +1% |  |  |  |  |  |
| 37 | `kcal_berries` | estimate | 3.00–3.60 kcal/g dry |  |  |  |  | -1% / +0% |  |  |  |  |  |
| 38 | `yield_greens` | sourced | 0.350–0.740 g/mol |  |  |  |  | -0% / +1% |  |  |  |  |  |
| 39 | `kcal_flax` | estimate | 5.20–5.90 kcal/g dry |  |  |  |  |  |  |  |  |  |  |
| 40 | `kcal_greens` | estimate | 2.50–3.30 kcal/g dry |  |  |  |  |  |  |  |  |  |  |
| 41 | `crawl_space_m` | estimate | 1.00–2.00 m |  |  |  |  |  |  |  |  |  |  |
| 42 | `hub_radius_per_width` | estimate | 1.00–1.20 hub radius / tube width |  |  |  |  |  |  |  |  |  |  |
| 43 | `rock_per_water_shield` | sourced | 1.40–1.75 t rock / t water |  |  |  |  |  |  |  |  |  |  |
| 44 | `soil_density` | estimate | 1.30–1.80 t/m3 |  |  |  |  |  |  |  |  |  |  |
| 45 | `regolith_density` | estimate | 1.60–2.00 t/m3 |  |  |  |  |  |  |  |  |  |  |

# Combined ranking

Each input's largest swing on any output, over representative designs (sizes, host classes and sites; `sensitivity.REPRESENTATIVE`), with the output and design where it occurs.

| Rank | Assumption | Status | Largest effect on | Low / high | Design |
|---|---|---|---|---|---|
| 1 | `ep_exhaust_km_s` | estimate | Shipping energy per torus | -31% / +61% | 2.5 km pair, H host, Eros |
| 2 | `lake_water_t_m2` | guess | Shipping energy per torus | -30% / +51% | 400 m pair, LL host, Itokawa |
| 3 | `nitrogen_recovery` | estimate | C-type per torus | +40% / -22% | 900 m six-stack, L host, Eros |
| 4 | `bake_mj_kg` | estimate | Processing energy per torus | -31% / +31% | 2.5 km pair, H host, Eros |
| 5 | `pv_efficiency` | estimate | Despun array at the site | +39% / -11% | 2.5 km pair, H host, Eros |
| 6 | `metal_wt_L` | sourced | Rock mined per torus (S-type) | +29% / -18% | 900 m six-stack, L host, Eros |
| 7 | `metal_wt_LL` | sourced | Rock mined per torus (S-type) | +29% / -18% | 1.6 km six-stack, LL host, Eros |
| 8 | `shield_areal_t_m2` | sourced | Mass per m² of floor | -20% / +22% | 400 m pair, LL host, Itokawa |
| 9 | `crop_light_mol` | estimate | People per torus | -17% / +25% | 1.6 km six-stack, LL host, Eros |
| 10 | `wire_stress_mpa` | estimate | Rock mined per torus (S-type) | +24% / -16% | 2.5 km pair, H host, Eros |
| 11 | `crush_mj_kg` | estimate | Processing energy per torus | -13% / +25% | 400 m pair, LL host, Itokawa |
| 12 | `ep_efficiency` | estimate | Shipping energy per torus | +20% / -14% | 400 m pair, LL host, Itokawa |
| 13 | `yield_wheat` | sourced | People per torus | -7% / +25% | 900 m six-stack, L host, Eros |
| 14 | `hull_frames_ref_mt` | estimate | Rock mined per torus (S-type) | -12% / +19% | 400 m pair, LL host, Itokawa |
| 15 | `radiator_temp_k` | estimate | Ideal heat margin (end-aperture limit / stack heat) | -13% / +15% | 900 m six-stack, L host, Eros |
| 16 | `hub_factory_metal_frac` | guess | Rock mined per torus (S-type) | -8% / +20% | 2.5 km pair, H host, Eros |
| 17 | `diet_kcal` | estimate | People per torus | +14% / -11% | 900 m six-stack, L host, Eros |
| 18 | `metal_wt_H` | sourced | Rock mined per torus (S-type) | +13% / -11% | 2.5 km pair, H host, Eros |
| 19 | `soil_water_vol_frac` | estimate | Shipping energy per torus | -10% / +10% | 400 m pair, LL host, Itokawa |
| 20 | `organics_shipped_t_m2` | guess | Shipping energy per torus | -10% / +10% | 400 m pair, LL host, Itokawa |
| 21 | `farm_planted_frac` | estimate | People per torus | -13% / +6% | 900 m six-stack, L host, Eros |
| 22 | `valley_diet_share` | estimate | People per torus | -7% / +9% | 900 m six-stack, L host, Eros |
| 23 | `c_water_wt` | sourced | C-type per torus | +16% / +0% | 400 m pair, LL host, Itokawa |
| 24 | `lamp_efficacy_umol_j` | sourced | Ideal heat margin (end-aperture limit / stack heat) | -7% / +7% | 900 m six-stack, L host, Eros |
| 25 | `crop_overhead` | estimate | People per torus | +5% / -8% | 900 m six-stack, L host, Eros |
| 26 | `yield_potato` | sourced | People per torus | -5% / +9% | 900 m six-stack, L host, Eros |
| 27 | `farm_delivery` | estimate | Despun array at the site | +9% / -4% | 1.6 km six-stack, LL host, Eros |
| 28 | `hull_frames_exponent` | estimate | Rock mined per torus (S-type) | +7% / -6% | 400 m pair, LL host, Itokawa |
| 29 | `ceiling_delivery` | estimate | Ideal heat margin (end-aperture limit / stack heat) | -8% / +4% | 2.5 km pair, H host, Eros |
| 30 | `yield_soybean` | estimate | People per torus | -5% / +6% | 1.6 km six-stack, LL host, Eros |
| 31 | `yield_lentils` | estimate | People per torus | -5% / +4% | 1.6 km six-stack, LL host, Eros |
| 32 | `c_nitrogen_wt` | sourced | C-type per torus | +4% / -4% | 900 m six-stack, L host, Eros |
| 33 | `other_loads_w_m2` | guess | Despun array at the site | -3% / +5% | 2.5 km pair, H host, Eros |
| 34 | `yield_flax` | estimate | People per torus | -3% / +3% | 2.5 km pair, H host, Eros |
| 35 | `kcal_wheat` | estimate | People per torus | -2% / +2% | 900 m six-stack, L host, Eros |
| 36 | `rock_density` | estimate | Mass per m² of floor | +2% / -1% | 400 m pair, LL host, Itokawa |
| 37 | `kcal_potato` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 38 | `kcal_soybean` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 39 | `yield_berries` | estimate | People per torus | -1% / +1% | 2.5 km pair, H host, Eros |
| 40 | `kcal_lentils` | estimate | People per torus | -1% / +1% | 900 m six-stack, L host, Eros |
| 41 | `kcal_berries` | estimate | People per torus | -1% / +0% | 900 m six-stack, L host, Eros |
| 42 | `yield_greens` | sourced | People per torus | -0% / +1% | 900 m six-stack, L host, Eros |
| 43 | `kcal_flax` | estimate | People per torus | -0% / +0% | 900 m six-stack, L host, Eros |
| 44 | `crawl_space_m` | estimate | Ideal heat margin (end-aperture limit / stack heat) | +0% / -0% | 400 m pair, LL host, Itokawa |
| 45 | `kcal_greens` | estimate | People per torus | -0% / +0% | 1.6 km six-stack, LL host, Eros |
| 46 | `soil_density` | estimate | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 47 | `hub_radius_per_width` | estimate | Ideal heat margin (end-aperture limit / stack heat) | +0% / -0% | 400 m pair, LL host, Itokawa |
| 48 | `regolith_density` | estimate | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |
| 49 | `rock_per_water_shield` | sourced | Mass per m² of floor | +0% / -0% | 400 m pair, LL host, Itokawa |

# Monte Carlo (2000 samples)

Each input drawn independently from a triangular distribution (low, value, high). The spread shows what the chosen ranges imply; it is not a physical confidence interval.

| Output | Unit | 5th percentile | Median | 95th percentile |
|---|---|---|---|---|
| Mass per m² of floor | t/m² | 35.2 | 40.4 | 45.5 |
| Rock mined per torus (S-type) | Mt | 13.7 | 17.2 | 22.1 |
| C-type per torus | Mt | 3.93 | 4.70 | 5.91 |
| Despun array at the site | km² | 1.27 | 1.51 | 1.87 |
| People per torus |  | 1,830 | 2,320 | 2,930 |
| Ideal heat margin (end-aperture limit / stack heat) | × | 1.89 | 2.19 | 2.51 |
| Processing energy per torus | PJ | 6.60 | 8.73 | 11.3 |
| Shipping energy per torus | PJ | 15.7 | 23.7 | 35.9 |
| Processing + shipping per torus | PJ | 24.0 | 32.5 | 45.0 |
| Energy-limited generation time | yr | 4.57 | 6.18 | 8.55 |
