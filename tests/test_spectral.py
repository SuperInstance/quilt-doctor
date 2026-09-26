"""Behavioral tests for the spectral lens — the heartbeat question.

The fourth lens: what is the project's period, and is the heartbeat
commensurate (rational teeth, a real rhythm) or incommensurate (quasiperiodic,
free-running)? Classical FFT and quantum QFT must AGREE on the spectrum —
that agreement is itself the receipt that the quantum measurement is honest.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quilt_doctor.lenses.spectral import SpectralLens


def weekly_series(n=56):
    """A real heartbeat: 7-day period with jitter."""
    return [3 + math.sin(2 * math.pi * i / 7.0) + 0.2 * math.sin(i) for i in range(n)]


def quasi_series(n=56):
    """Two incommensurate periods (7 and 13.7 days) — quasiperiodic."""
    return [3 + math.sin(2 * math.pi * i / 7.0) + math.sin(2 * math.pi * i / 13.7)
            for i in range(n)]


def noise_series(n=56, seed=3):
    import random
    random.seed(seed)
    return [random.uniform(0, 6) for _ in range(n)]


def test_weekly_cadence_has_a_dominant_period():
    p = SpectralLens(shots=8000).project(weekly_series(), [])
    assert round(p.receipts["dominant_period_days"]) == 7
    assert p.score > 0.7  # commensurate heartbeat = healthy rhythm


def test_quasiperiodic_signal_is_flagged_incommensurate():
    p = SpectralLens(shots=8000).project(quasi_series(), [])
    assert p.receipts["second_peak_ratio"] >= 0.5  # a real second tone
    assert "quasiperiodic" in p.verdict.lower() or "incommensurate" in p.verdict.lower()
    assert p.score < 0.7


def test_noise_has_no_heartbeat():
    p = SpectralLens(shots=8000).project(noise_series(), [])
    assert p.score < 0.5
    assert p.receipts["peak_concentration"] < 0.1


def test_classical_and_quantum_spectra_agree():
    """The load-bearing honesty receipt: QFT measurement and classical FFT
    must land on the same dominant bin, or the substrate is lying."""
    p = SpectralLens(shots=8000).project(weekly_series(), [])
    if "qft_top_bin" in p.receipts:  # quantum substrate present
        assert p.receipts["qft_top_bin"] == p.receipts["fft_top_bin"]
    assert p.receipts["substrate"] in ("qft+fft", "fft-only")


def test_every_projection_carries_receipts():
    p = SpectralLens(shots=4000).project(weekly_series(), [])
    for key in ("dominant_period_days", "shots", "peak_concentration", "second_peak_ratio"):
        assert key in p.receipts
