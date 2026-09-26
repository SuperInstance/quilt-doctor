# quilt-doctor — what's going on in `hermit`

## Signals
- 70 commits over 35 days (15 active days; peak 22/day)

## Projections
### JEPA — score 0.67
mild drift from predicted cadence (cos=0.55)

```
in_dist_cos: 0.708
extrapolation_cos: 0.55
differenced: True
window: 4
n: 35
```

### MOTH — score 0.56
signal is NOISE-LIKE (H-basis entropy 2.62/6 bits)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 2.616
hadamard_entropy_max_bits: 6
basis: hadamard
```

### SPECTRAL — score 0.25
no heartbeat (flat spectrum) — activity has no periodic structure

```
dominant_period_days: 3.05
fft_top_bin: 21
peak_concentration: 0.051
local_share: 0.21
second_peak_ratio: 0.998
substrate: qft+fft
shots: 8000
seed: 49354
qft_top_bin: 21
qft_agrees_with_fft: True
real_signal_fold: True
```

### JEV — score 0.46
recent work reads VAGUE (mean substance 0.46) — check what actually landed

```
judged: 12
mean_substance: 0.462
latency_ms: 289.2157919704914
model: jev-latest
```

## Substrate
- quilt WAL: 82 lines, verify: OK
- every verdict above is replayable from the chain
