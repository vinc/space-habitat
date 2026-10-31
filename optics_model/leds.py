"""LEDs made from asteroid material (notes §10, §13): what a torus's lighting takes, element by element.

The valley's white LEDs are blue InGaN dies under YAG:Ce phosphor; the farm's are blue InGaN and deep-red
(660 nm) AlGaInP dies. From the installed electricity (the valley at its noon peak, the tiers while lit):

die area = electricity / `led_die_w_mm2`; wafer grown = die area / `led_wafer_yield`.

Each wafer's epitaxial layers, its substrate and the reactor's feed:

- **Blue (InGaN on sapphire):** ~5 µm of GaN (buffer, n- and p-layers), five ~3 nm In0.15Ga0.85N wells,
  on ~0.65 mm of sapphire (Al₂O₃, grown from 5N alumina). Gallium fed = film / `mocvd_utilization`;
  indium incorporates poorly at GaN's growth temperatures, so ~5% of the indium fed ends in the wells.
  Ammonia `mocvd_ammonia_kg_m2` per m² of wafer (V/III ratios of thousands), most of it recoverable.
- **Red (AlGaInP on GaAs):** ~2 µm of (Al0.3Ga0.7)0.5In0.5P (cladding and wells), half of its group III
  indium, on ~0.35 mm of GaAs, etched away in thin-film dies (counted as consumed). Phosphine and arsine
  are the group V feeds.
- **Phosphor:** `led_phosphor_g_w` of YAG:Ce (Y2.94Ce0.06Al5O12) per W of white LED.

Replacement: each region's LEDs last `led_life_h` at its own photoperiod. Element densities and
compositions are standard; the layer thicknesses are typical of commercial dies (estimates).
"""

from habitat_model.power import farm_efficacy

# Film and substrate: thickness (m), density (kg/m3), {element: mass fraction}.
GAN = (5e-6, 6150, {"Ga": 0.833, "N": 0.167})
INGAN_WELLS = (15e-9, 6300, {"In": 0.19, "Ga": 0.65, "N": 0.16})
ALGAINP = (2e-6, 4400, {"In": 0.49, "Ga": 0.21, "Al": 0.035, "P": 0.265})
SAPPHIRE = (0.65e-3, 3980, {"Al": 0.529, "O": 0.471})
GAAS = (0.35e-3, 5320, {"Ga": 0.482, "As": 0.518})
YAG_CE = {"Y": 0.44, "Ce": 0.014, "Al": 0.227, "O": 0.32}
INDIUM_INCORPORATION = 0.05        # share of the indium fed ending in InGaN wells (estimate)
DIE_THINNED_M = 150e-6             # a finished die's thickness, for the mass imported as dies

# ppm by mass, (S-type ordinary chondrite, C-type CI-like), for the elements TRACE_PPM lacks.
# Indium per notes §10; arsenic, yttrium and cerium recalled from chondrite compilations (Lodders 2003
# for CI; Wasson & Kallemeyn 1988 for ordinary chondrites), to be checked.
EXTRA_PPM = {"In": (0.002, 0.078), "As": (1.6, 1.7), "Y": (2.0, 1.5), "Ce": (0.9, 0.6)}


def _add(out, layer, area, scale=1.0):
    t, rho, frac = layer
    for el, f in frac.items():
        out[el] = out.get(el, 0.0) + area * t * rho * f * scale


def installed(p, r, tiers):
    """Installed LED electricity (W): the valley at its noon peak, the farm's tiers while lit."""
    pw = r["power"]
    return pw["valley_sky"] * 24 / p.valley_day_h, tiers * pw["farm_per_tier"] * 24 / p.farm_photoperiod_h


