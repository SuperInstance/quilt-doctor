# JEV Field Notes — what the judgment lens is good for (2026-09-26)

Two live rounds (pong-quilt, jev-quilt, 12–54 commits each, real TypeSafe Jev
API calls) plus the eight-project fleet round. This is the "use jev
extensively and note what it's most/least useful" report.

## Most useful

1. **Hallucination receipts on vague claims.** hermit's "fixed critical
   reliability bugs without issue reports" scored 0.45 — and the receipt
   enumerated exactly what the claim lacked (no issue links, no failure
   modes, no before/after). The number is almost secondary; the receipt
   forces the model to make the gap legible. That is the product.
2. **Cross-repo comparability.** One rubric, four repos, two rounds:
   pong-quilt 0.74 / quilt-tools 0.70 / hermit 0.45 / jev-quilt 0.72→0.46.
   The axis is stable. The jev-quilt swing tracked a real shift — round 2's
   commits were genuinely more mechanical ("wip", "fix"). The lens caught a
   behavioral change, and reading the commits confirmed it. That is a
   diagnostic instrument, not a vibe.
3. **Abstention semantics.** Offline → 0.5 + `{"jev": "skipped"}` receipt.
   Absent lenses don't vote, so the quorum stays composable and honest.

## Least useful

1. **Small-n instability.** At 12 commits the mean swings on message mix,
   not substance. Below ~15 commits, treat the score as ±0.15 noise. The
   jev-quilt 0.72→0.46 swing was real, but we could only say so because we
   read the messages — the number alone wouldn't prove it at n=12.
2. **It can't see what the repo doesn't show.** "Adopted fleet-wide in
   production" scored on repo-surface evidence only. Its epistemic status is
   *verified-against-context*, never *true-in-the-world*. Every JEV verdict
   must carry that scope tag or it overclaims.
3. **Latency for CI gating.** 310–390ms per commit is fine for rounds; too
   slow for per-commit gates without batching. Batch n≥10 per call.

## The seam (v2 candidate)

JEV has no shuffle-null (judgment isn't series-shuffleable through the
commit series alone). But a **message-permutation null** would work: judge
shuffled commit messages as fake repos, calibrate the score's floor. If the
floor sits at 0.4, then 0.46 is indistinguishable from noise and the round-2
"shift" claim needs the receipts, not the number. Port of null-model
discipline into judgment — the last unguarded lens.
