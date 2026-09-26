# quilt-doctor — what's going on in `tidepool`

## Signals
- 17 commits over 35 days (7 active days; peak 7/day)

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
signal is NOISE-LIKE (H-basis entropy 2.41/6 bits)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 2.412
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.31
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 64.0
fft_top_bin: 1
peak_concentration: 0.063
local_share: 0.219
second_peak_ratio: 0.652
substrate: qft+fft
shots: 8000
qft_top_bin: 1
qft_agrees_with_fft: True
```

### JEV — score 0.83
recent work reads VERIFIABLE (mean substance 0.83 over 12 commits)

```
judged: 12
mean_substance: 0.826
latency_ms: 296.20051570236683
model: jev-latest
```

## Substrate
- quilt WAL: 41 lines, verify: OK
- every verdict above is replayable from the chain
