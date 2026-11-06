# Asteroid host–supplier networks

A first screening study, 31 October 2026. Extends the Eros reference to other silicate near-Earth hosts. The result is a shortlist for investigation, not a verified resource inventory or an executable transport plan.

## Settlement ladder (working scenario)

Each step goes to a new host and is a little larger than the last, so every host is chosen for the step it serves rather than ranked against Eros. The hosts fall into three size groups below Eros. Later habitats move on to the next group once a host's inventory is committed, by which time the smaller and darker bodies will be better characterised. This is the project's plan, not a universal optimum.

| Step | Habitat | Host group | Candidate hosts | Supply | What it proves | Main reservation |
|---|---|---|---|---|---|---|
| 1 | One 400 m torus, no farm tiers and no ecosystem: a synthetic environment for a small crew | 0.3–0.6 km | Apophis (post-2029 orbit; crewed round trip from 6.05 km/s) or Itokawa (from 9.41 km/s) | ~20 kt of volatiles per torus (~0.7 kt of it N₂): Ryugu (sampled) reaches Apophis at 5.6 km/s; Itokawa's sampled routes exceed the 6 km/s cutoff (Ryugu 6.3 km/s), its dark candidates don't | Rock jacket and double skin, cable spokes, despun array, nitrogen supply and life support, the factory chain, 1.5 rpm gravity; mining and controlling a potentially hazardous asteroid | A day–night cycle, if kept, leaves the power load unbalanced; Apophis's surface after its 2029 flyby is still to be seen |
| 2 | A 400 m pair, again without farms or ecosystem | 0.3–0.6 km | The other of Apophis and Itokawa; alternatives: Torifune, 1999 ND43, 1999 YB and 2001 QQ142 (Bennu within the cutoff for the last three), 2000 EX106, 2002 AA, 1991 BN | As step 1 | The co-rotating stack, the pair rule and the first build by an existing habitat's factory | Thermal-model sizes cut Torifune to 0.38 km, 2002 AA to 0.32 and 1991 BN to 0.29 (each ~1–2 such tori); 1999 YB, 1999 ND43 and 2001 QQ142 are still sized from H |
| 3 | One 900 m torus, then a 900 m pair, then a pair with farms | 0.8–1.0 km | Didymos, 1991 VH, Yuliya (0.77 km), Norwan, Bacchus | Bennu for Didymos (5.2 km/s) and Bacchus (3.9 km/s); dark candidates only for 1991 VH, Yuliya and Norwan | The full-size valley and, last, the farm rings and ecosystem | A 900 m torus needs ~32 Mt of LL rock: these hosts hold ~14–35 tori each; Didymos spins at the limit for loose material at 2 t/m³ and 1991 VH is a fast-rotating binary |
| 4 | 900 m and 1.6 km stacks with farms | ~2–2.5 km | Anteros first; Geographos as the alternative | Anteros: Ryugu at 5.3 km/s (sampled, within the cutoff) and dark candidates from 3.65 km/s; Geographos: dark candidates only, no sampled supplier below the 6 km/s cutoff | Multi-torus stacks at a scale that can still be visited and supplied from a mid-sized host | Anteros spins in 2.87 h (spin ÷ gravity ~0.66 at its equator); Geographos is the costliest host to reach from Earth (10.4 km/s, against 6.5 for Anteros) |
| 5 | The first large habitat: 1.6 km six-stacks | Eros | Eros | Ryugu and Bennu: the only measured nitrogen, enough for about two six-stacks at 70% recovery | The archipelago's main island | Routes to Ryugu and Bennu cost 4.5–5.9 km/s with up to 7.5 years between selected arrivals; their inventory can't be counted again for other hosts |

The 400 m tori never carry farm tiers or an ecosystem; nor do the first 900 m torus and pair: farms start with the next 900 m pair. The silicate NEAs between this size and Eros (Ivar, Eric, Sisyphus) and Ganymed above it fail the host orbit filter; the [evidence audit](asteroid-evidence.md) lists them and why. Apophis is used only on its post-2029 orbit. The torus counts below are material scenarios with every row's whole asteroid accessible; recovery and access losses reduce them.

## What was searched

The JPL SBDB query returned 327 asteroids with a recorded spectral classification. The stated cuts retained 18 hosts: S-complex/Q, or L/K silicate candidates, with q > 0.7 AU, Q < 2.5 AU, eccentricity < 0.4, inclination < 15° and H < 20; the existing reference hosts are retained explicitly. This is limited by SBDB's sparse taxonomy coverage, not a census of every potentially suitable NEO. Spectral L does not mean L ordinary chondrite. Differentiated objects and unclassified metal-rich hosts are outside this search.

Each host was screened against the existing 365 C-complex/dark candidates (snapshot 30 October 2026). The first grid used 30° departure/arrival true-anomaly steps and 60–720-day flights in 60-day steps; the best 18 per host were screened again at 15°. The best six were refined with the existing 10° grid and eight-seed pattern search, as were Bennu, Ryugu and the two best screened C-complex spectral candidates. Rounded supplier elements are adequate for screening but not final mission design. Host elements were fetched at full precision; Apophis uses Horizons' post-flyby orbit at 1 January 2030 instead of its current pre-2029 orbit. Grid screening can miss narrow minima: these are the best solutions found, not certified global minima.

The dated stage uses JPL Horizons' integrated states, every ten days from 2027 to 2077, interpolated using the existing cubic Hermite method. Departure dates span 2028–2072 in five-day steps; flights span 60–900 days in ten-day steps and are refined while keeping those bounds. Transfers are prograde, zero-revolution, two-impulse rendezvous. Both acceleration and braking are charged. Earth departure figures are heliocentric rendezvous costs: launch, Earth escape, capture and the spacecraft's mass are additional.

## Host comparison

Compare the columns rather than one weighted score. Array × is Q²: panel area relative to the same constant load at 1 AU, sized at aphelion. Seasonal ratio is perihelion/aphelion sunlight, not a prediction of interior temperature. Tori are complete 900 m or 1.6 km designs with three farm tiers; capacity uses the existing free-metal/shield budget, including the hub/factory allowance. LL/L capacities are material scenarios unless composition is established. They assume the entire asteroid is accessible and the model's assumed metal is recovered.

