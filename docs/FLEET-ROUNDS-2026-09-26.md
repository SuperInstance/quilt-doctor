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

## How to reproduce

```bash
python3 run_doctor.py <repo> docs/runs/<date>-<name>   # one project
python3 -m pytest tests -q                             # 21 behavioral tests
```
