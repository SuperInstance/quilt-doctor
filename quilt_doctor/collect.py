"""Signal collection — turn a repo's history into series + events."""

from __future__ import annotations

import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple


def collect_repo(repo_path, days: int = 35) -> Tuple[List[float], List[dict]]:
    """Parse git log -> (commits-per-day series over `days`, commit events)."""
    repo = Path(repo_path)
    fmt = "%ad%x1f%s"
    out = subprocess.run(
        ["git", "-C", str(repo), "log", f"--since={days} days ago",
         f"--pretty=format:{fmt}", "--date=short"],
        capture_output=True, text=True, check=True).stdout
    today = datetime.utcnow().date()
    buckets = {(today - timedelta(d)).isoformat(): 0 for d in range(days)}
    events: List[dict] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        date, _, subject = line.partition("\x1f")
        if date in buckets:
            buckets[date] += 1
        events.append({"type": "commit", "date": date, "subject": subject})
    dates = sorted(buckets)
    series = [buckets[d] for d in dates]
    return series, events
