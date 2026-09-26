"""The lens protocol — dynamic abstraction porting made literal.

A Lens projects the same signals through a different substrate. JEPA ports
the abstraction onto a linear predictor; MOTHquantum ports it onto a QPAM
quantum circuit; JEV ports it onto a TypeSafe decision model. The interface
never changes: project(series, events) -> Projection.

Every Projection carries receipts — substrate, config, and the numbers the
verdict stands on. No naked verdicts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


@dataclass
class Projection:
    kind: str                      # lens name: "jepa" | "moth" | "jev"
    verdict: str                   # one line a human reads
    score: float                   # 0..1 health along this axis
    receipts: Dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class Lens(Protocol):
    kind: str

    def project(self, series: List[float], events: List[dict]) -> Projection:
        ...


def available_lenses(jev_backend=None) -> List[Lens]:
    """Port in whatever substrates exist in this environment."""
    from .jepa import JepaLens
    from .moth import MothLens
    from .jev import JevLens
    from .oracle import OracleLens
    from .spectral import SpectralLens

    lenses: List[Lens] = [JepaLens(), MothLens(), OracleLens(), SpectralLens()]
    if jev_backend is not None:
        lenses.append(JevLens(backend=jev_backend))
    return lenses
