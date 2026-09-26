"""JEV lens — is the recorded work verifiable?

Ports the project's commit claims onto a TypeSafe Jev decision model and
asks the question debugging always asks first: "is any of this real?" A noul
aimed at the specific claim (session 16: specific nouls move on quality):
does this commit describe concrete, checkable engineering?

Offline: abstains with receipts {"jev": "skipped"} and a neutral 0.5 —
abstention is not condemnation.
"""

from __future__ import annotations

from typing import List

from . import Lens, Projection

_Q = ("Does this commit message describe concrete, verifiable engineering work "
      "(a named file, function, test, PR, or artifact) — as opposed to vague "
      "activity that no one could check?")


class JevLens(Lens):
    kind = "jev"

    def __init__(self, backend=None, max_events: int = 12):
        self.backend = backend
        self.max_events = max_events

    def project(self, series: List[float], events: List[dict]) -> Projection:
        commits = [e for e in events if e.get("type") == "commit"]
        sample = commits[-self.max_events:]
        if self.backend is None or not self.backend.available():
            return Projection(self.kind,
                              f"offline — {len(sample)} recent claims unjudged (skipped, not condemned)",
                              0.5, {"jev": "skipped", "sampled": len(sample)})
        if not sample:
            return Projection(self.kind, "no commit claims to judge", 0.5,
                              {"judged": 0})
        state = {"commits": [{"subject": e.get("subject", "")} for e in sample]}
        questions = [{"name": f"c{i}", "type": "noul", "instructions": _Q}
                     for i in range(len(sample))]
        judgments, meta = self.backend.decide_batch(state, questions)
        scores = [float(j.value) for j in judgments]
        mean = sum(scores) / len(scores)
        verdict = (f"recent work reads VERIFIABLE (mean substance {mean:.2f} over {len(scores)} commits)"
                   if mean >= 0.6 else
                   f"recent work reads VAGUE (mean substance {mean:.2f}) — check what actually landed")
        return Projection(self.kind, verdict, max(0.0, min(1.0, mean)),
                          {"judged": len(scores), "mean_substance": round(mean, 3),
                           "latency_ms": meta.get("latency_ms"), "model": "jev-latest"})
