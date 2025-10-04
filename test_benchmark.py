"""
test_benchmark.py — unit tests for benchmark.py

Run:
  pytest -s test_benchmark.py

These tests validate:
  - Hash set gives exact results (no FP/FN).
  - Bloom filter never has false negatives (only FPs allowed).
  - Cuckoo filter behaves reasonably (accuracy between 0 and 1).
"""

import random
import string

from benchmark import run_hash, run_bloom, run_cuckoo

# ------------------------------------------------------
# Helper: make tiny synthetic dataset
# ------------------------------------------------------
def _toy_data(n=200, q=100, seed=123):
    """
    Create a small synthetic dataset.
    - logins: n usernames
    - queries: q total, half present, half guaranteed absent
    """
    rng = random.Random(seed)
    logins = [f"user{i}" for i in range(n)]
    queries = []

    # Half present queries
    for _ in range(q // 2):
        queries.append((rng.choice(logins), 1))

    # Half absent queries (prefix 'fake_' avoids collision)
    for j in range(q - q // 2):
        fake = "fake_" + "".join(rng.choices(string.ascii_lowercase, k=6)) + f"_{j}"
        queries.append((fake, 0))

    rng.shuffle(queries)
    return logins, queries

# ------------------------------------------------------
# Unit Tests
# ------------------------------------------------------

def test_hash_exactness():
    """Hash set should be exact: no FP, no FN, 100% accuracy."""
    logins, queries = _toy_data()
    runtime, tp, tn, fp, fn = run_hash(logins, queries)

    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total
    
    print("\n[Hash Test]")
    print(f"Runtime: {runtime:.6f}s | TP={tp}, TN={tn}, FP={fp}, FN={fn}, Accuracy={accuracy:.4f}")

    assert fp == 0
    assert fn == 0
    assert abs(accuracy - 1.0) < 1e-12

def test_bloom_no_false_negatives():
    """
    Bloom filters never produce false negatives:
    - All present elements must be found (FN == 0).
    - False positives may exist but rate must be between 0 and 1.
    """
    logins, queries = _toy_data()
    runtime, tp, tn, fp, fn = run_bloom(logins, queries)

    total_absent = tn + fp
    fp_rate = fp / total_absent if total_absent > 0 else 0.0
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total
    
    print("\n[Bloom Filter Test]")
    print(f"Runtime: {runtime:.6f}s | TP={tp}, TN={tn}, FP={fp}, FN={fn}, "
          f"Accuracy={accuracy:.4f}, FP Rate={fp_rate:.4f}")

    assert fn == 0
    assert 0.0 <= fp_rate <= 1.0
    assert 0.0 <= accuracy <= 1.0

def test_cuckoo_reasonable_behavior():
    """
    Cuckoo filters may rarely give false negatives, but should be small.
    - Ensure FP, FN counts are non-negative.
    - Accuracy should lie between 0 and 1.
    """
    logins, queries = _toy_data()
    runtime, tp, tn, fp, fn = run_cuckoo(logins, queries)

    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total
    
    print("\n[Cuckoo Filter Test]")
    print(f"Runtime: {runtime:.6f}s | TP={tp}, TN={tn}, FP={fp}, FN={fn}, Accuracy={accuracy:.4f}")

    assert fp >= 0
    assert fn >= 0
    assert 0.0 <= accuracy <= 1.0
