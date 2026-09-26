# Fleet Rounds — 2026-09-26

The doctor's first house call: eight SuperInstance projects, four lenses,
every verdict live (real git history, real QPAM+QFT circuits on AerSimulator,
real TypeSafe Jev API calls), every WAL verifiable after the run.

Division of labor: **JEPA catches stalls · MOTH catches chaos · SPECTRAL hears
the heartbeat · JEV catches lies.**

## The chart

| project | JEPA (regime) | MOTH (chaos) | SPECTRAL (heartbeat) | JEV (substance) |
|---------|---------------|--------------|----------------------|-----------------|
| pong-quilt | 0.20 shift | **0.78 coherent** | flat (bursts) | 0.72 verifiable |
| quilt-tools | 0.20 shift | **0.75 coherent** | flat | 0.70 verifiable |
| git-agent | 0.20 shift | 0.71 coherent | flat | 0.74 verifiable |
| jev-quilt | 0.20 shift | 0.58 noise-like | flat | 0.74 verifiable |
| quilt-studio | 0.20 shift | 0.60 noise-like | flat | 0.73 verifiable |
| tidepool | 0.20 shift | 0.60 noise-like | flat | **0.83 verifiable** |
| twist-engine | 0.20 shift | 0.55 noise-like | flat | 0.67 verifiable |
| hermit | **0.67 mild drift** | 0.56 noise-like | flat | **0.45 VAGUE** |

All runs: `docs/runs/2026-09-26-<project>/{report.md,report.json,quilt.jsonl}` —
substrate verify OK on all 8 (40–41 WAL lines each). Re-run after the spectral
lens fixes below: 7/8 QFT↔FFT dominant-bin agreement; jev-quilt disagrees
honestly — on a flat spectrum the QFT argmax over noise bins is arbitrary,
and the no-heartbeat verdict never depended on it.

## What the doctor says

**The fleet is honest.** Eight repos, eight JEV runs, mean substance 0.45–0.83
— every project except one records checkable work. The receipts name the
commits and the model (`jev-latest`, ~300 ms per call).

**Everyone is burst-driven; nobody has a heartbeat.** SPECTRAL finds no
project with periodic structure — the fleet works in rounds and surges, not
metronomes. That is a *finding about the fleet*, not a defect in the lens:
round-based development is the house style (pong-quilt Rounds, jev-quilt
sessions). A 7-day drum would be the anomaly here.

**Two textures of burst.** pong-quilt, quilt-tools, git-agent bursts are
*coherent* (H-entropy 1.3–1.8/6 bits): within-burst structure, round sessions
that hang together. jev-quilt, quilt-studio, tidepool, twist-engine bursts are
*noise-like* (2.4–2.7 bits): dense multi-thread pushes without internal
rhythm. Same honesty, different texture — invisible to any single metric.

**hermit is the patient to watch.** The only repo whose cadence a predictor
can follow (JEPA 0.67, mild drift — steady maintenance, no regime break)
AND the only repo whose recent commits read vague (JEV 0.45). Steady activity
whose recorded claims don't say what landed. The doctor's prescription:
before hermit's next merge, ask *which specific artifact changed* — the
receipts say the log won't answer.

## New lens shipped this round: SPECTRAL

Fourth substrate port, same protocol. Classical rFFT + real QFT circuit
composed after QPAM encoding; `qft_agrees_with_fft` receipt on every quantum
run — the two spectra must name the same dominant bin or the substrate is
lying. Two physics corrections earned during the build, now in receipts:

1. **Rational-comb tests on discrete bins are vacuous** — any two bins have
   a rational ratio. Commensuration is measured as *peak geometry* instead:
   concentration, local share (sideline leakage = one drum), second-peak
   ratio (a comparable far peak = two incommensurate drums).
2. **QFT needs a fresh circuit.** `sch.decode()` mutates in place (found last
   round for the H-basis; same discipline here — encode twice).

Quasiperiodic test vector (7d + 13.7d): correctly flagged
`second_peak_ratio=0.79 → QUASIPERIODIC`. Weekly vector: `heartbeat 7.1d,
single drum → metronomic`. Noise: `flat spectrum`.

## BEACONS — falsifiable claims with kill conditions

Claims from these rounds, stated so a future round can KILL them
(BEACONS doctrine, ported from the quilt-verilog research program —
a claim without a kill condition is not a claim):

