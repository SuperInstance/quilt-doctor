"""MOTHquantum lens — is the project's signal music or noise?

Ports the signal onto a QPAM quantum circuit (moth-quantum's quantumaudio).
Two measurements, two truths:

- COMPUTATIONAL basis: encode amplitudes -> sample -> reconstruct. Lossless
  at honest shot budgets for ANY signal — a fidelity of 1.0 proves the
  substrate ran, nothing more. (Round-trip fidelity cannot discriminate
  coherence; verified empirically 2026-09-26.)
- HADAMARD basis: rotate every qubit by H before measurement. Periodic,
  structured cadence concentrates the Walsh-Hadamard spectrum -> low Shannon
  entropy of the counts; noise spreads it -> entropy near n qubits. The
  entropy of the rotated measurement IS the coherence meter.

Shot budget is a first-class honesty dial (pong-quilt L2 spec, verified
2026-09-24): starved shots produce noise, and the receipt says so.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np

from . import Lens, Projection


class MothLens(Lens):
    kind = "moth"

    def __init__(self, shots: int = 8000, scheme: str = "qpam"):
        self.shots = shots
        self.scheme = scheme

    def _to_audio(self, series: List[float]) -> np.ndarray:
        s = np.asarray(series, dtype=float)
        span = float(np.max(s) - np.min(s))
        a = ((s - np.min(s)) / span) * 2.0 - 1.0 if span > 1e-9 else np.zeros(len(s))
        n = 1
        while n < len(a):
            n *= 2
        padded = np.zeros(n)
        padded[:len(a)] = a
        return padded

    def _encode(self, audio: np.ndarray):
        import quantumaudio  # type: ignore
        sch = quantumaudio.load_scheme(self.scheme)
        return sch, sch.encode(audio, measure=False)

    def _fidelity(self, sch, circuit, audio: np.ndarray) -> float:
        decoded = sch.decode(circuit, shots=self.shots)
        a = audio - audio.mean()
        b = np.asarray(decoded, dtype=float)[:len(audio)] - np.mean(decoded)
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / denom) if denom > 1e-9 else 0.0

    def _hadamard_entropy(self, circuit) -> Optional[Tuple[float, int]]:
        """Rotate to the Hadamard basis, measure, return (H_bits, n_qubits)."""
        try:
            from qiskit import QuantumCircuit, transpile
            from qiskit_aer import AerSimulator
        except ImportError:
            return None
        nq = circuit.num_qubits
        qc = QuantumCircuit(nq, nq)
        qc.compose(circuit, inplace=True)
        for q in range(nq):
            qc.h(q)
        qc.measure(range(nq), range(nq))
        res = AerSimulator().run(transpile(qc, AerSimulator()),
                                 shots=self.shots).result()
        counts = res.get_counts()
        total = sum(counts.values())
        probs = np.asarray(list(counts.values()), dtype=float) / total
        h = float(-(probs * np.log2(probs)).sum())
        return h, nq

    def project(self, series: List[float], events: List[dict]) -> Projection:
        if len(series) < 4:
            return Projection(self.kind, "too little signal to encode (honest abstain)",
                              0.5, {"reason": "series<4"})
        try:
            audio = self._to_audio(series)
            if float(np.max(audio) - np.min(audio)) < 1e-9:
                return Projection(self.kind,
                                  "constant signal (perfectly coherent by definition)",
                                  1.0, {"fidelity": 1.0, "basis": "none",
                                        "shots": self.shots})
            # encode TWICE: sch.decode() attaches measurements in place, which
            # would corrupt the H-basis measurement if they shared a circuit
            sch, circuit_fid = self._encode(audio)
            _, circuit_h = self._encode(audio)
            fidelity = self._fidelity(sch, circuit_fid, audio)
        except ImportError:
            return Projection(self.kind,
                              "substrate unavailable — abstaining (quantumaudio not installed)",
                              0.5, {"shots": self.shots, "scheme": self.scheme,
                                    "note": "import error"})
        except Exception as exc:  # honest fallback, labeled (L2 spec pattern)
            return Projection(self.kind, f"substrate error — abstaining ({exc})",
                              0.5, {"shots": self.shots, "scheme": self.scheme,
                                    "note": str(exc)})

        hb = self._hadamard_entropy(circuit_h)
        receipts = {"fidelity": round(fidelity, 3), "shots": self.shots,
                    "scheme": self.scheme,
                    "shots_per_amplitude": round(self.shots / max(1, len(series)), 1)}
        if hb is not None:
            h_bits, nq = hb
            coherence = max(0.0, min(1.0, 1.0 - h_bits / max(1, nq)))
            receipts.update({"hadamard_entropy_bits": round(h_bits, 3),
                             "hadamard_entropy_max_bits": nq,
                             "basis": "hadamard"})
            verdict = (f"signal is COHERENT (H-basis entropy {h_bits:.2f}/{nq} bits, "
                       f"fidelity {fidelity:.2f} @ {self.shots} shots)"
                       if coherence > 0.6 else
                       f"signal is NOISE-LIKE (H-basis entropy {h_bits:.2f}/{nq} bits)")
            return Projection(self.kind, verdict, coherence, receipts)
        receipts["basis"] = "computational"
        return Projection(self.kind,
                          f"round-trip faithful (fidelity {fidelity:.2f}) but coherence "
                          "meter unavailable (qiskit missing) — abstain on music-vs-noise",
                          0.5, receipts)
