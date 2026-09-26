"""Verify a laya quilt-ledger JSONL WAL with the fleet fnv1a chain.

Cross-tool check: laya4quilt's QuiltLedger books rows (chain="fnv1a64"
canonical, "fnv1a32" legacy) and append_jsonl persists them; this module
re-verifies the file independently — no laya import, just the fleet
algorithm and the canonical form. Both widths are detected from the first
row's genesis convention (16-hex vs 8-hex chain_prev).
"""

from __future__ import annotations

import json
from pathlib import Path

OFFSET64 = 0xCBF29CE484222325
PRIME64 = 0x100000001B3
MASK64 = (1 << 64) - 1
OFFSET32 = 0x811C9DC5
PRIME32 = 0x01000193
MASK32 = 0xFFFFFFFF


def _fnv1a(data: str, width: int) -> str:
    if width == 64:
        h, prime, mask, fmt = OFFSET64, PRIME64, MASK64, "%016x"
    else:
        h, prime, mask, fmt = OFFSET32, PRIME32, MASK32, "%08x"
    for b in data.encode("utf-8"):
        h = ((h ^ b) * prime) & mask
    return fmt % h


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def verify_laya_wal(path: str):
    """Returns (ok, rows, first_bad_row_hash). Chain integrity row by row:
    row_hash recomputed over the canonical row minus row_hash; chain_prev
    must equal the previous row's hash, starting at the width's genesis."""
    p = Path(path)
    if not p.exists():
        return False, 0, "missing"
    lines = [l for l in p.read_text().splitlines() if l.strip()]
    if not lines:
        return True, 0, None
    try:
        rows = [json.loads(l) for l in lines]
    except json.JSONDecodeError:
        return False, 0, "unparseable"
    width = 64 if len(str(rows[0].get("chain_prev", ""))) == 16 else 32
    genesis = "0" * (16 if width == 64 else 8)
    prev = genesis
    for row in rows:
        body = {k: v for k, v in row.items() if k != "row_hash"}
        want = _fnv1a(_canonical(body), width)
        if row.get("chain_prev") != prev or row.get("row_hash") != want:
            return False, len(rows), row.get("row_hash", "unknown")
        prev = row["row_hash"]
    return True, len(rows), None


def _main(argv) -> int:
    if len(argv) != 2:
        print("usage: python -m quilt_doctor.laya_wal <wal.jsonl>")
        return 2
    ok, n, bad = verify_laya_wal(argv[1])
    status = "OK" if ok else "TAMPERED"
    print(f"[{status}] rows={n}" + ("" if ok else f" first_bad={bad}"))
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(_main(sys.argv))
