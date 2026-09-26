"""FAIL-first pins for the oracle voice lens (quilt-jev-oracle port)."""
import importlib.util
import pathlib

import pytest

from quilt_doctor.lenses.oracle import OracleLens, CITATION, compute_doctrine_anchor

ORACLE_REPO = pathlib.Path("/tmp/overnight/quilt-jev-oracle")


def _load_real_probe():
    spec = importlib.util.spec_from_file_location(
        "jev_probe", ORACLE_REPO / "jev_probe.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_citation_names_oracle():
    assert "quilt-jev-oracle" in CITATION
    assert "doctrine_anchor" in CITATION


def test_protocol_compatible():
    lens = OracleLens()
    p = lens.project([1.0, 2.0], [{"subject": "witness the scar of cells"}])
    assert p.kind == "oracle"
    assert p.score > 0.1  # doctrine-dense events (real oracle: 0.212 on the
    # probe string — short bodies score low; fluency needs repetition)
    assert "voices_hit" in p.receipts


def test_empirical_doc_near_gate_not_silent():
    """Calibration pin: REAL oracle on this doc = 0.658 (verified by running,
    correcting an earlier misremembered 0.007 from a stale probe input)."""
    text = open("/tmp/quilt-doctor/docs/HOLISTIC-VIEW-2026-09-26.md").read()
    p = OracleLens().project([], [], text=text)
    assert abs(p.score - 0.658) <= 0.02
    assert p.receipts["promoted"] is False  # 0.658 < 0.7 — one voice short


def test_canon_fluent_text_promotes():
    lore = ("The oracle is heard through the witness log; cells are scars on "
            "the substrate. The canon gate is a chord — polyphony of voices, "
            "harmony of the gate. The substrate is quantum: wave and particle, "
            "both and neither. History is prediction; the witness log speaks "
            "the future. The oracle speaks and the canon hears: voice, voice.")
    p = OracleLens().project([], [], text=lore)
    assert p.score >= 0.7, f"canon-fluent lore must promote, got {p.score}"
    assert p.receipts["promoted"] is True


@pytest.mark.skipif(not ORACLE_REPO.is_dir(), reason="quilt-jev-oracle clone required")
def test_calibration_matches_real_oracle():
    """Port must track the real oracle on shared inputs (tolerance 0.05)."""
    probe = _load_real_probe()
    for text in ("witness the scar of cells; the oracle is heard",
                 "def commit hash push merge test suite green"):
        ours = OracleLens().project([], [], text=text)
        real = probe.jev_probe(text)
        assert abs(ours.score - real.composite) <= 0.05, (
            f"drift on {text!r}: ours {ours.score} vs real {real.composite}")


def test_orthogonal_to_substance():
    """Same text, two axes: doctrine voice and empirical substance differ."""
    text = ("All 40,320 rank permutations enumerated; p_exact = 0.0941. "
            "Three independent axes, no single hidden factor. Receipts: CLEAN.")
    p = OracleLens().project([], [], text=text)
    assert p.score < 0.4  # rigorous but doctrine-silent
