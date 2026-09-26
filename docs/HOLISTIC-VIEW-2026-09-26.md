# The Holistic View — JEV × JEPA × MOTH on the Fleet

Date: 2026-09-26. Directives: "keep your scientists working with jev and
jepa and moth and close the gap of understanding in a holistic view."

## The question

Are the three lenses measuring **one thing or three things**? If one, their
scores should correlate across repos. If three, each sees something the
others cannot — and the holistic view is the triangulation, not the average.

## Protocol

Same 35-day window for all 8 fleet repos. JEV live via TypeSafe Jev (12
commits/repo, noul: "does this commit describe concrete, verifiable
engineering?"). JEPA on `diff(series)` with 15-permutation null. MOTH as
Hadamard-basis entropy at **16384 shots** (the converged budget — see
MOTH-SCALE-EXPERIMENT.md). Correlations: Spearman with **exact enumeration
of all 8! = 40,320 rank permutations** — no Monte Carlo, no sampling error,
p_min = 1/40320 ≈ 2.5e-5. Ties averaged. Confounder (active_days) declared
before looking at results; sufficient-only (n=5) subsets reported alongside.

## The matrix

| repo | active days | JEV substance | JEPA score | JEPA null_z | MOTH coherence@16k |
|---|---|---|---|---|---|
| pong-quilt | 3 | 0.709 | 0.200 | (starved) | 0.777 |
| quilt-tools | 3 | 0.695 | 0.200 | (starved) | 0.744 |
| git-agent | 2 | 0.742 | 0.200 | (starved) | 0.704 |
| tidepool | 7 | 0.825 | 0.200 | (see stats) | 0.594 |
| quilt-studio | 6 | 0.725 | 0.200 | (see stats) | 0.594 |
| jev-quilt | 6 | 0.748 | 0.200 | (see stats) | 0.602 |
| twist-engine | 5 | 0.673 | 0.200 | (see stats) | 0.544 |
| hermit | 15 | **0.450** | **0.672** | (see stats) | 0.564 |

## Results (exact p, full enumeration)

| test | n | rho | p_exact | verdict |
|---|---|---|---|---|
| moth ~ active_days | 8 | −0.639 | 0.094 | confounder has real pull (near-miss) |
| jepa_score ~ active_days | 8 | +0.584 | 0.250 | score degenerate below sufficiency |
| jev ~ active_days | 8 | −0.012 | **0.988** | hypothesis KILLED (below) |
| moth ~ jev (sufficient) | 5 | +0.800 | 0.133 | sign-stable, power-starved |
| moth ~ jepa_null_z (sufficient) | 5 | −0.600 | 0.350 | nothing |
| jev ~ jepa_null_z (sufficient) | 5 | **−0.900** | **0.083** | sign-stable, power-starved |

### Killed in public
"Continuously-working repos write vaguer commits" — my own speculation from
the round-1 hermit receipt (0.45). Exact p = 0.988 across the cohort. Hermit's
vagueness is hermit's culture, not a law of the fleet. A single repo must not
wear the fleet's clothes.

### Sign-stable but significance-starved
`jev ~ jepa_null_z`: rho = −0.900, and **the sign holds under every
leave-one-out** (−0.8 to −1.0 across all 5 deletions) — but p never reaches
0.05 (best 0.083; n=4 permutation floor is 0.042). Direction: repos with
classically unpredictable cadence write more verifiable commits. Registered
as a hypothesis with receipts, NOT a law. Re-test when the sufficient cohort
grows past n=8.

### The confounder, quantified
moth ~ active_days at rho −0.64 (p=0.094, near-miss even at n=8): the sprint
trap has real gravitational pull — more sparse activity, more trivially
"coherent" the quantum meter reads. This is the receipts-grade form of the
drum-solo finding.

## What each scientist sees that the others cannot

- **JEV reads content** — it is the only lens that opens the commit
  messages. No shuffle-null exists for judgment; that gap is stated on every
  receipt, not hidden. It fired hardest on hermit: the repo with the
  steadiest work writes the vaguest claims.
- **JEPA reads dynamics** — the only lens that asks "does yesterday predict
  today?" It fires only when there is variation to learn: 7 of 8 repos score
  *exactly* 0.200 — the score is a sufficiency gate below ~5 active days,
  not a measurement. Use null_z as the evidence column there.
- **MOTH reads phase** — the only quantum lens, and the only one that can be
  fooled by sparsity (the trap, now receipts-grade). At converged shots it
  agrees with the classical jackknife: no fleet heartbeat.

## The holistic verdict

**Three things, not one — at cohort scale, today.** No cross-lens
correlation survives exact permutation. But the triangulation converges on
two durable statements:

1. **Recording discipline and working discipline are decoupled.** hermit:
   JEPA 0.672 (work rhythm is real) × JEV 0.45 (the record of it is
   uncheckable) × MOTH 0.564 (rhythm real but irregular). The fleet's most
   predictable worker keeps the least checkable diary.
2. **Burst-driven everywhere, proven two independent ways.** Classical
   jackknife: 0/24 repo×lens windows STABLE. Quantum meter: best sufficient
   coherence 0.602. When two substrates disagree about nothing and agree
   about this, the answer is substrate-independent.

## Registered hypothesis (round 2 trigger)

`jev ~ jepa_null_z` negative coupling, rho −0.9, sign-stable under LOO,
p=0.083. Re-run when ≥8 repos have ≥5 active days. Until then it is a
hypothesis with a receipt, exactly the class of claim BEACONS doctrine
demands — and exactly the class this document refuses to overstate.
