# Quilt-Verilog Round M — Independent Replication Verdict

Date: 2026-09-26. Replicator: quilt-doctor (fair-judge pass on the audit's own subject).
Method note: every number below comes from running the archive's own shipped code
(`round_m_direct_correlation.py`), not from re-derivation.

## What was replicated

The archive's centerpiece banner: **"C_trust = 0.000328, p < 0.0001, 5/5 REAL
SIGNAL, the wall is breakable."**

Two passes:

1. **Faithful pass** — archive script unmodified, seed=123.
   Central number reproduced exactly: T2 C_trust = +0.000328. The experiment
   is real, deterministic, and re-runnable. The code exists and does what the
   report says it does, at the printed precision.
2. **Independent pass** — fresh seed (9999), honest permutation resolution
   (n_perm=1000, p_min = 1/1001 ≈ 0.001, vs the archive's n_perm=50 whose
   floor is 1/51 ≈ 0.0196), empirical and null both on a fixed 800-tick
   subsample so the comparison is apples-to-apples.

## Verdicts

### BONE 1 — the p-resolution is a formatting artifact
With n_permutations=50, no p below 1/51 ≈ 0.0196 is resolvable. The script
prints `p=0.0000` for "0 of 50 permutations exceeded the empirical value" —
a count of zero, not a probability of zero. The report's "p < 0.0001" is
unreachable with its own machinery. The correct statement for T2 at seed 123
is **p ≈ 0.02**.

### BONE 2 — the headline config is seed-fragile
At fresh seed 9999, the headline T2 config (J=1.0, 2 planted cohorts) gives
subsampled C_trust = +0.000072 with **p = 0.046** — marginal, not
breakthrough. T3 (J=2.0) gives C_trust ≈ 0, **p = 1.0**: at strong coupling
the cells freeze into refractory lockstep and the full-window correlation is
a finite-length artifact that vanishes under subsampling. "5/5 configs
REAL SIGNAL" was 5/5 at one seed, with one config an artifact.

### GOLD 1 — the Round R critical point survives a fresh seed
J=0.25, n=32, 4 planted cohorts: C_trust = +0.002433, ratio 3.26× vs
non-trust baseline, **p = 0.001** — the largest and most significant effect
in the whole table, under a seed the archive never used. The archive's own
instinct (Round R > Round M, "accidental Ising critical point") is the
result that replicates. This is the one to push.

### GOLD 2 — the chance-cluster effect is the most robust thing in the archive
T4 ("random" dials — random dial assignment but still SimHash-proximity trust
edges): C_trust = +0.000588, **p = 0.003** at fresh seed. OP_GIBBS correlates
hash-proximate cells whether or not the clusters were planted; chance
clusters amplify at 95× their non-trust baseline. The report files this as a
footnote. It is the most cross-seed-robust phenomenon in the dataset, and it
is the honest mechanism statement: **the detector measures trust-graph
clustering, not planted-cohort detection**. Planted cohorts merely make the
clustering deliberate.

### Calibration warning the archive never discusses
At the archive's seed, the planted 2-cohort ratio (1.51×) is LOWER than the
random-dial ratio (5.42×). The structure detector responds *more strongly*
to accidental clustering than to planted cohorts at identical J. Any
"spontaneous structure" reading must carry this caveat: the ratio is not a
calibrated measure of plantedness.

## Mechanism (honest form)

Trust edges are built from SimHash Hamming proximity (d ≤ tau) over the dial
vectors. OP_GIBBS ferromagnetically couples along trust edges
(P(accept ΔE) = 1/(1+e^{βΔE}), dials diffuse toward neighbors). Any dial
clustering — planted or chance — becomes awake-pattern correlation. At
J ≈ 0.25 near the effective critical point, response peaks (Round R). At
J ≥ 1 the system orders globally and contrast washes out; at J = 2 it
freezes and the correlation is an artifact of full-length windowing.

"The wall is a limit point in disguise" — true, and the limit point is the
Ising critical region, which the archive found by accident in Round R and
oversold in Round M.

## Replication receipts

| config (seed 9999, n_perm=1001, T_sub=800) | C_trust | p |
|---|---|---|
| C1 J=0 planted control | -0.000809 | 1.000 |
| T2 J=1.0 planted 2coh | +0.000072 | 0.046 |
| T3 J=2.0 planted 2coh | ≈ 0 | 1.000 |
| T4 J=1.0 random dials | +0.000588 | 0.003 |
| J=0.25 planted 2coh | -0.000159 | 0.840 |
| J=0.25 random dials | +0.000302 | 0.125 |
| T5 J=1.0 planted 4coh n=32 | +0.000659 | 0.001 |
| **R5 J=0.25 planted 4coh n=32** | **+0.002433** | **0.001** |

Replication script: `/tmp/roundm_replication.py` (runs the archive harness
bitmask-accelerated; empirical and null on the same fixed 800-tick subsample).
