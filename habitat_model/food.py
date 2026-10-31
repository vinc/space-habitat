"""Food: working diet -> light per person -> crop area, power and people per tier lit (§13)."""

DAY = 86400.0
CROPS = ("potato", "wheat", "soybean", "lentils", "berries", "flax", "greens")


def light_per_person(p):
    """Mol of light on the crops per person per day, per crop and in total (with seedlings and turnaround)."""
    shares = {c: getattr(p, f"share_{c}") for c in CROPS}
    farm_kcal = p.diet_kcal * (1 - p.valley_diet_share)
    per_crop = {}
    for crop, share in shares.items():
        kcal = farm_kcal * share / sum(shares.values())
        grams = kcal / getattr(p, f"kcal_{crop}")
        per_crop[crop] = grams / getattr(p, f"yield_{crop}")
    return per_crop, sum(per_crop.values()) * (1 + p.crop_overhead)


def compute(p, d, geo):
    per_crop, mol = light_per_person(p)
    farm_kcal = p.diet_kcal * (1 - p.valley_diet_share)
    crop_area = mol / p.crop_light_mol
    people_per_tier = geo["crop_area_per_tier"] * p.crop_light_mol / mol
    people = d.tiers_lit * people_per_tier
    lamp = (p.farm_lamp_efficacy_umol_j or p.lamp_efficacy_umol_j) * 1e-6
    return {
        "mol_per_crop": per_crop,
        "mol_per_person": mol,
        "crop_area_per_person": crop_area,
        "kcal_per_m2": farm_kcal / crop_area,
        "power_per_person": mol / DAY / lamp / p.farm_delivery,
        "people_per_tier": people_per_tier,
        "people": people,
        "floor_per_person": geo["floor_area"] / people if people else None,
    }