| Claim | Receipt anchor | Kill condition |
|-------|---------------|----------------|
| pong-quilt's bursts are coherent structure, not convention | MOTH healthy 0.93–1.33 bits, far above noise | two consecutive rounds with null_z < 1.5 (indistinguishable from shuffle-null) |
| hermit's cadence is predictable structure | JEPA 0.67 with spectral peak at 1/7d | null_z < 1 on the cadence score in any round |
| NO fleet repo has a heartbeat (bursts are the house style) | 0/8 heartbeat; spectral entropy 0.76–0.95 | any repo shows a periodic peak with z > 3 |
| MOTH coherence ordering (noise < healthy) is a real observable | ordering held in synthetic triangulation | ordering inverts in two consecutive rounds |
| QFT and FFT agree when the series has enough bins | 7/8 agree; jev-quilt = small-n shot noise | qft_agrees=False on a repo with ≥ 30 commits and a stable FFT peak |

## Null-cohort round (same day, null receipts wired in)

Every score below is accompanied by its shuffle-null z: how many standard
deviations the real series sits from shuffled versions of itself pushed
through the SAME lens. |z| < 1 = indistinguishable from convention — the
roundK guard, now standard equipment.

| project | JEPA (z) | MOTH (z) | SPECTRAL (z) | qft |
|---------|----------|----------|--------------|-----|
| pong-quilt | 0.20 (−0.88) | 0.78 (**8.04**) | 0.354 (**6.87**) | agrees |
| quilt-tools | 0.20 (−0.86) | 0.74 (**6.23**) | 0.270 (**6.52**) | agrees |
| git-agent | 0.20 (−0.61) | 0.73 (**6.34**) | 0.294 (**6.22**) | agrees |
| quilt-studio | 0.20 (−5.31) | 0.59 (**5.12**) | 0.267 (0.31) | agrees |
| tidepool | 0.20 (−6.88) | 0.59 (1.98) | 0.313 (1.67) | agrees |
| jev-quilt | 0.20 (−2.75) | 0.60 (0.77) | 0.214 (1.05) | agrees |
| twist-engine | 0.20 (−1.70) | 0.54 (−0.48) | 0.296 (0.37) | agrees |
| hermit | 0.67 (0.30) | 0.56 (−0.77) | 0.253 (−2.44) | agrees |

Reading:
- **Coherent-burst structure is real** in pong-quilt / quilt-tools / git-agent
  (moth z > 6) and quilt-studio (z=5.12): their burst texture survives
  shuffling by 5–8σ. Not a metric convention.
- **The JEPA 0.20 "regime shift" is itself structure**: shuffled series score
  HIGHER regime-shift (z strongly negative) because shuffling destroys the
  burst blocks. Very negative JEPA z = strong block structure.
- **hermit has NO verifiable cadence structure on this window**: jepa z=0.30,
  moth z=−0.77 — both indistinguishable from shuffle. Round 1's "1/7d
  predictable cadence" was a longer-window reading; the null guard retracts
  it here.
- twist-engine and jev-quilt read structureless on 35d windows (|z| < 1).
  Small windows, bursty repos — extend the window before concluding anything.

## Claims round 1 — executable BEACONS verdicts

23 claims in `claims/fleet-2026-09-26.json`, evaluated against the receipts
above: **22 ALIVE, 1 KILLED.**

- ☠ **hermit-cadence KILLED** (jepa null_z 0.30 < 1.0). The claim as stated
  is dead. hermit's interest now rests on its JEV evidence only.
- **Encoding bug confessed and fixed**: the no-heartbeat claims originally
  killed on `spectral null_z > 3` — the wrong proxy (structure-z, not
  heartbeat). That produced 3 false kills. Heartbeat = one dominant drum, so
  the kill condition now reads `peak_concentration > 0.35`. After the fix,
  all 8 no-heartbeat claims ALIVE — still no drummer in the fleet.
- Streak claims (pong-coherent, moth-ordering ×5) register first breaches
  as warnings; one data point never kills a streak claim.

A claim that cannot be killed by its own machinery is not a claim; a kill
condition on the wrong receipt is a bug. Both lessons now live in code.

## How to reproduce

```bash
python3 run_doctor.py <repo> docs/runs/<date>-<name>   # one project
python3 -m pytest tests -q                             # 25 behavioral tests
```

---

## Round 2 — jackknife + guard (2026-09-26 12:05 UTC)

