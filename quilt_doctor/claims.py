"""Executable BEACONS — falsifiable claims with kill conditions.

Doctrine ported from the quilt-verilog research program: a claim without a
kill condition is not a claim. The registry is machine-readable (JSON), the
evaluator is code, and every verdict names the observed receipt value that
kept it alive or killed it. Streak-based claims (kill_after_streak > 1)
model "two consecutive rounds below threshold" honestly: one breach is a
warning, not a death.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional

OPS = {
    "<": lambda a, b: a < b,
    "<=": lambda a, b: a <= b,
    ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
}


@dataclass
class Claim:
    id: str
    repo: str
    lens: str
    kill_if: dict                    # {"receipt": "null_z"|"score", "op", "value"}
    kill_after_streak: int = 1
    text: str = ""


@dataclass
class ClaimVerdict:
    claim_id: str
    repo: str
    lens: str
    status: str                      # ALIVE | KILLED | UNVERIFIABLE
    observed: Optional[float] = None
    kill_condition: str = ""
    text: str = ""


def load_registry(path: str) -> List[Claim]:
    data = json.loads(open(path).read())
    claims = []
    for rnd in data.get("rounds", []):
        for c in rnd.get("claims", []):
            claims.append(Claim(
                id=c["id"], repo=c["repo"], lens=c["lens"],
                kill_if=c["kill_if"],
                kill_after_streak=c.get("kill_after_streak", 1),
                text=c.get("text", "")))
    return claims


def _extract(projection: dict, key: str):
    if key == "score":
        return projection.get("score")
    return projection.get("receipts", {}).get(key)


def evaluate_claims(claims: List[Claim], projections_by_repo: Dict[str, list],
                    state: dict) -> List[ClaimVerdict]:
    """Evaluate claims against {repo: [projection, ...]}. `state` is mutated:
    state[claim_id] = {"streak": n} survives across rounds."""
    verdicts = []
    for c in claims:
        cond = c.kill_if
        rendered = f"{cond.get('receipt', 'score')} {cond['op']} {cond['value']}"
        projs = projections_by_repo.get(c.repo) or []
        match = next((p for p in projs
                      if (p.get("lens") or p.get("kind")) == c.lens), None)
        if match is None:
            verdicts.append(ClaimVerdict(c.id, c.repo, c.lens, "UNVERIFIABLE",
                                         kill_condition=rendered, text=c.text))
            continue
        observed = _extract(match, cond.get("receipt", "score"))
        if observed is None or not isinstance(observed, (int, float)):
            verdicts.append(ClaimVerdict(c.id, c.repo, c.lens, "UNVERIFIABLE",
                                         kill_condition=rendered, text=c.text))
            continue
        op = OPS[cond["op"]]
        breached = op(observed, cond["value"])
        slot = state.setdefault(c.id, {"streak": 0})
        if breached:
            slot["streak"] = slot.get("streak", 0) + 1
        else:
            slot["streak"] = 0
        status = "KILLED" if slot["streak"] >= c.kill_after_streak else "ALIVE"
        verdicts.append(ClaimVerdict(c.id, c.repo, c.lens, status,
                                     observed=observed,
                                     kill_condition=rendered, text=c.text))
    return verdicts


def _main(argv) -> int:
    if len(argv) < 3:
        print("usage: python -m quilt_doctor.claims <registry.json> "
              "<report.json> [report.json...]")
        return 2
    claims = load_registry(argv[1])
    by_repo = {}
    for path in argv[2:]:
        d = json.loads(open(path).read())
        repo = d.get("source", path)
        by_repo[repo] = d.get("projections", [])
    state_path = "/tmp/quilt-doctor/.claims-state.json"
    try:
        state = json.loads(open(state_path).read())
    except (OSError, json.JSONDecodeError):
        state = {}
    verdicts = evaluate_claims(claims, by_repo, state)
    for v in verdicts:
        obs = f"{v.observed:.3f}" if isinstance(v.observed, float) else "—"
        print(f"[{v.status:12}] {v.claim_id:24} {v.repo}  observed={obs}  "
              f"kill if {v.kill_condition}")
    open(state_path, "w").write(json.dumps(state, indent=1))
    return 0 if all(v.status != "KILLED" for v in verdicts) else 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
