"""Boundary receipts — hash-chained ledger rows for lens invocations.

Ports the row discipline of SuperInstance/wasm-cert-wedge (the TCB-boundary
receipt doctrine: one hash-chained row binds tool identity + invocation +
artifact hashes; a mismatch is a REFUSAL row, not silent compromise) onto
quilt-doctor's projection flow. Where the wedge receipts the compile
boundary of a WASM agent, this receipts the measurement boundary of a
debugging lens: BIND the input artifact, EFFECT the projection, TICK the
round, REFUSAL when verification fails.

Hash: FNV-1a64, fleet consensus (quilt kernel, git-agent, cowboy, oracle).

Stdlib only. Occurred/recorded split: rows are appended when the event
occurs; verification re-derives the chain independently.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, List, Optional

CITATION = ("SuperInstance/wasm-cert-wedge (TCB-boundary receipt doctrine: "
            "COMPILE/EFFECT/REFUSAL rows, occurred/recorded split); "
            "hash: FNV-1a64 fleet consensus")
GENESIS_PREV = "0" * 16  # 64-bit zero, same genesis convention as arcade


def fnv1a_64(s: str) -> int:
    h = 0xCBF29CE484222325
    for b in s.encode():
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _hex(h: int) -> str:
    return f"{h:016x}"


def _canon(obj: Any) -> str:
    import dataclasses
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        obj = dataclasses.asdict(obj)
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


@dataclass
class Row:
    op: str            # BIND | EFFECT | TICK | REFUSAL
    body: dict
    prev_hash: str
    row_hash: str = ""

    def seal(self) -> "Row":
        self.row_hash = _hex(fnv1a_64(f"{self.op}:{_canon(self.body)}:{self.prev_hash}"))
        return self


@dataclass
class BoundaryLedger:
    """Hash-chained invocation ledger. verify() re-derives independently."""
    rows: List[Row] = field(default_factory=list)
    citation: str = CITATION

    def _last_hash(self) -> str:
        return self.rows[-1].row_hash if self.rows else GENESIS_PREV

    def append(self, op: str, body: dict) -> Row:
        row = Row(op=op, body=body, prev_hash=self._last_hash()).seal()
        self.rows.append(row)
        return row

    def bind_artifact(self, name: str, content: str) -> Row:
        return self.append("BIND", {"artifact": name,
                                    "sha256": hashlib.sha256(content.encode()).hexdigest()[:16],
                                    "fnv1a64": _hex(fnv1a_64(content))})

    def effect_projection(self, lens: str, projection: dict) -> Row:
        return self.append("EFFECT", {"lens": lens,
                                      "projection_fnv1a64": _hex(fnv1a_64(_canon(projection)))})

    def tick(self, note: str = "") -> Row:
        return self.append("TICK", {"ts": round(time.time(), 3), "note": note})

    def refusal(self, reason: str) -> Row:
        return self.append("REFUSAL", {"reason": reason})

    def verify(self) -> List[str]:
        """Re-derive the chain. Returns violations; empty = clean."""
        violations: List[str] = []
        prev = GENESIS_PREV
        for i, row in enumerate(self.rows):
            expect = _hex(fnv1a_64(f"{row.op}:{_canon(row.body)}:{prev}"))
            if row.prev_hash != prev:
                violations.append(f"row {i}: prev_hash {row.prev_hash} != chain {prev}")
            if row.row_hash != expect:
                violations.append(f"row {i}: row_hash {row.row_hash} != derived {expect}")
            prev = row.row_hash
        return violations

    def to_jsonl(self, path: str | Path) -> None:
        with open(path, "w") as f:
            for r in self.rows:
                f.write(json.dumps({"op": r.op, "body": r.body,
                                    "prev_hash": r.prev_hash,
                                    "row_hash": r.row_hash}) + "\n")

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "BoundaryLedger":
        ledger = cls()
        with open(path) as f:
            for line in f:
                if line.strip():
                    d = json.loads(line)
                    ledger.rows.append(Row(op=d["op"], body=d["body"],
                                           prev_hash=d["prev_hash"],
                                           row_hash=d["row_hash"]))
        return ledger


def project_receipted(ledger: BoundaryLedger, artifact_name: str,
                      artifact_content: str, lens: str,
                      project_fn) -> dict:
    """Receipted measurement: BIND the artifact, run the lens, EFFECT the
    projection, TICK the round. A lens exception books a REFUSAL row and
    re-raises — a refusal is a receipt, not a silent gap."""
    ledger.bind_artifact(artifact_name, artifact_content)
    try:
        projection = project_fn(artifact_content)
    except Exception as e:
        ledger.refusal(f"{lens}: {type(e).__name__}: {e}")
        raise
    ledger.effect_projection(lens, projection)
    ledger.tick(note=f"{lens} on {artifact_name}")
    return projection
