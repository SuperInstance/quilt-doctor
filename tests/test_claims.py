"""Executable BEACONS — falsifiable claims with kill conditions, evaluated
against real receipts. A claim without a kill condition is not a claim.

Ported from the quilt-verilog research program's BEACONS doctrine and the
roundK-red lesson: claims must be checkable against receipts, and the
checker must be code, not a reader's memory.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quilt_doctor.claims import (Claim, ClaimVerdict, evaluate_claims,
                                 load_registry)


def proj(score, lens="moth", **receipts):
    return {"lens": lens, "score": score, "receipts": receipts}


def test_alive_when_above_kill_threshold():
    c = Claim(id="x", repo="r", lens="moth",
              kill_if={"receipt": "null_z", "op": "<", "value": 1.5})
    v = evaluate_claims([c], {"r": [proj(0.7, null_z=3.0)]}, state={})[0]
    assert v.status == "ALIVE"


def test_killed_when_breached_once_without_streak():
    c = Claim(id="x", repo="r", lens="moth",
              kill_if={"receipt": "null_z", "op": "<", "value": 1.5})
    v = evaluate_claims([c], {"r": [proj(0.7, null_z=0.4)]}, state={})[0]
    assert v.status == "KILLED"


def test_streak_of_two_required_when_configured():
    c = Claim(id="x", repo="r", lens="moth",
              kill_if={"receipt": "null_z", "op": "<", "value": 1.5},
              kill_after_streak=2)
    state = {}
    v1 = evaluate_claims([c], {"r": [proj(0.7, null_z=0.4)]}, state=state)[0]
    assert v1.status == "ALIVE"          # first breach: warning
    assert state["x"]["streak"] == 1
    v2 = evaluate_claims([c], {"r": [proj(0.7, null_z=0.4)]}, state=state)[0]
    assert v2.status == "KILLED"         # second consecutive breach: dead
    # recovery resets the streak
    v3 = evaluate_claims([c], {"r": [proj(0.7, null_z=3.0)]}, state=state)[0]
    assert v3.status == "ALIVE"
    assert state["x"]["streak"] == 0


def test_unverifiable_when_repo_missing():
    c = Claim(id="x", repo="ghost", lens="moth",
              kill_if={"receipt": "null_z", "op": "<", "value": 1.5})
    v = evaluate_claims([c], {"r": [proj(0.7, null_z=3.0)]}, state={})[0]
    assert v.status == "UNVERIFIABLE"


def test_unverifiable_when_receipt_missing():
    c = Claim(id="x", repo="r", lens="moth",
              kill_if={"receipt": "null_z", "op": "<", "value": 1.5})
    v = evaluate_claims([c], {"r": [proj(0.7)]}, state={})[0]
    assert v.status == "UNVERIFIABLE"


def test_registry_loads_from_json(tmp_path):
    reg = {"rounds": [{"id": "t", "claims": [
        {"id": "x", "repo": "r", "lens": "moth",
         "kill_if": {"receipt": "null_z", "op": "<", "value": 1.5}}]}]}
    p = tmp_path / "reg.json"
    p.write_text(json.dumps(reg))
    loaded = load_registry(str(p))
    assert loaded[0].id == "x"
    assert loaded[0].kill_if["value"] == 1.5


def test_agreement_operator_on_qft_receipts():
    c = Claim(id="x", repo="r", lens="spectral",
              kill_if={"receipt": "qft_agrees", "op": "==", "value": False})
    alive = evaluate_claims([c], {"r": [proj(0.5, lens="spectral", qft_agrees=True)]}, state={})[0]
    dead = evaluate_claims([c], {"r": [proj(0.5, lens="spectral", qft_agrees=False)]}, state={})[0]
    assert alive.status == "ALIVE"
    assert dead.status == "KILLED"


def test_fleet_registry_round_trips_real_report(tmp_path):
    """The shipped fleet registry must evaluate against a real report.json."""
    report = json.loads(Path("/tmp/qd-nullcheck/report.json").read_text())
    projs = {p.get("lens") or p.get("kind"): p for p in report["projections"]}
    reg = {
        "rounds": [{"id": "fleet-check", "claims": [
            {"id": "moth-structure-real", "repo": "jev-quilt", "lens": "moth",
             "kill_if": {"receipt": "null_z", "op": "<", "value": 1.0}},
            {"id": "no-ghost", "repo": "nonexistent", "lens": "moth",
             "kill_if": {"receipt": "null_z", "op": "<", "value": 1.0}}]}]}
    p = tmp_path / "reg.json"
    p.write_text(json.dumps(reg))
    verdicts = evaluate_claims(load_registry(str(p)),
                               {"jev-quilt": list(projs.values())}, state={})
    by_id = {v.claim_id: v.status for v in verdicts}
    assert by_id["moth-structure-real"] == "ALIVE"   # z=3.02 from the live run
    assert by_id["no-ghost"] == "UNVERIFIABLE"
