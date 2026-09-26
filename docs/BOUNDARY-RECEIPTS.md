# Boundary Receipts — hash-chained lens invocations (2026-09-26, overnight round 1)

**Doctrine ported:** `SuperInstance/wasm-cert-wedge` — receipt the TCB boundary.
Where the wedge binds agent source hash + tool identity + artifact hash in one
hash-chained row and books fuel-metered execution as EFFECT rows, quilt-doctor
now receipts its *measurement* boundary: every lens invocation books
BIND (input artifact) → EFFECT (projection hash) → TICK (round), and a lens
exception books REFUSAL and re-raises. A mismatch is a REFUSAL row, not a
silent gap.

**Module:** `quilt_doctor/wedge.py` — stdlib only, FNV-1a64 (fleet consensus,
cross-verified against quilt-arcade's kit.mjs: `fnv1a64("quilt") = 0x4b7fb2143373ce1e`
on both substrates), occurred/recorded split (rows appended when the event
occurs; `verify()` re-derives independently).

**Wiring:** `diagnose(..., ledger=BoundaryLedger())` — non-invasive, opt-in.

**Live run:** `env PYTHONPATH=<jev-quilt checkout> python3 examples/boundary_receipts.py`
— 8 projects × 4 lenses (JEPA / MOTHquantum / SPECTRAL / JEV-live):
**104 rows, verify: CLEAN.** Receipts: `docs/runs/boundary-ledger-2026-09-26.jsonl`
+ `docs/runs/boundary-receipts-2026-09-26.json`.

## Fleet round with boundary receipts (JEV live, 2026-09-26 ~09:55Z)

| project | JEPA | MOTH | SPECTRAL | JEV |
|---|---|---|---|---|
| git-agent | 0.200 | 0.703 | 0.301 | 0.748 |
| pong-quilt | 0.200 | 0.777 | 0.356 | 0.728 |
| quilt-tools | 0.200 | 0.744 | 0.270 | 0.694 |
| tidepool | 0.200 | 0.594 | 0.313 | 0.819 |
| quilt-studio | 0.200 | 0.594 | 0.267 | 0.719 |
| twist-engine | 0.200 | 0.543 | 0.296 | 0.667 |
| quilt-cowboy | 0.621 | 0.546 | 0.340 | 0.848 |
| hermit | 0.672 | 0.564 | 0.253 | 0.451 |

Notes (consistent with the morning holistic view):
- JEPA 0.200 across the six burst-driven repos = classical cadence
  predictability, not a stall verdict (sufficiency caveat self-carried).
- quilt-cowboy's JEPA 0.621 with JEV 0.848 = cadence AND receipts —
  the daemon narrates on a real adversarial spine.
- hermit remains the patient: JEPA 0.672, JEV 0.451 (vague claims).

## Why this matters (the moat)

Per the referral-graph weight law, an edge becomes VERIFIED by an in-repo
citation of canonical source. The IETF is taking agent receipts
standards-track (draft-marques-asqav) — transport commoditizes; ledger
semantics don't. A debugging tool whose every measurement is a
re-derivable chain row is the durable shape.

## Tests

`tests/test_wedge.py` — 10 pins: citation, genesis convention, fleet-consensus
hash, clean-chain verify, body tamper, prev-hash link, REFUSAL booking,
receipted-projection shape, JSONL roundtrip, truncation accounting.
