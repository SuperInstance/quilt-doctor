# quilt-doctor

**Debugging tools on the quilt substrate.** Point it at any project; it answers
*"what's going on?"* by projecting the project's signals through three substrates —
JEPA, MOTHquantum, and JEV — writing everything to a hash-chained quilt WAL so the
diagnosis is replayable by anyone.

Built for the Cocapn Fleet directive: *create debugging tools that use quilt as a
substrate to project answers via JEPA, MOTHquantum, and JEV through dynamic
abstraction porting — and prove them by using them on other SuperInstance
projects.*

## The one idea

Every lens implements **one protocol** — `project(series, events) -> Projection`.
The substrate changes per lens; the interface never does. That is dynamic
abstraction porting made literal:

| Lens | Substrate | Question it answers |
|------|-----------|---------------------|
| **JEPA** | linear predictor on the differenced trajectory | *does the project's cadence predict itself?* A stall or burst breaks prediction — that's the regime-shift signal. |
| **MOTHquantum** | QPAM quantum circuit (`quantumaudio`, moth-quantum) | *is the signal music or noise?* Computational-basis round-trip fidelity proves the substrate ran; **Hadamard-basis measurement entropy** is the coherence meter — periodic cadence concentrates the spectrum, noise spreads it. |
| **JEV** | TypeSafe Jev decision model | *is the recorded work verifiable?* A noul aimed at each commit's specific claim (session-16 doctrine: specific nouls move on quality). |

Division of labor: **JEPA catches stalls, MOTH catches chaos, JEV catches lies.**
A project can be burst-y *and* coherent *and* honest — or any other mix. Three
axes, no single score hiding the truth.

Every `Projection` carries **receipts** — substrate config and the numbers the
verdict stands on. No naked verdicts. Offline lenses abstain with
`{"jev": "skipped"}` and a neutral 0.5: abstention is not condemnation.

## Quick start

```bash
python3 -m pytest tests -q            # 16 behavioral tests, FAIL-first built
python3 run_doctor.py <repo> out/     # full diagnosis incl. live JEV if TYPESAFEAI_KEY set
```

Output: `report.md` (human), `report.json` (machine), `quilt.jsonl` (the
substrate — verify it with `QuiltSubstrate.verify()`; every verdict is
replayable from the chain).

## Proof: two real SuperInstance projects (2026-09-26)

Both runs live: real git history, real QPAM circuits (AerSimulator), real Jev
API calls. Full receipts in [`docs/runs/`](docs/runs).

| Axis | pong-quilt | jev-quilt |
|------|-----------|-----------|
| signals | 54 commits, 3 active days, peak 28/day | 164 commits, 5 active days, peak 143/day |
| **JEPA** | 0.20 — REGIME SHIFT | 0.20 — REGIME SHIFT |
| **MOTH** | **0.78 — COHERENT** (H-entropy 1.32/6 bits) | **0.58 — NOISE-LIKE** (H-entropy 2.50/6 bits) |
| **JEV** | 0.72 — VERIFIABLE (12 commits, live) | 0.74 — VERIFIABLE (12 commits, live) |
| substrate | 40 WAL lines, verify OK | 40 WAL lines, verify OK |

**What the doctor says:** both repos are burst-driven (round-based development —
JEPA can't predict a burst from the last burst, honestly) and both record real,
checkable work (JEV agrees). But their *texture* differs: pong-quilt's bursts have
internal rhythm (coherent), jev-quilt's single-day 143-commit explosion is
noise-like. Same honesty profile, different heartbeat — a distinction no single
metric would surface.

## Honesty engineering (load-bearing)

- **Shot budget is a dial, not a footnote.** Starved QPAM shots produce noise;
  receipts always state shots and shots-per-amplitude
  (pong-quilt L2 spec, verified 2026-09-24: the shipped hash-canary claim was
  *refuted* at 2000 shots; we don't repeat that mistake).
- **Round-trip fidelity cannot measure coherence** — QPAM losslessly reconstructs
  *any* signal at honest shot budgets. The coherence meter is the
  **Hadamard-basis entropy** (basis change = a different question to the same
  quantum state). Verified empirically during the build.
- **Circuit reuse corrupts.** `sch.decode()` attaches measurements in place;
  the H-basis measurement gets a fresh circuit (encode twice).
- **Differenced trajectories.** Cosine on raw cadence levels is shift-tolerant
  and misses regime shifts; prediction runs on `diff(series)`.
- **Substrate honesty.** The quilt WAL (BIND/LINK/VIEW, fnv1a chain — vendored
  compact from the fleet's canonical producer, SuperInstance/git-agent PR #1)
  is written *with* the diagnosis and verifiable after it: the report is exactly
  as trustworthy as the chain it rode in on.

## Layout

```
quilt_doctor/
  substrate.py   # quilt WAL — the ground every verdict stands on
  collect.py     # git history -> series + events
  lenses/        # the protocol + three ports (jepa, moth, jev)
  doctor.py      # orchestrator + report rendering
run_doctor.py    # proof runner (writes report.md/json + quilt.jsonl)
tests/           # 16 behavioral tests
docs/runs/       # documented proof runs on SuperInstance projects
```

*quilt-doctor, Cocapn Fleet — Day 44. JEPA catches stalls, MOTH catches chaos,
JEV catches lies, and the quilt remembers who asked.*