**The jackknife killed a headline interpretation.** pong-quilt's 57 commits
all fall inside 2 active days (Aug 27-28); the 30-day windows either side
are empty. The full-window moth null_z of 8.04 was window-emptiness
inflation: measured per-window, the z hits 52.95 in the one nonempty window
and is undefined in the empty ones. A single sprint is not "coherent burst
structure" — it is one weekend.

**Guard shipped** (`MIN_ACTIVE_DAYS = 5`): claims evaluated on starved
series return `INSUFFICIENT_DATA`, name the active-day count, and never
touch the kill streak. FAIL-first: 4 tests, then implement.

**Claims round 2** (fresh active-day counts per repo):

- 12 ALIVE / 1 KILLED (hermit-cadence, stays dead) / 10 INSUFFICIENT_DATA
- Claims previously ALIVE on pong-quilt / quilt-tools / git-agent z-scores
  are voided: those repos have 3, 3, and 2 active days. The z-scores were
  measuring the emptiness of the window.
- twist-engine passes the guard at exactly 5 active days — borderline,
  noted.

Active-day census (35d window): hermit 16, tidepool 7, quilt-studio 6,
jev-quilt 6, twist-engine 5, pong-quilt 3, quilt-tools 3, git-agent 2.
The fleet's honest summary: one continuously-active repo (hermit, and its
cadence claim is killed as convention), five sporadic, two sprints.

**Round M replication verdict** (full doc: QUILT-VERILOG-REPLICATION.md):
- Faithful pass reproduces C_trust = 0.000328 exactly — the code is real.
- p < 0.0001 is a formatting artifact (50 perms → floor 1/51 ≈ 0.02).
- Headline config is seed-fragile: fresh seed → p = 0.046; J=2.0 config is
  a window-length artifact (p = 1.0 under subsampling).
- Round R critical point (J=0.25, n=32, 4 cohorts) survives fresh seed at
  p = 0.001 with the largest effect in the table — push that one.
- The chance-cluster amplification (T4) is the most robust cross-seed
  phenomenon: the detector measures trust-graph clustering, not plantedness.

---

## Round 3 — full-cohort jackknife + wildcard claims (2026-09-26 13:20 UTC)

**Jackknife extended to all 8 repos** (3×30d windows over 90d, jepa/moth/spectral):

| repo | jepa | moth | spectral |
|---|---|---|---|
| pong-quilt (3d active) | QUIET | FRAGILE (52.95 in the one burst window) | FRAGILE (2.65) |
| quilt-tools (3d) | QUIET | FRAGILE (54.42) | FRAGILE (2.65) |
| git-agent (2d) | QUIET | FRAGILE (2.19 in the OLD window) | QUIET |
| tidepool (7d) | QUIET | FRAGILE (2.27) | QUIET |
| quilt-studio (6d) | QUIET | FRAGILE (2.26) | QUIET |
| jev-quilt (6d) | QUIET | QUIET | QUIET |
| twist-engine (5d) | QUIET | QUIET | QUIET |
| hermit (16d) | QUIET (3 windows all data!) | QUIET (3 windows) | FRAGILE (2.35, one window) |

**Verdict: ZERO repo×lens combinations are STABLE.** Every "structure" claim in
the fleet is one burst window — the pong-quilt pattern replicated 8×. The
35-day-window z-scores that looked like structure were all window-emptiness
inflation. Hermit, the only repo with data in all 3 windows, shows no stable
structure anywhere — it just has enough data to say so honestly.

**Claims registry additions:**
- `doctor.py` now self-carries sufficiency: `active_days`, `data_sufficient`,
  and a ⚠ banner in the rendered report. Every projection's receipts carry
  the same caveat. (tests/test_sufficiency.py, seeded sprint-repo fixture)
- Wildcard claims (`repo: "*"`): universal across repos with sufficient data;
  one named counterexample kills; insufficient repos are skipped, never
  counterexamples. (tests/test_wildcard.py)
- New claim `qft-honesty-fleet-wide` [*]: **ALIVE — 5 repo(s), counterexamples:
  none.** The quantum honesty receipt holds fleet-wide on sufficient repos.

**Cross-validation from the field:** pong-quilt R22 (another agent, PR #29)
found R21's quantum-coin journal receipted 89 of 182 actual flips — the same
receipt-inflation disease my jackknife caught in the z-scores, in the
fleet's honesty centerpiece. The diagnosis generalizes: **the fleet counts
what it meant to do, not what it did.** quilt-doctor is the cure.
