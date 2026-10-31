# Evidence behind the asteroid shortlist

Research checked on 31 October 2026. This audit separates surface classification, hydration, size and recoverable bulk resources. A spectral class does not establish an industrial nitrogen yield. The companion [network report](asteroid-networks.md) gives the calculations and sensitivity cases.

## Findings that change the shortlist

### 2011 AM24: more than a dark catalogue entry

The transport screen identifies (778852) 2011 AM24 as a low-cost supplier candidate for several hosts, notably 1991 VH. SBDB's spectral fields are empty in the saved catalogue, but published observations exist.

- Perna et al. (2018) report an unusual visible spectrum, tentatively D-type; it does not fit the standard templates well enough for them to retain it in the population analysis. This is a reason for follow-up, not a secure C-type label.
- The EPSC 2026 PRIAMOS team identifies 2011 AM24 as its baseline sample-return target for an ESA M8 mission proposal, citing its approximately 500 m size, low albedo and suitable transfers. A proposal is not a selected or flown mission, and its Earth-return trajectory analysis does not validate our host transfers.
- Goldstone's July 2024 observations provide an independent size check: delay-Doppler images suggest a rounded object with an equatorial diameter of about 500–600 m, consistent with NEOWISE's approximately 0.51 km value. Equatorial diameter is not a measured volume-equivalent diameter or mass.

This object deserves near-infrared/3 µm characterization and a nitrogen-sensitive sample analysis. It is a better-supported research target than the empty spectral field suggests, but remains an unverified resource.

