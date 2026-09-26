"""Behavioral tests for quilt-doctor's lens layer (dynamic abstraction porting).

Every lens implements ONE protocol: project(series, events) -> Projection.
The substrate changes per lens — linear predictor (JEPA), QPAM quantum
circuit (MOTH), TypeSafe decision model (JEV) — the interface never does.
These tests pin the protocol and each lens's honesty guarantees.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quilt_doctor.lenses import Lens, Projection, available_lenses
from quilt_doctor.lenses.jepa import JepaLens
from quilt_doctor.lenses.moth import MothLens
from quilt_doctor.lenses.jev import JevLens


def healthy_series(n=28):
    """Steady cadence: ~3 commits/day with mild jitter."""
    return [3 + math.sin(i / 3.0) for i in range(n)]


def broken_series(n=28):
    """Healthy for 3 weeks, then silence — the classic 'project went quiet'."""
    return [3 + math.sin(i / 3.0) for i in range(n - 7)] + [0] * 7


# ── the protocol every lens must satisfy (porting guarantee) ─────────────

@pytest.mark.parametrize("lens", [JepaLens(), MothLens(shots=512), JevLens(backend=None)])
def test_all_lenses_share_one_interface(lens):
    assert isinstance(lens, Lens)
    p = lens.project(healthy_series(), [])
    assert isinstance(p, Projection)
    assert p.kind in {lens.kind for lens in (JepaLens(), MothLens(), JevLens(None))}
    assert 0.0 <= p.score <= 1.0
    assert p.receipts  # every projection carries receipts — no naked verdicts


def test_registry_reports_availability():
    names = {l.kind for l in available_lenses(jev_backend=None)}
    assert "jepa" in names and "moth" in names  # local lenses always available
    names_jev = {l.kind for l in available_lenses(jev_backend=object())}
    assert "jev" in names_jev  # ported in when the substrate exists


# ── JEPA lens: predict the trajectory, flag where prediction fails ───────

def test_jepa_healthy_rhythm_scores_high():
    p = JepaLens().project(healthy_series(), [])
    assert p.score > 0.8


def test_jepa_sudden_silence_is_flagged():
    p = JepaLens().project(broken_series(), [])
    assert p.score < 0.6
    assert ("regime shift" in p.verdict.lower()
            or "anomal" in p.verdict.lower()
            or "drift" in p.verdict.lower())


def test_jepa_receipts_distinguish_fit_from_honesty():
    p = JepaLens().project(broken_series(), [])
    assert "in_dist_cos" in p.receipts and "extrapolation_cos" in p.receipts


# ── MOTH lens: QPAM coherence — is the project's signal music or noise? ──

def test_moth_periodic_signal_is_coherent():
    p = MothLens(shots=8000).project(healthy_series(), [])
    assert p.score > 0.6  # periodic cadence concentrates the H-basis spectrum
    assert p.receipts["shots"] == 8000  # shot budget is a first-class receipt
    assert "hadamard_entropy_bits" in p.receipts


def test_moth_noise_is_low_coherence():
    import random
    random.seed(7)
    noisy = [random.uniform(0, 6) for _ in range(28)]
    p = MothLens(shots=8000).project(noisy, [])
    assert p.score < 0.6
    # division of labor: a *stall* is still coherent structure — that's
    # JEPA's regime-shift case; MOTH answers music-vs-noise
    assert p.receipts["hadamard_entropy_bits"] > 1.8


def test_moth_low_shots_are_honest_about_noise():
    """My L2 spec's load-bearing finding: starved shots = noise, and the
    receipt must SAY so instead of canary-lying."""
    hi = MothLens(shots=8000).project(healthy_series(), [])
    lo = MothLens(shots=500).project(healthy_series(), [])
    assert lo.receipts["fidelity"] < hi.receipts["fidelity"]
    assert lo.receipts["shots"] < hi.receipts["shots"]


# ── JEV lens: substance judgment over commit claims ──────────────────────

class StubBackend:
    def __init__(self, score):
        self.score = score

    def available(self):
        return True

    def decide_batch(self, state, questions, model="jev-latest"):
        class J:
            def __init__(self, v):
                self.value = v
        return [J(self.score) for _ in questions], {"latency_ms": 0.1}


def test_jev_mean_substance_scores_commits():
    events = [{"type": "commit", "subject": "fix(core): repair hash chain in WAL"}]
    p = JevLens(backend=StubBackend(0.9)).project(healthy_series(), events)
    assert abs(p.score - 0.9) < 1e-6
    assert p.receipts["judged"] == 1


def test_jev_offline_is_honest_not_silent():
    p = JevLens(backend=None).project(healthy_series(),
                                      [{"type": "commit", "subject": "x"}])
    assert p.receipts["jev"] == "skipped"
    assert p.score == 0.5  # neutral, not zero — abstention is not condemnation
