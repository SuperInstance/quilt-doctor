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
signal is NOISE-LIKE (H-basis entropy 2.50/6 bits)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 2.497
hadamard_entropy_max_bits: 6
basis: hadamard
```

### JEV — score 0.74
recent work reads VERIFIABLE (mean substance 0.74 over 12 commits)

```
judged: 12
mean_substance: 0.736
latency_ms: 288.6558212339878
model: jev-latest
```

## Substrate
- quilt WAL: 40 lines, verify: OK
- every verdict above is replayable from the chain
