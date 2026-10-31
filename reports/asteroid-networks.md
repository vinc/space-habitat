# Asteroid host–supplier networks

A first screening study, 31 October 2026. Extends the Eros reference to other silicate near-Earth hosts. The result is a shortlist for investigation, not a verified resource inventory or an executable transport plan.

## Ranked research shortlist

This is a judgement about which networks to investigate first for this project's near-Earth, locally built habitats. It is not a universal optimum. Long-term inventory and evidence quality take precedence over a small saving in the best transfer found.

| Priority | Host and supplier network | Reason to investigate | Main reservation |
|---|---|---|---|
| 1 | Eros + 1999 XX262 / 2015 DX198; Ryugu and Bennu as sampled comparisons | Large, spacecraft-characterised host; several alternative delivery routes | Strong seasons; XX262 hydration is tentative and the dark suppliers' nitrogen is unknown |
| 2 | 1991 VH + 2011 AM24 / 2015 CV13 / 2015 AY245 | Milder seasons and an unusually inexpensive AM24 route | Finite LL-like metal inventory; fast-rotating binary; no sampled supplier below the adopted cutoff |
| 3 | 1999 YB + Bennu and the additional candidates in the dated table | Mildest seasons among the retained hosts, with a sampled-source comparison | Host diameter is inferred from H and assumed albedo; potentially only a few small tori |
| 4 | Torifune + 2001 WT1 / 2009 FD | Smaller solar array and a low-cost WT1 route; possible nursery | Limited host inventory, uncertain WT1 resources; catalogue size needs replacing with a volume model |

Geographos, Bacchus, Norwan and 2001 QQ142 remain trade-off alternatives in the tables; their presence on the central-estimate Pareto front does not establish a superior settlement site. Itokawa and Apophis are useful transport comparisons, but the conservative LL free-metal model gives only about one complete 900 m torus, before recovery/accessibility losses: that does not support a self-reproducing pair at those sites without another material source. L/H-rich material or silicate iron extraction changes that conclusion and needs its own evidence.

## What was searched

The JPL SBDB query returned 327 asteroids with a recorded spectral classification. The stated cuts retained 18 hosts: S-complex/Q, or L/K silicate candidates, with q > 0.7 AU, Q < 2.5 AU, eccentricity < 0.4, inclination < 15° and H < 20; the existing reference hosts are retained explicitly. This is limited by SBDB's sparse taxonomy coverage, not a census of every potentially suitable NEO. Spectral L does not mean L ordinary chondrite. Differentiated objects and unclassified metal-rich hosts are outside this search.

Each host was screened against the existing 365 C-complex/dark candidates (snapshot 30 October 2026). The first grid used 30° departure/arrival true-anomaly steps and 60–720-day flights in 60-day steps; the best 18 per host were screened again at 15°. The best six were refined with the existing 10° grid and eight-seed pattern search, as were Bennu, Ryugu and the two best screened C-complex spectral candidates. Rounded supplier elements are adequate for screening but not final mission design. Host elements were fetched at full precision; Apophis uses Horizons' post-flyby orbit at 1 January 2030 instead of its current pre-2029 orbit. Grid screening can miss narrow minima: these are the best solutions found, not certified global minima.

The dated stage uses JPL Horizons' integrated states, every ten days from 2027 to 2077, interpolated using the existing cubic Hermite method. Departure dates span 2028–2072 in five-day steps; flights span 60–900 days in ten-day steps and are refined while keeping those bounds. Transfers are prograde, zero-revolution, two-impulse rendezvous. Both acceleration and braking are charged. Earth departure figures are heliocentric rendezvous costs: launch, Earth escape, capture and the spacecraft's mass are additional.

## Host comparison

Compare the columns rather than one weighted score. Array × is Q²: panel area relative to the same constant load at 1 AU, sized at aphelion. Seasonal ratio is perihelion/aphelion sunlight, not a prediction of interior temperature. Tori are complete 900 m or 1.6 km designs with three farm tiers; capacity uses the existing free-metal/shield budget, including the hub/factory allowance. LL/L capacities are material scenarios unless composition is established. They assume the entire asteroid is accessible and the model's assumed metal is recovered.

