# Structural model (plan §2), first part

The parts of plan §2 that need no finite-element model: the wire, the tangent-chord net and the spin-up of a partial ring. It uses the system model (`habitat_model`) for the rim mass and geometry.

```bash
python -m structure_model                       # full report
python -m structure_model --anchor-spacing 20 --mismatch 0.02 --set wire_stress_mpa=900
```

| File | Contents |
|---|---|
| `wire.py` | strength classes of bridge wire, safety factors, thin-wire strength, relaxation and creep |
| `cable_net.py` | chord geometry, tension along a chord, uniform vs tapered mass, comparison with radial spokes, bowing |
| `spinup.py` | single-laced end zones of a partial ring, a local estimate of its joint tension, axis offset from a mass mismatch |
| `net_statics.py` | assembled statics of a ring or of two opposite arcs: one tension per chord, rigid segments, sliding / pinned / locked joints, tension-only chords, residual check |

## Findings

### Wire: ~1 GPa working stress is reachable, at the low end of bridge safety factors

- **Strength.** Suspension-bridge wire (~5 mm) comes in guaranteed classes of 1,570, 1,770 and 1,960 MPa, with a 0.2% proof stress of at least 75% of the guaranteed strength [Tokyo Rope]. Akashi Kaikyō used 1,765 MPa wire (180 kgf/mm², up from the usual 160) [JSCE 1995; FHWA]. Thinner wire is stronger: tire cord reaches ~3.2–3.5 GPa and saw wire ~4 GPa [encyclopedia.pub; Kobelco], and Bekaert's empirical high-strength threshold rises from ~1,460 MPa at 5 mm to ~2,250 MPa at 1 mm [US 4,854,032].
- **Safety factor.** Existing US bridge cables call for action below a factor of 2.15 (NCHRP Report 534, as applied in an Ohio DOT evaluation that found 2.41–2.44) [Ohio DOT 2013]. A Japanese study found cables designed with a factor of 2.0 on live loads still resist large earthquakes, and another proposes a cable factor of 1.8 in a load-factor format [JSCE 1996, 2002]. The design factors of ~2.5 for new cables and ~2.2 for Akashi-class spans are commonly quoted but weren't verified here: NCHRP 534 itself (onlinepubs.trb.org) couldn't be reached from this session.
- **So:** 1 GPa is a factor of ~1.96 on the strongest bridge class, at the low end of practice; or a factor of ~2.25 on ~1 mm wire. The spin load is static and well known, and the spokes are in vacuum (no corrosion, no hydrogen embrittlement), which argue for a lower factor than bridges, which carry traffic and weather. **The design need not change**, but the factor of safety is now a design decision to record: ~1 GPa means SF ~2 on bridge wire, or thinner wire.
- **Range in the system model** narrowed from 700–1,200 to **800–1,200 MPa**: 1,770 MPa wire at SF 2.2 to ~1 mm wire at SF ~1.9.

### Wire chemistry: the carbonyl route matters

- High-carbon wire steel tolerates very little phosphorus, sulfur or nickel: tire-cord patents limit P to ≤ 0.02%, S to ≤ 0.015% (preferably < 0.008%) and Ni to ≤ 0.05%; phosphorus embrittles the grain boundaries and sulfur forms MnS inclusions that break wires during drawing [wire-rod and metal-cord patents; Kobe Steel study; limits from search summaries]. Small Ni additions (0.05–0.8%) can help drawability, but ≥ 0.05% Ni has been reported to suppress the pearlite transformation in patenting.
- Chondritic metal is far outside that: with the notes' H-chondrite values (~1.6% Ni in the rock, ~17% free metal), the metal holds ~9% Ni, more in L and LL metal, plus phosphorus (phosphides) and sulfur (troilite) nearby.
- **So the spokes depend on refining**, not on the metal grains as mined. The carbonyl process the notes propose (§5a, §14) does it: nickel leaves at low pressure, and carbonyl iron is very pure (reduced grades > 99.5% Fe, < 0.1% C, < 0.01% N, < 0.5% O), because the pentacarbonyl itself is distilled clean [carbonyl-iron patents]. Pearlitic wire is then carbonyl iron + ~0.8% C, with a little Mn and Si for patenting, like ordinary bridge wire. No literature on drawing wire from meteoritic Fe-Ni directly was found; the Earth test (plan §8) should use carbonyl-refined iron and, for comparison, the as-separated metal.

