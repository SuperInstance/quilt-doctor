"""JEPA lens — does the project's trajectory predict itself?

JEPA pattern: context (past) -> predictor -> target (future); loss is the
verification gap. A project whose cadence predicts itself is in a stable
regime; a project whose recent past breaks the prediction is telling you
something changed — a stall, a burst, a regime shift. That's the debugging
signal: anomaly = where prediction fails.
"""

from __future__ import annotations

from typing import List

import numpy as np

from . import Lens, Projection


class JepaLens(Lens):
    kind = "jepa"

    def __init__(self, context_frac: float = 0.5):
        self.context_frac = context_frac

    def project(self, series: List[float], events: List[dict]) -> Projection:
        s = np.asarray(series, dtype=float)
        n = len(s)
        if n < 8:
            return Projection(self.kind, "too little history to predict (honest abstain)",
                              0.5, {"reason": "series<8", "n": n})
        # predict on DIFFERENCES: cosine on raw levels is shift-tolerant and
        # misses regime shifts; the differenced trajectory can't hide a stall
        ds = np.diff(s)
        k = max(4, int(len(ds) * self.context_frac))
        if len(ds) < 8:
            return Projection(self.kind, "too little history to predict (honest abstain)",
                              0.5, {"reason": "series<9", "n": n})
        win = min(4, k - 2)
        X = np.stack([ds[i:i + win] for i in range(k - win)])
        y = ds[win:k]
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        Xt = np.stack([ds[i:i + win] for i in range(k - win, len(ds) - win)])
        yt = ds[k:]
        pred = Xt @ coef

        def cos(a, b):
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

        in_dist = cos(y, X @ coef)
        extrap = cos(yt, pred) if len(yt) >= 2 else 1.0
        score = max(0.0, min(1.0, 0.5 * (in_dist + 1.0) * 0.4 + max(0.0, extrap) * 0.6))
        verdict = (f"trajectory predicts itself (differenced extrapolation cos={extrap:.2f})"
                   if extrap > 0.7 else
                   f"REGIME SHIFT: recent cadence breaks prediction (cos={extrap:.2f})"
                   if extrap < 0.2 else
                   f"mild drift from predicted cadence (cos={extrap:.2f})")
        return Projection(self.kind, verdict, score,
                          {"in_dist_cos": round(in_dist, 3),
                           "extrapolation_cos": round(extrap, 3),
                           "differenced": True, "window": win, "n": n})