| Host | Spectral record | D km | Year yr | Sunlight range × Earth | Seasonal ratio | Array × | 900 m tori LL / L | 1.6 km tori LL / L | Lowest phase-free Δv found |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| 137799 (1999 YB) | Sq | 0.491* | 1.52 | 0.50–0.67 | 1.35 | 2.02 | 3.8 / 7.5 | 0.7 / 1.5 | 4.42 km/s |
| 35107 (1991 VH) | Sk | 0.929 | 1.21 | 0.59–1.06 | 1.78 | 1.69 | 25.6 / 51.2 | 5.0 / 10.0 | 2.41 km/s |
| 99942 Apophis (post-2029) | Sq | 0.34 | 1.16 | 0.58–1.25 | 2.15 | 1.72 | 1.3 / 2.5 | 0.2 / 0.5 | 3.43 km/s |
| 98943 Torifune (2001 CC21) | L | 0.502* | 1.05 | 0.63–1.54 | 2.44 | 1.58 | 4.0 / 8.1 | 0.8 / 1.6 | 2.84 km/s |
| 433 Eros (A898 PA) | S/S | 16.8 | 1.76 | 0.31–0.78 | 2.48 | 3.18 | 203742.0 / 407484.0 | 39911.6 / 79823.1 | 3.16 km/s |
| 15745 Yuliya (1991 PM5) | S | 0.918* | 2.26 | 0.21–0.61 | 2.84 | 4.66 | 24.7 / 49.3 | 4.8 / 9.7 | 3.26 km/s |
| 1943 Anteros (1973 EC) | L/S | 2.3 | 1.71 | 0.31–0.88 | 2.85 | 3.23 | 388.2 / 776.4 | 76.0 / 152.1 | 3.64 km/s |
| 22099 (2000 EX106) | S: | 0.524 | 1.16 | 0.50–1.57 | 3.11 | 1.99 | 4.6 / 9.2 | 0.9 / 1.8 | 2.65 km/s |
| 25143 Itokawa (1998 SF36) | S(IV) | 0.33 | 1.52 | 0.35–1.10 | 3.16 | 2.87 | 1.0 / 1.9 | 0.2 / 0.4 | 3.87 km/s |
| 302311 (2002 AA) | Sq | 0.367* | 1.23 | 0.45–1.56 | 3.48 | 2.23 | 1.6 / 3.2 | 0.3 / 0.6 | 3.76 km/s |
| 139622 (2001 QQ142) | Sq | 0.563* | 1.69 | 0.29–1.04 | 3.61 | 3.46 | 5.7 / 11.4 | 1.1 / 2.2 | 1.28 km/s |
| 36017 (1999 ND43) | Sl | 0.384* | 1.88 | 0.25–0.92 | 3.67 | 4.01 | 1.8 / 3.6 | 0.4 / 0.7 | 3.27 km/s |
| 7480 Norwan (1994 PC) | S | 0.988* | 1.96 | 0.23–0.87 | 3.72 | 4.26 | 30.8 / 61.5 | 6.0 / 12.0 | 3.10 km/s |
| 1620 Geographos (1951 RA) | S/S | 2.56 | 1.39 | 0.36–1.46 | 4.04 | 2.77 | 535.3 / 1070.6 | 104.9 / 209.7 | 3.43 km/s |
| 2063 Bacchus (1977 HB) | Sq | 1.02 | 1.12 | 0.47–2.03 | 4.30 | 2.11 | 34.3 / 68.5 | 6.7 / 13.4 | 3.87 km/s |
| 189040 (2000 MU1) | S | 0.294* | 1.61 | 0.28–1.39 | 5.01 | 3.60 | 0.8 / 1.6 | 0.2 / 0.3 | 2.83 km/s |
| 65803 Didymos (1996 GT) | S | 0.78 | 2.11 | 0.19–0.97 | 5.03 | 5.16 | 15.1 / 30.3 | 3.0 / 5.9 | 3.80 km/s |
| 152560 (1991 BN) | Q | 0.395* | 1.73 | 0.25–1.33 | 5.40 | 4.07 | 2.0 / 3.9 | 0.4 / 0.8 | 3.54 km/s |

* Diameter estimated from H at an assumed albedo of 0.23. These are not measured sizes. Mass uses measured GM where present (notably Eros and Itokawa); otherwise it uses diameter and 2 t/m³. For H-only sizes, albedos 0.1–0.4 change mass to about 0.44–3.49× the tabulated proxy, before density uncertainty. For a thermally modelled diameter, even a small formal error may exclude substantial model uncertainty.

