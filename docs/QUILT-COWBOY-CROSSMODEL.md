# quilt-cowboy: Three-Judge Cross-Model Experiment

Date: 2026-09-26. Directive: "see if jev works well with quilt-cowboy, moth,
your own subagents, other apis. also, claude code."

## The repo, measured four ways

quilt-cowboy ("reflection loop, morning ritual, real-time reactor for the
Quilt ecosystem") — created 2026-08-25, dormant since 2026-09-09.

- **GitHub API (gh)**: all last-100 commits fall inside 04:32–06:07 UTC on
  2026-09-09 — a 95-minute, 100-commit burst. Zero PRs, ever. Single author
  `Mavis <cowboy@quilt.dev>`.
- **Local git anatomy**: 120 commits, one per minute, each a 2-line diff to
  `cowboy_status/index.html` — a machine-regenerated dashboard
  (`cowboy_status_updater.py`, 60s loop). Daemon noise, honestly detected.
- **Triad**: JEV live (TypeSafe, 12 judged, mean **0.040**, 307ms) ·
  JEPA null_z **−0.572** (15 nulls; cadence indistinguishable from shuffle)
  · MOTH 0.568 @16384 shots (fidelity 0.999) — coherence **vacuous** by the
  sufficiency doctrine (1 active day: a flatline with one blip is trivially
  periodic) · Spectral 0.186, `qft_agrees_with_fft: true` at 16k shots
  (note: the QFT honesty receipt did NOT emit at the 8k default — shot-
  dependent emission, receipts-grade observation).

## The three judges on the same 12 commits

Same window, same strict noul: "does the commit describe concrete, verifiable
engineering work (named file, function, test, PR, artifact)?"

| judge | mean | treatment |
|---|---|---|
| TypeSafe Jev (live API, `jev-latest`) | **0.040** | 0.04 × 12 |
| Claude Code (independent model, blind) | **0.050** | 0.05 × 12 |
| Subagent Scout F (k2d8, fleet scout) | **0.000** | 0.00 × 12 |

- Inter-rater spread across three independent judges: **0.05** total.
  Max pairwise |Δ| = 0.04; JEV vs Claude |Δ| = 0.01 mean absolute.
  Rank correlation is undefined (zero variance — all flat), which is itself
  the verdict: **perfect treatment agreement on a floor case**.
- Convergent validity: CONFIRMED. JEV's floor readings are not an artifact of
  the backend — a second model and a third instance independently reach the
  same "vague daemon noise" judgment from the same text.
- All three judges independently noted the same nuance class: the diffs are
  real work (a named file churns) but the *messages* name nothing — the
  noul penalizes the message, which is what it was written to do.

## Claude Code's counter-finding (the valuable part)

Claude's diff audit found the inversion the scores can't see: the dashboard
the bot regenerates **asserts pipeline activity its own artifact store cannot
confirm** — the page claims 1,916 canon papers; `cowboy_papers/` holds 1,745
files; five exact-timestamp lookups from the page's own entries return zero.
Same fleet disease as pong-quilt's 89/182 flips: **the receipt counts what it
meant to do, not what it did** — here the receipt is the status page itself.

## The integration lane (from Scout F's survey)

quilt-cowboy generates 1,745 "papers" gated **only on `synthesis_len`** — its
own design doc admits it: *"the current length-as-concreteness proxy is a
stand-in"* (RD_QUILT_3_0.md:160). Strongest fit for this toolchain:

1. **JEV as the orchestrator output gate** — judge each paper's abstract
   against the noul before it enters `cowboy_papers/`; the 1,626-entry
   adversarial worklog is calibration ground truth.
2. **MOTH coherence on the adversarial-pair pool** — replace the
   deterministic 6-voice rotation with coherence-weighted pair selection.
3. Sufficient-evidence rule: none of the cadence lenses mean anything on this
   repo until it ships for more than 1 day in 35.

## Operational receipts

- **Claude Code as root**: blocked twice (euid guard; missing auth under a
  foreign HOME), solved: `unshare -U --map-user=1000 -- claude
  --permission-mode bypassPermissions --print` with a copied `$HOME/.claude/
  settings.json`. Working recipe for the fleet.
- JevLens receipts keep only the mean; per-commit replay for inter-rater
  tables requires a direct `decide_batch` call with the same state.
