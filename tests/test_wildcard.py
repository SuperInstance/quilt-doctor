"""Wildcard claims: one universal claim evaluated across every repo with
sufficient data. Universal = killed by a single counterexample (with the
usual streak grace); insufficient-data repos are skipped, not counterexamples."""
import sys

sys.path.insert(0, "/tmp/quilt-doctor")


def test_wildcard_universal_pass():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = {
        "a": [{"lens": "spectral", "receipts": {"qft_agrees_with_fft": True}}],
        "b": [{"lens": "spectral", "receipts": {"qft_agrees_with_fft": True}}],
    }
    claim = Claim(id="qft-everywhere", repo="*", lens="spectral",
                  kill_if={"receipt": "qft_agrees_with_fft", "op": "==",
                           "value": False},
                  kill_after_streak=1, text="qft honesty receipt fleet-wide")
    v = evaluate_claims([claim], projs, {}, repo_active_days={"a": 10, "b": 10})
    assert v[0].status == "ALIVE"
    assert "2 repo" in str(v[0].observed)


def test_wildcard_single_counterexample_kills():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = {
        "a": [{"lens": "spectral", "receipts": {"qft_agrees_with_fft": True}}],
        "b": [{"lens": "spectral", "receipts": {"qft_agrees_with_fft": False}}],
    }
    claim = Claim(id="qft-everywhere", repo="*", lens="spectral",
                  kill_if={"receipt": "qft_agrees_with_fft", "op": "==",
                           "value": False},
                  kill_after_streak=1)
    v = evaluate_claims([claim], projs, {}, repo_active_days={"a": 10, "b": 10})
    assert v[0].status == "KILLED"
    assert "b" in str(v[0].observed)  # names the counterexample


def test_wildcard_streak_grace_across_rounds():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = {"b": [{"lens": "spectral",
                    "receipts": {"qft_agrees_with_fft": False}}]}
    claim = Claim(id="qft-everywhere", repo="*", lens="spectral",
                  kill_if={"receipt": "qft_agrees_with_fft", "op": "==",
                           "value": False},
                  kill_after_streak=2)
    state = {}
    v1 = evaluate_claims([claim], projs, state, repo_active_days={"b": 10})
    assert v1[0].status == "ALIVE"  # one breach, streak 1 < 2
    v2 = evaluate_claims([claim], projs, state, repo_active_days={"b": 10})
    assert v2[0].status == "KILLED"  # second consecutive breach


def test_wildcard_skips_insufficient_repos():
    from quilt_doctor.claims import Claim, evaluate_claims

    projs = {
        "a": [{"lens": "spectral", "receipts": {"qft_agrees_with_fft": True}}],
        "b": [{"lens": "spectral", "receipts": {"qft_agrees_with_fft": False}}],
    }
    claim = Claim(id="qft-everywhere", repo="*", lens="spectral",
                  kill_if={"receipt": "qft_agrees_with_fft", "op": "==",
                           "value": False},
                  kill_after_streak=1)
    # b has 2 active days -> skipped; a is not a counterexample
    v = evaluate_claims([claim], projs, {}, repo_active_days={"a": 10, "b": 2})
    assert v[0].status == "ALIVE"
    assert "1 repo" in str(v[0].observed)


def test_wildcard_all_insufficient_is_unverifiable():
    from quilt_doctor.claims import Claim, evaluate_claims

    claim = Claim(id="qft-everywhere", repo="*", lens="spectral",
                  kill_if={"receipt": "qft_agrees_with_fft", "op": "==",
                           "value": False})
    v = evaluate_claims([claim], {"a": []}, {},
                        repo_active_days={"a": 2})
    assert v[0].status == "UNVERIFIABLE"