Sources: [Perna et al., PSS 157, 82–95 (2018)](https://www.astrofit2.inaf.it/wp-content/uploads/2018/07/Perna2018A.pdf), [Mahlke et al., EPSC2026-482, PRIAMOS target identification](https://meetingorganizer.copernicus.org/EPSC2026/EPSC2026-482.html), [Goldstone observations, July 2024](https://echo.jpl.nasa.gov/asteroids/july2024.goldstone.planning.html).

### 1991 VH: mineralogy is known better than its SBDB label suggests

The saved SBDB record labels (35107) 1991 VH Sk. Le Corre et al. (2023) reclassify it as Sq and find mineralogy consistent with LL ordinary chondrites. LL is therefore the evidence-backed metal-yield scenario; the report's L column is an alternative, not a claim about this body.

Goldstone's 2025 summary describes a roughly kilometre-sized primary rotating in 2.62 hours, a secondary about 0.4 km across, and a binary period around 32.6 hours. Radar/lightcurve models give primary sizes around 1.1–1.2 km, compared with the saved NEOWISE-based SBDB diameter of 0.929 km. The network table deliberately retains the SBDB size for reproducibility and uses a 2 t/m³ proxy, not a claimed measured inventory. This conservative-looking proxy does not remove the uncertainty in extraction and free-metal yield. A literature mass/shape model should replace it before engineering use.

Sources: [Le Corre et al., PSJ 4, 91 (2023), author abstract](https://experts.arizona.edu/en/publications/mineralogical-characterization-and-phase-angle-study-of-two-binar/), [doi:10.3847/PSJ/acd10d](https://doi.org/10.3847/PSJ/acd10d), [Goldstone 2025 observations and physical summary](https://echo.jpl.nasa.gov/asteroids/1991vh.2025.goldstone.planning.html).

### 1999 YB: attractive orbit, uncertain capacity

(137799) 1999 YB has eccentricity about 0.075. Its mild orbital seasons are real orbital evidence; its capacity for habitats is much less certain. The saved SBDB record has Sq spectra but no diameter. The table therefore uses H at an assumed albedo of 0.23, and marks the result as estimated. It must not be presented as a measured approximately 0.49 km object. H/albedo-derived sizes and uncertain density make its metal inventory a characterization priority.

Hasegawa et al. (2018) also discuss it as a low-eccentricity, non-planet-crossing object between Earth and Mars. That does not establish long-term stability of an industrial settlement, for which numerical integrations and eventual perturbations from excavation/operations remain separate questions.

Sources: [JPL SBDB](https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=137799), [Hasegawa et al., PASJ 70, 114 (2018)](https://doi.org/10.1093/pasj/psy119).

### 2015 AY245: a T-type spectrum exists

This candidate appears as dark-only in SBDB's saved spectral fields, but Perna et al. (2018), Table 1, classify its visible spectrum T. Keep it as a primitive/dark candidate with unknown hydration and nitrogen, not a confirmed C-type or a proven volatile mine.

Source: [Perna et al. (2018), Table 1](https://www.astrofit2.inaf.it/wp-content/uploads/2018/07/Perna2018A.pdf).

## 1999 XX262: hydration and size remain uncertain

The Mahlke et al. (2022) classification table has one entry for (275611) 1999 XX262. Its spectral reference 57 maps to Popescu et al. (2019). The M4AST observation entry is `1999XX262_20140903_950_00`: 3 September 2014. Thus Ch is a reanalysis of existing observations, not an independent new observation confirming hydration.

The published table flags the h feature present, centred at 0.6924 µm with a feature signal-to-noise ratio of 1.4446. The underlying spectral-class probabilities are about 59% C and 41% B; these are not probabilities that water is present. Mahlke's method flags a feature above S/N 1, with visual confirmation; the paper warns that the automatic threshold alone yields many false positives. Popescu identify XX262 as B and do not report it among their explicit hydration-band detections. The appropriate description is a carbonaceous asteroid with a tentative visible hydration feature. Its bulk recoverable water and nitrogen are unknown.

The source diameter records behind SsODNet include:

| Study | Thermal-model diameter km | Albedo |
|---|---:|---:|
| Mainzer et al. 2011 | 2.426 ± 0.178 | 0.025 |
| Nugent et al. 2016 | 1.48 ± 0.01 | 0.040 |
| Masiero et al. 2020, first fit | 1.23 ± 0.45 | 0.074 |
| Masiero et al. 2020, second fit | 1.47 ± 0.49 | 0.051 |
| Masiero et al. 2021 | 1.49 ± 0.70 | 0.046 |

The 0.01 km formal uncertainty excludes the full thermal-model uncertainty. Nugent et al. estimate about 20% diameter uncertainty against independent methods. Do not inverse-variance combine the formal errors as independent complete uncertainties. The larger 2011 fit used a substantially different fitted beaming parameter; selecting which result is more reliable needs an analysis of geometry, photometry and thermal-model assumptions. The network base uses 1.483 km; 2.426 km is a separate approximately 4.4× volume sensitivity case.

NASA's PDS lists a Spitzer observation, but the original numerical NEOSurvey table could not be retrieved during the earlier investigation. No independently checked Spitzer fit is used here to adjudicate the size disagreement. Marsset et al.'s near-infrared thermal-tail fit should likewise not replace a dedicated radiometric diameter analysis.

Sources: [Popescu et al. (2019)](https://doi.org/10.1051/0004-6361/201935006), [Mahlke et al. (2022)](https://www.aanda.org/articles/aa/pdf/2022/09/aa43587-22.pdf), [Mahlke classification data](https://github.com/maxmahlke/classy/tree/main/data/mahlke2022), [M4AST observation index](https://github.com/maxmahlke/classy/blob/main/data/m4ast/m4ast.csv), [SsODNet source diameter records](https://ssp.imcce.fr/webservices/ssodnet/api/datacloud.php?-name=id:1999_XX262&-resource=diamalbedo&-mime=json), [Nugent et al. (2016)](https://doi.org/10.3847/0004-6256/152/3/63), [PDS Spitzer observation catalogue](https://pdssbn.astro.umd.edu/data_other/Spitzer.shtml).

## Remaining evidence limits

- **2001 WT1, 2015 DX198, 2014 BS32 and other dark candidates:** no resource claim follows from this screen. Where no spectrum is identified in the saved records or this focused audit, the report says the evidence is limited, not that no spectrum can exist anywhere.
- **1988 XB:** B-class spectroscopy and radar observations exist. B does not establish a Bennu-like nitrogen abundance. H-derived diameters at a default dark albedo need checking against physical measurements before inventory allocation.
- **Torifune:** SBDB's old spectral L label and missing diameter illustrate catalogue lag. Pre-flyby characterization reports a volume-equivalent diameter around 0.44 ± 0.06 km; subsequent flyby imaging reports different dimensions. The report retains an explicitly marked H-based proxy rather than mixing an average projected dimension with volume. The existing project mass is not independently validated by this screen.
- **Bennu/Ryugu:** samples provide strong chemical evidence, but industrial recovery efficiency and asteroid-wide representativeness remain assumptions. The network base applies the existing model's composition proxy consistently; it does not infer that every B/C/D/T object shares it.
- **Spectral type versus metal yield:** LL/L/H free-metal fractions are ordinary-chondrite model inputs. An S or Sq label alone does not measure recoverable metal. Geological accessibility and extraction recovery can reduce the tabulated material capacities.

Additional sources: [1988 XB radar summary](https://echo.jpl.nasa.gov/asteroids/1988XB/1988xb.2020.goldstone.planning.html), [Torifune ground-based characterization](https://arxiv.org/abs/2501.15644), [JAXA Torifune flyby information](https://www.isas.jaxa.jp/en/topics/004151.html).