| Host | Spectral record | D km | Year yr | Sunlight range × Earth | Seasonal ratio | Array × | 900 m tori LL / L | 1.6 km tori LL / L | Lowest phase-free Δv found |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| 137799 (1999 YB) | Sq | 0.491* | 1.52 | 0.50–0.67 | 1.35 | 2.02 | 3.8 / 7.5 | 0.7 / 1.5 | 4.42 km/s |
| 35107 (1991 VH) | Sk | 0.914† | 1.21 | 0.59–1.06 | 1.78 | 1.69 | 24.4 / 48.7 | 4.8 / 9.5 | 2.41 km/s |
| 99942 Apophis (post-2029) | Sq | 0.34† | 1.16 | 0.58–1.25 | 2.15 | 1.72 | 1.3 / 2.5 | 0.2 / 0.5 | 3.43 km/s |
| 98943 Torifune (2001 CC21) | L | 0.383† | 1.05 | 0.63–1.54 | 2.44 | 1.58 | 1.8 / 3.6 | 0.4 / 0.7 | 2.84 km/s |
| 433 Eros (A898 PA) | S/S | 17.6† | 1.76 | 0.31–0.78 | 2.48 | 3.18 | 203742.0 / 407484.0 | 39911.6 / 79823.1 | 3.16 km/s |
| 15745 Yuliya (1991 PM5) | S | 0.77† | 2.26 | 0.21–0.61 | 2.84 | 4.66 | 14.6 / 29.1 | 2.9 / 5.7 | 3.26 km/s |
| 1943 Anteros (1973 EC) | L/S | 2.31† | 1.71 | 0.31–0.88 | 2.85 | 3.23 | 390.8 / 781.5 | 76.5 / 153.1 | 3.64 km/s |
| 22099 (2000 EX106) | S: | 0.579† | 1.16 | 0.50–1.57 | 3.11 | 1.99 | 6.2 / 12.4 | 1.2 / 2.4 | 2.65 km/s |
| 25143 Itokawa (1998 SF36) | S(IV) | 0.326† | 1.52 | 0.35–1.10 | 3.16 | 2.87 | 1.0 / 1.9 | 0.2 / 0.4 | 3.87 km/s |
| 302311 (2002 AA) | Sq | 0.32† | 1.23 | 0.45–1.56 | 3.48 | 2.23 | 1.0 / 2.1 | 0.2 / 0.4 | 3.76 km/s |
| 139622 (2001 QQ142) | Sq | 0.563* | 1.69 | 0.29–1.04 | 3.61 | 3.46 | 5.7 / 11.4 | 1.1 / 2.2 | 1.28 km/s |
| 36017 (1999 ND43) | Sl | 0.384* | 1.88 | 0.25–0.92 | 3.67 | 4.01 | 1.8 / 3.6 | 0.4 / 0.7 | 3.27 km/s |
| 7480 Norwan (1994 PC) | S | 0.988* | 1.96 | 0.23–0.87 | 3.72 | 4.26 | 30.8 / 61.5 | 6.0 / 12.0 | 3.10 km/s |
| 1620 Geographos (1951 RA) | S/S | 2.44† | 1.39 | 0.36–1.46 | 4.04 | 2.77 | 464.1 / 928.2 | 90.9 / 181.8 | 3.43 km/s |
| 2063 Bacchus (1977 HB) | Sq | 1.03† | 1.12 | 0.47–2.03 | 4.30 | 2.11 | 34.9 / 69.7 | 6.8 / 13.7 | 3.87 km/s |
| 189040 (2000 MU1) | S | 0.294* | 1.61 | 0.28–1.39 | 5.01 | 3.60 | 0.8 / 1.6 | 0.2 / 0.3 | 2.83 km/s |
| 65803 Didymos (1996 GT) | S | 0.761† | 2.11 | 0.19–0.97 | 5.03 | 5.16 | 14.1 / 28.1 | 2.8 / 5.5 | 3.80 km/s |
| 152560 (1991 BN) | Q | 0.29† | 1.73 | 0.25–1.33 | 5.40 | 4.07 | 0.8 / 1.6 | 0.2 / 0.3 | 3.54 km/s |

† SsODNet's best estimate (thermal model, radar or spacecraft; `logistics_model/data/network_physical.json`), which replaces the SBDB catalogue size; unmarked sizes are SBDB's. * Diameter estimated from H at an assumed albedo of 0.23. These are not measured sizes. Mass uses measured GM where present (notably Eros and Itokawa); otherwise it uses diameter and 2 t/m³. For H-only sizes, albedos 0.1–0.4 change mass to about 0.44–3.49× the tabulated proxy, before density uncertainty. For a thermally modelled diameter, even a small formal error may exclude substantial model uncertainty.

Central-estimate Pareto front (smaller array, smaller best Δv, larger LL inventory; the seasonal ratio is not an axis, since the array is sized at aphelion and the perihelion surplus goes to industry): 433 Eros (A898 PA); 1620 Geographos (1951 RA); 2063 Bacchus (1977 HB); 7480 Norwan (1994 PC); 35107 (1991 VH); 98943 Torifune (2001 CC21); 139622 (2001 QQ142). This front ignores evidence quality and is not robust to uncertain sizes/compositions. The dated stage covers it plus the named reference and ladder hosts: 137799 (1999 YB), 1943 Anteros (1973 EC), 65803 Didymos (1996 GT), 25143 Itokawa (1998 SF36), 99942 Apophis (post-2029), 15745 Yuliya (1991 PM5), 302311 (2002 AA), 36017 (1999 ND43), 152560 (1991 BN), 22099 (2000 EX106).

## Dated host–supplier routes

All routes use the same 6 km/s service cutoff for comparison; it is a study choice, not an engineering limit. A retained opportunity is a refined local minimum, with no two departures within 120 days. The gap is the largest spacing between these selected arrival opportunities, including the beginning and end of the 2028–2072 horizon. It is not a continuous no-service interval: departures away from minima may also be usable.

