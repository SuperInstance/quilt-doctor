# quilt-doctor — what's going on in `pong-quilt`

## Signals
- 54 commits over 35 days (3 active days; peak 28/day)

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

### MOTH — score 0.78
signal is COHERENT (H-basis entropy 1.32/6 bits, fidelity 1.00 @ 20000 shots)

```
fidelity: 1.0
shots: 20000
scheme: qpam
shots_per_amplitude: 571.4
hadamard_entropy_bits: 1.322
hadamard_entropy_max_bits: 6
basis: hadamard
```

### JEV — score 0.72
recent work reads VERIFIABLE (mean substance 0.72 over 12 commits)

```
judged: 12
mean_substance: 0.719
latency_ms: 310.57303585112095
model: jev-latest
```

## Substrate
- quilt WAL: 40 lines, verify: OK
- every verdict above is replayable from the chain
