# quilt-doctor — what's going on in `git-agent`

## Signals
- 4 commits over 35 days (2 active days; peak 2/day)

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

### MOTH — score 0.71
signal is COHERENT (H-basis entropy 1.76/6 bits, fidelity 1.00 @ 20000 shots)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 1.76
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.30
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 64.0
fft_top_bin: 1
peak_concentration: 0.06
local_share: 0.206
second_peak_ratio: 0.845
substrate: qft+fft
shots: 8000
qft_top_bin: 63
qft_agrees_with_fft: False
```

### JEV — score 0.74
recent work reads VERIFIABLE (mean substance 0.74 over 4 commits)

```
judged: 4
mean_substance: 0.742
latency_ms: 299.8004239052534
model: jev-latest
```

## Substrate
- quilt WAL: 41 lines, verify: OK
- every verdict above is replayable from the chain
