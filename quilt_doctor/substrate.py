"""Quilt substrate — the WAL under the diagnosis.

Compact vendored implementation of the fleet's 5-opcode quilt spine
(canonical producer: SuperInstance/git-agent PR #1). Observations become
BIND (the doctor session) / LINK (signals) / VIEW (projections) lines,
hash-chained with fnv1a, replayable. The diagnosis is exactly as
trustworthy as the chain it rode in on.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

FNV_OFFSET = 0xcbf29ce484222325
FNV_PRIME = 0x100000001b3
MASK64 = (1 << 64) - 1


def fnv1a(s: str) -> str:
    h = FNV_OFFSET
    for b in s.encode("utf-8"):
        h = ((h ^ b) * FNV_PRIME) & MASK64
    return f"{h:016x}"


def _canonical(d: Dict[str, Any]) -> str:
    return json.dumps(d, sort_keys=True, separators=(",", ":"))


class QuiltSubstrate:
    def __init__(self, wal_path):
        self.wal_path = Path(wal_path)
        self._lines: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if self.wal_path.exists():
            self._lines = [json.loads(l) for l in
                           self.wal_path.read_text().splitlines() if l.strip()]

    def wal(self) -> List[Dict[str, Any]]:
        return list(self._lines)

    def append(self, op: str, cell: str, args: Dict[str, Any]) -> Dict[str, Any]:
        line = {"op": op, "cell": cell, "args": args,
                "seq": len(self._lines),
                "prev_hash": self._lines[-1]["hash"] if self._lines else "0" * 16}
        line["hash"] = fnv1a(_canonical({k: v for k, v in line.items() if k != "hash"}))
        self._lines.append(line)
        self.wal_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.wal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(line, sort_keys=True) + "\n")
        return line

    def record_observation(self, series, events, source: str, projections=None):
        self.append("BIND", "doctor/session",
                    {"tool": "quilt-doctor", "source": str(source)})
        for i, v in enumerate(series):
            self.append("LINK", "doctor/signal",
                        {"axis": "commits_per_day", "t": i, "value": v})
        self.append("LINK", "doctor/events", {"count": len(events)})
        if projections:
            for p in projections:
                self.append("VIEW", f"doctor/projection/{p.kind}",
                            {"verdict": p.verdict, "score": p.score,
                             "receipts": p.receipts})

    def verify(self) -> Dict[str, Any]:
        prev_hash, prev_seq, divergences = "0" * 16, -1, []
        for i, line in enumerate(self._lines):
            expect_prev = prev_hash
            recomputed = fnv1a(_canonical({k: v for k, v in line.items() if k != "hash"}))
            if line["hash"] != recomputed:
                divergences.append({"seq": i, "why": "hash_mismatch"})
            if line["prev_hash"] != expect_prev:
                divergences.append({"seq": i, "why": "chain_break"})
            if line["seq"] != i:
                divergences.append({"seq": i, "why": "seq_gap"})
            prev_hash, prev_seq = line["hash"], i
        return {"ok": not divergences, "divergences": divergences,
                "lines": len(self._lines)}
