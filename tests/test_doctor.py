"""Behavioral tests for quilt-doctor's orchestrator: collect -> substrate ->
lenses -> projected report. Uses a synthetic repo (built in tmp) so the whole
path runs offline except where a lens substrate is explicitly provided."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from quilt_doctor.collect import collect_repo
from quilt_doctor.substrate import QuiltSubstrate
from quilt_doctor.doctor import diagnose, render_report_md


def make_synthetic_repo(tmp_path, days=28, commits_per_day=3):
    repo = tmp_path / "synthetic"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "core.py").write_text("def core():\n    return 1\n")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    env = {"GIT_AUTHOR_DATE": "2026-09-01T10:00:00", "GIT_COMMITTER_DATE": "2026-09-01T10:00:00"}
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True, env={**os.environ, **env})
    for d in range(days):
        for c in range(commits_per_day):
            date = f"2026-09-{(d % 28) + 1:02d}T{c + 9:02d}:00:00"
            (repo / "core.py").write_text(f"def core():\n    return {d * 10 + c}\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            env = {"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
            subprocess.run(["git", "commit", "-qm", f"feat: commit {d}-{c} on core"],
                           cwd=repo, check=True, env={**os.environ, **env})
    return repo


def test_collect_produces_series_and_events(tmp_path):
    repo = make_synthetic_repo(tmp_path)
    series, events = collect_repo(repo)
    assert len(series) >= 28
    assert sum(series) >= 70  # 85 commits; 6 land on future dates outside the window
    assert all(e["type"] == "commit" for e in events)
    assert any("core" in e["subject"] for e in events)


def test_substrate_writes_verifiable_quilt_wal(tmp_path):
    series, events = [3, 3, 3], [{"type": "commit", "subject": "a"}]
    sub = QuiltSubstrate(wal_path=tmp_path / "q.jsonl")
    sub.record_observation(series, events, source="test")
    report = sub.verify()
    assert report["ok"] is True
    ops = {l["op"] for l in sub.wal()}
    assert ops & {"BIND", "LINK", "VIEW"}


def test_diagnose_runs_available_lenses_and_renders(tmp_path):
    repo = make_synthetic_repo(tmp_path)
    sub = QuiltSubstrate(wal_path=tmp_path / "q.jsonl")
    result = diagnose(repo, substrate=sub, jev_backend=None)
    assert {p.kind for p in result.projections} >= {"jepa", "moth"}
    md = render_report_md(result)
    for section in ("quilt-doctor", "Signals", "JEPA", "MOTH", "substrate"):
        assert section.lower() in md.lower()
    # report must be replayable: the substrate WAL verifies after diagnosis
    assert sub.verify()["ok"] is True


def test_report_is_json_serializable(tmp_path):
    repo = make_synthetic_repo(tmp_path)
    result = diagnose(repo, substrate=QuiltSubstrate(wal_path=tmp_path / "q.jsonl"),
                      jev_backend=None)
    blob = json.dumps({"projections": [p.__dict__ for p in result.projections],
                       "receipts": result.receipts}, default=str)
    assert "jepa" in blob and "moth" in blob
