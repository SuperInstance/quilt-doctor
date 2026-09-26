"""Book a moth-quantum coherence round as moth-ledger cells.

Division of labor (quilt-doctor doctrine): QPAM round-trip fidelity is
LOSSLESS for any signal — it proves the substrate ran, it cannot measure
coherence. The coherence meter here is the computational-basis Shannon
entropy of the encoded state: structured signals concentrate their mass on
few basis states (low entropy); noise spreads to the full 2^n (max entropy).

Basis note (earned, not assumed): a Hadamard-basis marginal ones-ratio is
NOT a coherence meter — a Z-concentrated spike Fourier-spreads to uniform
marginals and so does small-n noise. If the fleet ever wants an H-basis
meter, it must use joint distribution shape, not marginals. This bridge
stays in Z where concentration is directly honest.

Booked cells:
  FINDING/v1  one per planted signal — severity is the exact top-state
              mass q16_from_parts(top_count, shots) — refuse-never-round.
              The entropy itself is evidence in context (floats allowed
              there; only severity must be exact).
  VERDICT/v1  CONFIRMED iff the meter agreed with the planted ground truth
  ROUND_CLOSE the trial balance — unclosed expectations VIOLATE, so an
              imbalanced round can never be receipted as honest
  REFUSAL/v1  if the quantum stack is unavailable: one per expectation with
              context.close="REFUSED" — the bridge abstains, never fakes,
              and the books still balance (credits, not silence).

Usage (with moth-ledger on PYTHONPATH):
    PYTHONPATH=/path/to/moth-ledger/src python3 examples/moth_ledger_bridge.py
"""
from __future__ import annotations

import hashlib
import json
import math
import tempfile
from pathlib import Path

TARGET_REPO = "moth-quantum/quantum-audio"   # the real upstream (Moth Quantum) — SuperInstance/moth-quantum is a phantom
TARGET_COMMIT = "c8263fa6bc67"               # tag v0.2.0, verified via gh api 2026-09-27
SURFACE_ID = "qpam.z_basis_shannon_entropy"
CWE = "CWE-682"                        # incorrect calculation: coherence claimed, not measured
N_QUBITS = 3                           # 8 samples
SHOTS = 4096
THRESHOLD_BITS = 2.6                   # measured separation: sine 2.23 vs noise 2.88 (max 3.0)

# planted ground truth: expectation_id -> is_coherent
PLANTED = {
    "coh-periodic": True,              # single-period structure: concentrated mass
    "coh-noise": False,                # uniform random: spread to max entropy
}


def _signals():
    periodic = [math.sin(2 * math.pi * i / 8) for i in range(8)]
    # deterministic pseudo-noise (seeded — the round replays bit-for-bit)
    import random
    rng = random.Random(0x4D4F5448)  # "MOTH"
    noise = [rng.random() for _ in range(8)]
    return {"coh-periodic": periodic, "coh-noise": noise}


def _z_measure(samples, shots):
    """QPAM-encode, measure in the computational basis, return the honest meter:
    (entropy_bits, n_qubits, top_count) — all integers except entropy."""
    import numpy as np
    from quantumaudio import QPAM
    from qiskit_aer import Aer
    sch = QPAM()
    circuit = sch.encode(np.asarray(samples, dtype=float))
    n = circuit.num_qubits
    h = circuit.copy()
    h.measure_all()
    counts = Aer.get_backend("qasm_simulator").run(h, shots=shots).result().get_counts()
    total = sum(counts.values())
    entropy = -sum((v / total) * math.log2(v / total) for v in counts.values())
    top = max(counts.values())
    return entropy, n, top


def run_round(ledger_path, shots=SHOTS, threshold_bits=THRESHOLD_BITS):
    """Run the round; book every cell; return the close summary dict."""
    from moth_ledger import Ledger, Q16, close_round, make_producer, sha256_hex

    ledger = Ledger(ledger_path)
    producer = make_producer("quilt-doctor.moth-ledger-bridge", "1.0.0")
    occurred = "2026-09-27T01:00:00Z"  # pinned: the round is replayable, wall clock is not evidence

    try:
        measured = {exp: _z_measure(samples, shots) for exp, samples in _signals().items()}
        quantum_ran = True
    except Exception as exc:  # abstain honestly — credits, not silence
        quantum_ran = False
        for exp in PLANTED:
            ledger.append_refusal(
                producer, occurred,
                reason=f"quantum stack unavailable: {type(exc).__name__}",
                extra={"expectation_id": exp, "close": "REFUSED"},
            )

    if quantum_ran:
        for exp, (entropy, n, top_count) in measured.items():
            repro = sha256_hex(json.dumps(
                {"samples": _signals()[exp], "shots": shots, "threshold_bits": threshold_bits},
                sort_keys=True).encode())
            finding = ledger.append_finding(
                producer, occurred,
                target_repo=TARGET_REPO, target_commit=TARGET_COMMIT,
                surface_id=SURFACE_ID, cwe=CWE,
                severity=Q16.from_parts(top_count, shots),
                repro_hash=repro,
                extra={"expectation_id": exp,
                       "entropy_bits": round(entropy, 6), "n_qubits": n,
                       "top_state_mass": round(top_count / shots, 6),
                       "planted_coherent": PLANTED[exp]},
            )
            meter_says_coherent = entropy < threshold_bits
            verdict = "CONFIRMED" if meter_says_coherent == PLANTED[exp] else "REFUTED"
            rationale = (f"meter coherent={meter_says_coherent} (entropy {entropy:.4f} bits "
                         f"vs threshold {threshold_bits}); planted={PLANTED[exp]}")
            ledger.append_verdict(
                producer, occurred,
                finding_id=finding["id"], verdict=verdict,
                rationale_hash=sha256_hex(rationale.encode()),
            )

    close = close_round(ledger, producer, occurred,
                        round_id="moth-quantum-coherence-001",
                        expectations=list(PLANTED))
    ok, problems = ledger.verify_chain()
    return {
        "ledger": str(ledger.path),
        "quantum_ran": quantum_ran,
        "chain_verifies": ok,
        "chain_problems": problems,
        "closes": close["closes"],
        "close_row_id": close["id"],
    }


if __name__ == "__main__":
    out = Path(tempfile.mkdtemp(prefix="moth-ledger-round-")) / "round-001.jsonl"
    print(json.dumps(run_round(out), indent=2))
