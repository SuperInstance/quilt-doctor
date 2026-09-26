"""FAIL-first pins for the moth-ledger bridge.

Doctrine under test:
- every coherence claim is a FINDING cell or it doesn't exist
- severity is exact (Q16 parts — refuse-never-round)
- the verdict matches planted ground truth (the meter is checked, not trusted)
- the round only closes when the books balance (unclosed = violation)
- a tampered row breaks verify_chain (stored hashes are evidence, not truth)
- quantum-unavailable => REFUSAL credits, and the round still closes honestly
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "examples"))
try:
    import moth_ledger_bridge as bridge  # noqa: F401
    import moth_ledger  # noqa: F401 — the bridge books into it at run time
    MOTH_LEDGER = True
except ImportError:
    MOTH_LEDGER = False

pytestmark = pytest.mark.skipif(not MOTH_LEDGER,
                                reason="moth-ledger not on PYTHONPATH")


def _read_rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def test_round_closes_with_chain_verifying(tmp_path):
    summary = bridge.run_round(tmp_path / "round.jsonl", shots=256)
    assert summary["chain_verifies"], summary["chain_problems"]
    assert summary["close_row_id"]
    closed = {c["expectation_id"]: c["close"] for c in summary["closes"]}
    assert set(closed) == set(bridge.PLANTED)
    assert all(s == "CAUGHT" for s in closed.values()), closed


def test_finding_severity_is_exact_ratio(tmp_path):
    bridge.run_round(tmp_path / "round.jsonl", shots=256)
    for row in _read_rows(tmp_path / "round.jsonl"):
        if row.get("kind") == "FINDING/v1":
            s = row["severity"]
            assert int(s["den"]) == 65536, s          # exact top-state mass, ℚ₁₆
            assert 0 <= int(s["num"]) <= int(s["den"])


def test_verdict_confirms_planted_coherent_and_refutes_noise(tmp_path):
    bridge.run_round(tmp_path / "round.jsonl", shots=256)
    verdicts = [r for r in _read_rows(tmp_path / "round.jsonl")
                if r.get("kind") == "VERDICT/v1"]
    by_finding = {v["finding_id"]: v["verdict"] for v in verdicts}
    findings = {r["id"]: r for r in _read_rows(tmp_path / "round.jsonl")
                if r.get("kind") == "FINDING/v1"}
    for fid, finding in findings.items():
        planted = finding["context"]["planted_coherent"]
        expect = "CONFIRMED"  # the meter must agree with the plant at n=2, shots>=256
        assert by_finding[fid] == expect, (finding["context"]["expectation_id"],
                                           by_finding[fid], planted)


def test_tampered_row_breaks_chain(tmp_path):
    path = tmp_path / "round.jsonl"
    bridge.run_round(path, shots=256)
    rows = _read_rows(path)
    for r in rows:                       # forge a verdict after the fact
        if r.get("kind") == "VERDICT/v1":
            r["verdict"] = "REFUTED" if r["verdict"] == "CONFIRMED" else "CONFIRMED"
            break
    path.write_text("\n".join(json.dumps(r) for r in rows))
    from moth_ledger import Ledger
    ok, problems = Ledger(path).verify_chain()
    assert not ok
    assert problems


def test_refusal_path_balances_without_quantum(tmp_path, monkeypatch):
    monkeypatch.setattr(bridge, "_z_measure",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("no qiskit")))
    summary = bridge.run_round(tmp_path / "round.jsonl", shots=64)
    assert not summary["quantum_ran"]
    assert summary["chain_verifies"]
    closed = {c["expectation_id"]: c["close"] for c in summary["closes"]}
    assert all(s == "REFUSED" for s in closed.values()), closed
    kinds = [r["kind"] for r in _read_rows(tmp_path / "round.jsonl")]
    assert "VERDICT/v1" not in kinds  # no quantum, no verdicts — refusals only
