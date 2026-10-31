# Finite-thrust trajectories and a dated shipping schedule

First computational study, 31 October 2026. Feasible trajectories and schedules are conditional on the assumed freighter hardware and refuelling infrastructure. This is not a flight-ready mission or a proof of the optimal supplier, fleet, propulsion system or construction schedule. 2030–2050 are illustrative orbital epochs, not a proposed habitat construction timeline.

## Assumptions

A ship delivers 1 kt of mixed N₂, water and organics. Its dry mass is 200 t, including the array, power electronics, propulsion and tanks. It has 20 MW at 1 AU, capped at that electrical power inside 1 AU and falling as 1/r² outside. These hardware numbers are guesses, not sourced mass budgets. The assumed dry mass is held equal between propulsion cases for comparison; no mass-driver hardware design or containment/handling system for its large propellant loads is established.

Electric propulsion: 30 km/s exhaust, 65% electrical-to-jet efficiency. The hypothetical onboard residue mass driver: 3 km/s, 50%. Both may load up to eleven times their delivered vehicle-plus-payload mass in propellant. Every departure refuels locally: the supplier provides outbound propellant, Eros provides return propellant. Producing and storing compatible propellant at both ends is an explicit infrastructure assumption, not a demonstrated capability. Tank capacity is not separately constrained.

One 900 m torus per ten years consumes 10.59 kt of shipped products per year. Demand is continuous and constant, not exponential cluster growth. Ships begin at their supplier; unloading/refuelling and return loading each take 30 days. Initial cargo stock at Eros is supplied before the horizon, outside this schedule. There are no construction-line, supplier mining/processing, propellant production, docking or launch-rate limits, losses, spares, hotel power or contingency reserves. Aggregate cargo is treated as fungible; individual commodity inventories and fuel reserves still need a coupled source-processing model.

Ryugu is the sampled chemical reference. XX262's recoverable nitrogen remains unmeasured; its shipments are conditional on useful resources being established. See the [composition evidence audit](asteroid-evidence.md). Cargo capacity and propellant production are not deducted from supplier inventories in this study.

## Trajectory method and acceptance

Backward direct shooting from the arrival state, with constant inertial throttle vectors in equal-duration segments; Sun gravity, variable mass, and distance-dependent solar power. A feasibility phase starts from a zero-thrust guess, before SLSQP minimises initial mass at fixed dates, with rendezvous constraints and throttle norm ≤1. Backward mass flow stays positive during optimisation. The arrival target carries a 0.1% numerical fuel reserve above dry vehicle and cargo; real contingency reserves are additional. A final feasibility projection can refine the constraints. Near-feasible controls can also be corrected against adaptive backward integration before the final independent forward check, removing RK4 error near the power-cap corner. Integrated Horizons states define the endpoints; planetary forces along the flight, gravity assists and close approaches are not modelled. The dynamics can make multiple revolutions, but the search does not enumerate revolution families.

The equations are `F_max = 2 η P / v_e`, `dm/dt = -F_max |u| / v_e`, and `dv/dt = -μ r / |r|³ + F_max u / m`, with `|u| ≤ 1`. For fixed exhaust speed and efficiency, flight electricity is `m_propellant v_e² / (2 η)`. Unused arrival fuel is not counted as consumed propellant or as cargo.

Each result is reintegrated with adaptive DOP853, segment by segment, independently of the RK4 used in optimisation. It must arrive within 10 km and 0.1 m/s, stay above 0.5 AU, respect throttle within 1e-7 and retain the required delivered mass within 1e-7 of it. These are screening tolerances, not docking requirements. Feasible iteration-limited results are retained as upper bounds; objective convergence is recorded separately and does not establish global optimality. Failed solves are recorded as 'not found', not as proof that a route is impossible.

Only a sparse menu is searched: three promising departure dates per source, seeded by local minima of a 5-day impulsive scan with 240–720-day flights, refined within 60–900 days, dates separated by ≥500 days, and one alternative duration 90 days longer if needed. Return seeds are searched after the outbound arrival and turnaround, up to five years later. This does not compare all possible off-window departures, low-thrust windows, payloads, power levels or exhaust speeds.

