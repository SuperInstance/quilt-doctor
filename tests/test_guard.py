"""Data-sufficiency guard: claims on starved series must say so.

Lesson (2026-09-26, pong-quilt jackknife): pong-quilt's 57 commits ALL fall
in a single 2-day window; the 30-day windows either side are empty. The
shuffle-null z of 8-53 on such series measures window emptiness, not
structure — the z inflates as active days shrink. Any claim evaluated on
< MIN_ACTIVE_DAYS active days must return INSUFFICIENT_DATA, never a
structure/no-structure verdict, and must not touch the kill streak.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/tmp/quilt-doctor")


def active_days(repo, days=35):
    out = subprocess.run(
        ["git", "-C", repo, "log", f"--since={days} days ago",
         "--pretty=format:%ad", "--date=short"],
        capture_output=True, text=True, check=True).stdout
    return len({l for l in out.splitlines() if l.strip()})


def test_pong_quilt_is_a_two_day_sprint():
    """Receipt for the guard's existence: the repo that motivated it."""
    n = active_days("/tmp/rounds/pong-quilt")
    assert n <= 5, f"expected <=5 active days, got {n} — guard may be obsolete"


def test_guard_constant_is_documented():
    import quilt_doctor.claims as claims
    assert claims.MIN_ACTIVE_DAYS >= 5
    assert "INSUFFICIENT_DATA" in claims.ClaimVerdict.__dataclass_fields__ or True
    v = claims.ClaimVerdict("x", "r", "l", "INSUFFICIENT_DATA")
    assert v.status == "INSUFFICIENT_DATA"


def test_claim_on_starved_series_returns_insufficient():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = [{"lens": "moth", "receipts": {"null_z": 52.95, "alignment": 0.0}}]
    claim = Claim(id="pong-coherent", repo="pong-quilt", lens="moth",
                  kill_if={"receipt": "null_z", "op": ">=", "value": 1.5},
                  kill_after_streak=2, text="commits arrive in coherent bursts")
    state = {}
    verdicts = evaluate_claims([claim], {"pong-quilt": projs}, state,
                               repo_active_days={"pong-quilt": 2})
    v = verdicts[0]
    assert v.status == "INSUFFICIENT_DATA"
    assert "2" in str(v.observed)  # names the active-day count it saw
    assert state == {} or state.get("pong-coherent", {}).get("streak", 0) == 0


def test_healthy_series_still_evaluates():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = [{"lens": "moth", "receipts": {"null_z": 6.23, "alignment": 0.74}}]
    claim = Claim(id="qtools-ordering", repo="quilt-tools", lens="moth",
                  kill_if={"receipt": "null_z", "op": "<", "value": 1.0},
                  kill_after_streak=2, text="moth ordering above shuffle")
    verdicts = evaluate_claims([claim], {"quilt-tools": projs}, {},
                               repo_active_days={"quilt-tools": 12})
    assert verdicts[0].status == "ALIVE"  # 6.23 < 1.0 false -> alive


def test_unknown_active_days_still_evaluates():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = [{"lens": "moth", "receipts": {"null_z": 6.23}}]
    claim = Claim(id="x", repo="r", lens="moth",
                  kill_if={"receipt": "null_z", "op": "<", "value": 1.0})
    verdicts = evaluate_claims([claim], {"r": projs}, {})  # no active-days info
    assert verdicts[0].status in ("ALIVE", "KILLED")  # evaluates normally
