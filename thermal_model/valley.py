"""The valley's day/night temperature swing (plan §6), steady-periodic, by harmonics.

One surface node per m² of floor: the air, the vegetation's water and the ponds (well mixed) are capacities;
the soil below is a semi-infinite conductor (admittance e sqrt(i w), e its effusivity). By day the sky's
light lands on it (all of it ends as heat in the valley); the people and machines add a constant load. The
cooling takes heat out at U (W/m²K) towards a coolant held at a fixed temperature: the cold ceiling's
radiation and the air handling. Over a day the valley loses what it gains, so only the swing matters:
each harmonic of the daily heating gives Q_n / (U + Y_n), Y_n = i w_n C + e sqrt(i w_n).
"""

import math

DAY = 86400.0
HOURS = 3600.0

# Soils, per m² of floor (general handbook ranges, unsourced): conductivity W/mK, volumetric heat J/m³K.
SOILS = {"moist": (1.5, 2.5e6), "dry": (0.3, 1.3e6)}
WATER_C = 4.18e6       # J/m³K
AIR_CP = 1005.0        # J/kgK

# Two looks of the same valley (notes §16): an arid canyon and a fern gully.
CASES = {
    "Arid canyon": {"soil": "dry", "pond_frac": 0.0, "pond_depth": 0.0, "biomass_water": 3.0},
    "Baseline": {"soil": "moist", "pond_frac": 0.02, "pond_depth": 1.0, "biomass_water": 10.0},
    "Fern gully": {"soil": "moist", "pond_frac": 0.05, "pond_depth": 1.5, "biomass_water": 30.0},
}


def air_heat_capacity(p):
    """Volumetric heat capacity of the habitat's air (J/m³K), from its configured pressure and temperature."""
    from habitat_model.mass import air

    gases = air(p, 1.0, p.pressure_kpa)
    return (gases["n2"] + gases["o2"]) * AIR_CP


def capacity(case, air_height, air_c):
    """Heat capacity per m² of floor following the day (J/m²K), soil apart."""
    return (air_c * air_height + WATER_C * case["biomass_water"] / 1000
            + WATER_C * case["pond_frac"] * case["pond_depth"])


def effusivity(case):
    k, c = SOILS[case["soil"]]
    return math.sqrt(k * c)


def swing(case, light_w_m2, day_hours, u, air_height, air_c, harmonics=200, samples=480):
    """Peak-to-peak temperature swing (K) and the hour of the maximum, for light_w_m2 on during day_hours;
    air_c: the air's volumetric heat capacity (J/m³K)."""
    c, e = capacity(case, air_height, air_c), effusivity(case)
    duty = day_hours / 24
    temps = []
    for j in range(samples):
        t = j / samples * DAY
        total = 0.0
        for n in range(1, harmonics + 1):
            w = 2 * math.pi * n / DAY
            # Square-wave heating from 0 to duty * DAY: complex amplitude of its n-th harmonic.
            q = light_w_m2 * (1 - complex(math.cos(w * duty * DAY), -math.sin(w * duty * DAY))) / (1j * 2 * math.pi * n)
            y = 1j * w * c + e * complex(math.sqrt(w / 2), math.sqrt(w / 2))     # e sqrt(i w)
            total += 2 * (q / (u + y) * complex(math.cos(w * t), math.sin(w * t))).real
        temps.append(total)
    hi, lo = max(temps), min(temps)
    return {"swing": hi - lo, "peak_hour": temps.index(hi) / samples * 24, "capacity": c, "effusivity": e,
            # Daily penetration depth of the soil: where the swing falls to 1/e.
            "soil_depth": math.sqrt(2 * SOILS[case["soil"]][0] / SOILS[case["soil"]][1] / (2 * math.pi / DAY))}


def light_on_floor(p, day_hours):
    """The sky's light reaching the floor while lit (W/m²): the daily dose in mol over the lit hours."""
    return p.valley_light_mol * 1e6 * p.par_j_per_umol / (day_hours * HOURS)
