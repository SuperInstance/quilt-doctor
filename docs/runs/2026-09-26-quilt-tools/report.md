# quilt-doctor — what's going on in `quilt-tools`

## Signals
- 20 commits over 35 days (3 active days; peak 13/day)

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

### MOTH — score 0.75
signal is COHERENT (H-basis entropy 1.48/6 bits, fidelity 1.00 @ 20000 shots)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 1.482
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.27
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 64.0
fft_top_bin: 1
peak_concentration: 0.054
local_share: 0.187
second_peak_ratio: 0.841
substrate: qft+fft
shots: 8000
qft_top_bin: 1
qft_agrees_with_fft: True
```

### JEV — score 0.70
recent work reads VERIFIABLE (mean substance 0.70 over 12 commits)

```
judged: 12
mean_substance: 0.697
latency_ms: 294.849157333374
model: jev-latest
```

## Substrate
- quilt WAL: 41 lines, verify: OK
- every verdict above is replayable from the chain