| Host | Supplier | Composition evidence | Best Δv km/s | Departure | Flight days | Retained ≤6 km/s opportunities | Largest selected-arrival gap yr |
|---|---|---|---:|---|---:|---:|---:|
| 433 Eros (A898 PA) | (2015 DX198) | dark only; N unknown | 3.19 | 2071-03-02 | 393 | 17 | 8.0 |
| 433 Eros (A898 PA) | 275611 (1999 XX262) | B spectra; tentative Ch feature | 3.91 | 2067-11-05 | 404 | 24 | 11.5 |
| 433 Eros (A898 PA) | (2002 BM26) | P/X spectrum; N unknown | 4.00 | 2065-09-21 | 386 | 11 | 8.2 |
| 433 Eros (A898 PA) | 162173 Ryugu (1999 JU3) | sample return | 4.52 | 2061-07-21 | 318 | 10 | 15.0 |
| 433 Eros (A898 PA) | 101955 Bennu (1999 RQ36) | sample return | 5.90 | 2049-03-02 | 174 | 1 | 22.4 |
| 1620 Geographos (1951 RA) | 511243 (2014 BS32) | dark only; N unknown | 3.44 | 2049-01-24 | 266 | 12 | 4.9 |
| 1620 Geographos (1951 RA) | 480936 (2003 QH5) | dark only; N unknown | 4.27 | 2045-11-03 | 275 | 18 | 14.8 |
| 1620 Geographos (1951 RA) | (2016 FW14) | dark only; N unknown | 4.82 | 2064-08-28 | 383 | 11 | 5.6 |
| 1620 Geographos (1951 RA) | 175706 (1996 FG3) | C spectrum; N unknown | 8.08 | 2062-03-22 | 327 | 0 | 44.0 |
| 1620 Geographos (1951 RA) | 162173 Ryugu (1999 JU3) | sample return | 12.78 | 2054-05-03 | 152 | 0 | 44.0 |
| 1620 Geographos (1951 RA) | 101955 Bennu (1999 RQ36) | sample return | 10.00 | 2064-11-22 | 517 | 0 | 44.0 |
| 1943 Anteros (1973 EC) | 381181 (2007 LV19) | dark only; N unknown | 3.65 | 2048-11-25 | 355 | 17 | 13.9 |
| 1943 Anteros (1973 EC) | 276786 (2004 KD1) | dark only; N unknown | 3.81 | 2060-01-09 | 366 | 12 | 6.9 |
| 1943 Anteros (1973 EC) | 108519 (2001 LF) | dark only; N unknown | 4.08 | 2051-05-05 | 389 | 12 | 9.6 |
| 1943 Anteros (1973 EC) | 162173 Ryugu (1999 JU3) | sample return | 5.31 | 2060-07-31 | 343 | 7 | 12.4 |
| 1943 Anteros (1973 EC) | 101955 Bennu (1999 RQ36) | sample return | 8.23 | 2070-10-26 | 287 | 0 | 44.0 |
| 2063 Bacchus (1977 HB) | 101955 Bennu (1999 RQ36) | sample return | 3.94 | 2061-07-03 | 240 | 13 | 12.8 |
| 2063 Bacchus (1977 HB) | 85774 (1998 UT18) | C spectrum; N unknown | 4.78 | 2054-07-24 | 335 | 10 | 14.0 |
| 2063 Bacchus (1977 HB) | (2014 EQ49) | dark only; N unknown | 5.27 | 2048-09-24 | 243 | 17 | 9.6 |
| 2063 Bacchus (1977 HB) | 162173 Ryugu (1999 JU3) | sample return | 6.91 | 2034-06-04 | 407 | 0 | 44.0 |
| 7480 Norwan (1994 PC) | 778852 (2011 AM24) | D? spectrum / radar size; N unknown | 3.09 | 2065-09-26 | 600 | 24 | 2.3 |
| 7480 Norwan (1994 PC) | (2005 QL) | dark only; N unknown | 3.73 | 2049-11-21 | 718 | 16 | 4.2 |
| 7480 Norwan (1994 PC) | (2016 SH45) | dark only; N unknown | 4.79 | 2039-08-30 | 732 | 7 | 11.6 |
| 7480 Norwan (1994 PC) | 7753 (1988 XB) | B spectrum; N unknown | 4.15 | 2046-03-24 | 471 | 12 | 10.4 |
| 7480 Norwan (1994 PC) | 162173 Ryugu (1999 JU3) | sample return | 8.81 | 2071-05-07 | 566 | 0 | 44.0 |
| 7480 Norwan (1994 PC) | 101955 Bennu (1999 RQ36) | sample return | 7.45 | 2059-05-26 | 267 | 0 | 44.0 |
| 15745 Yuliya (1991 PM5) | (2015 CV13) | dark only; N unknown | 3.31 | 2067-11-14 | 276 | 10 | 5.4 |
| 15745 Yuliya (1991 PM5) | 393359 (1998 ME3) | dark only; N unknown | 4.51 | 2048-06-20 | 690 | 7 | 15.8 |
| 15745 Yuliya (1991 PM5) | 26760 (2001 KP41) | dark only; N unknown | 5.03 | 2059-05-14 | 295 | 5 | 26.9 |
| 15745 Yuliya (1991 PM5) | 14402 (1991 DB) | C spectrum; N unknown | 7.52 | 2029-01-14 | 418 | 0 | 44.0 |
| 15745 Yuliya (1991 PM5) | 162173 Ryugu (1999 JU3) | sample return | 9.51 | 2032-01-30 | 511 | 0 | 44.0 |
| 15745 Yuliya (1991 PM5) | 101955 Bennu (1999 RQ36) | sample return | 11.55 | 2043-08-28 | 492 | 0 | 44.0 |
| 22099 (2000 EX106) | 778852 (2011 AM24) | D? spectrum / radar size; N unknown | 2.63 | 2065-03-13 | 330 | 23 | 7.4 |
| 22099 (2000 EX106) | 234145 (2000 EW70) | dark only; N unknown | 4.08 | 2062-07-13 | 268 | 14 | 4.5 |
| 22099 (2000 EX106) | 175706 (1996 FG3) | C spectrum; N unknown | 4.50 | 2054-06-15 | 299 | 12 | 12.8 |
| 22099 (2000 EX106) | 162173 Ryugu (1999 JU3) | sample return | 8.63 | 2069-11-08 | 289 | 0 | 44.0 |
| 22099 (2000 EX106) | 101955 Bennu (1999 RQ36) | sample return | 9.45 | 2028-02-04 | 347 | 0 | 44.0 |
| 25143 Itokawa (1998 SF36) | 252558 (2001 WT1) | dark only; N unknown | 3.86 | 2054-09-08 | 322 | 14 | 4.6 |
| 25143 Itokawa (1998 SF36) | (2010 GU21) | dark only; N unknown | 4.58 | 2066-04-17 | 790 | 22 | 6.8 |
| 25143 Itokawa (1998 SF36) | (2015 DE176) | C colours only; N unknown | 5.19 | 2062-04-28 | 548 | 4 | 19.7 |
| 25143 Itokawa (1998 SF36) | 65679 (1989 UQ) | B spectrum; N unknown | 5.14 | 2069-12-22 | 184 | 15 | 5.3 |
| 25143 Itokawa (1998 SF36) | 162173 Ryugu (1999 JU3) | sample return | 6.28 | 2069-09-16 | 351 | 0 | 44.0 |
| 25143 Itokawa (1998 SF36) | 101955 Bennu (1999 RQ36) | sample return | 8.42 | 2059-02-18 | 218 | 0 | 44.0 |
| 35107 (1991 VH) | 778852 (2011 AM24) | D? spectrum / radar size; N unknown | 2.48 | 2068-01-12 | 239 | 37 | 13.3 |
| 35107 (1991 VH) | (2015 AY245) | T spectrum; N unknown | 5.72 | 2028-09-15 | 509 | 3 | 39.5 |
| 35107 (1991 VH) | (2015 CV13) | dark only; N unknown | 4.85 | 2048-09-06 | 296 | 11 | 6.0 |
| 35107 (1991 VH) | 175706 (1996 FG3) | C spectrum; N unknown | 6.99 | 2058-10-25 | 256 | 0 | 44.0 |
| 35107 (1991 VH) | 162173 Ryugu (1999 JU3) | sample return | 8.34 | 2056-11-16 | 274 | 0 | 44.0 |
| 35107 (1991 VH) | 101955 Bennu (1999 RQ36) | sample return | 9.74 | 2047-05-10 | 254 | 0 | 44.0 |
| 36017 (1999 ND43) | 275611 (1999 XX262) | B spectra; tentative Ch feature | 3.55 | 2038-04-01 | 308 | 21 | 4.5 |
| 36017 (1999 ND43) | 190161 (2005 TJ174) | C colours only; N unknown | 3.67 | 2038-12-25 | 513 | 16 | 4.1 |
| 36017 (1999 ND43) | 101955 Bennu (1999 RQ36) | sample return | 4.03 | 2048-09-25 | 484 | 22 | 3.6 |
| 36017 (1999 ND43) | 162173 Ryugu (1999 JU3) | sample return | 5.92 | 2059-09-06 | 468 | 1 | 33.0 |
| 65803 Didymos (1996 GT) | 162741 (2000 WG6) | dark only; N unknown | 3.88 | 2038-07-28 | 399 | 6 | 11.4 |
| 65803 Didymos (1996 GT) | 7753 (1988 XB) | B spectrum; N unknown | 3.81 | 2046-02-21 | 559 | 14 | 8.1 |
| 65803 Didymos (1996 GT) | 190161 (2005 TJ174) | C colours only; N unknown | 3.97 | 2038-11-04 | 900 | 13 | 6.2 |
| 65803 Didymos (1996 GT) | 162173 Ryugu (1999 JU3) | sample return | 7.12 | 2058-06-03 | 582 | 0 | 44.0 |
| 65803 Didymos (1996 GT) | 101955 Bennu (1999 RQ36) | sample return | 5.17 | 2048-12-07 | 395 | 16 | 4.0 |
| 98943 Torifune (2001 CC21) | 252558 (2001 WT1) | dark only; N unknown | 2.99 | 2053-01-27 | 279 | 26 | 6.8 |
| 98943 Torifune (2001 CC21) | 410777 (2009 FD) | C/Ch spectrum; N unknown | 5.44 | 2042-09-13 | 276 | 7 | 6.3 |
| 98943 Torifune (2001 CC21) | 65679 (1989 UQ) | B spectrum; N unknown | 6.01 | 2039-11-08 | 182 | 0 | 44.0 |
| 98943 Torifune (2001 CC21) | 162173 Ryugu (1999 JU3) | sample return | 7.64 | 2061-11-17 | 300 | 0 | 44.0 |
| 98943 Torifune (2001 CC21) | 101955 Bennu (1999 RQ36) | sample return | 8.43 | 2030-03-14 | 427 | 0 | 44.0 |
| 99942 Apophis (post-2029) | 234145 (2000 EW70) | dark only; N unknown | 3.42 | 2070-12-23 | 332 | 21 | 3.8 |
| 99942 Apophis (post-2029) | 175706 (1996 FG3) | C spectrum; N unknown | 4.10 | 2055-09-15 | 226 | 13 | 10.9 |
| 99942 Apophis (post-2029) | 252558 (2001 WT1) | dark only; N unknown | 4.76 | 2058-10-01 | 268 | 11 | 20.4 |
| 99942 Apophis (post-2029) | 162173 Ryugu (1999 JU3) | sample return | 5.63 | 2069-11-03 | 264 | 4 | 11.3 |
| 99942 Apophis (post-2029) | 101955 Bennu (1999 RQ36) | sample return | 8.45 | 2067-03-16 | 432 | 0 | 44.0 |
| 137799 (1999 YB) | 101955 Bennu (1999 RQ36) | sample return | 4.43 | 2067-04-27 | 400 | 19 | 6.6 |
| 137799 (1999 YB) | 275611 (1999 XX262) | B spectra; tentative Ch feature | 5.11 | 2067-07-17 | 260 | 13 | 7.5 |
| 137799 (1999 YB) | 511243 (2014 BS32) | dark only; N unknown | 5.15 | 2031-12-12 | 255 | 10 | 7.4 |
| 137799 (1999 YB) | 162173 Ryugu (1999 JU3) | sample return | 7.06 | 2065-10-03 | 288 | 0 | 44.0 |
| 139622 (2001 QQ142) | 477490 (2010 CG18) | dark only; N unknown | 1.28 | 2028-11-16 | 276 | 26 | 17.4 |
| 139622 (2001 QQ142) | 162741 (2000 WG6) | dark only; N unknown | 4.58 | 2066-02-03 | 621 | 12 | 14.3 |
| 139622 (2001 QQ142) | 85774 (1998 UT18) | C spectrum; N unknown | 5.17 | 2028-04-23 | 483 | 4 | 37.2 |
| 139622 (2001 QQ142) | 162173 Ryugu (1999 JU3) | sample return | 7.07 | 2061-03-04 | 381 | 0 | 44.0 |
| 139622 (2001 QQ142) | 101955 Bennu (1999 RQ36) | sample return | 5.49 | 2039-05-27 | 376 | 4 | 11.9 |
| 152560 (1991 BN) | 7753 (1988 XB) | B spectrum; N unknown | 3.65 | 2064-10-12 | 272 | 29 | 21.3 |
| 152560 (1991 BN) | (2007 VG189) | dark only; N unknown | 3.86 | 2061-01-23 | 735 | 15 | 3.9 |
| 152560 (1991 BN) | 175706 (1996 FG3) | C spectrum; N unknown | 3.92 | 2049-10-27 | 387 | 17 | 3.4 |
| 152560 (1991 BN) | 162173 Ryugu (1999 JU3) | sample return | 7.21 | 2069-12-19 | 495 | 0 | 44.0 |
| 152560 (1991 BN) | 101955 Bennu (1999 RQ36) | sample return | 7.32 | 2054-07-11 | 481 | 0 | 44.0 |
| 302311 (2002 AA) | 434632 (2005 WE) | dark only; N unknown | 6.40 | 2071-03-13 | 629 | 0 | 44.0 |
| 302311 (2002 AA) | 136793 (1997 AQ18) | C spectrum; N unknown | 5.12 | 2047-06-19 | 298 | 37 | 1.2 |
| 302311 (2002 AA) | 175706 (1996 FG3) | C spectrum; N unknown | 5.80 | 2041-05-19 | 261 | 2 | 18.5 |
| 302311 (2002 AA) | 162173 Ryugu (1999 JU3) | sample return | 6.30 | 2032-04-02 | 279 | 0 | 44.0 |
| 302311 (2002 AA) | 101955 Bennu (1999 RQ36) | sample return | 6.82 | 2059-03-15 | 330 | 0 | 44.0 |

