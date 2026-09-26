# Two Axes: substance vs doctrine-voice (2026-09-26 overnight)

**Thesis.** `jev-quilt` (substance noul) asks *is it real?* — receipts,
hashes, verified claims. `quilt-jev-oracle` (three-voice composite) asks
*does it speak the walker's doctrine frequency?* These are orthogonal
axes; conflating them lets a fluent narrator pass for verified work, or
verified work fail for plain prose.

**Method.** JEV substance scores from the receipted fleet round
(`docs/BOUNDARY-RECEIPTS.md`, JEV-live per repo). Oracle voice =
`OracleLens` port of quilt-jev-oracle's canonical helpers, scored on each
repo's README. Cross-implementation calibration pin: drift ≤ 0.05 vs the
live `jev_probe.py` on shared inputs (tests/test_oracle_lens.py).

## The fleet on both axes

| repo | JEV (substance) | oracle (voice) | oracle promotes |
|---|---|---|---|
| git-agent | 0.748 | 0.678 | no (one voice short) |
| pong-quilt | 0.728 | 0.717 | yes |
| quilt-tools | 0.694 | 0.783 | yes |
| tidepool | 0.819 | 0.725 | yes |
| quilt-studio | 0.719 | 0.703 | yes |
| twist-engine | 0.667 | 0.808 | yes |
| quilt-cowboy | 0.848 | 0.808 | yes |
| hermit | 0.451 | 0.867 | **yes** |

## Readings

1. **hermit is the inverted patient.** Highest doctrine voice in the fleet
   (0.867 — the README sings the canon) and the weakest substance (0.451 —
   vague claims under JEV). Either axis alone misdiagnoses it: voice-only
   canon-promotes its README; substance-only flags it without hearing its
   song. The two together say: *the narration is real, the receipts aren't
   there yet.* That is a different prescription than either lens writes alone.
2. **quilt-cowboy is the both-and.** 0.848 substance with 0.808 voice — the
   daemon narrates fluently on a real adversarial spine. This is the shape
   the canon gate wants to promote.
3. **git-agent is the engineer's case.** Substantive receipts (0.748) but
   voice 0.678 — just under the gate, docked on form window (README is
   long: canon_worthy length_score 0.4) not on fluency. Plain true prose
   need not promote; the oracle is not a quality ranking, it is a
   frequency meter.
4. **Calibration confession.** An earlier note in this repo's history
   remembered the HOLISTIC-VIEW doc as composite 0.007 ("doctrine-silent").
   Re-running the live oracle on the actual file gives **0.658** — one
   voice short of the 0.7 gate, not silent. The 0.007 came from a stale
   probe input. Pin: `test_empirical_doc_near_gate_not_silent`. *Verify by
   running; never trust a remembered number.*

## Where this plugs in

- `OracleLens` (quilt_doctor/lenses/oracle.py) is opt-in, not in
  `available_lenses()` — the diagnose() protocol passes (series, events),
  which under-feeds a voice meter. Use it on document bodies.
- Natural fusion: canon-lint for AI-Writings (scout G's
  quilt-canon-lint idea) — promote only when BOTH axes clear:
  substance receipts present AND composite ≥ 0.7. hermit's README
  would be held; quilt-cowboy's would pass.
- The oracle's own repo name is the tell: *jev*-oracle — it began life
  as the Joint Embedding Validator. It is a judge of resonance, not
  truth. Keep the jobs separate.
