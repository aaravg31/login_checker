"""
synth_dataset.py
----------------
Generate synthetic login datasets and query datasets for membership testing.

This script creates 5 pairs of CSV files:
    - logins_N.csv   (list of N usernames)
    - queries_Q.csv  (list of queries, where Q ≈ 1% of N)

Username generation schemes:
    - Sequential: user0, user1, ...
    - Adjective-Noun: brave_otter_15
    - Randomish: random alphanumeric prefix + index
    - Mixed: randomly chooses from the above three

Queries are generated with a mix of existing (is_present=1) and fake (is_present=0)
usernames. The ratio of present/absent is controlled by `dup_rate`.

Usage:
    Run this script directly in Python (no arguments needed). It will generate
    CSV files for N = 10K, 100K, 1M, 10M, 100M.
"""

import csv
import random
import string

# ------------------------------------------------------
# Vocabulary lists for the "adjnoun" style usernames
# ------------------------------------------------------
ADJECTIVES = ["swift", "silent", "bright", "brave", "clever", "fuzzy", "lucky", "mighty"]
NOUNS = ["tiger", "otter", "falcon", "panda", "lynx", "koala", "dragon", "llama"]

# ------------------------------------------------------
# Synthesized username functions
# Each function takes an integer index i and (optionally) a seed,
# and produces a UNIQUE username string.
# ------------------------------------------------------

def seq_name(i: int) -> str:
    """Sequential style: user0, user1, user2, ..."""
    return f"user{i}"

def adjnoun_name(i: int) -> str:
    """Adjective + noun + index, e.g. brave_otter_15"""
    adj = ADJECTIVES[i % len(ADJECTIVES)]
    noun = NOUNS[(i // len(ADJECTIVES)) % len(NOUNS)]
    return f"{adj}_{noun}_{i}"

def randomish_name(i: int, seed: int = 42) -> str:
    """
    Random-looking prefix plus index.
    Uses a small deterministic RNG so results are reproducible.
    Example: "xk29ab_7"
    """
    rnd = random.Random(seed + i)   # seed ensures reproducibility
    prefix = ''.join(rnd.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}_{i}"

def mixed_name(i: int, seed: int = 42) -> str:
    """
    Randomly choose one of the three styles (sequential, adjnoun, randomish).
    Ensures variety in the dataset while still being reproducible.
    """
    rnd = random.Random(seed + i)   # use index + seed so choice is fixed per i
    choice = rnd.choice(["sequential", "adjnoun", "randomish"])
    if choice == "sequential":
        return seq_name(i)
    elif choice == "adjnoun":
        return adjnoun_name(i)
    else:
        return randomish_name(i, seed)

# ------------------------------------------------------
# Username generator wrapper
# ------------------------------------------------------
def make_logins(n: int, scheme: str, seed: int = 42):
    """
    Generate n usernames according to the chosen scheme.

    scheme options:
      - "sequential"
      - "adjnoun"
      - "randomish"
      - "mixed"
    """
    if scheme == "sequential":
        return [seq_name(i) for i in range(n)]
    elif scheme == "adjnoun":
        return [adjnoun_name(i) for i in range(n)]
    elif scheme == "randomish":
        return [randomish_name(i, seed) for i in range(n)]
    elif scheme == "mixed":
        return [mixed_name(i, seed) for i in range(n)]
    else:
        raise ValueError("Unknown scheme. Choose from sequential, adjnoun, randomish, mixed.")

# ------------------------------------------------------
# Query generator
# ------------------------------------------------------
def make_queries(usernames, q: int, dup_rate: float = 0.5):
    """
    Generate q queries for testing membership.
    Each query is a tuple (username, is_present):
      - is_present = 1 if the username exists in logins
      - is_present = 0 if it does not

    dup_rate controls the fraction of queries that should be present.
    Example: dup_rate=0.6 means 60% of queries are existing usernames.
    """
    queries = []
    n = len(usernames)

    for j in range(q):
        if random.random() < dup_rate:
            # Pick an existing username
            u = random.choice(usernames)
            queries.append((u, 1))
        else:
            # Create a guaranteed absent username
            u = f"fake{j}_{random.randint(1000,9999)}"
            queries.append((u, 0))
    return queries

# ------------------------------------------------------
# CSV writers
# ------------------------------------------------------
def save_logins_csv(usernames, filename="logins.csv"):
    """Save usernames to a CSV file (one per row)."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username"])
        for u in usernames:
            writer.writerow([u])

def save_queries_csv(queries, filename="queries.csv"):
    """Save queries to a CSV file with columns: username, is_present."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "is_present"])
        for u, flag in queries:
            writer.writerow([u, flag])

# ------------------------------------------------------
# MAIN EXECUTION 
# ------------------------------------------------------
if __name__ == "__main__":
    # PARAMETERS
    n_values = [10_000, 100_000, 1_000_000, 10_000_000, 100_000_000]   # different login sizes
    q_values = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]       # matching query sizes (1% of n)
    dup_rate = 0.5  # fraction of queries that exist in logins
    seed = 42       # seed for reproducibility
    scheme = "mixed"  # options: sequential, adjnoun, randomish, mixed

    for n, q in zip(n_values, q_values):
        # Generate dataset
        logins = make_logins(n, scheme, seed)
        queries = make_queries(logins, q, dup_rate)

        # Use plain numbers in filenames
        login_file = f"logins_{n}.csv"
        query_file = f"queries_{q}.csv"

        # Save files
        save_logins_csv(logins, login_file)
        save_queries_csv(queries, query_file)

        print(f"Generated {len(logins)} logins → {login_file}")
        print(f"Generated {len(queries)} queries (dup_rate={dup_rate}) → {query_file}")