## Supplier redundancy and stock

Two alternatives are shown: sampled bodies only (Bennu/Ryugu), and all dated candidate routes. The latter assumes every listed candidate proves useful; it is an exploration target, not assured supply. Suppliers are counted once per host. Their inventory cannot also be allocated in full to every other host.

The illustrative stock covers constant construction of one 900 m torus per ten years, using its shipped N₂ + water + organics demand. It is gap × annual cargo, with no freighter payload, processing rate, loss, contingency reserve or exponential cluster growth. It is not a complete logistics stock requirement.

| Host | Earth → host best km/s | Sampled-source selected-arrival gap yr | All-candidate gap yr | Illustrative cargo stock kt |
|---|---:|---:|---:|---:|
| 433 Eros (A898 PA) | 6.92 | 7.5 | 2.7 | 28 |
| 1620 Geographos (1951 RA) | 10.42 | 44.0 | 3.7 | 39 |
| 1943 Anteros (1973 EC) | 6.47 | 12.4 | 4.1 | 43 |
| 2063 Bacchus (1977 HB) | 8.25 | 12.8 | 7.3 | 78 |
| 7480 Norwan (1994 PC) | 8.06 | 44.0 | 2.0 | 22 |
| 15745 Yuliya (1991 PM5) | 9.22 | 44.0 | 5.0 | 53 |
| 22099 (2000 EX106) | 6.10 | 44.0 | 4.5 | 47 |
| 25143 Itokawa (1998 SF36) | 4.30 | 44.0 | 4.4 | 46 |
| 35107 (1991 VH) | 7.31 | 44.0 | 6.0 | 64 |
| 36017 (1999 ND43) | 6.30 | 3.6 | 1.9 | 20 |
| 65803 Didymos (1996 GT) | 6.12 | 4.0 | 2.7 | 29 |
| 98943 Torifune (2001 CC21) | 4.11 | 44.0 | 6.3 | 67 |
| 99942 Apophis (post-2029) | 3.90 | 11.3 | 3.8 | 40 |
| 137799 (1999 YB) | 5.09 | 6.6 | 3.6 | 38 |
| 139622 (2001 QQ142) | 6.66 | 11.9 | 3.4 | 36 |
| 152560 (1991 BN) | 6.89 | 44.0 | 3.2 | 34 |
| 302311 (2002 AA) | 9.16 | 44.0 | 1.2 | 13 |

