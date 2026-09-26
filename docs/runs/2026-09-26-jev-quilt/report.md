# quilt-doctor — what's going on in `jev-quilt`

## Signals
- 164 commits over 35 days (5 active days; peak 143/day)

## Projections
### JEPA — score 0.20
REGIME SHIFT: recent cadence breaks prediction (cos=0.00)

```
in_dist_cos: 0.0
extrapolation_cos: 0.0
differenced: True
window: 4
n: 35
```

### MOTH — score 0.58
signal is NOISE-LIKE (H-basis entropy 2.52/6 bits)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 2.518
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.17
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 3.05
fft_top_bin: 21
peak_concentration: 0.035
local_share: 0.234
second_peak_ratio: 0.996
substrate: qft+fft
shots: 8000
seed: 49354
qft_top_bin: 19
qft_agrees_with_fft: False
real_signal_fold: True
```

### JEV — score 0.75
recent work reads VERIFIABLE (mean substance 0.75 over 12 commits)

```
judged: 12
mean_substance: 0.748
latency_ms: 284.19817611575127
model: jev-latest
```

## Substrate
- quilt WAL: 81 lines, verify: OK
- every verdict above is replayable from the chain
