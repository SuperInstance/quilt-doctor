"""Null-model receipts for every projection.

Ported doctrine from the quilt-verilog 14-round iteration archive
(roundK-red, roundM): the null model IS the experiment. Every lens score
is compared against a shuffle-null of the same series pushed through the
same lens; the z-score is the honest signal. A lens that scores shuffled
data the same as real data is measuring a convention, not the project —
exactly the J(∅,∅)=1.0 artifact class that produced a false "breakthrough"
in round K.
"""

from __future__ import annotations

import random
from typing import List

from . import Lens, Projection


def with_null_receipts(lens: Lens, series: List[float], events: List[dict],
                       n_null: int = 25, seed: int = 0x0DDB) -> Projection:
    """Project, then push `n_null` seeded shuffles through the same lens and
    attach the null distribution + z-score to the receipts."""
    p = lens.project(series, events)
    if len(series) < 4 or n_null < 2:
        p.receipts.update({"null_mean": None, "null_std": None,
                           "null_z": None, "null_n": n_null})
        return p
    rng = random.Random(seed)
    nulls = []
    for _ in range(n_null):
        shuffled = list(series)
        rng.shuffle(shuffled)
        nulls.append(lens.project(shuffled, events).score)
    mean = sum(nulls) / len(nulls)
    var = sum((s - mean) ** 2 for s in nulls) / max(1, len(nulls) - 1)
    std = var ** 0.5
    z = (p.score - mean) / std if std > 1e-9 else 0.0
    p.receipts.update({
        "null_mean": round(mean, 4),
        "null_std": round(std, 4),
        "null_z": round(z, 3),
        "null_n": n_null,
        "null_seed": seed,
    })
    return p