## Ladder hosts: size, spin and access

Sizes are SsODNet's best estimates where published, with the catalogue size for comparison. Spin ÷ gravity is the centrifugal acceleration over gravity at 2 t/m³: at a sphere's equator (it depends only on the period, reaching 1 at ~2.33 h) and at the tips of the long axis of a homogeneous ellipsoid where SBDB gives a shape. Real tapered ends hold less; above ~0.5, anchoring and excavation need a shape-model gravity field. The Earth round trip is NASA's NHATS minimum (crewed-mission accounting from low Earth orbit, within its 12 km/s and 450-day limits); a dash means no trip within those limits. The heliocentric Earth → host cost of the dated stage is given for every host.

| Step | Host | D km (source) | Catalogue D km | Rotation h | Spin ÷ gravity: equator / tips | Earth → host, dated km/s | Earth round trip, NHATS km/s |
|---|---|---|---:|---:|---|---:|---:|
| 1 | 99942 Apophis (post-2029) | 0.34 (Radar shape modeling) | 0.34 | 30.56 | 0.01 / — | 3.90 | 6.05 (354 d) |
| 1 | 25143 Itokawa (1998 SF36) | 0.326 (Rendez-vous with a spacecraft) | 0.33 | 12.13 | 0.04 / 0.08 | 4.30 | 9.41 (210 d) |
| 2 | 98943 Torifune (2001 CC21) | 0.383 (ThermoPhysical Model) | 0.502 | 5.02 | 0.22 / — | 4.11 | 8.99 (450 d) |
| 2 | 302311 (2002 AA) | 0.32 (Near-Earth Asteroid Thermal Model) | 0.367 | 4.13 | 0.32 / — | 9.16 | — |
| 2 | 152560 (1991 BN) | 0.29 (Near-Earth Asteroid Thermal Model) | 0.395 | 3.49 | 0.45 / — | 6.89 | — |
| 2 | 36017 (1999 ND43) | 0.384 (H, albedo 0.23) | 0.384 | 5.79 | 0.16 / — | 6.30 | — |
| 2 | 137799 (1999 YB) | 0.491 (H, albedo 0.23) | 0.491 | 9.39 | 0.06 / — | 5.09 | — |
| 2 | 22099 (2000 EX106) | 0.579 (Near-Earth Asteroid Thermal Model) | 0.524 | 6.33 | 0.14 / — | 6.10 | — |
| 2 | 139622 (2001 QQ142) | 0.563 (H, albedo 0.23) | 0.563 | — | — | 6.66 | 11.79 (370 d) |
| 3 | 65803 Didymos (1996 GT) | 0.761 (Rendez-vous with a spacecraft) | 0.78 | 2.26 | 1.07 / 1.10 | 6.12 | — |
| 3 | 35107 (1991 VH) | 0.914 (Near-Earth Asteroid Thermal Model) | 0.929 | 2.62 | 0.79 / — | 7.31 | 11.16 (370 d) |
| 3 | 15745 Yuliya (1991 PM5) | 0.77 (Near-Earth Asteroid Thermal Model) | 0.918 | 3.25 | 0.52 / — | 9.22 | — |
| 3 | 7480 Norwan (1994 PC) | 0.988 (H, albedo 0.23) | 0.988 | 35.90 | 0.00 / — | 8.06 | — |
| 3 | 2063 Bacchus (1977 HB) | 1.03 (Near-Earth Asteroid Thermal Model) | 1.02 | 14.90 | 0.02 / 0.05 | 8.25 | — |
| 4 | 1943 Anteros (1973 EC) | 2.31 (Near-Earth Asteroid Thermal Model) | 2.3 | 2.87 | 0.66 / — | 6.47 | 11.71 (370 d) |
| 4 | 1620 Geographos (1951 RA) | 2.44 (ThermoPhysical Model) | 2.56 | 5.22 | 0.20 / 0.48 | 10.42 | — |
| 5 | 433 Eros (A898 PA) | 17.6 (Rendez-vous with a spacecraft) | 16.8 | 5.27 | 0.20 / 0.62 | 6.92 | — |

