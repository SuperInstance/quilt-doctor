#!/usr/bin/env python3
"""Proof run: quilt-doctor against a real SuperInstance project.

Usage: python3 run_doctor.py <repo_path> <out_dir>
Writes report.md, report.json, and quilt.jsonl (the substrate WAL) so the
whole diagnosis is replayable by anyone.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "/root/.openclaw/workspace/jev-quilt")  # TypeSafeBackend (live JEV)

from quilt_doctor.doctor import diagnose, render_report_md
from quilt_doctor.substrate import QuiltSubstrate


def main():
    repo = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    jev_backend = None
    try:
        from jev_quilt.typesafe_client import TypeSafeBackend
        jev_backend = TypeSafeBackend()
        if not jev_backend.available():
            jev_backend = None
    except Exception as exc:
        print(f"JEV unavailable ({exc}) — running with local lenses only")

    substrate = QuiltSubstrate(wal_path=out / "quilt.jsonl")
    d = diagnose(repo, substrate=substrate, jev_backend=jev_backend)

    (out / "report.md").write_text(render_report_md(d))
    (out / "report.json").write_text(json.dumps({
        "source": d.source,
        "projections": [p.__dict__ for p in d.projections],
        "substrate": d.substrate_report,
        "receipts": d.receipts,
    }, indent=2, default=str))
    print(render_report_md(d))
    print(f"-> {out}/report.md | report.json | quilt.jsonl "
          f"(verify: {d.substrate_report['ok']})")


if __name__ == "__main__":
    main()
