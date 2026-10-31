"""Lighting architectures compared (plan §7 follow-up): what the pipes cost, and what could replace them.

Each architecture is the same chain as the baseline (`scenes.converged`: lamps → pipes or luminaires →
light box or farm tier, the layout sized for the power its own delivery needs), with its inputs changed:

- **Pipes, shorter or more heavily loaded:** the pipe model as it stands, at another length or W per metre
  (more power per lamp at the ends, fewer pipes, so the light box and tier take back less).
- **Sulfur lamps in the light box (no pipes):** rows of ~1 kW lamps in small reflectors, `lamp_spacing_m`
  apart along each row, behind a deeper diffuser; in the farm, rows over the beds, higher above the canopy.
  The reflector loses 1 − `luminaire_efficiency` of the light and sends back `luminaire_albedo` of what
  falls on it. Their heat is shed in the ceiling's service space (and above each tier) instead of at the
  hub's sources.
- **LEDs (adopted):** strips in the light box and over the beds, white (`lamp_efficacy_umol_j`) in the
  valley and blue + red over the crops (`farm_lamp_efficacy_umol_j`), or white throughout. What making them
  locally takes is in `leds.py`.

The sulfur architectures (the fallback) run at `sulfur_efficacy_umol_j`, or the sector plants' efficacy.

The rows of lamps are traced as continuous line sources, fair once the diffuser (or the canopy) is at least
a lamp spacing away.
"""

from habitat_model import Design, evaluate, load, params

from . import scenes

N = 100_000


def options(p):
    """[(name, overrides, the pipe's own efficiency (None: the pipe model), what it is)]."""
    lamp_row = p.lamp_power_w / p.lamp_spacing_m
    sulfur = {"lamp_efficacy_umol_j": p.sulfur_efficacy_umol_j, "farm_lamp_efficacy_umol_j": 0}
    sector = {"lamp_efficacy_umol_j": p.sector_efficacy_umol_j * p.waveguide_efficiency, "farm_lamp_efficacy_umol_j": 0}
    in_box = {**sulfur, "pipe_coupling": p.luminaire_efficiency, "pipe_albedo": p.luminaire_albedo, "pipe_diameter_m": 0.15,
              "pipe_emit_arc_deg": 180.0, "pipe_w_per_m": lamp_row, "diffuser_gap_m": max(p.diffuser_gap_m, 1.5),
              "farm_pipe_gap_m": max(p.farm_pipe_gap_m, 0.8)}
    led = {"lamp_efficacy_umol_j": p.lamp_efficacy_umol_j, "farm_lamp_efficacy_umol_j": p.farm_lamp_efficacy_umol_j,
           "pipe_coupling": 1.0,   # efficacy measured at the fixture's output: no loss before the light box
           "pipe_albedo": 0.5, "pipe_diameter_m": 0.1, "pipe_w_per_m": p.led_w_per_m}
    short_heavy = {**sulfur, "pipe_length_m": 20.0, "pipe_w_per_m": 600.0}
    return [
        ("Pipes, 40 m at 300 W/m (as first proposed)", sulfur, None, "pairs of ~6 kW lamps, small magnetrons"),
        ("Pipes, 20 m", {**sulfur, "pipe_length_m": 20.0}, None, "pairs of ~3 kW lamps"),
        ("Pipes at 600 W/m", {**sulfur, "pipe_w_per_m": 600.0}, None, "pairs of ~12 kW lamps per 40 m pipe"),
        ("Pipes, 20 m at 600 W/m", short_heavy, None, "pairs of ~6 kW lamps per 20 m pipe"),
        ("Pipes, 20 m at 600 W/m, 915 MHz plants", {**short_heavy, **sector}, None,
         "the same, fed by sector plants through waveguides"),
        (f"~{p.lamp_power_w / 1e3:g} kW lamps in the light box", in_box, 1.0,
         f"rows of lamps {p.lamp_spacing_m:g} m apart in reflectors, small magnetrons, a 1.5 m deep diffuser"),
        (f"~{p.lamp_power_w / 1e3:g} kW lamps in the light box, 915 MHz plants",
         {**in_box, **sector}, 1.0, "the same, fed by sector plants through waveguides"),
        ("LEDs, white throughout", {**led, "farm_lamp_efficacy_umol_j": 0}, 1.0,
         f"strips at {p.led_w_per_m:g} W/m, {p.lamp_efficacy_umol_j:g} µmol/J"),
        ("LEDs, white in the valley, blue + red in the farm (adopted)", led, 1.0,
         f"the farm at {p.farm_lamp_efficacy_umol_j:g} µmol/J (magenta light, no phosphor)"),
    ]


def bulbs(p, q, r, overrides, tiers=3):
    """Installed lamp power (W, the valley at its noon peak and the farm's tiers while lit) and the number
    of bulbs: pipes take a lamp at each end, lamps in the box are `lamp_power_w` each, LEDs none counted."""
    pw = r["power"]
    installed = pw["valley_sky"] * 24 / q.valley_day_h + tiers * pw["farm_per_tier"] * 24 / q.farm_photoperiod_h
    if overrides.get("lamp_efficacy_umol_j") not in (p.sulfur_efficacy_umol_j, p.sector_efficacy_umol_j * p.waveguide_efficiency):
        return installed, None
    size = p.lamp_power_w if overrides.get("pipe_coupling") == p.luminaire_efficiency else q.pipe_w_per_m * q.pipe_length_m / 2
    return installed, installed / size


def evaluate_option(p, overrides, pipe_eff, n=N):
    """The converged chain for one architecture, and its params (deliveries and efficacy in place)."""
    q = params(load(), **{**vars(p), **overrides})
    pr = None if pipe_eff is None else {"efficiency": pipe_eff}
    d = scenes.converged(q, n=n, pipe_result=pr)
    return d, d["params"]


def system(q, radius=900, n_tori=6, tiers=3):
    """The system model's power and array for a design with q's deliveries and efficacy."""
    des = Design(radius_m=radius, n_tori=n_tori, tiers_lit=tiers, host_class="LL", site="Eros", c_partner="Ryugu")
    return des, evaluate(q, des)