Central-estimate Pareto front (smaller array, smaller seasonal ratio, smaller best Δv, larger LL inventory): 433 Eros (A898 PA); 1620 Geographos (1951 RA); 2063 Bacchus (1977 HB); 7480 Norwan (1994 PC); 35107 (1991 VH); 98943 Torifune (2001 CC21); 137799 (1999 YB); 139622 (2001 QQ142). This front ignores evidence quality and is not robust to uncertain sizes/compositions. The dated stage covers it plus Eros, 1999 YB, 1991 VH, Torifune, Geographos, Didymos and Itokawa.

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

## Supplier redundancy and stock

Two alternatives are shown: sampled bodies only (Bennu/Ryugu), and all dated candidate routes. The latter assumes every listed candidate proves useful; it is an exploration target, not assured supply. Suppliers are counted once per host. Their inventory cannot also be allocated in full to every other host.

The illustrative stock covers constant construction of one 900 m torus per ten years, using its shipped N₂ + water + organics demand. It is gap × annual cargo, with no freighter payload, processing rate, loss, contingency reserve or exponential cluster growth. It is not a complete logistics stock requirement.

| Host | Earth → host best km/s | Sampled-source selected-arrival gap yr | All-candidate gap yr | Illustrative cargo stock kt |
|---|---:|---:|---:|---:|
| 433 Eros (A898 PA) | 6.92 | 7.5 | 2.7 | 28 |
| 1620 Geographos (1951 RA) | 10.42 | 44.0 | 3.7 | 39 |
| 2063 Bacchus (1977 HB) | 8.25 | 12.8 | 7.3 | 78 |
| 7480 Norwan (1994 PC) | 8.06 | 44.0 | 2.0 | 22 |
| 25143 Itokawa (1998 SF36) | 4.30 | 44.0 | 4.4 | 46 |
| 35107 (1991 VH) | 7.31 | 44.0 | 6.0 | 64 |
| 65803 Didymos (1996 GT) | 6.12 | 4.0 | 2.7 | 29 |
| 98943 Torifune (2001 CC21) | 4.11 | 44.0 | 6.3 | 67 |
| 99942 Apophis (post-2029) | 3.90 | 11.3 | 3.8 | 40 |
| 137799 (1999 YB) | 5.09 | 6.6 | 3.6 | 38 |
| 139622 (2001 QQ142) | 6.66 | 11.9 | 3.4 | 36 |

## Resource sensitivity

For unmeasured suppliers the evidence-based lower bound is **zero useful nitrogen**. The positive cases below are deliberately illustrative, not confidence intervals or measured ore grades. For unvisited suppliers the base case borrows the existing model's 0.24 wt% N and 70% recovery; it does not assign those values as observations of other asteroids. Carbonaceous taxonomy and hydration do not establish nitrogen abundance.

For unvisited bodies the lower positive scenario uses 0.8× diameter, 1.0 t/m³, 0.05 wt% N and 50% recovery; the higher uses 1.2× diameter, 1.6 t/m³, 0.25 wt% N and 90% recovery. Both retain the model's 6.4 wt% available-water assumption and enforce the smaller of N and water capacity. These water assumptions also need validation. For Bennu/Ryugu, diameter and density stay fixed. Bennu uses 0.23 / 0.24 / 0.25 wt% N (Glavin et al. 2025); Ryugu uses 0.1437 / 0.1454 / 0.1471 wt% N (Yokoyama et al. 2025, Table 1). The Ryugu interval is the published ±2σ uncertainty on the sample-based mean, not a bound on the whole asteroid. Both bodies use 50 / 70 / 90% industrial recovery, an assumption separate from the sample measurements. Ryugu's base capacity is consequently ~54 small tori rather than ~89 under the common Bennu-like proxy. The wider habitat model retains that common proxy; only this network comparison uses body-specific N. Extracting soil organics/other nutrients, excavation accessibility and maintaining a residual asteroid are outside this capacity calculation.