Method references: [ESA zero-order-hold low-thrust transcription](https://esa.github.io/pykep/trajopt.html), [SciPy SLSQP](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html), [SciPy solve_ivp / DOP853](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html). This implementation uses SciPy, not pykep.

## Verified reusable cycles

Return arrivals are followed by the source turnaround before a ship is available again. Electrical energy and propellant below include both flights. Energy to manufacture propellant or process cargo is additional.

| Supplier / propulsion | Cargo departure | Delivery | Return departure | Ready at supplier | Flight propellant kt | Flight electricity PJ |
|---|---|---|---|---|---:|---:|
| Ryugu / electric | 2031-07-28 | 2032-07-07 | 2036-01-05 | 2036-11-20 | 0.44 | 0.302 |
| Ryugu / electric | 2036-03-04 | 2036-11-04 | 2041-02-15 | 2042-02-06 | 0.45 | 0.313 |
| Ryugu / electric | 2041-03-09 | 2042-02-12 | 2046-02-08 | 2047-04-09 | 0.52 | 0.359 |
| Ryugu / residue mass driver (hypothetical) | 2031-07-28 | 2032-07-07 | 2036-01-05 | 2036-11-20 | 9.12 | 0.082 |
| Ryugu / residue mass driver (hypothetical) | 2036-03-04 | 2036-11-04 | 2041-02-15 | 2042-02-06 | 12.95 | 0.117 |
| 1999 XX262 / electric | 2036-01-08 | 2038-05-22 | 2038-06-21 | 2039-09-09 | 1.97 | 1.365 |
| 1999 XX262 / electric | 2037-12-02 | 2040-02-18 | 2040-03-19 | 2041-07-27 | 1.35 | 0.937 |
| 1999 XX262 / electric | 2039-10-20 | 2041-08-14 | 2043-03-08 | 2044-07-18 | 0.61 | 0.419 |
| 1999 XX262 / residue mass driver (hypothetical) | 2036-01-08 | 2038-02-21 | 2043-03-08 | 2044-07-18 | 13.97 | 0.126 |
| 1999 XX262 / residue mass driver (hypothetical) | 2037-12-02 | 2040-02-18 | 2040-03-19 | 2041-07-27 | 15.40 | 0.139 |
| 1999 XX262 / residue mass driver (hypothetical) | 2039-10-20 | 2041-08-14 | 2043-03-08 | 2044-07-18 | 13.87 | 0.125 |

## Fleet and host-stock trade-offs

An integer linear programme allocates voyages to the verified cycles. A ship cannot depart again before its return and turnaround; explicit ship IDs verify the allocation. Host inventory is checked immediately before every delivery and at horizon end. Final stock must be at least initial stock, so a large initial stock cannot hide a net shipping deficit. First minimise initial stock, then voyages, then flight electricity among the remaining ties. Tie-break solver statuses are saved. 'Not supported' means this fleet cannot meet the stated demand on this sparse menu, not that no better schedule exists. No inference is made beyond 2050.

| Supplier / propulsion | Ships | Installed electrical power at 1 AU GW | Voyages | Initial host stock kt | Delivered kt | Flight electricity PJ |
|---|---:|---:|---:|---:|---:|---:|
| Ryugu / electric | 60 | 1.20 | Not supported | | | |
| Ryugu / electric | 120 | 2.40 | 212 | 26.6 | 212.0 | 69.36 |
| Ryugu / electric | 240 | 4.80 | 212 | 26.6 | 212.0 | 64.11 |
| Ryugu / residue mass driver (hypothetical) | 60 | 1.20 | Not supported | | | |
| Ryugu / residue mass driver (hypothetical) | 120 | 2.40 | Not supported | | | |
| Ryugu / residue mass driver (hypothetical) | 240 | 4.80 | 212 | 26.6 | 212.0 | 17.40 |
| 1999 XX262 / electric | 60 | 1.20 | Not supported | | | |
| 1999 XX262 / electric | 120 | 2.40 | 212 | 88.8 | 212.0 | 175.86 |
| 1999 XX262 / electric | 240 | 4.80 | 212 | 88.8 | 212.0 | 115.12 |
| 1999 XX262 / residue mass driver (hypothetical) | 60 | 1.20 | Not supported | | | |
| 1999 XX262 / residue mass driver (hypothetical) | 120 | 2.40 | Not supported | | | |
| 1999 XX262 / residue mass driver (hypothetical) | 240 | 4.80 | 212 | 86.2 | 212.0 | 26.50 |

## Dated deliveries for the smallest supported tested fleet

These are actual allocations from the integer schedule, not merely candidate launch windows. The smallest feasible fleet among the three tested sizes is shown; this is not the minimum fleet over all possible trajectories. Stock values are immediately before and after each delivery. Ship identities and return availability are saved in the JSON.

| Supplier / propulsion | Fleet ships | Ships sailing | Cargo departure | Delivery | Cargo kt | Host stock before / after kt |
|---|---:|---:|---|---|---:|---:|
| Ryugu / electric | 120 | 120 | 2031-07-28 | 2032-07-07 | 120.0 | 0.0 / 120.0 |
| Ryugu / electric | 120 | 92 | 2041-03-09 | 2042-02-12 | 92.0 | 18.3 / 110.3 |
| Ryugu / residue mass driver (hypothetical) | 240 | 212 | 2031-07-28 | 2032-07-07 | 212.0 | 0.0 / 212.0 |
| 1999 XX262 / electric | 120 | 92 | 2036-01-08 | 2038-05-22 | 92.0 | 0.0 / 92.0 |
| 1999 XX262 / electric | 120 | 120 | 2039-10-20 | 2041-08-14 | 120.0 | 57.8 / 177.8 |
| 1999 XX262 / residue mass driver (hypothetical) | 240 | 37 | 2036-01-08 | 2038-02-21 | 37.0 | 0.0 / 37.0 |
| 1999 XX262 / residue mass driver (hypothetical) | 240 | 175 | 2039-10-20 | 2041-08-14 | 175.0 | 0.2 / 175.2 |

## Numerical record

28 trajectory attempts, 22 independently accepted. 22 accepted legs did not converge the mass objective; their costs are feasible upper bounds. The JSON saves every control vector, engine setting, epoch, mass, optimizer status, verification error and selected ship ID. Input hashes cover code, settings, cargo demand and the saved orbital data; stale reports are rejected.

## Reproduce

```bash
python -m pip install -r requirements.txt
python -m logistics_model.shipping_study --solve --report
python -m unittest tests.test_shipping
```

Solving uses saved ephemerides and no network. Individual trajectory attempts are cached by solver/data/numerical settings plus leg parameters; changing fleet sizes or report text can reuse them. Older feasible controls are reused only after revalidation against current dynamics and endpoints, labelled as upper bounds rather than a new converged optimisation. Failed attempts are not reused after an optimiser change. The full report also validates the study code, settings and demand. --report alone is fast. This closes a first finite-thrust and dated-fleet modelling step; it leaves hardware sizing, propellant sourcing, denser launch searches, source throughput, reserves and uncertainty sweeps open.
