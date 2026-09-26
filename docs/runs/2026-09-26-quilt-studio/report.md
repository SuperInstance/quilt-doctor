# quilt-doctor — what's going on in `quilt-studio`

## Signals
- 52 commits over 35 days (6 active days; peak 25/day)

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

### MOTH — score 0.60
signal is NOISE-LIKE (H-basis entropy 2.42/6 bits)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 2.423
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.27
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 32.0
fft_top_bin: 2
peak_concentration: 0.053
local_share: 0.222
second_peak_ratio: 0.879
substrate: qft+fft
shots: 8000
qft_top_bin: 62
qft_agrees_with_fft: False
```

### JEV — score 0.73
recent work reads VERIFIABLE (mean substance 0.73 over 12 commits)

```
judged: 12
mean_substance: 0.726
latency_ms: 353.82020100951195
model: jev-latest
```

## Substrate
- quilt WAL: 41 lines, verify: OK
- every verdict above is replayable from the chain