## Supply per ladder step

Volatiles shipped per torus (N₂, water and organics for the soil; the system model's demand for the step's design, LL host), the best sampled and dark routes from the dated stage, and the illustrative stock for one torus per ten years through the largest gap between selected arrivals (sampled sources only, then all dated candidates). Dark candidates' nitrogen is unmeasured and can be zero.

| Step | Habitat | Shipped per torus kt | Host | Best sampled route | Best dark route | Stock, sampled / all kt |
|---|---|---:|---|---|---|---:|
| 1 | 400 m torus | 19.81 | 99942 Apophis (post-2029) | 162173 Ryugu (1999 JU3): 5.63 km/s, 4 opportunities | 234145 (2000 EW70): 3.42 km/s, 21 opportunities | 22.3 / 7.5 |
| 1 | 400 m torus | 19.81 | 25143 Itokawa (1998 SF36) | 162173 Ryugu (1999 JU3): 6.28 km/s, 0 opportunities | 252558 (2001 WT1): 3.86 km/s, 14 opportunities | 87.2 / 8.7 |
| 2 | 400 m pair | 19.81 | 99942 Apophis (post-2029) | 162173 Ryugu (1999 JU3): 5.63 km/s, 4 opportunities | 234145 (2000 EW70): 3.42 km/s, 21 opportunities | 22.3 / 7.5 |
| 2 | 400 m pair | 19.81 | 25143 Itokawa (1998 SF36) | 162173 Ryugu (1999 JU3): 6.28 km/s, 0 opportunities | 252558 (2001 WT1): 3.86 km/s, 14 opportunities | 87.2 / 8.7 |
| 2 | 400 m pair | 19.81 | 98943 Torifune (2001 CC21) | 162173 Ryugu (1999 JU3): 7.64 km/s, 0 opportunities | 252558 (2001 WT1): 2.99 km/s, 26 opportunities | 87.2 / 12.5 |
| 2 | 400 m pair | 19.81 | 302311 (2002 AA) | 162173 Ryugu (1999 JU3): 6.30 km/s, 0 opportunities | 136793 (1997 AQ18): 5.12 km/s, 37 opportunities | 87.2 / 2.5 |
| 2 | 400 m pair | 19.81 | 152560 (1991 BN) | 162173 Ryugu (1999 JU3): 7.21 km/s, 0 opportunities | 7753 (1988 XB): 3.65 km/s, 29 opportunities | 87.2 / 6.3 |
| 2 | 400 m pair | 19.81 | 36017 (1999 ND43) | 101955 Bennu (1999 RQ36): 4.03 km/s, 22 opportunities | 275611 (1999 XX262): 3.55 km/s, 21 opportunities | 7.2 / 3.8 |
| 2 | 400 m pair | 19.81 | 137799 (1999 YB) | 101955 Bennu (1999 RQ36): 4.43 km/s, 19 opportunities | 275611 (1999 XX262): 5.11 km/s, 13 opportunities | 13.0 / 7.1 |
| 2 | 400 m pair | 19.81 | 22099 (2000 EX106) | 162173 Ryugu (1999 JU3): 8.63 km/s, 0 opportunities | 778852 (2011 AM24): 2.63 km/s, 23 opportunities | 87.2 / 8.9 |
| 2 | 400 m pair | 19.81 | 139622 (2001 QQ142) | 101955 Bennu (1999 RQ36): 5.49 km/s, 4 opportunities | 477490 (2010 CG18): 1.28 km/s, 26 opportunities | 23.6 / 6.6 |
| 3 | 900 m torus, then pair; then a pair with farms | 105.91 | 65803 Didymos (1996 GT) | 101955 Bennu (1999 RQ36): 5.17 km/s, 16 opportunities | 7753 (1988 XB): 3.81 km/s, 14 opportunities | 42.8 / 28.7 |
| 3 | 900 m torus, then pair; then a pair with farms | 105.91 | 35107 (1991 VH) | 162173 Ryugu (1999 JU3): 8.34 km/s, 0 opportunities | 778852 (2011 AM24): 2.48 km/s, 37 opportunities | 466.0 / 63.9 |
| 3 | 900 m torus, then pair; then a pair with farms | 105.91 | 15745 Yuliya (1991 PM5) | 162173 Ryugu (1999 JU3): 9.51 km/s, 0 opportunities | (2015 CV13): 3.31 km/s, 10 opportunities | 466.0 / 52.7 |
| 3 | 900 m torus, then pair; then a pair with farms | 105.91 | 7480 Norwan (1994 PC) | 101955 Bennu (1999 RQ36): 7.45 km/s, 0 opportunities | 778852 (2011 AM24): 3.09 km/s, 24 opportunities | 466.0 / 21.6 |
| 3 | 900 m torus, then pair; then a pair with farms | 105.91 | 2063 Bacchus (1977 HB) | 101955 Bennu (1999 RQ36): 3.94 km/s, 13 opportunities | 85774 (1998 UT18): 4.78 km/s, 10 opportunities | 135.6 / 77.6 |
| 4 | 900 m and 1.6 km stacks with farms | 363.31 | 1943 Anteros (1973 EC) | 162173 Ryugu (1999 JU3): 5.31 km/s, 7 opportunities | 381181 (2007 LV19): 3.65 km/s, 17 opportunities | 450.8 / 147.3 |
| 4 | 900 m and 1.6 km stacks with farms | 363.31 | 1620 Geographos (1951 RA) | 101955 Bennu (1999 RQ36): 10.00 km/s, 0 opportunities | 511243 (2014 BS32): 3.44 km/s, 12 opportunities | 1598.5 / 135.3 |
| 5 | 1.6 km six-stacks | 363.31 | 433 Eros (A898 PA) | 162173 Ryugu (1999 JU3): 4.52 km/s, 10 opportunities | (2015 DX198): 3.19 km/s, 17 opportunities | 273.4 / 96.8 |

