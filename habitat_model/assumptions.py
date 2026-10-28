"""The assumptions file: one entry per input, with its range, source and status."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

DEFAULT_PATH = Path(__file__).with_name("assumptions.toml")
STATUSES = ("sourced", "estimate", "guess", "design")


@dataclass(frozen=True)
class Assumption:
    name: str
    group: str
    value: float
    unit: str
    low: float
    high: float
    source: str
    status: str

    @property
    def varies(self):
        """Whether the sensitivity sweep moves this input."""
        return self.low != self.high


def load(path=DEFAULT_PATH):
    """Read the assumptions file into {name: Assumption}."""
    data = tomllib.loads(Path(path).read_text())
    out = {}
    for group, entries in data.items():
        for name, e in entries.items():
            if name in out:
                raise ValueError(f"duplicate assumption {name!r}")
            value = float(e["value"])
            low = float(e.get("low", value))
            high = float(e.get("high", value))
            if not low <= value <= high:
                raise ValueError(f"{name}: value {value} outside [{low}, {high}]")
            if e["status"] not in STATUSES:
                raise ValueError(f"{name}: unknown status {e['status']!r}")
            out[name] = Assumption(name, group, value, e["unit"], low, high, e["source"], e["status"])
    return out


def params(assumptions, **overrides):
    """The values as attributes (p.shield_areal_t_m2), with optional overrides."""
    values = {name: a.value for name, a in assumptions.items()}
    unknown = set(overrides) - set(values)
    if unknown:
        raise KeyError(f"unknown assumptions: {', '.join(sorted(unknown))}")
    values.update(overrides)
    return SimpleNamespace(**values)
