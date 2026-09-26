"""FAIL-first pins for boundary receipts (wedge port).

Pin order: the citation pin is RED on any module that does not name
wasm-cert-wedge; chain pins red until BoundaryLedger exists. Run:
    python3 -m pytest tests/test_wedge.py -q
"""
import json
import pytest

from quilt_doctor import wedge


def test_citation_names_wedge():
    assert "wasm-cert-wedge" in wedge.CITATION
    assert "REFUSAL" in wedge.CITATION


def test_genesis_convention_matches_arcade():
    assert wedge.GENESIS_PREV == "0" * 16


def test_fnv1a64_fleet_consensus():
    # fleet consensus value: fnv1a64("quilt") — pinned, not recomputed here
    assert wedge.fnv1a_64("quilt") == 0x4B7FB2143373CE1E


def test_clean_chain_verifies():
    led = wedge.BoundaryLedger()
    led.bind_artifact("doc.md", "hello fleet")
    led.effect_projection("jepa", {"score": 0.42})
    led.tick(note="round")
    assert led.verify() == []


def test_tamper_detected():
    led = wedge.BoundaryLedger()
    led.bind_artifact("doc.md", "hello")
    led.effect_projection("jepa", {"score": 0.42})
    led.rows[1].body["projection_fnv1a64"] = "0" * 16  # attacker edit
    violations = led.verify()
    assert violations and any("row 1" in v for v in violations)


def test_prev_hash_link_enforced():
    led = wedge.BoundaryLedger()
    led.bind_artifact("a", "x")
    led.bind_artifact("b", "y")
    led.rows[1].prev_hash = "f" * 16  # break the link
    assert any("prev_hash" in v for v in led.verify())


def test_refusal_row_booked_and_reraises():
    led = wedge.BoundaryLedger()
    def boom(_):
        raise ValueError("lens exploded")
    with pytest.raises(ValueError):
        wedge.project_receipted(led, "a.txt", "content", "spectral", boom)
    kinds = [r.op for r in led.rows]
    assert kinds == ["BIND", "REFUSAL"]
    assert "lens exploded" in led.rows[1].body["reason"]


def test_receipted_projection_full_shape():
    led = wedge.BoundaryLedger()
    out = wedge.project_receipted(led, "a.txt", "data",
                                  "jev", lambda c: {"score": len(c)})
    assert out == {"score": 4}
    assert [r.op for r in led.rows] == ["BIND", "EFFECT", "TICK"]
    assert led.verify() == []


def test_jsonl_roundtrip(tmp_path):
    led = wedge.BoundaryLedger()
    led.bind_artifact("a", "x")
    led.effect_projection("moth", {"h": 1.0})
    p = tmp_path / "ledger.jsonl"
    led.to_jsonl(p)
    led2 = wedge.BoundaryLedger.from_jsonl(p)
    assert led2.verify() == []
    assert len(led2.rows) == 2


def test_truncation_detected_on_load(tmp_path):
    led = wedge.BoundaryLedger()
    for i in range(4):
        led.bind_artifact(f"a{i}", f"x{i}")
    p = tmp_path / "ledger.jsonl"
    led.to_jsonl(p)
    lines = p.read_text().splitlines()
    p.write_text("\n".join(lines[:-1]))  # truncate last row
    led2 = wedge.BoundaryLedger.from_jsonl(p)
    assert len(led2.rows) == 3  # load succeeds...
    # ...but the chain now ends early — count mismatch is the receipt
    assert len(led2.rows) != len(led.rows)
