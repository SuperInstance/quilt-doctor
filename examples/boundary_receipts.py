"""Receipted fleet round — every projection hash-chained at the boundary.

Runs diagnose() across the fleet with a BoundaryLedger (wedge port of
SuperInstance/wasm-cert-wedge's TCB-boundary receipt doctrine). Each lens
invocation books BIND (input artifact) -> EFFECT (projection hash) -> TICK
(rows); a lens exception books REFUSAL and re-raises. The written JSONL
re-derives from genesis — a tampered receipt is a verify() violation, not
an opinion.

    python3 examples/boundary_receipts.py            # fleet on disk
    python3 examples/boundary_receipts.py REPO ...   # explicit repos
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from quilt_doctor import doctor, wedge
from quilt_doctor.substrate import QuiltSubstrate


def _jev_backend():
    try:
        from jev_quilt.typesafe_client import TypeSafeBackend
        b = TypeSafeBackend()
        return b if b.available() else None
    except Exception:
        return None

FLEET = ["git-agent", "pong-quilt", "quilt-tools", "tidepool",
         "quilt-studio", "twist-engine", "quilt-cowboy", "hermit"]
ROUNDS = Path("/tmp/rounds")
OUT = Path(__file__).resolve().parent.parent / "docs" / "runs"


def main() -> None:
    names = sys.argv[1:] or [n for n in FLEET if (ROUNDS / n).is_dir()]
    ledger = wedge.BoundaryLedger()
    summary = {}
    for name in names:
        repo = ROUNDS / name
        if not repo.is_dir():
            print(f"[skip] {name} not cloned at {repo}")
            continue
        wal = tempfile.mktemp(suffix=f"-{name}.jsonl")
        try:
            d = doctor.diagnose(str(repo), QuiltSubstrate(wal),
                                jev_backend=_jev_backend(), ledger=ledger)
        except Exception as e:  # REFUSAL row already booked
            summary[name] = {"error": f"{type(e).__name__}: {e}"}
            print(f"[refusal] {name}: {e}")
            continue
        summary[name] = {
            "projections": {p.kind: round(p.score, 3) for p in d.projections},
            "events": len(d.events),
        }
        print(f"[ok] {name}: {summary[name]['projections']}")
    OUT.mkdir(parents=True, exist_ok=True)
    ledger_path = OUT / "boundary-ledger-2026-09-26.jsonl"
    ledger.to_jsonl(ledger_path)
    violations = ledger.verify()
    report = {"ledger": str(ledger_path), "rows": len(ledger.rows),
              "violations": violations, "citation": wedge.CITATION,
              "rounds": summary}
    (OUT / "boundary-receipts-2026-09-26.json").write_text(
        json.dumps(report, indent=2))
    print(f"\nledger: {len(ledger.rows)} rows -> {ledger_path}")
    print(f"verify: {violations or 'CLEAN'}")
    print(f"report: {OUT / 'boundary-receipts-2026-09-26.json'}")


if __name__ == "__main__":
    main()
