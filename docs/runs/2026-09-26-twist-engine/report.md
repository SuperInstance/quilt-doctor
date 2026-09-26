# quilt-doctor — what's going on in `twist-engine`

## Signals
- 17 commits over 35 days (5 active days; peak 7/day)

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

### MOTH — score 0.54
signal is NOISE-LIKE (H-basis entropy 2.74/6 bits)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 2.74
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.30
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 32.0
fft_top_bin: 2
peak_concentration: 0.059
local_share: 0.226
second_peak_ratio: 0.852
substrate: qft+fft
shots: 8000
seed: 49354
qft_top_bin: 2
qft_agrees_with_fft: True
real_signal_fold: True
```

### JEV — score 0.68
recent work reads VERIFIABLE (mean substance 0.68 over 12 commits)

```
judged: 12
mean_substance: 0.682
latency_ms: 314.0660785138607
model: jev-latest
```

## Substrate
- quilt WAL: 82 lines, verify: OK
- every verdict above is replayable from the chain