| Supplier | Catalogue D km | Evidence | 900 m tori: lower positive / base / higher | 1.6 km tori: lower positive / base / higher |
|---|---:|---|---:|---:|
| 101955 Bennu (1999 RQ36) | 0.484 | sample return | 9.6 / 14.0 / 18.8 | 1.8 / 2.6 / 3.4 |
| 162173 Ryugu (1999 JU3) | 0.896 | sample return | 38.0 / 53.8 / 70.0 | 7.0 / 9.9 / 12.8 |
| 162741 (2000 WG6) | 3.94 | dark only; N unknown | 485.1 / 7576.4 / 23574.9 | 88.9 / 1389.0 / 4322.0 |
| 175706 (1996 FG3) | 1.2 | C spectrum; N unknown | 13.5 / 211.1 / 656.9 | 2.5 / 38.7 / 120.4 |
| 190161 (2005 TJ174) | 3.04 | C colours only; N unknown | 222.2 / 3470.3 / 10798.4 | 40.7 / 636.2 / 1979.7 |
| (2002 BM26) | 0.84 | P/X spectrum; N unknown | 4.7 / 73.1 / 227.6 | 0.9 / 13.4 / 41.7 |
| (2005 QL) | 1.85 | dark only; N unknown | 49.8 / 777.5 / 2419.4 | 9.1 / 142.5 / 443.6 |
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
| 275611 (1999 XX262) | 1.48 | B spectra; tentative Ch feature | 25.8 / 402.5 / 1252.4 | 4.7 / 73.8 / 229.6 |
| 410777 (2009 FD) | 0.472 | C/Ch spectrum; N unknown | 0.8 / 13.0 / 40.4 | 0.2 / 2.4 / 7.4 |
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
2. Treat Torifune and Itokawa as nursery candidates rather than automatically extrapolating to an indefinitely growing cluster. Keep all mass estimates separate from measured free-metal abundance.
3. Obtain or reanalyse spectra for the low-cost dark candidates before resource planning; for XX262, confirm the weak hydration feature and measure the 3 µm region. No unvisited candidate here has a verified recoverable-nitrogen inventory.
4. Re-run the selected routes with low-thrust trajectories, propulsion/power/dry-mass constraints, full launch intervals and supplier throughput. Include multi-revolution arcs and perturbations along the transfer itself. The current model uses integrated endpoint states but a two-body transfer arc.
5. Assess mining mechanics separately: spin, binaries, gravity, anchoring and excavation can distinguish otherwise similar orbits. 1991 VH is a binary and a fast rotator; low seasonal variation does not make its surface operations easy.

## Validation

The logistics and network tests cover a circular-orbit Lambert solution, the Hohmann transfer, resource bottlenecks, orbital sunlight, opportunity unions and the flight-time bounds. The saved endpoint checks independently query Horizons at the exact optimized dates for XX262 → Eros, AM24 → 1991 VH and 2010 CG18 → 2001 QQ142. They test interpolation and object identity, not global optimality or a full perturbed transfer. See `logistics_model/data/network_endpoint_checks.json` for the states and numerical differences.

## Reproduce

```bash
python -m logistics_model.networks --fetch
python -m logistics_model.networks --screen --spectral
python -m logistics_model.networks --fetch-vectors --fetch-evidence
python -m logistics_model.networks --windows
python -m logistics_model.networks --verify
python -m logistics_model.networks --report
python -m unittest tests.test_networks tests.test_logistics
```

Use --fetch-vectors to resume missing bodies without changing the acquisition dates of cached data. Use --refresh-vectors to fetch every selected body again, then --windows to recompute routes. Screen caches are matched to hashes of their host/supplier inputs, and dated windows to a hash of the ephemeris bytes. The report rejects stale inputs/results. Only --fetch, --fetch-vectors, --refresh-vectors, --fetch-evidence and --verify need network access. The dated selection is the central-estimate Pareto front plus the named reference/comparison hosts, each with its three lowest refined costs, best screened spectral C-complex supplier, Ryugu, Bennu and Earth. Snapshots contain the exact selection and results. Start a fresh --screen by removing `network_screen.json`; an interrupted run resumes its saved hosts.

Sources: [JPL SBDB query API](https://ssd-api.jpl.nasa.gov/doc/sbdb_query.html), [SBDB object API](https://ssd-api.jpl.nasa.gov/doc/sbdb.html), [Horizons API](https://ssd-api.jpl.nasa.gov/doc/horizons.html), [SsODNet](https://ssp.imcce.fr/webservices/ssodnet/). Sample N sources: [Glavin et al. 2025](https://doi.org/10.1038/s41550-024-02472-9), [Yokoyama et al. 2025, Table 1](https://doi.org/10.2343/geochemj.GJ25002). The complete habitat demand comes from the current checked-in `habitat_model/assumptions.toml`; all resource assumptions remain provisional.
