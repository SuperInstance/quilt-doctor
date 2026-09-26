"""Null-model discipline — ported from the quilt-verilog iteration archive.

The archive's central lesson (roundK-red, roundM, probe-kit): **the null
model IS the experiment.** A metric's impressive number means nothing until
it is compared against the right null — a shuffle of the same data through
the SAME lens. If the lens scores shuffled data about the same as real
data, the lens is measuring a convention, not the project.

Every lens projection must carry `null_mean`, `null_std`, `null_z` in its
receipts. The verdict uses the z-score, never the raw metric.
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quilt_doctor.lenses.jepa import JepaLens
from quilt_doctor.lenses import Projection


def healthy_series(n=28):
    return [3 + math.sin(i / 3.0) for i in range(n)]


def test_every_projection_carries_null_receipts():
    from quilt_doctor.lenses.nulls import with_null_receipts

    p = with_null_receipts(JepaLens(), healthy_series(), [], n_null=5)
    for key in ("null_mean", "null_std", "null_z", "null_n"):
        assert key in p.receipts, f"missing null receipt: {key}"


def test_null_z_is_large_for_structured_series():
    """A periodic series must score far from its shuffle-null — otherwise
    the lens measures nothing (the roundK failure mode)."""
    from quilt_doctor.lenses.nulls import with_null_receipts

    p = with_null_receipts(JepaLens(), healthy_series(), [], n_null=9)
    assert abs(p.receipts["null_z"]) >= 1.0


def test_shuffle_null_is_deterministic_with_seed():
    from quilt_doctor.lenses.nulls import with_null_receipts

    a = with_null_receipts(JepaLens(), healthy_series(), [], n_null=5, seed=7)
    b = with_null_receipts(JepaLens(), healthy_series(), [], n_null=5, seed=7)
    assert a.receipts["null_mean"] == b.receipts["null_mean"]
    assert a.receipts["null_std"] == b.receipts["null_std"]


def test_null_util_runs_any_lens():
    from quilt_doctor.lenses.nulls import with_null_receipts

    lens = JepaLens()
    p = with_null_receipts(lens, healthy_series(), [], n_null=5, seed=1)
    assert isinstance(p, Projection)
    assert p.receipts["null_n"] == 5
