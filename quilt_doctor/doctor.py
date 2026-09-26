"""Orchestrator — collect -> substrate -> lenses -> diagnosis -> report."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .collect import collect_repo
from .substrate import QuiltSubstrate
from .lenses import Projection, available_lenses


@dataclass
class Diagnosis:
    source: str
    series: List[float]
    events: List[dict]
    projections: List[Projection]
    substrate_report: Dict[str, Any] = field(default_factory=dict)
    receipts: Dict[str, Any] = field(default_factory=dict)
    active_days: int = 0
    data_sufficient: bool = True


def diagnose(repo_path, substrate: QuiltSubstrate,
             jev_backend=None, moth_shots: int = 20000) -> Diagnosis:
    series, events = collect_repo(repo_path)
    lenses = available_lenses(jev_backend=jev_backend)
    for lens in lenses:
        if lens.kind == "moth":
            lens.shots = moth_shots
    active_days = sum(1 for v in series if v > 0)
    data_sufficient = active_days >= 5  # MIN_ACTIVE_DAYS; claims.py mirrors this
    projections = []
    for l in lenses:
        if l.kind == "jev":
            p = l.project(series, events)  # judgment has no shuffle-null
        else:
            from .lenses.nulls import with_null_receipts
            p = with_null_receipts(l, series, events, n_null=15)
        # every projection self-carries the sufficiency caveat (pong-quilt
        # lesson: a 2-day sprint scores z=52 on an empty window)
        p.receipts["active_days"] = active_days
        p.receipts["data_sufficient"] = data_sufficient
        projections.append(p)
    substrate.record_observation(series, events, source=repo_path,
                                 projections=projections)
    report = substrate.verify()
    return Diagnosis(source=str(repo_path), series=series, events=events,
                     projections=projections, substrate_report=report,
                     receipts={"wal": report, "events": len(events),
                               "active_days": active_days,
                               "data_sufficient": data_sufficient},
                     active_days=active_days,
                     data_sufficient=data_sufficient)


def render_report_md(d: Diagnosis) -> str:
    out = [f"# quilt-doctor — what's going on in `{Path(d.source).name}`", ""]
    active_days = d.active_days
    out.append("## Signals")
    out.append(f"- {len(d.events)} commits over {len(d.series)} days "
               f"({active_days} active days; peak {max(d.series) if d.series else 0}/day)")
    if not d.data_sufficient:
        out.append(f"- ⚠ INSUFFICIENT DATA: {active_days} active day(s) < 5 — "
                   "null_z below measures window emptiness, not structure.")
    out.append("")
    out.append("## Projections")
    for p in d.projections:
        out.append(f"### {p.kind.upper()} — score {p.score:.2f}")
        out.append(p.verdict)
        out.append("")
        out.append("```")
        for k, v in p.receipts.items():
            out.append(f"{k}: {v}")
        out.append("```")
        out.append("")
    out.append("## Substrate")
    wr = d.substrate_report
    out.append(f"- quilt WAL: {wr.get('lines')} lines, verify: "
               f"{'OK' if wr.get('ok') else 'DIVERGED'}")
    out.append("- every verdict above is replayable from the chain")
    return "\n".join(out) + "\n"
