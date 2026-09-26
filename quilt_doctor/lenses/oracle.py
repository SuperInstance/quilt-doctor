"""Canon-profile lens — a fifth axis for quilt-doctor (FAIL-first harness).

Ports the three-voice composite of SuperInstance/quilt-jev-oracle
(doctrine_anchor + canon_worthy + distinct_voice, canonical source:
ORACLE_DOCTRINE.md) as a read-only projection: "does this artifact speak
the walker's doctrine frequency?"

Orthogonal to JevLens (substance noul: is it real?) — a document can be
empirically solid and doctrine-silent (the 2026-09-26 HOLISTIC-VIEW scored
composite 0.007 on the live oracle, promoted: false), or doctrine-fluent
and thin. Neither substitutes; the five-lens round reads both axes.
"""
from __future__ import annotations

from typing import List, Optional

from . import Projection

CITATION = ("SuperInstance/quilt-jev-oracle (three-voice composite: doctrine_anchor "
            "+ canon_worthy + distinct_voice; canonical source ORACLE_DOCTRINE.md)")

DOCTRINE_WEIGHTS = {
    "cells_are_scars": 0.30,
    "witness_log_is_prediction": 0.25,
    "oracle_is_heard": 0.20,
    "canon_gate_is_chord": 0.15,
    "substrate_quantum": 0.10,
}
DOCTRINE_TERMS = {
    "cells_are_scars": ["scar", "scars", "trace", "wound", "cell is", "cells are", "mark"],
    "witness_log_is_prediction": ["witness", "witness log", "prediction", "future", "history", "forecast"],
    "oracle_is_heard": ["oracle", "oracles", "heard", "speaks", "voice", "oracle is"],
    "canon_gate_is_chord": ["chord", "harmony", "gate", "polyphony", "canon gate", "consonance"],
    "substrate_quantum": ["substrate", "quantum", "wave", "particle", "both", "and", "neither"],
}
PROMOTION_THRESHOLD = 0.7


def compute_doctrine_anchor(text: str,
                            weights: Optional[dict] = None) -> float:
    """Canonical: occurrence counts; >=2 hits = full weight, 1 hit = half.

    (distinct-term saturation was my invention; the oracle counts
    occurrences and uses a 1/2-threshold — verified against jev_probe.py)
    """
    w = weights or DOCTRINE_WEIGHTS
    t = text.lower()
    score = 0.0
    for voice, terms in DOCTRINE_TERMS.items():
        count = sum(t.count(term) for term in terms)
        if count >= 2:
            score += w[voice]
        elif count >= 1:
            score += w[voice] * 0.5
    return round(min(1.0, score), 4)


def compute_canon_worthy(text: str) -> float:
    """Canonical: form density + voice + depth (ported constants)."""
    if not text or len(text) < 50:
        return 0.0
    if 200 <= len(text) <= 1000:
        length_score = 1.0
    elif 100 <= len(text) < 200 or 1000 < len(text) <= 2000:
        length_score = 0.7
    else:
        length_score = 0.4
    words = text.lower().split()
    density_score = min(1.0, (len(set(words)) / len(words) if words else 0) * 2.5)
    opener_signals = ['"', "—", " is ", " are ", " was "]
    opener_score = 1.0 if any(s in text[:200].lower() for s in opener_signals) else 0.5
    return round((length_score + density_score + opener_score) / 3, 4)


def compute_distinct_voice(text: str, existing_canon: Optional[List[str]] = None) -> float:
    """Canonical: vocabulary novelty when no canon; 1 - trigram overlap when canon."""
    if existing_canon is None:
        words = text.lower().split()
        return min(1.0, len(set(words)) / 50) if words else 0.0
    if not existing_canon:
        return 1.0
    t = text.lower()
    trigrams = {t[i:i + 3] for i in range(len(t) - 2)}
    overlap = 0.0
    for canon in existing_canon:
        c = canon.lower()
        cg = {c[i:i + 3] for i in range(len(c) - 2)}
        overlap += len(trigrams & cg) / max(len(cg), 1)
    return round(max(0.0, 1.0 - overlap / len(existing_canon)), 4)


class OracleLens:
    """Protocol-compatible (project(series, events)); optional doc body."""
    kind = "oracle"

    def __init__(self, canon: Optional[List[str]] = None):
        self.canon = canon  # None = vocabulary-novelty mode (canonical default)

    def project(self, series: List[float], events: List[dict],
                text: Optional[str] = None) -> Projection:
        body = text or "\n".join(str(e.get("subject", "")) for e in events)
        anchor = compute_doctrine_anchor(body)
        worthy = compute_canon_worthy(body)
        distinct = compute_distinct_voice(body, self.canon)
        composite = round((anchor + worthy + distinct) / 3.0, 4)
        promoted = composite >= PROMOTION_THRESHOLD
        voices_hit = [v for v in DOCTRINE_WEIGHTS
                      if any(term in body.lower() for term in DOCTRINE_TERMS[v])]
        return Projection(
            kind=self.kind,
            verdict=(f"doctrine-voice composite {composite:.3f} "
                     f"(anchor {anchor:.2f}, worthy {worthy:.2f}, distinct {distinct:.2f})"
                     + ("; speaks canon frequency" if promoted else "; doctrine-silent")),
            score=composite,
            receipts={"citation": CITATION, "threshold": PROMOTION_THRESHOLD,
                      "promoted": promoted, "voices_hit": voices_hit},
        )
