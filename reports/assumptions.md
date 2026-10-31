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
| `lake_floor_frac` | 0.02000 | share of the floor under ponds and streams | 0.01000–0.05000 | guess | small ponds and streams giving the biosphere access to water, not a main feature (design intent, 29 Oct 2026); replaces the fitted lake water (plan §5) |
| `lake_depth_m` | 1.000 | m, mean depth | 0.5000–1.500 | guess | within the 1 m fill, so the jacket is left as it is (§6) |
| `ballast_frac` | 0.0005000 | share of the rim's mass | 0.0001000–0.002000 | guess | unbalanced mass at the rim, as a share of the rim's mass, trimmed by ballast water (rim trains, stores, water moved between valleys; §5e, §12); construction scatter is trimmed with rock |
| `biomass_water_kg_m2` | 10.00 | kg per m2 of floor | 3.000–30.00 | estimate | standing vegetation: temperate woodland ~15-30 kg/m2 of dry biomass, about as much water fresh, on part of the floor (unsourced) |
| `hull_frames_ref_mt` | 0.3000 | Mt at the reference radius | 0.2000–0.4500 | estimate | §5c, hull and frames of a 900 m torus |
| `hull_frames_ref_radius_m` | 900.0 | m | fixed | design | §5c |
| `hull_frames_exponent` | 2.300 | exponent of r | 2.100–2.500 | estimate | §5c, fitted to the 900 m and 1.6 km estimates |
| `hull_min_gauge_frac` | 0.3000 | fraction of the 1 g hull | 0.2000–0.5000 | estimate | §9, hull and frames floored at ~30% of their 1 g mass |
| `plate_stress_mpa` | 300.0 | MPa (working, von Mises) | 200.0–500.0 | guess | §5d used 500 MPa for the first design's ring and 250 MPa for plain carbonyl iron; ~300 MPa is a 690 MPa structural steel at a factor of ~2.3 |
| `skin_min_gauge_m` | 0.01000 | m of steel | 0.005000–0.02000 | estimate | §12, hull at minimum gauge (1 cm per hull): the pressure hull and the outer cell wall |
| `cell_wall_min_gauge_m` | 0.005000 | m of steel | 0.003000–0.01000 | guess | bulkheads and cell walls of the rock jacket at their thinnest |
| `cell_size_m` | 10.00 | m | fixed | design | spacing of the jacket's bulkheads and cell walls, as the chords' anchors (§12) |
| `hub_shell_m` | 0.02000 | m of steel | 0.005000–0.05000 | guess | the shared hub's structural wall (a thin tube of the hub's radius); dynamics_model only |
| `bumper_m` | 0.002000 | m of steel | 0.001000–0.003000 | estimate | §13, thin outer bumper (~1-3 mm) |
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
| `farm_lamp_efficacy_umol_j` | 0 | umol/J at the wall in the farm; 0: as the valley's lamps | fixed | design | design: set by an architecture with different farm lamps (blue + red LEDs) |
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
| `solar_absorptivity` | 0.1500 | fraction | 0.1000–0.3000 | estimate | white radiator paint (AZ-93-like ~0.15 new, degrading towards ~0.3; unsourced) |
| `par_j_per_umol` | 0.2200 | J per umol of light | 0.2000–0.2500 | estimate | energy of visible light per photon, ~0.22 J/umol for a sunlight-like spectrum (unsourced) |
| `coolant_dt_k` | 10.00 | K | 5.000–15.00 | estimate | temperature rise of the coolant across the heat source (design choice to optimise) |
| `coolant_loops_per_torus` | 12.00 | loops | 6.000–24.00 | guess | independent radiator loops per torus or farm ring, one per radiator spoke (guess) |
| `pump_efficiency` | 0.7000 | fraction | 0.5000–0.8000 | estimate | large water pumps (unsourced) |
| `valley_cooling_u` | 7.000 | W/m2K | 3.000–15.00 | estimate | cold ceiling's radiation (~5 W/m2K) and air handling, valley to coolant (unsourced) |
| `crush_mj_kg` | 0.08500 | MJ per kg of S-type rock | 0.05000–0.1500 | estimate | §5e, §10: ~1e15 J for ~12 Mt, ~3e15 J for ~32 Mt |
| `bake_mj_kg` | 1.500 | MJ per kg of C-type | 1.000–2.000 | estimate | §19, C-type processing ~1-2 MJ/kg (unsourced) |
| `organics_shipped_t_m2` | 0.1000 | t per m2 of floor | 0.05000–0.1500 | guess | §15, carbon/organics ~15-50 kt per 900 m torus |
| `ep_exhaust_km_s` | 30.00 | km/s | 20.00–50.00 | estimate | §15, electric propulsion |
| `ep_efficiency` | 0.6000 | fraction | 0.5000–0.7000 | estimate | §15, electric propulsion |
| `electrothermal_exhaust_km_s` | 6.000 | km/s | 4.000–8.000 | estimate | arcjets and microwave electrothermal thrusters on water (unsourced) |
| `electrothermal_efficiency` | 0.3500 | fraction | 0.2500–0.4500 | estimate | arcjets and microwave electrothermal thrusters (unsourced) |
| `mass_driver_efficiency` | 0.5000 | fraction | 0.3000–0.8000 | guess | mass driver as a reaction engine (O'Neill), electricity to jet power (guess) |
| `moe_mj_kg_fe` | 10.00 | MJ of electricity per kg of iron | 7.000–14.00 | estimate | §10, molten-oxide electrolysis: ~5 MJ/kg minimum, ~7-14 with losses |
| `moe_heat_mj_kg_fe` | 17.00 | MJ of furnace heat per kg of iron | 8.000–20.00 | estimate | §10, melting ~8-9 kg of rock per kg of iron at ~2 MJ/kg, partly recovered from the hot slag |
| `electrolysis_mj_kg_water` | 20.00 | MJ of electricity per kg of water split | 16.00–25.00 | estimate | ~15.9 MJ/kg (higher heating value) at 65-100% efficiency (unsourced) |
| `pv_silicon_kg_m2` | 0.4000 | kg of silicon per m2 of array | 0.1000–0.8000 | estimate | wafer cells ~150-200 um thick, with kerf losses; thin cells at the low end (unsourced) |
| `other_vitamins_t` | 50.00 | t per 900 m torus, scaled with the floor | 10.00–200.0 | guess | electronics, dopants, catalysts, cesium, microbes and seeds (§10, §13): kilograms to tonnes each (guess) |
| `kcal_per_l_o2` | 4.850 | kcal of food per litre of O2 (STP) | 4.700–5.000 | estimate | indirect calorimetry, mixed diet (general physiology, unsourced) |
| `respiratory_quotient` | 0.8700 | mol CO2 per mol O2 | 0.8000–0.9500 | estimate | mixed diet (general physiology, unsourced) |
| `harvest_index` | 0.5000 | edible share of the carbon the crops fix | 0.4000–0.6000 | estimate | wheat, soybean and potato in controlled environments (~0.4-0.7; unsourced) |
| `organics_carbon_frac` | 0.5000 | kg C per kg of imported organics | 0.4000–0.5800 | estimate | soil organic matter ~50-58% carbon (unsourced) |
| `soil_labile_frac` | 0.3000 | share of the soil's organic carbon that decays fast | 0.1000–0.5000 | guess | fresh compost and residues (guess) |
| `soil_labile_turnover_yr` | 1.000 | years | 0.5000–3.000 | guess | fresh organic matter in warm moist soil (guess) |
| `soil_stable_turnover_yr` | 30.00 | years | 10.00–100.0 | guess | humus (guess) |
| `humification_frac` | 0.2000 | share of decaying labile carbon that becomes humus | 0.1000–0.3000 | guess | (guess) |
| `valley_biomass_start` | 1.000 | kg C per m2 of floor, as planted | 0.2000–3.000 | guess | young plantings (guess) |
| `valley_biomass_max` | 8.000 | kg C per m2 of floor, grown | 4.000–15.00 | guess | temperate woodland ~10-20 kg C/m2 with roots, less under a dim sky and on part of the floor (guess) |
| `valley_growth_rate` | 0.2000 | per year (logistic) | 0.1000–0.4000 | guess | woodland reaching most of its biomass in ~20-40 years (guess) |
| `litter_turnover_yr` | 8.000 | years (standing biomass shed as litter) | 4.000–20.00 | guess | leaves yearly, wood over decades (guess) |
| `farm_co2_pa` | 100.0 | Pa of CO2 at the crops | 60.00–150.0 | estimate | §13: ~1,000 ppm at sea level, as in NASA's growth chambers |
| `co2_half_saturation_pa` | 35.00 | Pa | 25.00–50.00 | estimate | C3 canopy response: ~+30% from 400 to 800 ppm (unsourced) |
| `duct_exchange_m3_s` | 400.0 | m3/s of air between the valleys and the farm ring, per torus | 100.0–1,000 | guess | ducts along the hub (§13; to size) |
| `co2_limit_pa` | 500.0 | Pa | 300.0–700.0 | estimate | ~5,000 ppm at sea level, the usual long-term exposure limit (unsourced) |
| `o2_min_kpa` | 17.00 | kPa | 16.00–19.00 | estimate | ~1,800 m altitude's O2 partial pressure (unsourced) |
| `leak_frac_yr` | 0.001000 | share of the air lost per year | 0.0001000–0.01000 | guess | seals, docking, airlocks (guess) |
| `o2_regen_mj_kg` | 25.00 | MJ per kg of O2 recovered from CO2 | 15.00–40.00 | estimate | CO2 -> C + O2 needs ~12 MJ/kg of O2; Bosch or Sabatier with electrolysis at ~50% (unsourced) |
| `pipe_coupling` | 0.8500 | share of the lamp's light entering the pipe inside its acceptance cone | 0.7500–0.9200 | guess | sulfur bulb in a reflector aimed into the pipe (guess) |
| `pipe_diameter_m` | 0.2500 | m | fixed | design | §13, ~25 cm prism light pipes |
| `pipe_length_m` | 40.00 | m, fed from both ends | fixed | design | §13, a pair of lamps per ~40 m pipe |
| `pipe_w_per_m` | 300.0 | W of lamp electricity per m of pipe | fixed | design | §13, a pair of ~6 kW lamps per 40 m pipe |
| `pipe_cone_deg` | 27.60 | degrees, half-angle guided by the prism film | fixed | estimate | acrylic prism film (n ~1.49): total internal reflection within ~27.6° of the axis (Whitehead et al. 1982, recalled) |
| `film_loss_per_reflection` | 0.01000 | share absorbed per reflection | 0.005000–0.02000 | estimate | prism film absorption and imperfections (unsourced) |
| `extractor_efficiency` | 0.8500 | share of the light scattered by the extractor that leaves the pipe | 0.7500–0.9500 | guess | white scattering strip inside the pipe (guess) |
| `extractor_max_frac` | 0.3000 | largest share of reflections landing on the extractor | fixed | design | extractor up to about a third of the circumference (design) |
| `pipe_end_return` | 0.5000 | share of the light reaching a pipe's far end that the other lamp's reflector sends back | 0.2000–0.8000 | guess | guess |
| `pipe_emit_arc_deg` | 180.0 | degrees of the pipe's circumference that glow, centred downward | fixed | design | extractor on the top, light leaving through the bottom (design) |
| `pipe_albedo` | 0.8000 | share of the light falling on a pipe from outside that it sends back out | 0.6000–0.9000 | guess | prism film reflecting much of it, the rest re-guided (guess) |
| `mgo_reflectance` | 0.9500 | fraction | 0.9000–0.9800 | estimate | §13, magnesium oxide ~95-98% fresh; less with dust and age |
| `diffuser_transmittance` | 0.6000 | fraction, diffuse | 0.4500–0.7500 | estimate | opal or sandblasted patterned glass, strongly diffusing (unsourced) |
| `diffuser_absorptance` | 0.05000 | fraction (the rest is reflected, diffusely) | 0.02000–0.1000 | estimate | low-iron glass with scattering (unsourced) |
| `diffuser_gap_m` | 0.7500 | m from the pipes' bottom to the diffuser | fixed | design | §13, about one pipe-width (~0.5-1 m) |
| `valley_day_h` | 12.00 | hours the sky is lit | fixed | design | §13, a 12 h day |
| `floor_albedo` | 0.1000 | PAR reflectance of the valley's floor and plants | 0.05000–0.2000 | estimate | vegetation reflects ~5-10% of PAR (unsourced) |
| `canopy_reflectance` | 0.08000 | PAR reflectance of a crop canopy | 0.05000–0.1200 | estimate | unsourced |
| `aisle_reflectance` | 0.5000 | fraction, diffuse | 0.2000–0.9000 | guess | aisle floors, painted (guess) |
| `canopy_height_m` | 0.6000 | m above the tier's floor | 0.3000–1.000 | estimate | dwarf wheat, soybean, potatoes (§13) |
| `farm_pipe_gap_m` | 0.3000 | m from the canopy's top to the pipes' bottom | fixed | design | §13, pipes just above the canopy |
| `bed_width_m` | 2.400 | m | fixed | design | beds and aisles for 80% planted (§13) |
| `aisle_width_m` | 0.6000 | m | fixed | design | walking aisles, 80% planted (§13) |
| `tier_clear_m` | 2.200 | m from a tier's floor to the underside of the next | fixed | design | §13, 2.5 m floor to floor less ~0.3 m of floor |
| `farm_photoperiod_h` | 16.00 | hours a zone is lit, on average | 12.00–20.00 | estimate | §13, day lengths by crop (estimate) |
| `luminaire_efficiency` | 0.8800 | share of a lamp's light leaving its reflector | 0.8000–0.9300 | guess | a ~1 kW sulfur lamp in a small specular reflector (guess) |
| `luminaire_albedo` | 0.6000 | share of the light falling on a lamp and reflector that it sends back | 0.4000–0.8000 | guess | guess |
| `lamp_power_w` | 1,000 | W per lamp, lamps straight in the light box | fixed | design | §13, ~1 kW sulfur lamps |
| `lamp_spacing_m` | 1.500 | m between lamps along a row | fixed | design | design |
| `sector_efficacy_umol_j` | 1.750 | umol/J at the wall, sulfur bulbs behind 915 MHz sector plants | 1.600–1.800 | estimate | §13: Fusion's bulbs >2 umol per J of microwaves, behind ~85% sources: ~1.7-1.8 |
| `waveguide_efficiency` | 0.9000 | share of a sector plant's microwaves reaching the bulbs | 0.8000–0.9500 | guess | waveguide runs of a few hundred metres (guess) |
| `led_efficacy_umol_j` | 3.000 | umol/J at the wall, white LEDs | 2.700–3.500 | estimate | §13: ~3.4 umol/J (white + red) at the best (Kusuma et al. 2020) |
| `led_fixture_efficiency` | 0.9500 | share of the LEDs' light leaving the fixture | 0.9000–0.9700 | estimate | estimate |
| `led_w_per_m` | 200.0 | W per m of LED strip | fixed | design | design |
| `led_farm_efficacy_umol_j` | 3.600 | umol/J at the wall, blue + red LEDs | 3.200–4.100 | estimate | best fixtures ~3.7 (DLC list, 2022) to 4.1 (Hortilux NXTLED, claimed); Kusuma et al. 2020: ~4.1 potential |
| `led_farm_red_share` | 0.8000 | share of the farm LEDs' electricity driving red (660 nm) dies | 0.7000–0.9000 | guess | ~10-20% blue photons for crops (guess) |
| `led_die_w_mm2` | 0.3000 | W of electricity per mm2 of LED die | 0.1500–1.000 | estimate | mid-power dies driven gently for efficacy (~0.2-0.5 W on ~1 mm2) to high-power at ~1 W/mm2 (estimate) |
| `led_wafer_yield` | 0.7000 | share of the epitaxial wafer ending as working dies | 0.5000–0.8500 | guess | edge exclusion, streets and binning (guess) |
| `mocvd_utilization` | 0.2500 | share of the gallium fed to the reactor ending in the film | 0.1500–0.4000 | estimate | ~25% for conventional MOCVD (Atomic Precision Systems, NCCAVS 2019, a vendor comparison) |
| `mocvd_ammonia_kg_m2` | 100.0 | kg of ammonia per m2 of GaN wafer grown | 50.00–200.0 | estimate | ~50 slpm for ~5 h a run (NCCAVS 2019) over a ~0.1 m2 batch (estimate) |
| `led_phosphor_g_w` | 0.003000 | g of YAG:Ce phosphor per W of white LED | 0.001500–0.006000 | guess | a few mg per mid-power package (guess) |
| `led_life_h` | 50,000 | hours to 70% output | 30,000–100,000 | estimate | §13 (L70 ratings, not yet sourced) |
| `dose_limit_msv_yr` | 20.00 | mSv per year, dose equivalent | fixed | design | §5b, Globus & Strout (2017): the general population's limit, at solar minimum |
| `solar_min_phi_mv` | 300.0 | MV, force-field modulation potential | 250.0–450.0 | estimate | deep solar minimum (2009-2010) in the Usoskin et al. (2005) convention, recalled |
| `solar_max_phi_mv` | 1,000 | MV, force-field modulation potential | fixed | estimate | solar maximum, recalled |
| `leading_nucleon_z` | 0.3000 | spectrum-weighted moment Z_NN of the leading nucleon | 0.2500–0.3500 | estimate | nucleon attenuation ~120 g/cm2 in air (Gaisser, Cosmic Rays and Particle Physics, recalled) |
| `cascade_nucleons_coeff` | 0.5000 | cascade nucleons per collision per A^(1/3) of the target | 0.3000–0.8000 | guess | intranuclear cascade multiplicity (guess) |
| `cascade_nucleon_mev` | 100.0 | MeV, mean energy of cascade nucleons | 60.00–150.0 | guess | guess |
| `evaporation_neutrons_coeff` | 0.2000 | evaporation neutrons per collision per A^0.6 of the target | 0.1000–0.3000 | guess | ~1 for oxygen, ~2 for iron (guess) |
| `knockout_alphas_coeff` | 0.1000 | light ions (d, t, 3He, alpha) knocked out per collision per A^(1/3) of the target | 0.05000–0.2000 | guess | guess |
| `fast_neutron_dose_psv_cm2` | 350.0 | pSv cm2, fluence to dose equivalent, 0.1-20 MeV group | 250.0–420.0 | estimate | ICRP 74: ~90 at 0.1 MeV, ~420 at 1-10 MeV (recalled) |
| `stability_margin` | 0.2000 | required I_axis / I_transverse - 1 | fixed | design | §11, 20% margin |
