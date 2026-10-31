"""Disturbances on the flexible stack (plan §4): how far they move it, what they put on the rim
links and nets, and how they die out.

- Rim trains: a train of mass m running antispinward at v in a torus's rim tube (radius R) goes
  round at lambda = w - v / R in the inertial frame: a load m R lambda^2 whirling at lambda, below
  the spin and forward, the band where the stack has no modes once it is passively stable (its
  forward modes all beat the spin). At v = w R the train floats at rest in space and pulls on
  nothing.
- Imbalance (ballast, stores, crowds): fixed in the rotating frame, so a load m e w^2 whirling at
  lambda = w; the ballast tanks trim it (notes §5), the worst case is the tanks' full capacity
  (an unbalanced e M at the rim of the end torus, untrimmed).
- Docking: a ship's lateral miss as an impulse at the dock (the hub's first node), followed
  through the damped modes; it turns the stack's angular momentum by Delta H / H, a lasting tilt of
  the axis, and starts a nutation that the dissipation damps.
- Sunlight pressure on the despun array (and the tori's rims, seen edge-on): a force along the
  Sun's line, perpendicular to the axis, at the centre of pressure; its torque turns the axis
  sideways at tau / H. The torque turns with the Sun once an orbit, and with the push falling as
  1 / d^2 Kepler's second law makes it sum to zero over an orbit, eccentric or not: the axis
  only wobbles, by up to 2 tau_a a^2 / (h H) (tau_a at the orbit's semi-major axis a, h its
  specific angular momentum).
- The despun array's bearing: its friction Q acts between array and hub (on the hub against the
  spin, on the array with it). The drive holding the array facing the Sun acts between the same
  two bodies and must cancel Q on the array, so its reaction cancels Q on the hub: compensated, no
  torque is left on the stack, which keeps its spin; the friction only costs the drive's power,
  Q w, as heat. Uncompensated (the drive off, or the bearing seized), friction drags the array up
  to the stack's spin in J_a w / Q, the stack giving up the array's share, J_a / (J + J_a), once:
  the array's own inertia about the axis is all there is to exchange.

Damping: with every forward mode above the spin, no amount of dissipation turning with the stack
destabilises it; dissipation only sets how fast a disturbance dies out (the damped solve's decay
times).
"""

import math

import numpy as np

from . import stack as st

SOLAR_PRESSURE = 4.56e-6       # N/m^2, sunlight absorbed at 1 AU (1361 W/m^2 / c)
ARRAY_PUSH = 1.3               # push over the absorbed value for the array (some reflected, guess)
RIM_PUSH = 1.0                 # the tori's dark rims, absorbing
AU = 1.495978707e11
GM_SUN = 1.32712440018e20
YEAR = 3.15576e7
CENTURY = 100 * YEAR

TRAIN_MASS = 50e3              # kg, one rim train (notes §12)
TRAIN_SPEEDS = (5.0, 10.0, 20.0, 44.0)
SHIP_MASS = 1e7                # kg, a 10 kt freighter (guess)
SHIP_MISS = 0.1                # m/s, its lateral miss at contact (guess; spacecraft dock at ~0.03-0.1)
MAST = 100.0                   # m, the array's mast beyond the stack's end (guess)
BEARING_FRICTION = 1e4         # N m, the despun array's bearing friction (guess; "almost unloaded")


def angular_momentum(s):
    polar = s.hub_polar.sum() + sum(b.polar for b in s.bodies)
    return polar * s.omega, polar


def centre_of_mass(s):
    masses = np.concatenate([s.hub_mass, [b.mass for b in s.bodies], list(s.point_masses.values())])
    zs = np.concatenate([s.hub_nodes, [b.z for b in s.bodies], [s.hub_nodes[i] for i in s.point_masses]])
    return float((masses * zs).sum() / masses.sum())


def loads(s, q):
    """Largest link force, net force and torus offset for a response q (complex amplitudes or one
    instant of a transient)."""
    link = [k_lat * abs(c @ q) for (_, _, k_lat, _), (c, _) in zip(s.links, s.link_vectors())]
    springs = [k * abs(c @ q) for _, _, k, c in s.spring_vectors()]
    tori = [abs(q[s.body_dof(b)]) for b, body in enumerate(s.bodies) if body.name.startswith("torus")]
    return {"link": max(link, default=0.0), "net": max(springs, default=0.0), "torus": max(tori)}


def rim_train(s, geo, torus=0, mass=TRAIN_MASS, speed=20.0):
    """Steady response to one train in torus `torus`'s rim tube (radius r - w)."""
    radius = geo["radius"] - geo["width"]
    lam = s.omega - speed / radius
    f = np.zeros(s.size(), dtype=complex)
    f[s.body_dof(torus)] = mass * radius * lam ** 2
    q = s.response(lam, f)
    return {"speed": speed, "lambda": lam, "force": mass * radius * lam ** 2, **loads(s, q)}