### Creep: plan for ~0.5–1.3 m of stretch

Cold-drawn wire relaxes ~5% in 1,000 h at half its strength (r = 30 f/f_u − 10%), and about twice that in the long term [BME Periodica Polytechnica]. Read as creep under constant load, a spoke at 1 GPa on 1,960 MPa wire stretches by ~0.2 m (400 m torus), ~0.5 m (900 m), ~0.85 m (1.6 km) and ~1.3 m (2.5 km) over the long term. The "compliant joints" of the notes therefore need adjustable lengths of order a metre, or the chords must be pre-stretched.

### Tangent-chord net: same mass as radial spokes; taper barely helps

- A chord at angle θ to the radial (sin θ = c/r) pulls the rim at only cos θ, but its length per anchor is r cos θ instead of r, so the mass is the same as radial spokes: **within 0.06%** at every size, not the ~0.2% loss the notes estimate. The system model's spoke formula therefore holds for the net.
- With 1.1 × the hub radius as the tangent circle, θ ≈ 4.3° at every size (the geometry is self-similar), as in the notes.
- **Tapering** the chords to uniform stress saves only 1.2% at 900 m, 2.2% at 1.6 km and 3.6% at 2.5 km; uniform cables are fine.
- **Bowing.** The across-chord component of the spin load (ω² c) bows each chord away from the axis by ρω²cL²/2σ: ~2.3 m at 900 m, ~7 m at 1.6 km, ~18 m at 2.5 km. The window for the hub and factory grows by that much; the chords cross at their bowed positions.
- At one anchor every 10 m, each chord end carries ~105 MN at 900 m and ~180 MN at 1.6 km. A **uniform** chord needs ~1,080 cm² at 900 m (a cable ~37 cm across) and ~1,920 cm² at 1.6 km, sized at mid-chord where its own spin load adds most; ~1,050 / ~1,800 cm² is only the end area of a tapered chord.

### Spin-up of a partial ring (provisional)

- A chord's far end lands 2θ r off the point opposite (134 m at 900 m, 238 m at 1.6 km). Two opposite arcs therefore each have a **single-laced zone of 2θ r at each end**, where anchors keep only the chord whose far end lands on the other arc. Every anchor has a chord only if each arc spans more than 4θ r: ~270 m at 900 m (about five 56 m segments, ~0.56 Mt with rock), ~480 m at 1.6 km.
- **Assembled statics** (`net_statics.py`): each chord is one elastic member with a single tension, the rim is cut into rigid segments, and the joints are springs, *sliding* (free along the rim, shear only), *pinned* (tension and shear) or *locked* (also bending). Slack chords are dropped, and each segment's force and moment balance is checked (residuals ~1e-5 or better). It reproduces the finished net: with sliding joints, chord tensions within ±4% of the formula (the spread is the discrete anchor positions). A first, local estimate (`spinup.partial_arc`) assigned tensions anchor by anchor, so one cable could carry different tensions at its two ends; it is kept only as a cross-check of the joint tension.
- **The chords carry twice their finished load on the shortest arcs.** With locked joints every chord of a ~4θ r arc pulls ~2× its finished tension: ~2,000 MPa at full spin in cables sized for 1 GPa. Stresses scale with spin², so **this stage must stay below ~0.71 of the final spin rate** (at every size), or use extra cables, or hang longer arcs (0.83 at ~1.5 × 4θ r, 0.92 at ~3 ×, at 900 m).
- **The joints carry tension and bending until the ring closes.** ~0.9–1% of a full ring's hoop force on the shortest arcs (~176 MN at 900 m at full spin, ~550 MN at 1.6 km), close to the local estimate's 1.1%, plus a moment (~6 GN·m at 900 m). Longer locked arcs carry less chord load but much larger moments (~70 GN·m at 1.5 × 4θ r, ~220 GN·m at 3 × at 900 m): with rigid segments that depends heavily on the model, and it is the case for the finite-element model.
- **Sliding joints can't hold a partial ring** (no equilibrium: the end segments have nothing to resist their pull along the rim), and pinned joints only some arc lengths. So the joints must be locked during construction.
- **And released once the ring is closed:** with locked joints the closed ring behaves as a hoop and the hull takes ~64% of the load at 900 m (~50% at 1.6 km) in this model, as the notes warn (strain compatibility). The joints must slide along the rim after closure, or the spokes be made stiffer.
- **Imbalance:** the stack spins freely about its centre of mass, so a mismatch between paired arcs shifts the spin axis away from the assembly's geometric centre rather than loading a bearing: ~3.6 m for a 1% mismatch on the first pair of 900 m arcs, ~7.5 m at 2.5 km. The hub and the net move together, so this is not a loss of clearance between them; their relative motion needs the stabilising lines' stiffness, still open.

