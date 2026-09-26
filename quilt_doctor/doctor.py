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


def diagnose(repo_path, substrate: QuiltSubstrate,
             jev_backend=None, moth_shots: int = 20000) -> Diagnosis:
    series, events = collect_repo(repo_path)
    lenses = available_lenses(jev_backend=jev_backend)
    for lens in lenses:
        if lens.kind == "moth":
            lens.shots = moth_shots
    projections = [l.project(series, events) for l in lenses]
    substrate.record_observation(series, events, source=repo_path,
                                 projections=projections)
    report = substrate.verify()
    return Diagnosis(source=str(repo_path), series=series, events=events,
                     projections=projections, substrate_report=report,
                     receipts={"wal": report, "events": len(events)})


def render_report_md(d: Diagnosis) -> str:
    out = [f"# quilt-doctor — what's going on in `{Path(d.source).name}`", ""]
    active_days = sum(1 for v in d.series if v > 0)
    out.append("## Signals")
    out.append(f"- {len(d.events)} commits over {len(d.series)} days "
               f"({active_days} active days; peak {max(d.series) if d.series else 0}/day)")
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
