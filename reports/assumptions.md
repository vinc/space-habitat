# Assumptions

| Name | Value | Unit | Range | Status | Source |
|---|---|---|---|---|---|
| `width_ratio` | 16.00 | r/w | fixed | design | §2b, adopted design rule |
| `hub_radius_per_width` | 1.080 | hub radius / tube width | 1.000–1.200 | estimate | §12, large hub (~60 / 110 / 170 m) |
| `farm_ring_radius_frac` | 0.4000 | r | fixed | design | §13, farm rings at ~0.4 r |
| `farm_ring_width_frac` | 0.9000 | w | fixed | design | §13, farm ring width ~0.9 of the tube width |
| `farm_planted_frac` | 0.8000 | fraction of each tier | 0.7000–0.8500 | estimate | §13, ~80% of each tier planted |
| `farm_ring_height_m` | 8.500 | m | fixed | design | §13, three tiers ~2.5 m apart, ~8.5 m in all |
| `farm_ring_gap_m` | 10.00 | m | fixed | design | farm section: clear gap between neighbouring farm rings (as between tori) |
| `farm_section_gap_m` | 50.00 | m | fixed | design | farm section: clear gap between the last torus envelope and the first farm ring |
| `radiator_inner_frac` | 0.4000 | r | fixed | design | main section: radiator panels on the spokes from ~0.4 r out to the tori's envelopes (the stretch the in-plane farm ring used to bound) |
| `farm_radiator_outer_frac` | 1.000 | r | 0.6000–1.400 | guess | farm section: radiator panels on the farm spokes from the farm rings out to this radius (a guess, to model) |
| `farm_tiers_built` | 3.000 | tiers | fixed | design | §13, all three tiers built with the torus |
| `pressure_kpa` | 70.00 | kPa | fixed | design | §3c, design atmosphere |
| `o2_partial_kpa` | 20.27 | kPa | fixed | design | §3c, sea-level O2 partial pressure (20% of 101.325 kPa) |
| `farm_pressure_kpa` | 70.00 | kPa | 30.00–70.00 | guess | §13, the farm's own atmosphere (to decide): lower pressure possible; the valley's 70 kPa taken (conservative) |
| `air_temperature_k` | 288.1 | K | fixed | design | §3b |
| `shield_areal_t_m2` | 11.00 | t/m2 | 9.000–13.00 | sourced | §5b, Globus & Strout (2017): ~11 t/m2 of rock for 20 mSv/yr; plan §2 checks it |
| `rock_per_water_shield` | 1.571 | t rock / t water | 1.400–1.750 | sourced | §6, Globus: 11 t/m2 of regolith ~ 7 t/m2 of water |
| `rock_density` | 2.000 | t/m3 | 1.800–2.200 | estimate | §5e, compacted crushed rock: ~5.5 m for 11 t/m2 |
| `crawl_space_m` | 1.500 | m | 1.000–2.000 | estimate | §13, double outer skin: empty crawl space of ~1-2 m outside the rock cells |
| `fill_depth_m` | 1.000 | m | fixed | design | §6 |
| `fill_soil_frac` | 0.5000 | fraction of the fill depth | fixed | design | §10, 0.5 m soil + 0.5 m regolith |
| `soil_density` | 1.600 | t/m3 | 1.300–1.800 | estimate | §6, moist agricultural soil (unsourced) |
| `regolith_density` | 1.800 | t/m3 | 1.600–2.000 | estimate | §6, regolith / mine tailings (unsourced) |
| `soil_water_vol_frac` | 0.2500 | m3 water / m3 soil | 0.1500–0.3500 | estimate | §6, ~25% water by volume |
| `lake_water_t_m2` | 0.2500 | t per m2 of floor | 0.1000–0.5000 | guess | fitted so that water needed matches §7 (~0.15 / 0.4 / 0.9 Mt); the notes give no breakdown |
| `hull_frames_ref_mt` | 0.3000 | Mt at the reference radius | 0.2000–0.4500 | estimate | §5c, hull and frames of a 900 m torus |
| `hull_frames_ref_radius_m` | 900.0 | m | fixed | design | §5c |
| `hull_frames_exponent` | 2.300 | exponent of r | 2.100–2.500 | estimate | §5c, fitted to the 900 m and 1.6 km estimates |
| `hull_min_gauge_frac` | 0.3000 | fraction of the 1 g hull | 0.2000–0.5000 | estimate | §9, hull and frames floored at ~30% of their 1 g mass |
| `wire_stress_mpa` | 1,000 | MPa (working) | 800.0–1,200 | estimate | structure_model/README.md: 1,770 MPa bridge wire at SF 2.2 to ~1 mm wire (~2.25 GPa) at SF ~1.9; 1 GPa is SF ~1.96 on 1,960 MPa wire |
| `steel_density` | 7,900 | kg/m3 | fixed | sourced | §5a |
| `hub_factory_metal_frac` | 0.2500 | fraction of torus steel | 0.1500–0.5000 | guess | §10, hub, dock and factory (guess): 1.1 -> 1.4 Mt, 5.8 -> 7.3 Mt, 22 -> 27 Mt |
| `spinup_exhaust_km_s` | 3.000 | km/s | 2.000–4.000 | estimate | §7, water thrusters |
| `farm_shell_m` | 0.01000 | m of steel | 0.005000–0.02000 | guess | §13, farm ring mass (rough) |
| `farm_growing_kg_m2` | 100.0 | kg per m2 planted | 50.00–200.0 | guess | §13, growing systems (rough) |
| `array_kg_m2` | 3.000 | kg/m2 | 2.000–5.000 | estimate | §13, thin-film panels plus structure |
| `radiator_kg_m2` | 5.000 | kg per m2 of two-sided panel | 3.000–10.00 | estimate | §13, heat rejection |
| `metal_wt_H` | 0.1700 | free metal, wt fraction | 0.1500–0.1900 | sourced | §10, ordinary-chondrite review: ~8.4 vol% |
| `metal_wt_L` | 0.09000 | free metal, wt fraction | 0.07000–0.1100 | sourced | §10, ~4.1 vol% |
| `metal_wt_LL` | 0.04500 | free metal, wt fraction | 0.03500–0.05500 | sourced | §10, ~2 vol% |
| `s_bulk_density` | 2.000 | t/m3 | 1.600–2.400 | estimate | §10, S-type rubble pile |
| `c_bulk_density` | 1.200 | t/m3 | 1.100–1.300 | sourced | §10, Bennu-like |
| `c_nitrogen_wt` | 0.002400 | wt fraction | 0.002300–0.002500 | sourced | §10, Bennu samples ~0.23-0.25 wt% N (Glavin et al. 2025) |
| `nitrogen_recovery` | 0.7000 | fraction | 0.5000–0.9000 | estimate | §10, §19 |
| `c_water_wt` | 0.06400 | wt fraction | 0.05000–0.08000 | sourced | §10, 0.71 wt% H at Bennu's surface (Praet et al. 2021) |
| `c_carbon_wt` | 0.04500 | wt fraction | 0.04000–0.05000 | sourced | §10, Bennu samples |
| `valley_light_mol` | 15.00 | mol/m2/day on the floor | fixed | design | §13, light-box ceiling sizing |
| `ceiling_delivery` | 0.7500 | fraction | 0.6500–0.8000 | estimate | §13, light box: ~20-30% ceiling losses (to verify, plan §6) |
| `lamp_efficacy_umol_j` | 1.400 | umol/J at the wall | 1.300–1.500 | sourced | §13, sulfur lamps (Maclennan et al. 1994); 915 MHz sources would give ~1.75 |
| `farm_delivery` | 0.8500 | fraction | 0.7500–0.9000 | estimate | §13, light pipes just above the canopy (estimate) |
| `other_loads_w_m2` | 15.00 | W per m2 of floor | 10.00–25.00 | guess | §19, ~5 MW per 900 m torus, ~15 MW per 1.6 km torus (guess) |
| `pv_efficiency` | 0.2500 | fraction | 0.1800–0.2800 | estimate | §13, 25% assumed; ~18-22% in the concentrator comparison |
| `solar_constant_w_m2` | 1,361 | W/m2 at 1 AU | fixed | sourced | standard value |
| `locked_output_frac` | 0.6366 | fraction (2/pi) | fixed | design | §13, a locked two-sided array averages 2/pi |
| `seasonal_sky_frac` | 0.5000 | fraction of the normal sky at aphelion | fixed | design | §15, seasonal sky |
| `diet_kcal` | 2,500 | kcal per person per day | 2,200–2,800 | estimate | §13, working diet |
| `valley_diet_share` | 0.07000 | fraction of calories | 0–0.1500 | estimate | §13, permaculture and food forest |
| `crop_overhead` | 0.1000 | fraction | 0.05000–0.2000 | estimate | §13, seedlings and turnaround |
| `crop_light_mol` | 36.00 | mol/m2/day on the crops | 30.00–45.00 | estimate | §13, average over crops and day lengths |
| `share_potato` | 0.3300 | fraction of calories | fixed | design | §13, working diet |
| `share_wheat` | 0.2800 | fraction of calories | fixed | design | §13, working diet |
| `share_soybean` | 0.1500 | fraction of calories | fixed | design | §13, working diet |
| `share_lentils` | 0.07000 | fraction of calories | fixed | design | §13, working diet |
| `share_berries` | 0.05000 | fraction of calories | fixed | design | §13, working diet |
| `share_flax` | 0.03000 | fraction of calories | fixed | design | §13, working diet |
| `share_greens` | 0.02000 | fraction of calories | fixed | design | §13, working diet |
| `yield_potato` | 0.3700 | g/mol | 0.3000–0.6000 | sourced | §13, Tibbitts et al. (best ~0.60) |
| `yield_wheat` | 0.1800 | g/mol | 0.1500–0.4000 | sourced | §13, Bugbee & Salisbury (best ~0.40) |
| `yield_soybean` | 0.1500 | g/mol | 0.1200–0.2200 | estimate | §13 (unsourced estimate) |
| `yield_lentils` | 0.1500 | g/mol | 0.1000–0.2200 | estimate | §13 (unsourced estimate) |
| `yield_berries` | 0.2500 | g/mol | 0.2000–0.3000 | estimate | §13 (unsourced estimate) |
| `yield_flax` | 0.07000 | g/mol | 0.05000–0.1200 | estimate | §13 (unsourced estimate) |
| `yield_greens` | 0.4300 | g/mol | 0.3500–0.7400 | sourced | §13, Jin et al. 2023 (best ~0.74) |
| `kcal_potato` | 3.700 | kcal/g dry | 3.500–3.900 | estimate | §13, implied by ~600 mol per person |
| `kcal_wheat` | 3.600 | kcal/g dry | 3.400–3.800 | estimate | §13, implied by ~1,080 mol per person |
| `kcal_soybean` | 4.450 | kcal/g dry | 4.200–4.700 | estimate | §13, implied by ~560 mol per person |
| `kcal_lentils` | 3.650 | kcal/g dry | 3.400–3.900 | estimate | §13, implied by ~320 mol per person |
| `kcal_berries` | 3.300 | kcal/g dry | 3.000–3.600 | estimate | §13, implied by ~150 mol per person |
| `kcal_flax` | 5.600 | kcal/g dry | 5.200–5.900 | estimate | §13, implied by ~190 mol per person |
| `kcal_greens` | 2.900 | kcal/g dry | 2.500–3.300 | estimate | §13, implied by ~40 mol per person |
| `radiator_emissivity` | 0.9000 | fraction | 0.7900–0.9300 | sourced | AZ-93 white paint 0.91 +/- 0.02; silvered Teflon OSR ~0.79 (thermal control coating patent US 10,100,203) |
| `radiator_temp_k` | 285.0 | K | 275.0–295.0 | estimate | §13, passive loops colder than the habitat |
| `crush_mj_kg` | 0.08500 | MJ per kg of S-type rock | 0.05000–0.1500 | estimate | §5e, §10: ~1e15 J for ~12 Mt, ~3e15 J for ~32 Mt |
| `bake_mj_kg` | 1.500 | MJ per kg of C-type | 1.000–2.000 | estimate | §19, C-type processing ~1-2 MJ/kg (unsourced) |
| `organics_shipped_t_m2` | 0.1000 | t per m2 of floor | 0.05000–0.1500 | guess | §15, carbon/organics ~15-50 kt per 900 m torus |
| `ep_exhaust_km_s` | 30.00 | km/s | 20.00–50.00 | estimate | §15, electric propulsion |
| `ep_efficiency` | 0.6000 | fraction | 0.5000–0.7000 | estimate | §15, electric propulsion |
| `stability_margin` | 0.2000 | required I_axis / I_transverse - 1 | fixed | design | §11, 20% margin |