def imbalance(s, geo, mass_e):
    """Steady response to an unbalanced mass_e at the rim of the first torus (fixed in the rotating
    frame), with the axis's tilt at the dock (the stack turning about its tilted principal axis)."""
    f = np.zeros(s.size(), dtype=complex)
    f[s.body_dof(0)] = mass_e * geo["radius"] * s.omega ** 2
    q = s.response(s.omega, f)
    return {"mass": mass_e, "force": mass_e * geo["radius"] * s.omega ** 2,
            "dock_offset": abs(q[0]), "dock_tilt": abs(q[1]), **loads(s, q)}


def docking(s, ship=SHIP_MASS, miss=SHIP_MISS, damping=0.01, spins=40, samples=1600):
    """Transient after a ship's lateral impulse at the dock (the hub's first node): peak loads, the
    axis's lasting turn (Delta H / H) against the rigid estimate, and the nutation's decay."""
    impulse = ship * miss
    m, _, _ = s.matrices()
    v = np.zeros(s.size(), dtype=complex)
    v[0] = impulse / m[0, 0]
    period = 2 * math.pi / s.omega
    times = np.linspace(0, spins * period, samples)
    q = s.transient(v, times, damping=damping)
    peaks = {key: max(loads(s, qi)[key] for qi in q) for key in ("link", "net", "torus")}
    h, _ = angular_momentum(s)
    arm = centre_of_mass(s) - s.hub_nodes[0]
    freq, growth = s.modes(damping=damping)
    # The vibrations only: the rigid tilt (lambda ~ 0) is the axis's lasting turn, not a nutation.
    vibrating = np.abs(freq) > 1e-3 * s.omega
    decaying = growth[vibrating & (growth < -st_floor(s))]
    slowest = float(-decaying.max()) if len(decaying) else None
    return {"impulse": impulse, "axis_turn": impulse * arm / h, **peaks,
            "decay_hours": (1 / slowest / 3600) if slowest else None}


def st_floor(s):
    return 1e-6 * s.omega


def silhouette(s, geo, n_tori):
    """Area seen from the Sun (m^2) and its centre along the axis: each torus edge-on, each farm
    ring edge-on (both as rectangles 2 r_outer wide)."""
    parts = []
    for body in s.bodies:
        if body.name.startswith("torus"):
            parts.append((2 * geo["envelope_outer"] * 2 * geo["envelope_radius"], body.z))
        else:
            parts.append((2 * (geo["farm_radius"] + geo["farm_height"]) * geo["farm_width"], body.z))
    area = sum(a for a, _ in parts)
    return area, sum(a * z for a, z in parts) / area


def sunlight(s, geo, array_area, n_tori, a_au=1.0, e=0.0):
    """Sunlight's torque on the stack about its centre of mass and the axis's yearly wobble."""
    zc = centre_of_mass(s)
    rim_area, rim_z = silhouette(s, geo, n_tori)
    z_array = s.hub_nodes[-1] + MAST
    p = SOLAR_PRESSURE / a_au ** 2
    torque = abs(p * (ARRAY_PUSH * array_area * (z_array - zc) + RIM_PUSH * rim_area * (rim_z - zc)))
    h, _ = angular_momentum(s)
    a = a_au * AU
    spec = math.sqrt(GM_SUN * a * (1 - e * e))
    # The torque at distance d is torque (a / d)^2; d^2 dnu/dt = spec, so dH = torque a^2 / spec dnu:
    # over an orbit H's tip circles with diameter 2 torque a^2 / spec.
    wobble = 2 * torque * a * a / spec / h
    return {"torque": torque, "rate": torque / h, "wobble": wobble, "array_force": p * ARRAY_PUSH * array_area,
            "rim_force": p * RIM_PUSH * rim_area, "arm_array": z_array - zc, "arm_rims": rim_z - zc}


def array_polar(array_mass, array_area):
    """The despun array's inertia about the spin axis: a flat square facing the Sun, the axis in
    its plane through its middle (m s^2 / 12)."""
    return array_mass * array_area / 12


def bearing(s, array_mass, array_area, friction=BEARING_FRICTION):
    """The despun array's bearing and drive (friction Q, N m): compensated by the drive, no torque on
    the stack and a power Q w; uncompensated, the time for friction to drag the array up to the
    spin, and the share of the stack's spin it then takes, once."""
    _, polar = angular_momentum(s)
    j_a = array_polar(array_mass, array_area)
    return {"friction": friction, "net_torque": 0.0, "power": friction * s.omega,
            "spin_up_hours": j_a * s.omega / friction / 3600, "spin_share": j_a / (polar + j_a), "j_array": j_a}