A 44-year gap means no selected arrival in the 2028–2072 horizon: that route never comes within the 6 km/s cutoff, so the stock column is the whole horizon's demand. The 400 m tori carry no farm, so their nitrogen is the valley's air alone; their soil organics are still counted, and a synthetic interior would need less.

## Resource sensitivity

For unmeasured suppliers the evidence-based lower bound is **zero useful nitrogen**. The positive cases below are deliberately illustrative, not confidence intervals or measured ore grades. For unvisited suppliers the base case borrows the existing model's 0.24 wt% N and 70% recovery; it does not assign those values as observations of other asteroids. Carbonaceous taxonomy and hydration do not establish nitrogen abundance.

For unvisited bodies the lower positive scenario uses 0.8× diameter, 1.0 t/m³, 0.05 wt% N and 50% recovery; the higher uses 1.2× diameter, 1.6 t/m³, 0.25 wt% N and 90% recovery. Both retain the model's 6.4 wt% available-water assumption and enforce the smaller of N and water capacity. These water assumptions also need validation. For Bennu/Ryugu, diameter and density stay fixed. Bennu uses 0.23 / 0.24 / 0.25 wt% N (Glavin et al. 2025); Ryugu uses 0.1437 / 0.1454 / 0.1471 wt% N (Yokoyama et al. 2025, Table 1). The Ryugu interval is the published ±2σ uncertainty on the sample-based mean, not a bound on the whole asteroid. Both bodies use 50 / 70 / 90% industrial recovery, an assumption separate from the sample measurements. Ryugu's base capacity is consequently ~54 small tori rather than ~89 under the common Bennu-like proxy. The habitat model also sizes Ryugu's C-type at its measured grade; unvisited candidates keep the common proxy. Extracting soil organics/other nutrients, excavation accessibility and maintaining a residual asteroid are outside this capacity calculation.

| Supplier | Catalogue D km | Evidence | 900 m tori: lower positive / base / higher | 1.6 km tori: lower positive / base / higher |
|---|---:|---|---:|---:|
| 101955 Bennu (1999 RQ36) | 0.484 | sample return | 9.6 / 14.0 / 18.8 | 1.8 / 2.6 / 3.4 |
| 108519 (2001 LF) | 1.42 | dark only; N unknown | 22.8 / 355.6 / 1106.4 | 4.2 / 65.2 / 202.8 |
| 136793 (1997 AQ18) | 1.27 | C spectrum; N unknown | 16.2 / 253.2 / 787.8 | 3.0 / 46.4 / 144.4 |
| 14402 (1991 DB) | 0.6 | C spectrum; N unknown | 1.7 / 26.7 / 82.9 | 0.3 / 4.9 / 15.2 |
| 162173 Ryugu (1999 JU3) | 0.896 | sample return | 38.0 / 53.8 / 70.0 | 7.0 / 9.9 / 12.8 |
| 162741 (2000 WG6) | 3.94 | dark only; N unknown | 485.1 / 7576.4 / 23574.9 | 88.9 / 1389.0 / 4322.0 |
| 175706 (1996 FG3) | 1.2 | C spectrum; N unknown | 13.5 / 211.1 / 656.9 | 2.5 / 38.7 / 120.4 |
| 190161 (2005 TJ174) | 3.04 | C colours only; N unknown | 222.2 / 3470.3 / 10798.4 | 40.7 / 636.2 / 1979.7 |
| (2002 BM26) | 0.84 | P/X spectrum; N unknown | 4.7 / 73.1 / 227.6 | 0.9 / 13.4 / 41.7 |
| (2005 QL) | 1.85 | dark only; N unknown | 49.8 / 777.5 / 2419.4 | 9.1 / 142.5 / 443.6 |
| (2007 VG189) | 0.505 | dark only; N unknown | 1.0 / 15.9 / 49.5 | 0.2 / 2.9 / 9.1 |
| (2010 GU21) | 0.51 | dark only; N unknown | 1.0 / 16.4 / 50.9 | 0.2 / 3.0 / 9.3 |
| (2014 EQ49) | 0.379 | dark only; N unknown | 0.4 / 6.7 / 20.9 | 0.1 / 1.2 / 3.8 |
| (2015 AY245) | 0.374 | T spectrum; N unknown | 0.4 / 6.5 / 20.1 | 0.1 / 1.2 / 3.7 |
| (2015 CV13) | 0.437 | dark only; N unknown | 0.7 / 10.3 / 32.0 | 0.1 / 1.9 / 5.9 |
| (2015 DE176) | 0.679 | C colours only; N unknown | 2.5 / 38.6 / 120.2 | 0.5 / 7.1 / 22.0 |
| (2015 DX198) | 0.349 | dark only; N unknown | 0.3 / 5.2 / 16.3 | 0.1 / 1.0 / 3.0 |
| (2016 FW14) | 0.366 | dark only; N unknown | 0.4 / 6.1 / 18.8 | 0.1 / 1.1 / 3.5 |
| (2016 SH45) | 0.82 | dark only; N unknown | 4.4 / 68.0 / 211.7 | 0.8 / 12.5 / 38.8 |
| 234145 (2000 EW70) | 0.344 | dark only; N unknown | 0.3 / 5.0 / 15.6 | 0.1 / 0.9 / 2.9 |
| 252558 (2001 WT1) | 0.533 | dark only; N unknown | 1.2 / 18.7 / 58.1 | 0.2 / 3.4 / 10.7 |
| 26760 (2001 KP41) | 5.4 | dark only; N unknown | 1244.1 / 19431.2 / 60463.1 | 228.1 / 3562.3 / 11084.7 |
| 275611 (1999 XX262) | 1.48 | B spectra; tentative Ch feature | 25.8 / 402.5 / 1252.4 | 4.7 / 73.8 / 229.6 |
| 276786 (2004 KD1) | 1.72 | dark only; N unknown | 40.2 / 627.9 / 1953.9 | 7.4 / 115.1 / 358.2 |
| 381181 (2007 LV19) | 0.602 | dark only; N unknown | 1.7 / 26.9 / 83.8 | 0.3 / 4.9 / 15.4 |
| 393359 (1998 ME3) | 0.774 | dark only; N unknown | 3.7 / 57.2 / 178.0 | 0.7 / 10.5 / 32.6 |
| 410777 (2009 FD) | 0.472 | C/Ch spectrum; N unknown | 0.8 / 13.0 / 40.4 | 0.2 / 2.4 / 7.4 |
| 434632 (2005 WE) | 1.15 | dark only; N unknown | 12.0 / 187.7 / 584.0 | 2.2 / 34.4 / 107.1 |
| 477490 (2010 CG18) | 0.652 | dark only; N unknown | 2.2 / 34.2 / 106.4 | 0.4 / 6.3 / 19.5 |
| 480936 (2003 QH5) | 0.537 | dark only; N unknown | 1.2 / 19.1 / 59.5 | 0.2 / 3.5 / 10.9 |
| 511243 (2014 BS32) | 1.2 | dark only; N unknown | 13.5 / 210.6 / 655.3 | 2.5 / 38.6 / 120.1 |
| 65679 (1989 UQ) | 0.918 | B spectrum; N unknown | 6.1 / 95.5 / 297.1 | 1.1 / 17.5 / 54.5 |
| 7753 (1988 XB) | 1.49 | B spectrum; N unknown | 25.9 / 405.0 / 1260.2 | 4.8 / 74.2 / 231.0 |
| 778852 (2011 AM24) | 0.511 | D? spectrum / radar size; N unknown | 1.1 / 16.5 / 51.2 | 0.2 / 3.0 / 9.4 |
| 85774 (1998 UT18) | 0.939 | C spectrum; N unknown | 6.5 / 102.2 / 317.9 | 1.2 / 18.7 / 58.3 |