## Still open in plan §2

- Finite-element model of one tube segment (rock cells, double skin, floor fill, hung ceiling cells; 1 g and 70 kPa) to check the r^2.3 hull-and-frames estimate. sfepy is available from PyPI here as a source package (it needs compiling); a small purpose-built shell model in numpy is the alternative.
- The hub held in the net by stabilising lines (its motion relative to the net under imbalance), and the net's stiffness for the stack dynamics (plan §4).
- Fatigue: the spin load is static; the cyclic loads (rim trains, ballast transfers, day/night temperatures) are small and belong with the stack dynamics.

## Sources

- Tokyo Rope, suspension-bridge wire catalogue — strength classes, proof stress at 75% of the guaranteed strength: https://www.tokyorope.co.jp/english/product/catalog/pdf/scs.pdf
- JSCE (Doboku Gakkai Ronbunshu) 1995 — Akashi Kaikyō wire at 180 kgf/mm²: https://www.jstage.jst.go.jp/article/jscej1984/1995/528/1995_528_57/_article/-char/en
- FHWA Public Roads (1998), the world's longest bridges — Akashi's 180 vs 160 kgf/mm² wire: https://webarchive.library.unt.edu/eot2008/20090117161258/http:/www.tfhrc.gov/pubrds/julaug98/worlds.htm
- Nippon Steel, XSTEELIA — Akashi cable with 1,770 vs 1,960 MPa wire (50,000 vs 45,000 t): https://www.nipponsteel.com/en/steelinc/product/xsteelia/environmental.html
- Ohio DOT, 2013 cable strength evaluation report — NCHRP 534 action level 2.15, measured 2.41–2.44: https://ftp.dot.state.oh.us/PUB/Districts/D02/Programmatic/September%202025/LUC-116431%20%20LUC-2-18.62%20NSTM%20Inspection%20and%20Load%20Rating/2013%20Cable%20Strength%20Evaluation%20Report.pdf
- NCHRP Report 534 (not reachable from this session): https://www.trb.org/NCHRP/Blurbs/163301.aspx
- JSCE 1996 — safety factor 2.0 on live loads, earthquake resistance: https://www.jstage.jst.go.jp/article/jscej1984/1996/549/1996_549_43/_article/-char/en
- JSCE 2002 — proposed partial factors, cable γC = 1.8: https://www.jstage.jst.go.jp/article/jscej1984/2002/717/2002_717_161/_article/-char/en
- Kobelco Technology Review No. 30 — tire cord strength trend, saw wire ~4,000 MPa: https://www.kobelco.co.jp/english/ktr/pdf/ktr_30/062-065.pdf
- Encyclopedia.pub, automobile tire steel wire — super-tensile cord 3,200–3,500 MPa: https://encyclopedia.pub/entry/download_pdf/5cf696261fe7f74cc52b5a785d3884f5
- US 4,854,032 (Bekaert) — high-tensile wire by drawing pearlite; R = 2250 − 1130 log d: https://patents.google.com/patent/US4854032
- Spring steel wire patent — P ≤ 0.015%, Ni 0.05–0.8% helps drawability: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8192562
- Metal-cord steel patents, from search summaries (which of them carries the S < 0.015% and Ni ≤ 0.05% limits wasn't checked; patents.google.com isn't reachable from this session): https://patents.google.com/patent/US3984238, https://patents.google.com/patent/US4176513A/de
- The influence of phosphorus and sulphur on the deformability of high-carbon wire (Kobe Steel): https://wirenet.org/product/the-influence-of-phosphorus-and-sulphur-contents-on-the-plastic-deformability-of-high-carbon-steel-wire/
- Steel wire rod patent — ≥ 0.05% Ni suppresses pearlite in patenting: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9255306
- Carbonyl iron silicide powder patent — reduced carbonyl iron > 99.5% Fe, < 0.1% C, < 0.01% N: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6309620
- Periodica Polytechnica (BME) — relaxation of cold-drawn wire, r% = 30 f0/fpt − 10, final ≈ 2 × 1,000 h: https://pp.bme.hu/ci/article/download/4056/3161/7814
