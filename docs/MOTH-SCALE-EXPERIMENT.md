# MOTHquantum at Fleet Scale — Instrument Characterization

Date: 2026-09-26. Substrate: quantumaudio QPAM + qiskit Aer (moth lens).
Trigger: Casey's standing directive to use the environment's quantum keys at
grand scale, and the pong-quilt L2 lesson — a shipped hash-canary claim was
refuted at 2000 shots, so **the shot budget is a first-class receipt**.
Raw rows: `docs/moth-scale-2026-09-26.json` (8 repos × 4 budgets = 32 runs,
journaled to the quilt WAL).

## Q1 — What does the shot budget buy? (fidelity convergence)

| shots | fidelity range across 8 repos |
|---|---|
| 256 | 0.961 – 0.979 |
| 1024 | 0.986 – 0.996 |
| **4096** | **0.996 – 0.999** |
| 16384 | 0.999 – 1.000 |

Fidelity converges to 3-decimal honesty at **≥ 4096 shots**. Below that, any
fidelity claim carries sampling error in the third decimal. Production
default (20000) is fully converged; 4096 is the minimum honest budget.
This is the direct fix for the L2 refutation class: nobody can ship a
2000-shot canary again without the budget itself testifying.

## Q2 — The coherence meter at scale (Hadamard-basis entropy, max 6 bits)

Entropy rankings are **identical at 4096 and 16384 shots for all 8 repos** —
the ranking is a property of the repos, not the budget, once converged.

Coherence ladder at 16384 shots (1 − h/6):

| repo | active days | coherence | reading |
|---|---|---|---|
| pong-quilt | 3 | 0.777 | sprint sparsity, not rhythm |
| quilt-tools | 3 | 0.744 | sprint sparsity |
| git-agent | 2 | 0.704 | sprint sparsity |
| jev-quilt | 6 | 0.602 | marginal |
| tidepool | 7 | 0.594 | marginal |
| quilt-studio | 6 | 0.594 | marginal |
| hermit | 16 | 0.564 | below threshold |
| twist-engine | 5 | 0.544 | below threshold |

**Two traps found by running:**

1. **Low-shot coherence bias is optimistic.** Coherence at 256 shots reads
   0.02–0.05 HIGH for nearly every repo (sampling noise concentrates the
   H-basis distribution). Never report coherence below 4096 shots.
2. **A sprint is a drum solo.** The three "most coherent" repos are the three
   starved ones (2–3 active days). A mostly-zero cadence vector is trivially
   periodic. The coherence meter measures signal-shape entropy, not health,
   not structure, not virtue — among repos with sufficient data, coherence
   maxes at 0.602, barely at the 0.6 "music" threshold. **No fleet repo has a
   strong quantum heartbeat.** The classical jackknife (0/24 STABLE) and the
   quantum meter (best sufficient reading 0.602) agree: the house style is
   burst-driven everywhere.

## Q3 — Honesty across budgets

QFT-agreement receipts live in the spectral lens (verified fleet-wide ALIVE
by the `qft-honesty-fleet-wide` wildcard claim: 5 sufficient repos, zero
counterexamples). The moth sweep abstains on qft by design; cross-budget
honesty is the spectral lens's invariant, not the moth's.

## Doctrine upgrades (now in the receipts, not just this doc)

- `moth_shots=20000` default stays; **4096 is the floor for any reported
  fidelity/coherence number**.
- Coherence verdicts on starved series must carry the sufficiency caveat
  (doctor.py now annotates this automatically).
- A coherence ranking without an active-days column is a trap. Both columns
  or silence.
