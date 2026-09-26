"""FAIL-first: diagnosis reports must self-carry data-sufficiency."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/tmp/quilt-doctor")


def _seed_repo(path, spec):
    """spec: {date_iso: n_commits} — create commits on those days."""
    import os
    env = dict(os.environ,
               GIT_AUTHOR_DATE="", GIT_COMMITTER_DATE="")
    for date, n in spec.items():
        for i in range(n):
            f = Path(path) / f"f{date}-{i}.txt"
            f.write_text(f"{date}-{i}")
            subprocess.run(["git", "-C", path, "add", str(f.name)],
                           check=True, capture_output=True)
            env["GIT_AUTHOR_DATE"] = f"{date}T12:00:00+00:00"
            env["GIT_COMMITTER_DATE"] = f"{date}T12:00:00+00:00"
            subprocess.run(["git", "-C", path, "commit", "-q", "-m", f"{date}-{i}"],
                           check=True, capture_output=True, env=env)


def test_diagnosis_carries_sufficiency(tmp_path):
    from quilt_doctor.substrate import QuiltSubstrate
    from quilt_doctor.doctor import diagnose

    repo = tmp_path / "sprint-repo"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"],
                   check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"],
                   check=True)
    # 8 commits across 2 days only (like pong-quilt's sprint)
    from datetime import datetime, timedelta, timezone
    today = datetime.now(timezone.utc).date()
    _seed_repo(str(repo), {
        (today - timedelta(days=1)).isoformat(): 5,
        (today - timedelta(days=2)).isoformat(): 3,
    })
    sub = QuiltSubstrate(tmp_path / "wal.jsonl")
    diag = diagnose(str(repo), sub)
    assert diag.active_days == 2
    assert diag.data_sufficient is False
    # projections annotated too
    for p in diag.projections:
        assert p.receipts.get("active_days") == 2
        assert p.receipts.get("data_sufficient") is False


def test_healthy_repo_is_sufficient(tmp_path):
    from quilt_doctor.substrate import QuiltSubstrate
    from quilt_doctor.doctor import diagnose

    repo = tmp_path / "steady-repo"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"],
                   check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"],
                   check=True)
    from datetime import datetime, timedelta, timezone
    today = datetime.now(timezone.utc).date()
    _seed_repo(str(repo), {
        (today - timedelta(days=d)).isoformat(): 2 for d in range(10)})
    sub = QuiltSubstrate(tmp_path / "wal2.jsonl")
    diag = diagnose(str(repo), sub)
    assert diag.active_days == 10
    assert diag.data_sufficient is True