def budget(p, r, tiers=3):
    """Dies, wafers and materials for one torus's LEDs (kg), and their yearly replacement."""
    valley_w, farm_w = installed(p, r, tiers)
    blue_farm = (1 - p.led_farm_red_share) * farm_w if p.farm_lamp_efficacy_umol_j else farm_w
    red_w = farm_w - blue_farm
    white_w = valley_w + (0.0 if p.farm_lamp_efficacy_umol_j else farm_w)
    blue_w = white_w + (blue_farm if p.farm_lamp_efficacy_umol_j else 0.0)
    die = {"blue": blue_w / (p.led_die_w_mm2 * 1e6), "red": red_w / (p.led_die_w_mm2 * 1e6)}   # m2
    wafer = {k: v / p.led_wafer_yield for k, v in die.items()}

    wells, film = {}, {}
    _add(wells, INGAN_WELLS, wafer["blue"])
    _add(film, GAN, wafer["blue"])
    _add(film, ALGAINP, wafer["red"])
    fed = {el: m / p.mocvd_utilization for el, m in film.items()}
    for el, m in wells.items():   # indium at its own (poor) incorporation
        fed[el] = fed.get(el, 0.0) + m / (INDIUM_INCORPORATION if el == "In" else p.mocvd_utilization)
        film[el] = film.get(el, 0.0) + m
    substrate = {}
    _add(substrate, SAPPHIRE, wafer["blue"])
    _add(substrate, GAAS, wafer["red"])
    phosphor = white_w * p.led_phosphor_g_w / 1e3
    for el, f in YAG_CE.items():
        substrate[el] = substrate.get(el, 0.0) + phosphor * f    # consumed with the dies, like a substrate

    use = {el: fed.get(el, 0.0) + substrate.get(el, 0.0) for el in set(fed) | set(substrate)}
    use.pop("O", None)
    ammonia = p.mocvd_ammonia_kg_m2 * wafer["blue"]

    hours = {"valley": p.valley_day_h * 365.25, "farm": p.farm_photoperiod_h * 365.25}
    life_yr = {k: p.led_life_h / h for k, h in hours.items()}
    share_valley = valley_w / (valley_w + farm_w)
    per_year = share_valley / life_yr["valley"] + (1 - share_valley) / life_yr["farm"]
    return {"valley_w": valley_w, "farm_w": farm_w, "white_w": white_w, "red_w": red_w, "die_m2": die,
            "wafer_m2": wafer, "film": film, "fed": fed, "substrate": substrate, "use": use,
            "phosphor": phosphor, "ammonia": ammonia, "life_yr": life_yr, "replaced_per_yr": per_year,
            "dies_imported": DIE_THINNED_M * (die["blue"] * SAPPHIRE[1] + die["red"] * GAAS[1]) + phosphor}


def contained(r, element):
    """kg of an element in the torus's source bodies (S-type host + C-type partner)."""
    from habitat_model.materials import TRACE_PPM
    s_ppm, c_ppm = TRACE_PPM.get(element) or EXTRA_PPM[element]
    m = r["materials"]
    return (s_ppm or 0.0) * 1e-6 * m["s_type"] + c_ppm * 1e-6 * m["c_type"]


# The fab, step by step: (step, what it needs, where it comes from, status).
CHAIN = [
    ("Gallium", "6N–7N metal, kilograms", "~5–10 ppm in the rock, with the aluminium in the silicates and clays; "
     "a by-product of the leach line, then electrowinning and zone refining", "⚠ recovery at ~10 ppm"),
    ("Indium", "grams (blue) to kilograms (red AlGaInP)", "~2 ppb (S-type) to ~78 ppb (C-type): the scarcest "
     "input, from the leach line's zinc and copper streams", "⚠ / ✗ for red"),
    ("Precursors", "trimethylgallium, -indium, -aluminium; 7N ammonia; silane, Cp₂Mg; phosphine (red)",
     "metals + methyl chloride (methanol + HCl, C-type carbon and chlorine); Haber–Bosch ammonia from the "
     "C-type's nitrogen; distillation to 6N", "✓ chemistry, ⚠ purity"),
    ("Substrates", "sapphire wafers (blue), GaAs (red)", "5N alumina from the silicates' plagioclase, "
     "Kyropoulos growth (~2,050 °C), sawn and polished; or GaN on silicon, from a semiconductor-silicon line "
     "(the one local PV would need)", "⚠"),
    ("Epitaxy", "MOCVD reactors: steel chamber, SiC-coated graphite susceptor, ~1,050 °C, ~100 mbar",
     "steel, carbon, silicon carbide: all local; the controls are electronics (vitamins)", "✓"),
    ("Patterning", "~5–7 mask layers at micron scale: contact or proximity lithography, no steppers",
     "chromium-on-quartz masks, novolac resists (phenol, formaldehyde), chlorine plasma etching", "✓"),
    ("Contacts", "p-contact and current spreading (ITO, or Ni/Ag), n-contact (Ti/Al)",
     "ITO needs indium again: a thin nickel–silver or ZnO:Al instead; titanium, nickel, aluminium local", "⚠"),
    ("Phosphor (valley)", "YAG:Ce, ~0.1–0.4 t per torus", "yttrium ~2 ppm, cerium ~1 ppm: rare-earth "
     "separation by solvent extraction, at kilogram scale a lab process", "⚠"),
    ("Packaging", "lead frames or chip-on-board, encapsulant, heat spreaders",
     "copper or steel boards, phosphor in glass (local glass) instead of silicone, copper bond wire", "✓"),
    ("Drivers", "constant-current supplies, ~1 per kW", "silicon or GaN power transistors, capacitors, "
     "ferrite inductors: electronics, the same vitamin as the rest of the habitat's", "✗ vitamin"),
]
