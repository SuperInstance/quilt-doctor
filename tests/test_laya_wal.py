"""check-laya-wal: verify a laya quilt-ledger JSONL WAL with the fleet chain.

Producer/consumer split: rows are booked by laya4quilt's QuiltLedger
(chain="fnv1a64"), persisted via append_jsonl; THIS module re-verifies the
file with the fleet fnv1a-64 algorithm, no laya import required. The two
repos must agree on the chain or the fleet substrate story is a lie.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quilt_doctor.laya_wal import verify_laya_wal

LAYA = "/tmp/laya4quilt"


def make_wal(tmp_path, n=3, chain="fnv1a64"):
    sys.path.insert(0, LAYA)
    from laya.quilt import QuiltLedger
    led = QuiltLedger(actor="crab", engine="test", chain=chain)
    for i in range(n):
        led.decide({"s": i}, [{"q": str(i)}],
                   lambda s, q, i=i: {"answers": {"a": i}, "model": "t"})
    p = str(tmp_path / "quilt.jsonl")
    led.append_jsonl(p)
    return p, led


def test_verifies_producer_file(tmp_path):
    if not Path(LAYA).exists():
        pytest.skip("laya4quilt checkout absent")
    p, led = make_wal(tmp_path)
    ok, rows, bad = verify_laya_wal(p)
    assert ok
    assert rows == 3
    assert bad is None


def test_pins_tamper_at_its_own_row(tmp_path):
    if not Path(LAYA).exists():
        pytest.skip("laya4quilt checkout absent")
    p, led = make_wal(tmp_path, n=4)
    lines = Path(p).read_text().splitlines()
    row = json.loads(lines[1])
    row["payload"]["answers"]["a"] = 999
    lines[1] = json.dumps(row, sort_keys=True, separators=(",", ":"))
    Path(p).write_text("\n".join(lines) + "\n")
    ok, rows, bad = verify_laya_wal(p)
    assert not ok
    assert bad == led.rows[1]["row_hash"]


def test_detects_broken_chain_link(tmp_path):
    if not Path(LAYA).exists():
        pytest.skip("laya4quilt checkout absent")
    p, led = make_wal(tmp_path, n=3)
    lines = Path(p).read_text().splitlines()
    row = json.loads(lines[2])
    row["chain_prev"] = "f" * 16  # valid hash, wrong link
    lines[2] = json.dumps(row, sort_keys=True, separators=(",", ":"))
    Path(p).write_text("\n".join(lines) + "\n")
    ok, _, bad = verify_laya_wal(p)
    assert not ok
    assert bad == led.rows[2]["row_hash"]


def test_legacy_32bit_wal_verifies_with_correct_genesis(tmp_path):
    if not Path(LAYA).exists():
        pytest.skip("laya4quilt checkout absent")
    p, led = make_wal(tmp_path, chain="fnv1a32")
    ok, rows, bad = verify_laya_wal(p)
    assert ok and rows == 3 and bad is None


def test_empty_and_missing_files(tmp_path):
    p = tmp_path / "empty.jsonl"
    p.write_text("")
    assert verify_laya_wal(str(p)) == (True, 0, None)
    ok, rows, bad = verify_laya_wal(str(tmp_path / "nope.jsonl"))
    assert (ok, rows, bad) == (False, 0, "missing")