These are alternative allocations of the same supplier, not cumulative counts of 900 m and 1.6 km tori. For XX262, 1.48 km remains the working diameter; the published 2.426 km alternative would multiply volume and conditional inventory by about 4.4. It is not folded into the higher scenario as though it were established.

## Evidence audit and research priorities

See [asteroid-evidence.md](asteroid-evidence.md) for the composition and size audit. The raw supplier records are in `logistics_model/data/network_evidence.json`; selected host physical parameters retain their original JPL references in `network_hosts.json`. Multiple catalogue entries or taxonomies need not represent independent observations.

1. Keep Eros as the large, spacecraft-characterised reference; compare 1991 VH as a smaller mild-season LL-like host and 1999 YB as a low-eccentricity but poorly sized host. Their finite metal inventory matters more than a small Δv saving if the goal is many generations at the same site.
2. Treat the 0.3–0.6 km hosts (Apophis, Itokawa, Torifune) as demonstrator sites for one torus or one pair, not as clusters that grow indefinitely. Keep all mass estimates separate from measured free-metal abundance.
3. Obtain or reanalyse spectra for the low-cost dark candidates before resource planning; for XX262, confirm the weak hydration feature and measure the 3 µm region. No unvisited candidate here has a verified recoverable-nitrogen inventory.
4. Re-run the selected routes with low-thrust trajectories, propulsion/power/dry-mass constraints, full launch intervals and supplier throughput. Include multi-revolution arcs and perturbations along the transfer itself. The current model uses integrated endpoint states but a two-body transfer arc.
5. Assess mining mechanics separately: spin, binaries, gravity, anchoring and excavation can distinguish otherwise similar orbits. The ladder-host table screens spin only: Didymos (~1.1 at 2 t/m³), 1991 VH (~0.8, a binary), Anteros (~0.7), Eros's tips (~0.6) and Yuliya (~0.5) need shape-model gravity fields first.

## Validation

The logistics and network tests cover a circular-orbit Lambert solution, the Hohmann transfer, resource bottlenecks, orbital sunlight, opportunity unions and the flight-time bounds. The saved endpoint checks independently query Horizons at the exact optimized dates for XX262 → Eros, AM24 → 1991 VH and 2010 CG18 → 2001 QQ142. They test interpolation and object identity, not global optimality or a full perturbed transfer. See `logistics_model/data/network_endpoint_checks.json` for the states and numerical differences.

## Reproduce

```bash
python -m logistics_model.networks --fetch
python -m logistics_model.networks --screen --spectral
python -m logistics_model.networks --fetch-vectors --fetch-evidence --fetch-physical
python -m logistics_model.networks --windows
python -m logistics_model.networks --verify
python -m logistics_model.networks --report
python -m unittest tests.test_networks tests.test_logistics
```

Use --fetch-vectors to resume missing bodies without changing the acquisition dates of cached data. Use --refresh-vectors to fetch every selected body again, then --windows to recompute routes. Screen caches are matched to hashes of their host/supplier inputs, and dated windows to a hash of the ephemeris bytes. The report rejects stale inputs/results. Only --fetch, --fetch-vectors, --refresh-vectors, --fetch-evidence, --fetch-physical and --verify need network access. The dated selection is the central-estimate Pareto front plus the named reference/comparison hosts, each with its three lowest refined costs, best screened spectral C-complex supplier, Ryugu, Bennu and Earth. Snapshots contain the exact selection and results. Start a fresh --screen by removing `network_screen.json`; an interrupted run resumes its saved hosts.

Sources: [JPL SBDB query API](https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html), [SBDB object API](https://ssd-api.jpl.nasa.gov/doc/sbdb.html), [Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html), [SsODNet](https://ssp.imcce.fr/webservices/ssodnet/). Sample N sources: [Glavin et al. 2025](https://doi.org/10.1038/s41550-024-02472-9), [Yokoyama et al. 2025, Table 1](https://doi.org/10.2343/geochemj.GJ25002). The complete habitat demand comes from the current checked-in `habitat_model/assumptions.toml`; all resource assumptions remain provisional.
