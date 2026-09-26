"""Spectral lens — what is the project's heartbeat, and is it one drum or two?

The fourth question in the doctor's round: JEPA catches stalls, MOTH catches
chaos, JEV catches lies, SPECTRAL hears the heartbeat.

The cadence series is a signal: zero-padded to a power of two, spectrum taken
classically (numpy rFFT) and — when the quantum substrate is present —
measured on a real QFT circuit composed after QPAM amplitude encoding. The
two spectra must agree; that agreement is the honesty receipt.

Commensuration doctrine (twist-engine, ported): a single drum leaks energy
into sidelobes NEAR its fundamental — high local share, low second-peak
ratio. Two incommensurate drums put a second comparable peak FAR from the
first — that is quasiperiodicity, and it is a different diagnosis from
"no heartbeat" (flat spectrum). Any two frequency bins have a rational ratio
on a discrete grid, so rational-comb tests on bins are vacuous; the honest
observables are concentration, local share, and second-peak ratio.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from . import Lens, Projection


class SpectralLens(Lens):
    kind = "spectral"

    def __init__(self, shots: int = 8000, local_radius: int = 3,
                 second_tone_threshold: float = 0.5, seed: int = 0xC0CA):
        self.shots = shots
        self.local_radius = local_radius
        self.second_tone_threshold = second_tone_threshold
        self.seed = seed

    def _signal(self, series: List[float]) -> np.ndarray:
        s = np.asarray(series, dtype=float)
        s = s - s.mean()
        n = 1
        while n < len(s):
            n *= 2
        padded = np.zeros(n)
        padded[:len(s)] = s
        return padded

    def _fft_spectrum(self, sig: np.ndarray) -> np.ndarray:
        mag = np.abs(np.fft.rfft(sig))
        if len(mag) > 1:
            mag[0] = 0.0  # DC is not a heartbeat
        return mag

    def _qft_spectrum(self, sig: np.ndarray) -> Optional[np.ndarray]:
        try:
            import quantumaudio
            from qiskit import QuantumCircuit, transpile
            from qiskit.circuit.library import QFT
            from qiskit_aer import AerSimulator
        except ImportError:
            return None
        try:
            sch = quantumaudio.load_scheme("qpam")
            span = float(np.max(sig) - np.min(sig))
            if span < 1e-9:
                return None
            audio = ((sig - np.min(sig)) / span) * 2.0 - 1.0
            enc = sch.encode(audio, measure=False)
            nq = enc.num_qubits
            qc = QuantumCircuit(nq, nq)
            qc.compose(enc, inplace=True)
            qc.compose(QFT(nq, inverse=False), inplace=True)
            qc.measure(range(nq), range(nq))
            sim = AerSimulator(seed_simulator=self.seed)
            counts = sim.run(transpile(qc, sim), shots=self.shots).result().get_counts()
            probs = np.zeros(2 ** nq)
            total = sum(counts.values())
            for bitstr, c in counts.items():
                probs[int(bitstr, 2)] = c / total
            # QPAM amplitudes are real ⇒ the QFT spectrum is conjugate-symmetric
            # (bins k and N−k are the same physical frequency). Fold before
            # comparing to the rFFT — otherwise shot noise picks a mirror.
            n = len(probs)
            folded = np.zeros(n // 2 + 1)
            folded[0] = probs[0]
            for k in range(1, n // 2):
                folded[k] = probs[k] + probs[n - k]
            folded[n // 2] = probs[n // 2]
            if len(folded) > 1:
                folded[0] = 0.0  # DC is not a heartbeat
            return folded
        except Exception:
            return None

    def project(self, series: List[float], events: List[dict]) -> Projection:
        if len(series) < 16:
            return Projection(self.kind, "too little history for a spectrum (honest abstain)",
                              0.5, {"reason": "series<16", "n": len(series)})
        sig = self._signal(series)
        mag = self._fft_spectrum(sig)
        total = mag.sum() + 1e-12
        fft_bin = int(np.argmax(mag))
        n = len(sig)
        period_days = (n / fft_bin) if 0 < fft_bin < n // 2 else 0.0
        concentration = float(mag[fft_bin] / total) if fft_bin else 0.0

        near = np.zeros_like(mag)
        lo = max(1, fft_bin - self.local_radius)
        hi = min(len(mag), fft_bin + self.local_radius + 1)
        near[lo:hi] = mag[lo:hi]
        far = mag.copy()
        far[lo:hi] = 0.0
        local_share = float(near.sum() / total)
        second_tone = float(far.max() / mag[fft_bin]) if mag[fft_bin] > 1e-9 else 0.0

        receipts = {
            "dominant_period_days": round(period_days, 2) if period_days else None,
            "fft_top_bin": fft_bin,
            "peak_concentration": round(concentration, 3),
            "local_share": round(local_share, 3),
            "second_peak_ratio": round(second_tone, 3),
            "substrate": "fft-only",
            "shots": self.shots,
            "seed": self.seed,
        }

        qft_probs = self._qft_spectrum(sig)
        if qft_probs is not None and qft_probs.max() > 0:
            qft_bin = int(np.argmax(qft_probs))
            receipts["qft_top_bin"] = qft_bin
            receipts["substrate"] = "qft+fft"
            receipts["qft_agrees_with_fft"] = (qft_bin == fft_bin)
            receipts["real_signal_fold"] = True

        if concentration < 0.10:
            return Projection(self.kind,
                              "no heartbeat (flat spectrum) — activity has no periodic structure",
                              max(0.0, min(0.5, concentration * 5)), receipts)
        if second_tone >= self.second_tone_threshold:
            score = max(0.0, min(1.0, 0.3 + 0.3 * concentration))
            return Projection(self.kind,
                              f"heartbeat ~{period_days:.1f}d PLUS a second tone "
                              f"(ratio {second_tone:.2f}) — QUASIPERIODIC, incommensurate drums",
                              score, receipts)
        score = max(0.0, min(1.0, 0.5 + 0.5 * local_share))
        return Projection(self.kind,
                          f"heartbeat {period_days:.1f}d, single drum (local share "
                          f"{local_share:.2f}) — metronomic cadence",
                          score, receipts)
